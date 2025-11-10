"""
Schemas Pydantic para usuarios
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schema base para usuario"""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Schema para crear un usuario"""
    password: str


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema de usuario en base de datos"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """Schema de usuario para respuesta"""
    pass


class UserLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema para token de acceso"""
    access_token: str
    token_type: str = "bearer"

