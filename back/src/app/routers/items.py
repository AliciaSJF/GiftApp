"""
Router para endpoints de items
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions import NotFoundError
from app.core.logging_config import get_logger
from app.db.session import get_db
from app.schemas import item as item_schema
from app.services import item_service as item_service_module

router = APIRouter(prefix="/items", tags=["items"])
logger = get_logger(__name__)


@router.post("/", response_model=item_schema.Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item: item_schema.ItemCreate,
    owner_id: int,  # En producción, esto vendría del token JWT
    db: Session = Depends(get_db)
):
    """Crea un nuevo item"""
    return item_service_module.create_item(db=db, item=item, owner_id=owner_id)


@router.get("/", response_model=List[item_schema.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    owner_id: int = None,
    db: Session = Depends(get_db)
):
    """Obtiene una lista de items"""
    items = item_service_module.get_items(db, skip=skip, limit=limit, owner_id=owner_id)
    return items


@router.get("/{item_id}", response_model=item_schema.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Obtiene un item por ID"""
    db_item = item_service_module.get_item(db, item_id=item_id)
    if db_item is None:
        raise NotFoundError(resource="Item", identifier=item_id)
    return db_item


@router.put("/{item_id}", response_model=item_schema.Item)
def update_item(
    item_id: int,
    item_update: item_schema.ItemUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un item"""
    db_item = item_service_module.update_item(db, item_id, item_update)
    if db_item is None:
        raise NotFoundError(resource="Item", identifier=item_id)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Elimina un item"""
    success = item_service_module.delete_item(db, item_id)
    if not success:
        raise NotFoundError(resource="Item", identifier=item_id)

