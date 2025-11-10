from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class ItemActivity(Base):
    """Comentarios/actividad (opcional)."""

    __tablename__ = "item_activity"

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
    actor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    kind = Column(Text, nullable=False)  # 'note', 'status_change', 'auto_split', 'invite_sent', etc.
    payload = Column(JSONB, nullable=True)  # Datos adicionales de la actividad
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    item = relationship("Item", back_populates="activity")
    actor = relationship("User", back_populates="item_activities")

