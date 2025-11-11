"""Repositorio para operaciones de usuarios."""
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    """Repositorio para operaciones de base de datos relacionadas con usuarios."""

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db

    def get(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID."""
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por nombre de usuario."""
        return self.db.query(User).filter(User.username == username).first()

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> Sequence[User]:
        """Obtiene una lista paginada de usuarios."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(
        self, *, email: str, username: str, hashed_password: str
    ) -> User:
        """Crea un usuario."""
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, *, values: dict) -> User:
        """Actualiza campos de un usuario."""
        for field, value in values.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Elimina un usuario."""
        self.db.delete(user)
        self.db.commit()
