"""
Servicio de lógica de negocio para usuarios
"""
from typing import List, Optional

from sqlalchemy.orm import Session
from app.core.exceptions import ValidationError
from app.core.logging_config import get_logger
from app.core.security import verify_password, generate_password_salt, verify_password_strength
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas import user as user_schema
from app.utils.hashing import hash_password

logger = get_logger(__name__)


class UserService:
    """Servicio de lógica de negocio para usuarios."""

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el servicio con un repositorio de usuarios.
        
        Args:
            user_repository: Repositorio de usuarios
        """
        self.logger = logger
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID."""
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email."""
        return self.user_repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por nombre de usuario."""
        return self.user_repository.get_by_username(username)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtiene una lista de usuarios."""
        return list(self.user_repository.get_multi(skip=skip, limit=limit))

    def create_user(self, user: user_schema.UserRegister) -> User:
        """Crea un nuevo usuario."""
        self.logger.debug(f"Creando usuario: {user.username}")
        if not verify_password_strength(user.password):
            raise ValidationError(message="La contraseña debe tener al menos una mayúscula, una minúscula, un dígito y un carácter especial", field="password")

        password_salt = generate_password_salt()

        hashed_password = hash_password(user.password)


        new_user = self.user_repository.create(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
        )
        self.logger.info(f"Usuario creado: ID={new_user.id}, username={new_user.username}")
        return new_user

    def update_user(
        self,
        user_id: int,
        user_update: user_schema.UserUpdate,
    ) -> Optional[User]:
        """Actualiza un usuario existente."""
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        return self.user_repository.update(db_user, values=update_data)

    def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario."""
        db_user = self.get_user(user_id)
        if not db_user:
            return False

        self.user_repository.delete(db_user)
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autentica credenciales de usuario."""
        user = self.get_user_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None
        return user
