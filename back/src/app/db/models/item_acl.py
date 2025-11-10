from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class ItemACL(Base):
    """ACL adicional solo si visibility='restricted'."""

    __tablename__ = "item_acl"

    item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    subject_kind = Column(Text, primary_key=True, nullable=False, index=True)  # 'user' o 'group'
    subject_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True)

    # Relaciones
    item = relationship("Item", back_populates="acl")

