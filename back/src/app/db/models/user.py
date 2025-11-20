from sqlalchemy import Boolean, Column, DateTime, String, Text, Integer
from sqlalchemy.dialects.postgresql import CITEXT, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class User(Base):
    """Modelo de usuario con autenticación OAuth."""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    email = Column(CITEXT, unique=True, index=True, nullable=True)  # Puede ser NULL si el proveedor no comparte email
    email_verified = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(Text, nullable=True)
    password_salt = Column(Text, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, nullable=False, default=0)

    display_name = Column(Text, nullable=True)  # Nombre visible en la UI
    avatar_url = Column(Text, nullable=True)  # Foto del proveedor (si hay)
    locale = Column(Text, nullable=True)  # "es-ES", "en-US", etc.
    is_active = Column(Boolean, nullable=False, default=True)  # Para bloquear cuentas
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    auth_identities = relationship("AuthIdentity", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    owned_groups = relationship("Group", foreign_keys="Group.owner_id", back_populates="owner", cascade="all, delete-orphan")
    group_memberships = relationship("GroupMember", foreign_keys="GroupMember.user_id", back_populates="user", cascade="all, delete-orphan")
    created_wishlists = relationship("Wishlist", back_populates="creator", cascade="all, delete-orphan")
    item_claims = relationship("ItemClaim", back_populates="user", cascade="all, delete-orphan")
    item_contributions = relationship("ItemContribution", back_populates="user", cascade="all, delete-orphan")
    sent_contribution_invites = relationship("ContributionInvite", foreign_keys="ContributionInvite.inviter_id", back_populates="inviter", cascade="all, delete-orphan")
    item_activities = relationship("ItemActivity", back_populates="actor", cascade="all, delete-orphan")
