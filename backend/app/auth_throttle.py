"""Limiter les tentatives de connexion dans PostgreSQL, commun à toutes les instances.

Les identifiants sont hachés par HMAC ; aucun e-mail ni IP n'est persisté ici.
Le compteur est réservé AVANT le PBKDF2, même si l'utilisateur n'existe pas.
"""
from __future__ import annotations

import hashlib
import hmac
import math
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from .config import get_settings
from .models import LoginThrottle

MAX_ATTEMPTS = 10
WINDOW = timedelta(minutes=2)
BLOCK = timedelta(minutes=2)


def throttle_key(email: str) -> str:
    """Éviter de stocker l'adresse e-mail dans les compteurs."""
    secret = get_settings().jwt_secret.encode("utf-8")
    return hmac.new(secret, ("login:" + email.casefold()).encode("utf-8"), hashlib.sha256).hexdigest()


def _utc(value: datetime) -> datetime:
    # SQLite perd parfois les informations de fuseau lors des tests.
    return value if value.tzinfo else value.replace(tzinfo=UTC)


def reserve_login_attempt(db: Session, email: str) -> None:
    """Réserver atomiquement une tentative, avant vérification du mot de passe."""
    key = throttle_key(email)
    now = datetime.now(UTC)
    data = {"key": key, "attempt_count": 0, "window_started_at": now}
    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        insert = pg_insert(LoginThrottle).values(**data).on_conflict_do_nothing(index_elements=["key"])
    elif dialect == "sqlite":
        insert = sqlite_insert(LoginThrottle).values(**data).on_conflict_do_nothing(index_elements=["key"])
    else:
        raise RuntimeError(f"Limitation d'authentification indisponible : dialecte {dialect}")
    db.execute(insert)
    row = db.scalar(select(LoginThrottle).where(LoginThrottle.key == key).with_for_update())
    if row is None:
        raise RuntimeError("Compteur d'authentification introuvable.")

    if row.blocked_until and _utc(row.blocked_until) > now:
        seconds = math.ceil((_utc(row.blocked_until) - now).total_seconds())
        db.commit()
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "Trop de tentatives : réessayez dans quelques minutes.",
            headers={"Retry-After": str(max(1, seconds))},
        )
    if now - _utc(row.window_started_at) >= WINDOW:
        row.attempt_count = 0
        row.window_started_at = now
        row.blocked_until = None

    row.attempt_count += 1
    if row.attempt_count > MAX_ATTEMPTS:
        row.blocked_until = now + BLOCK
        db.commit()
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "Trop de tentatives : réessayez dans quelques minutes.",
            headers={"Retry-After": str(int(BLOCK.total_seconds()))},
        )

    # Nettoyer les anciennes identités HMAC inactives pour ne pas grossir sans limite.
    db.execute(
        delete(LoginThrottle).where(
            LoginThrottle.key != key,
            LoginThrottle.window_started_at < now - timedelta(days=1),
        )
    )
    db.commit()


def clear_login_attempts(db: Session, email: str) -> None:
    """Réinitialiser le compteur après une authentification réussie."""
    db.execute(delete(LoginThrottle).where(LoginThrottle.key == throttle_key(email)))
    # L'appelant valide dans la même transaction ses changements de session.
