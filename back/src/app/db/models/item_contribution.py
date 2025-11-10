from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class ItemContribution(Base):
    """Contribuciones por persona (para regalos en grupo)."""

    __tablename__ = "item_contributions"

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
    amount_cents = Column(Integer, nullable=False)  # Importe en céntimos
    locked = Column(Boolean, nullable=False, default=False)  # Si el usuario fijó su importe explícito
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    item = relationship("Item", back_populates="contributions")
    user = relationship("User", back_populates="item_contributions")

    __table_args__ = (
        CheckConstraint("amount_cents >= 0", name="check_amount_positive"),
        UniqueConstraint("item_id", "user_id", name="uq_item_contribution"),
    )

