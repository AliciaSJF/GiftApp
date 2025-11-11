"""Repositorio para operaciones de identidades de autenticación."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.auth_identity import AuthIdentity


class AuthIdentityRepository:
    """Repositorio para operaciones de base de datos relacionadas con identidades de autenticación."""

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db

    def get_by_provider_and_user_id(
        self, provider: str, provider_user_id: str
    ) -> Optional[AuthIdentity]:
        """Obtiene una identidad por proveedor y ID de usuario del proveedor."""
        return (
            self.db.query(AuthIdentity)
            .filter(
                AuthIdentity.provider == provider,
                AuthIdentity.provider_user_id == provider_user_id,
            )
            .first()
        )

    def get_by_user_id(self, user_id: UUID) -> list[AuthIdentity]:
        """Obtiene todas las identidades de un usuario."""
        return self.db.query(AuthIdentity).filter(AuthIdentity.user_id == user_id).all()

    def create(
        self,
        *,
        user_id: UUID,
        provider: str,
        provider_user_id: str,
        provider_email: Optional[str] = None,
        email_verified: Optional[bool] = None,
    ) -> AuthIdentity:
        """Crea una nueva identidad de autenticación."""
        auth_identity = AuthIdentity(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_email=provider_email,
            email_verified=email_verified,
        )
        self.db.add(auth_identity)
        self.db.commit()
        self.db.refresh(auth_identity)
        return auth_identity

    def update(
        self, auth_identity: AuthIdentity, *, values: dict
    ) -> AuthIdentity:
        """Actualiza campos de una identidad de autenticación."""
        for field, value in values.items():
            setattr(auth_identity, field, value)
        self.db.commit()
        self.db.refresh(auth_identity)
        return auth_identity
