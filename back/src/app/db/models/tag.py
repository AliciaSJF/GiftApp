from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Tag(Base):
    """Modelo de tags."""

    __tablename__ = "tags"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
        index=True
    )
    name = Column(Text, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    wishlists = relationship("WishlistTag", back_populates="tag", cascade="all, delete-orphan")


class WishlistTag(Base):
    """Modelo de relación muchos-a-muchos entre wishlists y tags."""

    __tablename__ = "wishlist_tags"

    wishlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wishlists.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    tag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )

    # Relaciones
    wishlist = relationship("Wishlist", back_populates="tags")
    tag = relationship("Tag", back_populates="wishlists")

