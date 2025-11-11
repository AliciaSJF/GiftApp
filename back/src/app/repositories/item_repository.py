"""Repositorio para operaciones de items."""
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.db.models.item import Item


class ItemRepository:
    """Repositorio para operaciones de base de datos relacionadas con items."""

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db

    def get(self, item_id: int) -> Optional[Item]:
        """Obtiene un item por ID."""
        return self.db.get(Item, item_id)

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
    ) -> Sequence[Item]:
        """Obtiene una lista paginada de items, opcionalmente filtrados por propietario."""
        query = self.db.query(Item)
        if owner_id is not None:
            query = query.filter(Item.owner_id == owner_id)
        return query.offset(skip).limit(limit).all()

    def create(self, *, owner_id: int, data: dict) -> Item:
        """Crea un item."""
        item = Item(owner_id=owner_id, **data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: Item, *, values: dict) -> Item:
        """Actualiza campos de un item."""
        for field, value in values.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Item) -> None:
        """Elimina un item."""
        self.db.delete(item)
        self.db.commit()
