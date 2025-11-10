"""Repositorio para operaciones de items."""
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.db.models.item import Item


def get(db: Session, item_id: int) -> Optional[Item]:
    """Obtiene un item por ID."""
    return db.get(Item, item_id)


def get_multi(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
) -> Sequence[Item]:
    """Obtiene una lista paginada de items, opcionalmente filtrados por propietario."""
    query = db.query(Item)
    if owner_id is not None:
        query = query.filter(Item.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()


def create(db: Session, *, owner_id: int, data: dict) -> Item:
    """Crea un item."""
    item = Item(owner_id=owner_id, **data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update(db: Session, item: Item, *, values: dict) -> Item:
    """Actualiza campos de un item."""
    for field, value in values.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item: Item) -> None:
    """Elimina un item."""
    db.delete(item)
    db.commit()
