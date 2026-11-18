"""Pydantic request/response models (the public API contract)."""
from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints, field_validator


def _aware(value: datetime | None) -> datetime | None:
    # SQLite returns naive datetimes; everything is stored in UTC.
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


UTCDateTime = Annotated[datetime, AfterValidator(_aware)]

Role = Literal["user", "agent", "admin"]
Status = Literal["open", "in_progress", "resolved", "closed"]
Priority = Literal["low", "normal", "high", "critical"]
Category = Literal["hardware", "software", "network", "access", "other"]

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=120)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, max_length=5000)]
Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=120)]
Password = Annotated[str, StringConstraints(min_length=8, max_length=128)]
CommentBody = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=5000)]


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _email(value: str) -> str:
    value = value.strip().lower()
    if len(value) > 254 or not _EMAIL_RE.match(value):
        raise ValueError("Adresse e-mail invalide.")
    return value


EmailStr = Annotated[str, AfterValidator(_email)]


def _no_nul(value: str) -> str:
    if "\x00" in value:
        raise ValueError("Le texte ne doit pas contenir de caractère NUL.")
    return value


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Users & auth ----------
class UserBrief(ORM):
    id: int
    full_name: str
    email: str
    role: Role


class UserOut(UserBrief):
    is_active: bool
    created_at: UTCDateTime
    last_login_at: UTCDateTime | None = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RegisterIn(BaseModel):
    email: EmailStr
    full_name: Name
    password: Password


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserOut


class PasswordChangeIn(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: Password


class UserCreateIn(RegisterIn):
    role: Role = "user"


class UserUpdateIn(BaseModel):
    full_name: Name | None = None
    role: Role | None = None
    is_active: bool | None = None
    password: Password | None = None


# ---------- Tickets ----------
class TicketCreateIn(BaseModel):
    title: Title
    description: Description = ""
    priority: Priority = "normal"
    category: Category = "other"

    _check_title = field_validator("title", "description")(_no_nul)


class TicketUpdateIn(BaseModel):
    title: Title | None = None
    description: Description | None = None
    priority: Priority | None = None
    category: Category | None = None
    assignee_id: int | None = Field(default=None, description="0 pour désassigner")

    _check_title = field_validator("title", "description")(_no_nul)


class StatusChangeIn(BaseModel):
    status: Status


class CommentIn(BaseModel):
    body: CommentBody

    _check_body = field_validator("body")(_no_nul)


class CommentOut(ORM):
    id: int
    body: str
    author: UserBrief
    created_at: UTCDateTime


class EventOut(ORM):
    id: int
    kind: str
    from_value: str | None
    to_value: str | None
    actor: UserBrief
    created_at: UTCDateTime


class TicketOut(ORM):
    id: int
    title: str
    description: str
    status: Status
    priority: Priority
    category: Category
    requester: UserBrief
    assignee: UserBrief | None
    created_at: UTCDateTime
    updated_at: UTCDateTime
    resolved_at: UTCDateTime | None
    closed_at: UTCDateTime | None
    comment_count: int = 0


class TicketDetailOut(TicketOut):
    comments: list[CommentOut]
    events: list[EventOut]
    allowed_transitions: list[Status]
    can_edit: bool


class TicketPage(BaseModel):
    items: list[TicketOut]
    total: int
    page: int
    page_size: int
    pages: int


# ---------- Stats ----------
class DayPoint(BaseModel):
    date: str
    created: int
    resolved: int


class AgentLoad(BaseModel):
    id: int
    full_name: str
    open: int


class StatsOut(BaseModel):
    total: int
    by_status: dict[str, int]
    by_priority: dict[str, int]
    by_category: dict[str, int]
    unassigned_open: int
    assigned_to_me: int
    mine_active: int
    critical_open: int
    avg_resolution_hours: float | None
    timeline: list[DayPoint]
    agents: list[AgentLoad]
