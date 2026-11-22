"""FastAPI dependencies: database session and authenticated user."""
from __future__ import annotations

import hmac
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .db import get_db
from .models import User
from .security import csrf_for_session, decode_access_token, password_fingerprint

bearer = HTTPBearer(auto_error=False)

DB = Annotated[Session, Depends(get_db)]


def current_user(
    db: DB, request: Request, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # CLI : Authorization Bearer. Navigateur : cookie HttpOnly de même origine.
    token = credentials.credentials if credentials is not None else request.cookies.get("opsdesk_session")
    if not token:
        raise unauthorized
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise unauthorized from None
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise unauthorized
    # Un changement de mot de passe invalide les anciens jetons sur toutes les instances.
    if not hmac.compare_digest(str(payload.get("pwd", "")), password_fingerprint(user.password_hash)):
        raise unauthorized
    if credentials is None and request.method not in ("GET", "HEAD", "OPTIONS"):
        # Une requête utilisant le cookie exige aussi un CSRF lié à cette session.
        expected = csrf_for_session(token)
        provided = request.headers.get("x-csrf-token") or ""
        browser_cookie = request.cookies.get("opsdesk_csrf") or ""
        if not (hmac.compare_digest(provided, expected) and hmac.compare_digest(browser_cookie, expected)):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Jeton CSRF manquant ou invalide.")
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def staff_user(user: CurrentUser) -> User:
    if not user.is_staff:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Réservé à l'équipe support.")
    return user


def admin_user(user: CurrentUser) -> User:
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Réservé aux administrateurs.")
    return user


StaffUser = Annotated[User, Depends(staff_user)]
AdminUser = Annotated[User, Depends(admin_user)]
