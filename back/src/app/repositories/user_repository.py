"""Repositorio para operaciones de usuarios."""
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.db.models.user import User


def get(db: Session, user_id: int) -> Optional[User]:
    """Obtiene un usuario por ID."""
    return db.get(User, user_id)


def get_by_email(db: Session, email: str) -> Optional[User]:
    """Obtiene un usuario por email."""
    return db.query(User).filter(User.email == email).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    """Obtiene un usuario por nombre de usuario."""
    return db.query(User).filter(User.username == username).first()


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> Sequence[User]:
    """Obtiene una lista paginada de usuarios."""
    return db.query(User).offset(skip).limit(limit).all()


def create(db: Session, *, email: str, username: str, hashed_password: str) -> User:
    """Crea un usuario."""
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, *, values: dict) -> User:
    """Actualiza campos de un usuario."""
    for field, value in values.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    """Elimina un usuario."""
    db.delete(user)
    db.commit()
