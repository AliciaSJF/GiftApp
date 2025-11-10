"""
Servicio de lógica de negocio para items
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.db.models.item import Item
from app.repositories import item_repository
from app.schemas import item as item_schema

logger = get_logger(__name__)


def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Obtiene un item por ID."""
    return item_repository.get(db, item_id)


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
) -> List[Item]:
    """Obtiene una lista de items."""
    return list(
        item_repository.get_multi(
            db, skip=skip, limit=limit, owner_id=owner_id
        )
    )


def create_item(db: Session, item: item_schema.ItemCreate, owner_id: int) -> Item:
    """Crea un nuevo item."""
    return item_repository.create(
        db,
        owner_id=owner_id,
        data=item.model_dump(),
    )


def update_item(
    db: Session,
    item_id: int,
    item_update: item_schema.ItemUpdate,
) -> Optional[Item]:
    """Actualiza un item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    return item_repository.update(db, db_item, values=update_data)


def delete_item(db: Session, item_id: int) -> bool:
    """Elimina un item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return False

    item_repository.delete(db, db_item)
    return True

