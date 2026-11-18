from __future__ import annotations

import math
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import Select, case, func, or_, select
from sqlalchemy.orm import selectinload

from ..deps import DB, AdminUser, CurrentUser
from ..models import Comment, Ticket, TicketEvent, User, utcnow
from ..observability import TICKET_TRANSITIONS, TICKETS_CREATED
from ..schemas import (
    Category,
    CommentIn,
    CommentOut,
    EventOut,
    Priority,
    Status,
    StatusChangeIn,
    TicketCreateIn,
    TicketDetailOut,
    TicketOut,
    TicketPage,
    TicketUpdateIn,
)
from ..workflow import TransitionError, allowed_transitions, check_transition

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

SORTS = {
    "newest": Ticket.created_at.desc(),
    "oldest": Ticket.created_at.asc(),
    "updated": Ticket.updated_at.desc(),
    "priority": None,  # handled below
}
PRIORITY_RANK = {"critical": 0, "high": 1, "normal": 2, "low": 3}


def _visible(query: Select, user: User) -> Select:
    return query if user.is_staff else query.where(Ticket.requester_id == user.id)


def _get_ticket(db: DB, ticket_id: int, user: User, *, detail: bool = False) -> Ticket:
    # populate_existing: always reload relationships (assignee, comments…) after a commit.
    query = select(Ticket).where(Ticket.id == ticket_id).execution_options(populate_existing=True)
    if detail:
        query = query.options(selectinload(Ticket.comments), selectinload(Ticket.events))
    ticket = db.scalar(_visible(query, user))
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket introuvable.")
    return ticket


def _event(db: DB, ticket: Ticket, actor: User, kind: str, before=None, after=None) -> None:
    db.add(TicketEvent(ticket=ticket, actor_id=actor.id, kind=kind, from_value=before, to_value=after))


def _can_edit(ticket: Ticket, user: User) -> bool:
    return user.is_staff or (ticket.requester_id == user.id and ticket.status == "open")


def _out(ticket: Ticket, comment_count: int) -> TicketOut:
    item = TicketOut.model_validate(ticket)
    item.comment_count = comment_count
    return item


def _detail(ticket: Ticket, user: User) -> TicketDetailOut:
    base = TicketOut.model_validate(ticket).model_dump()
    base["comment_count"] = len(ticket.comments)
    return TicketDetailOut(
        **base,
        comments=[CommentOut.model_validate(c) for c in ticket.comments],
        events=[EventOut.model_validate(e) for e in ticket.events],
        allowed_transitions=allowed_transitions(ticket.status, is_staff=user.is_staff),
        can_edit=_can_edit(ticket, user),
    )


