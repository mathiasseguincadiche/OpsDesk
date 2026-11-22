"""Hachage PBKDF2-SHA256 des mots de passe et émission des jetons JWT."""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt

from .config import get_settings

_ALGO = "pbkdf2_sha256"


def hash_password(password: str, iterations: int | None = None) -> str:
    iterations = iterations or get_settings().password_hash_iterations
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return "$".join(
        [_ALGO, str(iterations), base64.b64encode(salt).decode(), base64.b64encode(digest).decode()]
    )


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iterations, salt_b64, digest_b64 = stored.split("$")
        if algo != _ALGO:
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
    except (ValueError, TypeError):
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
    return hmac.compare_digest(candidate, expected)


def password_fingerprint(password_hash: str) -> str:
    """Lier une session au hachage actuel du mot de passe, sans divulguer ce hachage."""
    return hmac.new(
        get_settings().jwt_secret.encode("utf-8"), password_hash.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def csrf_for_session(token: str) -> str:
    """Signer un jeton CSRF lié à la session sans exposer sa valeur JWT."""
    return hmac.new(
        get_settings().jwt_secret.encode("utf-8"),
        ("opsdesk-csrf:" + token).encode("utf-8"), hashlib.sha256,
    ).hexdigest()


def create_access_token(user_id: int, role: str, password_hash: str) -> tuple[str, int]:
    settings = get_settings()
    expires_in = settings.jwt_expire_minutes * 60
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id), "role": role, "pwd": password_fingerprint(password_hash),
        "iat": now, "exp": now + timedelta(seconds=expires_in),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, expires_in


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
