"""Ticket lifecycle rules, independent of HTTP and of the database.

    open ──► in_progress ──► resolved ──► closed
      │          ▲  │            │          │
      │          └──┴── reopen ◄─┘          │
      └──────────────► closed ◄─────────────┘ (reopen: closed ──► open)
"""
from __future__ import annotations

TRANSITIONS: dict[str, set[str]] = {
    "open": {"in_progress", "closed"},
    "in_progress": {"open", "resolved"},
    "resolved": {"in_progress", "closed"},
    "closed": {"open"},
}

# What a simple requester may do on their own ticket: accept or refuse the resolution.
REQUESTER_TRANSITIONS: dict[str, set[str]] = {
    "resolved": {"in_progress", "closed"},
    "open": {"closed"},
}


class TransitionError(ValueError):
    pass


def check_transition(current: str, target: str, *, is_staff: bool) -> None:
    if target == current:
        raise TransitionError("Le ticket est déjà dans ce statut.")
    if target not in TRANSITIONS.get(current, set()):
        raise TransitionError(f"Transition « {current} → {target} » non autorisée.")
    if not is_staff and target not in REQUESTER_TRANSITIONS.get(current, set()):
        raise PermissionError("Seule l'équipe support peut effectuer ce changement de statut.")


def allowed_transitions(current: str, *, is_staff: bool) -> list[str]:
    allowed = TRANSITIONS.get(current, set())
    if not is_staff:
        allowed = allowed & REQUESTER_TRANSITIONS.get(current, set())
    order = ["open", "in_progress", "resolved", "closed"]
    return [status for status in order if status in allowed]
