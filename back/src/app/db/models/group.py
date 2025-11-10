from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Group(Base):
    """Modelo de grupos (Familia, Amigas, Clase, etc.)."""

    __tablename__ = "groups"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    name = Column(Text, nullable=False)  # p.ej. Familia, Amigas, Clase
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_groups")
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")


class GroupMember(Base):
    """Modelo de miembros de grupos."""

    __tablename__ = "group_members"

    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    added_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    group = relationship("Group", back_populates="members")
    user = relationship("User", foreign_keys=[user_id], back_populates="group_memberships")
    added_by_user = relationship("User", foreign_keys=[added_by])

