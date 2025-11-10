"""
Servicio de lógica de negocio para usuarios
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.core.security import verify_password
from app.db.models.user import User
from app.repositories import user_repository
from app.schemas import user as user_schema
from app.utils.hashing import hash_password

logger = get_logger(__name__)


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Obtiene un usuario por ID."""
    return user_repository.get(db, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obtiene un usuario por email."""
    return user_repository.get_by_email(db, email)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Obtiene un usuario por nombre de usuario."""
    return user_repository.get_by_username(db, username)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Obtiene una lista de usuarios."""
    return list(user_repository.get_multi(db, skip=skip, limit=limit))


def create_user(db: Session, user: user_schema.UserCreate) -> User:
    """Crea un nuevo usuario."""
    logger.debug(f"Creando usuario: {user.username}")
    hashed_password = hash_password(user.password)
    new_user = user_repository.create(
        db,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    logger.info(f"Usuario creado: ID={new_user.id}, username={new_user.username}")
    return new_user


def update_user(
    db: Session,
    user_id: int,
    user_update: user_schema.UserUpdate,
) -> Optional[User]:
    """Actualiza un usuario existente."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    return user_repository.update(db, db_user, values=update_data)


def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un usuario."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    user_repository.delete(db, db_user)
    return True


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Autentica credenciales de usuario."""
    user = get_user_by_username(db, username)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None
    return user

