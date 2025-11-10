"""
Schemas Pydantic para items
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Schema base para item"""
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema para crear un item"""
    pass


class ItemUpdate(BaseModel):
    """Schema para actualizar un item"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class ItemInDB(ItemBase):
    """Schema de item en base de datos"""
    id: int
    is_completed: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Item(ItemInDB):
    """Schema de item para respuesta"""
    pass

