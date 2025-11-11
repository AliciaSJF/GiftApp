"""
Servicio de lógica de negocio para items
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.db.models.item import Item
from app.repositories.item_repository import ItemRepository
from app.schemas import item as item_schema

logger = get_logger(__name__)


class ItemService:
    """Servicio de lógica de negocio para items."""

    def __init__(self, item_repository: ItemRepository):
        """
        Inicializa el servicio con un repositorio de items.
        
        Args:
            item_repository: Repositorio de items
        """
        self.logger = logger
        self.item_repository = item_repository

    def get_item(self, item_id: int) -> Optional[Item]:
        """Obtiene un item por ID."""
        return self.item_repository.get(item_id)

    def get_items(
        self,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
    ) -> List[Item]:
        """Obtiene una lista de items."""
        return list(
            self.item_repository.get_multi(
                skip=skip, limit=limit, owner_id=owner_id
            )
        )

    def create_item(self, item: item_schema.ItemCreate, owner_id: int) -> Item:
        """Crea un nuevo item."""
        return self.item_repository.create(
            owner_id=owner_id,
            data=item.model_dump(),
        )

    def update_item(
        self,
        item_id: int,
        item_update: item_schema.ItemUpdate,
    ) -> Optional[Item]:
        """Actualiza un item."""
        db_item = self.get_item(item_id)
        if not db_item:
            return None

        update_data = item_update.model_dump(exclude_unset=True)
        return self.item_repository.update(db_item, values=update_data)

    def delete_item(self, item_id: int) -> bool:
        """Elimina un item."""
        db_item = self.get_item(item_id)
        if not db_item:
            return False

        self.item_repository.delete(db_item)
        return True
