from sqlalchemy import Column, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.models.enums import ListRole, SubjectType
from app.db.session import Base


class Wishlist(Base):
    """Modelo de listas de deseos."""

    __tablename__ = "wishlists"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relaciones
    creator = relationship("User", back_populates="created_wishlists")
    permissions = relationship("WishlistPermission", back_populates="wishlist", cascade="all, delete-orphan")
    tags = relationship("WishlistTag", back_populates="wishlist", cascade="all, delete-orphan")
    items = relationship("Item", back_populates="wishlist", cascade="all, delete-orphan")


class WishlistPermission(Base):
    """Modelo de permisos de listas (ACL por rol)."""

    __tablename__ = "wishlist_permissions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    wishlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wishlists.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    subject_kind = Column(Text, nullable=False, index=True)  # 'user' o 'group' - usar SubjectType enum en la aplicación
    subject_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # users.id o groups.id
    role = Column(
        Text,
        nullable=False,
        default=ListRole.VIEWER.value
    )  # 'owner', 'editor', 'viewer' - usar ListRole enum en la aplicación

    # Relaciones
    wishlist = relationship("Wishlist", back_populates="permissions")

    __table_args__ = (
        # Unique constraint para (wishlist_id, subject_kind, subject_id)
        UniqueConstraint("wishlist_id", "subject_kind", "subject_id", name="uq_wishlist_permission"),
    )

