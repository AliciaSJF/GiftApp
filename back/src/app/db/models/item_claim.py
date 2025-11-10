from sqlalchemy import Column, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.models.enums import ClaimStatus
from app.db.session import Base


class ItemClaim(Base):
    """Estado de 'me lo pido / lo compré / etc.'."""

    __tablename__ = "item_claims"

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
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    status = Column(
        Text,
        nullable=False
    )  # interested/claimed/purchased/released/cancelled - usar ClaimStatus enum
    note = Column(Text, nullable=True)  # "¿alguien se apunta? pongo 20€"
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relaciones
    item = relationship("Item", back_populates="claims")
    user = relationship("User", back_populates="item_claims")

    __table_args__ = (
        # Un estado activo por usuario
        UniqueConstraint("item_id", "user_id", name="uq_item_claim"),
    )

