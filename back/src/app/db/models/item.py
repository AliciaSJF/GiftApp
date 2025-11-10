from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Item(Base):
    """Modelo de items de una lista de deseos."""

    __tablename__ = "items"

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
    source_url = Column(Text, nullable=False)  # URL del producto
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    brand = Column(Text, nullable=True)
    price_cents = Column(Integer, nullable=True)  # Precio objetivo (al crear)
    currency = Column(Text, default="EUR")
    image_url = Column(Text, nullable=True)
    item_metadata = Column("metadata", JSONB, nullable=True)  # Datos del scraper (tallas, color, specs…)
    visibility = Column(Text, nullable=False, default="list")  # 'list' o 'restricted'
    max_contributors = Column(Integer, nullable=True)  # Límites cuando se pide cofinanciación
    min_contributors = Column(Integer, nullable=True)
    target_amount_cents = Column(Integer, nullable=True)  # Si difiere de price_cents (p.ej. vale regalo)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relaciones
    wishlist = relationship("Wishlist", back_populates="items")
    acl = relationship("ItemACL", back_populates="item", cascade="all, delete-orphan")
    claims = relationship("ItemClaim", back_populates="item", cascade="all, delete-orphan")
    contributions = relationship("ItemContribution", back_populates="item", cascade="all, delete-orphan")
    contribution_invites = relationship("ContributionInvite", back_populates="item", cascade="all, delete-orphan")
    activity = relationship("ItemActivity", back_populates="item", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("visibility IN ('list', 'restricted')", name="check_visibility_valid"),
    )
