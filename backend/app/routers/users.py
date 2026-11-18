from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from ..deps import DB, AdminUser, StaffUser
from ..models import User
from ..schemas import UserBrief, UserCreateIn, UserOut, UserUpdateIn
from ..security import hash_password

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(_: AdminUser, db: DB):
    return db.scalars(select(User).order_by(User.role.desc(), User.full_name)).all()


@router.get("/agents", response_model=list[UserBrief])
def list_agents(_: StaffUser, db: DB):
    """People a ticket can be assigned to."""
    return db.scalars(
        select(User).where(User.role.in_(("agent", "admin")), User.is_active.is_(True)).order_by(User.full_name)
    ).all()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateIn, _: AdminUser, db: DB):
    if db.scalar(select(User).where(func.lower(User.email) == payload.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Un compte existe déjà avec cette adresse.")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdateIn, admin: AdminUser, db: DB):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable.")
    if user.id == admin.id and (payload.role not in (None, "admin") or payload.is_active is False):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Vous ne pouvez pas retirer vos propres droits d'administrateur.")
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.role is not None:
        user.role = payload.role
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.password is not None:
        user.password_hash = hash_password(payload.password)
    db.commit()
    return user
