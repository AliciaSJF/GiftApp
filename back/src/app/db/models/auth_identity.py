from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import BYTEA, CITEXT, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class AuthIdentity(Base):
    """Modelo de identidades externas (Google, Facebook, GitHub, Apple, etc.)."""

    __tablename__ = "auth_identity"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    provider = Column(
        Text,
        nullable=False,
        index=True
    )  # 'google', 'facebook', 'github', 'apple'
    provider_user_id = Column(Text, nullable=False)  # "sub" de OpenID / ID único del proveedor
    auth0_sub = Column(Text, nullable=True, unique=True, index=True)
    
    provider_email = Column(CITEXT, nullable=True)  # Email reportado por proveedor (si lo comparte)
    email_verified = Column(Boolean, nullable=True)  # Verificación de ese proveedor (si aplica)
    
    # Tokens: guarda SÓLO si de verdad los necesitas para APIs del proveedor
    # Si no, evita almacenarlos
    access_token_encrypted = Column(BYTEA, nullable=True)
    refresh_token_encrypted = Column(BYTEA, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="auth_identities")

    # Constraints
    __table_args__ = (
        # Constraint para asegurar que provider sea uno de los valores permitidos
        CheckConstraint(
            "provider IN ('google', 'facebook', 'github', 'apple')",
            name="check_provider_valid"
        ),
        # Constraint único para (provider, provider_user_id) - clave para "linking" de cuentas
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user_id"),
    )

