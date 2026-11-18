from __future__ import annotations

from collections import Counter
from datetime import UTC, timedelta

from fastapi import APIRouter, Query
from sqlalchemy import func, select

from ..deps import DB, CurrentUser
from ..models import CATEGORIES, PRIORITIES, STATUSES, Ticket, User, utcnow
from ..schemas import AgentLoad, DayPoint, StatsOut

router = APIRouter(prefix="/api/stats", tags=["stats"])


def _utc(value):
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


@router.get("", response_model=StatsOut)
def stats(db: DB, user: CurrentUser, days: int = Query(default=14, ge=7, le=90)):
    scope = select(Ticket)
    if not user.is_staff:
        scope = scope.where(Ticket.requester_id == user.id)
    tickets = scope.subquery()

    def grouped(column) -> dict[str, int]:
        return dict(db.execute(select(column, func.count()).group_by(column)).all())

    by_status = grouped(tickets.c.status)
    by_priority = grouped(tickets.c.priority)
    by_category = grouped(tickets.c.category)
    active = tickets.c.status.in_(("open", "in_progress"))
    unassigned_open = db.scalar(
        select(func.count()).select_from(tickets).where(active, tickets.c.assignee_id.is_(None))
    )
    assigned_to_me = db.scalar(
        select(func.count()).select_from(tickets).where(active, tickets.c.assignee_id == user.id)
    )
    mine_active = db.scalar(
        select(func.count()).select_from(tickets).where(active, tickets.c.requester_id == user.id)
    )
    critical_open = db.scalar(
        select(func.count()).select_from(tickets).where(active, tickets.c.priority == "critical")
    )

    # Resolution time and daily timeline are computed in Python: portable across
    # PostgreSQL and SQLite and cheap at this scale (bounded by the time window).
    since = utcnow() - timedelta(days=days - 1)
    since_day = since.date()
    created_per_day: Counter = Counter()
    resolved_per_day: Counter = Counter()
    for created_at, resolved_at in db.execute(
        select(tickets.c.created_at, tickets.c.resolved_at).where(
            (tickets.c.created_at >= since.replace(hour=0, minute=0, second=0, microsecond=0))
            | (tickets.c.resolved_at >= since.replace(hour=0, minute=0, second=0, microsecond=0))
        )
    ).all():
        created_per_day[_utc(created_at).date()] += 1
        if resolved_at:
            resolved_per_day[_utc(resolved_at).date()] += 1

    durations = [
        (_utc(resolved) - _utc(created)).total_seconds() / 3600
        for created, resolved in db.execute(
            select(tickets.c.created_at, tickets.c.resolved_at).where(tickets.c.resolved_at.is_not(None))
        ).all()
    ]

    timeline = []
    for offset in range(days):
        day = since_day + timedelta(days=offset)
        timeline.append(
            DayPoint(date=day.isoformat(), created=created_per_day[day], resolved=resolved_per_day[day])
        )

    agents = []
    if user.is_staff:
        rows = db.execute(
            select(User.id, User.full_name, func.count(Ticket.id))
            .outerjoin(Ticket, (Ticket.assignee_id == User.id) & Ticket.status.in_(("open", "in_progress")))
            .where(User.role.in_(("agent", "admin")), User.is_active.is_(True))
            .group_by(User.id, User.full_name)
            .order_by(func.count(Ticket.id).desc(), User.full_name)
        ).all()
        agents = [AgentLoad(id=r[0], full_name=r[1], open=r[2]) for r in rows]

    return StatsOut(
        total=sum(by_status.values()),
        by_status={s: by_status.get(s, 0) for s in STATUSES},
        by_priority={p: by_priority.get(p, 0) for p in PRIORITIES},
        by_category={c: by_category.get(c, 0) for c in CATEGORIES},
        unassigned_open=unassigned_open or 0,
        assigned_to_me=assigned_to_me or 0,
        mine_active=mine_active or 0,
        critical_open=critical_open or 0,
        avg_resolution_hours=round(sum(durations) / len(durations), 1) if durations else None,
        timeline=timeline,
        agents=agents,
    )
