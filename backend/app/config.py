"""Application settings, read from environment variables.

Every secret can be given either directly (``JWT_SECRET``) or through a file
(``JWT_SECRET_FILE``), which is the convention used by Docker Compose secrets
and Kubernetes secret volumes.
"""
from __future__ import annotations

import os
import secrets
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _read_secret(name: str) -> str | None:
    """Return ``$NAME`` or the content of the file pointed to by ``$NAME_FILE``."""
    file_path = os.environ.get(f"{name}_FILE")
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()
    return os.environ.get(name)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    app_name: str = "OpsDesk"
    app_version: str = "2.0.0"
    app_revision: str = "dev"
    environment: str = "development"
    log_level: str = "INFO"
    log_format: str = Field(default="json", description="json or text")

    # Database: either a full DATABASE_URL, or the DB_* components.
    database_url: str | None = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "opsdesk"
    db_user: str = "opsdesk"
    db_pool_size: int = 5
    db_connect_retries: int = 30

    # Auth
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 12
    password_hash_iterations: int = 390_000
    allow_registration: bool = True

    # Bootstrap
    admin_email: str = "admin@opsdesk.local"
    admin_name: str = "Administrateur"
    seed_demo_data: bool = True

    # HTTP
    cors_origins: str = ""

    @property
    def sqlalchemy_url(self) -> str:
        if self.database_url:
            url = self.database_url
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+psycopg://", 1)
            return url
        password = _read_secret("DB_PASSWORD") or ""
        return (
            f"postgresql+psycopg://{quote_plus(self.db_user)}:{quote_plus(password)}"
            f"@{self.db_host}:{self.db_port}/{quote_plus(self.db_name)}"
        )

    @property
    def jwt_secret(self) -> str:
        return _JWT_SECRET

    @property
    def admin_password(self) -> str:
        return _read_secret("ADMIN_PASSWORD") or "ChangeMe123!"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# A missing JWT secret is tolerated in development (random per process) but
# tokens are then invalidated at each restart and not shared between replicas.
_JWT_SECRET = _read_secret("JWT_SECRET") or secrets.token_urlsafe(48)


def _require_production_secret(name: str, minimum: int = 1) -> str:
    value = _read_secret(name)
    if not value or len(value.strip()) < minimum:
        raise RuntimeError(f"{name} (ou {name}_FILE) est obligatoire et doit être suffisamment long en production.")
    normalized = value.strip().casefold()
    if normalized.startswith(("change-me", "changeme")) or normalized == "demo1234!":
        raise RuntimeError(f"{name} ne doit pas utiliser une valeur de démonstration.")
    return value


def _validate_production_settings(settings: Settings) -> None:
    jwt = _require_production_secret("JWT_SECRET", minimum=32)
    admin = _require_production_secret("ADMIN_PASSWORD")
    if jwt == admin:
        raise RuntimeError("JWT_SECRET et ADMIN_PASSWORD doivent être distincts.")
    if not settings.database_url:
        db = _require_production_secret("DB_PASSWORD")
        if db in (jwt, admin):
            raise RuntimeError("Les trois secrets doivent être distincts.")
    # A complete DATABASE_URL is an alternative to DB_*; its credentials are
    # managed independently and must be checked by the deployment operator.


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.environment == "production":
        _validate_production_settings(settings)
    return settings