@router.get("", response_model=TicketPage)
def list_tickets(
    db: DB,
    user: CurrentUser,
    q: str | None = Query(default=None, max_length=120),
    status_: list[Status] | None = Query(default=None, alias="status"),
    priority: list[Priority] | None = Query(default=None),
    category: list[Category] | None = Query(default=None),
    assignee: str | None = Query(default=None, description="me, none, ou un identifiant"),
    mine: bool = False,
    sort: Literal["newest", "oldest", "updated", "priority"] = "newest",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    comment_count = (
        select(func.count(Comment.id)).where(Comment.ticket_id == Ticket.id).correlate(Ticket).scalar_subquery()
    )
    query = _visible(select(Ticket), user)
    if q:
        term = q.strip().lstrip("#")
        conditions = [Ticket.title.ilike(f"%{term}%"), Ticket.description.ilike(f"%{term}%")]
        if term.isdigit():
            conditions.append(Ticket.id == int(term))
        query = query.where(or_(*conditions))
    if status_:
        query = query.where(Ticket.status.in_(status_))
    if priority:
        query = query.where(Ticket.priority.in_(priority))
    if category:
        query = query.where(Ticket.category.in_(category))
    if mine:
        query = query.where(Ticket.requester_id == user.id)
    if assignee == "me":
        query = query.where(Ticket.assignee_id == user.id)
    elif assignee == "none":
        query = query.where(Ticket.assignee_id.is_(None))
    elif assignee and assignee.isdigit():
        query = query.where(Ticket.assignee_id == int(assignee))

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0

    if sort == "priority":
        rank = case(PRIORITY_RANK, value=Ticket.priority)
        query = query.order_by(rank, Ticket.created_at.desc())
    else:
        query = query.order_by(SORTS[sort], Ticket.id.desc())

    rows = db.execute(
        query.add_columns(comment_count).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return TicketPage(
        items=[_out(ticket, count) for ticket, count in rows],
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.post("", response_model=TicketDetailOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreateIn, db: DB, user: CurrentUser, response: Response):
    ticket = Ticket(**payload.model_dump(), requester_id=user.id, status="open")
    db.add(ticket)
    db.flush()
    _event(db, ticket, user, "created", None, "open")
    db.commit()
    TICKETS_CREATED.labels(ticket.priority).inc()
    response.headers["Location"] = f"/api/tickets/{ticket.id}"
    return _detail(_get_ticket(db, ticket.id, user, detail=True), user)


@router.get("/{ticket_id}", response_model=TicketDetailOut)
def get_ticket(ticket_id: int, db: DB, user: CurrentUser):
    return _detail(_get_ticket(db, ticket_id, user, detail=True), user)


@router.patch("/{ticket_id}", response_model=TicketDetailOut)
def update_ticket(ticket_id: int, payload: TicketUpdateIn, db: DB, user: CurrentUser):
    ticket = _get_ticket(db, ticket_id, user)
    if not _can_edit(ticket, user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Ce ticket ne peut plus être modifié.")
    changes = payload.model_dump(exclude_unset=True)

    if "assignee_id" in changes:
        if not user.is_staff:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Seule l'équipe support peut assigner un ticket.")
        new_id = changes.pop("assignee_id") or None
        if new_id is not None:
            agent = db.get(User, new_id)
            if agent is None or not agent.is_staff or not agent.is_active:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Ce membre du support est introuvable.")
        if new_id != ticket.assignee_id:
            before = ticket.assignee.full_name if ticket.assignee else None
            ticket.assignee_id = new_id
            _event(db, ticket, user, "assigned", before, agent.full_name if new_id else None)

    for field in ("priority", "category"):
        if field in changes and changes[field] is not None and changes[field] != getattr(ticket, field):
            _event(db, ticket, user, f"{field}_changed", getattr(ticket, field), changes[field])
            setattr(ticket, field, changes[field])
    edited = False
    for field in ("title", "description"):
        if field in changes and changes[field] is not None and changes[field] != getattr(ticket, field):
            setattr(ticket, field, changes[field])
            edited = True
    if edited:
        _event(db, ticket, user, "edited")
    ticket.updated_at = utcnow()
    db.commit()
    return _detail(_get_ticket(db, ticket.id, user, detail=True), user)


@router.post("/{ticket_id}/status", response_model=TicketDetailOut)
def change_status(ticket_id: int, payload: StatusChangeIn, db: DB, user: CurrentUser):
    ticket = _get_ticket(db, ticket_id, user)
    # Row lock (no-op on SQLite) so two agents cannot change the status concurrently,
    # then reload the ticket to read the status committed by the other transaction.
    db.execute(select(Ticket.id).where(Ticket.id == ticket.id).with_for_update())
    db.refresh(ticket)
    before = ticket.status
    try:
        check_transition(before, payload.status, is_staff=user.is_staff)
    except PermissionError as error:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(error)) from None
    except TransitionError as error:
        raise HTTPException(status.HTTP_409_CONFLICT, str(error)) from None

    now = utcnow()
    ticket.status = payload.status
    ticket.updated_at = now
    if payload.status == "resolved":
        ticket.resolved_at = now
    elif payload.status == "closed":
        ticket.closed_at = now
        ticket.resolved_at = ticket.resolved_at or now
    elif payload.status in ("open", "in_progress"):
        ticket.resolved_at = None
        ticket.closed_at = None
    # Taking a ticket in charge assigns it to the agent if nobody owns it yet.
    if payload.status == "in_progress" and ticket.assignee_id is None and user.is_staff:
        ticket.assignee_id = user.id
        _event(db, ticket, user, "assigned", None, user.full_name)
    _event(db, ticket, user, "status_changed", before, payload.status)
    db.commit()
    TICKET_TRANSITIONS.labels(before, payload.status).inc()
    return _detail(_get_ticket(db, ticket.id, user, detail=True), user)


@router.post("/{ticket_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(ticket_id: int, payload: CommentIn, db: DB, user: CurrentUser):
    ticket = _get_ticket(db, ticket_id, user)
    comment = Comment(ticket_id=ticket.id, author_id=user.id, body=payload.body)
    db.add(comment)
    ticket.updated_at = utcnow()
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: DB, admin: AdminUser):
    ticket = _get_ticket(db, ticket_id, admin)
    db.delete(ticket)
    db.commit()
