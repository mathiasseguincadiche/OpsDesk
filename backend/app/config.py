"""Application settings, read from environment variables.

Every secret can be given either directly (``JWT_SECRET``) or through a file
(``JWT_SECRET_FILE``), which is the convention used by Podman/Docker secrets
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


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.environment == "production":
        if not _read_secret("JWT_SECRET"):
            raise RuntimeError("JWT_SECRET (ou JWT_SECRET_FILE) est obligatoire en production.")
        if len(_JWT_SECRET) < 32:
            raise RuntimeError("JWT_SECRET doit contenir au moins 32 caractères.")
    return settings
