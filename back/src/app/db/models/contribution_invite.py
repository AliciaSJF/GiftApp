from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.models.enums import InviteStatus, SubjectType
from app.db.session import Base


class ContributionInvite(Base):
    """Invitaciones a aportar (a usuarios o grupos)."""

    __tablename__ = "contribution_invites"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    inviter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    subject_kind = Column(Text, nullable=False)  # 'user' o 'group' - usar SubjectType enum
    subject_id = Column(UUID(as_uuid=True), nullable=False)  # ID del usuario o grupo
    suggested_each_cents = Column(Integer, nullable=True)  # Reparto sugerido en el momento del envío
    status = Column(
        Text,
        nullable=False,
        default="pending"
    )  # pending/accepted/declined/expired - usar InviteStatus enum
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    responded_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    item = relationship("Item", back_populates="contribution_invites")
    inviter = relationship("User", foreign_keys=[inviter_id], back_populates="sent_contribution_invites")

