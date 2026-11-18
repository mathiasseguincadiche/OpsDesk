"""Database engine, session factory and startup helpers."""
from __future__ import annotations

import logging
import time
from collections.abc import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import get_settings

log = logging.getLogger("opsdesk.db")


class Base(DeclarativeBase):
    pass


def build_engine(url: str) -> Engine:
    if url.startswith("sqlite"):
        from sqlalchemy.pool import StaticPool

        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool if ":memory:" in url else None,
        )
    settings = get_settings()
    return create_engine(
        url,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_pool_size,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={"connect_timeout": 5, "application_name": "opsdesk-api"},
    )


engine: Engine = build_engine(get_settings().sqlalchemy_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_database(retries: int) -> None:
    """Block until the database answers, so the API survives a slow DB start."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError as error:
            if attempt == retries:
                raise
            log.warning("database_not_ready attempt=%s/%s error=%s", attempt, retries, error.orig.__class__.__name__)
            time.sleep(2)


def database_is_up() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:  # noqa: BLE001 - any failure means "not ready"
        return False
