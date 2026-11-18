from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from ..config import get_settings
from ..deps import DB, CurrentUser
from ..models import User, utcnow
from ..observability import LOGINS
from ..schemas import LoginIn, PasswordChangeIn, RegisterIn, TokenOut, UserOut
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _token_for(user: User) -> TokenOut:
    token, expires_in = create_access_token(user.id, user.role)
    return TokenOut(access_token=token, expires_in=expires_in, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: DB):
    user = db.scalar(select(User).where(func.lower(User.email) == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        LOGINS.labels("failure").inc()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou mot de passe incorrect.")
    if not user.is_active:
        LOGINS.labels("disabled").inc()
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Ce compte est désactivé.")
    user.last_login_at = utcnow()
    db.commit()
    LOGINS.labels("success").inc()
    return _token_for(user)


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: DB):
    if not get_settings().allow_registration:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Les inscriptions sont fermées.")
    if db.scalar(select(User).where(func.lower(User.email) == payload.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Un compte existe déjà avec cette adresse.")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role="user",
        last_login_at=utcnow(),
    )
    db.add(user)
    db.commit()
    return _token_for(user)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(payload: PasswordChangeIn, user: CurrentUser, db: DB):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Mot de passe actuel incorrect.")
    user.password_hash = hash_password(payload.new_password)
    db.commit()


@router.get("/config")
def public_config():
    settings = get_settings()
    return {"allow_registration": settings.allow_registration, "demo_mode": settings.seed_demo_data}
