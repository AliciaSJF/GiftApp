"""
Router para endpoints de usuarios
"""
from fastapi import APIRouter, status
from typing import List
from datetime import timedelta

from app.core.config import settings
from app.core.dependencies import UserServiceDep
from app.core.logging_config import get_logger
from app.core.exceptions import NotFoundError, AlreadyExistsError, AuthenticationError
from app.core.security import create_access_token
from app.schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger(__name__)


@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: user_schema.UserCreate,
    user_service: UserServiceDep,
):
    """Crea un nuevo usuario"""
    logger.info(f"Intentando crear usuario: {user.username} ({user.email})")
    
    # Verificar si el usuario ya existe
    db_user = user_service.get_user_by_email(user.email)
    if db_user:
        raise AlreadyExistsError(resource="Usuario", field="email", value=user.email)
    
    db_user = user_service.get_user_by_username(user.username)
    if db_user:
        raise AlreadyExistsError(resource="Usuario", field="username", value=user.username)
    
    new_user = user_service.create_user(user)
    logger.info(f"Usuario creado exitosamente: ID={new_user.id}, username={new_user.username}")
    return new_user


@router.get("/", response_model=List[user_schema.User])
def read_users(user_service: UserServiceDep, skip: int = 0, limit: int = 100):
    """Obtiene una lista de usuarios"""
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, user_service: UserServiceDep):
    """Obtiene un usuario por ID"""
    db_user = user_service.get_user(user_id)
    if db_user is None:
        raise NotFoundError(resource="Usuario", identifier=user_id)
    return db_user


@router.put("/{user_id}", response_model=user_schema.User)
def update_user(
    user_id: int,
    user_update: user_schema.UserUpdate,
    user_service: UserServiceDep,
):
    """Actualiza un usuario"""
    db_user = user_service.update_user(user_id, user_update)
    if db_user is None:
        raise NotFoundError(resource="Usuario", identifier=user_id)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, user_service: UserServiceDep):
    """Elimina un usuario"""
    success = user_service.delete_user(user_id)
    if not success:
        raise NotFoundError(resource="Usuario", identifier=user_id)


@router.post("/login", response_model=user_schema.Token)
def login(user_credentials: user_schema.UserLogin, user_service: UserServiceDep):
    """Autentica un usuario y devuelve un token JWT"""
    logger.info(f"Intento de login para usuario: {user_credentials.username}")
    
    user = user_service.authenticate_user(
        user_credentials.username, user_credentials.password
    )
    if not user:
        raise AuthenticationError(
            message="Credenciales incorrectas",
            details={"username": user_credentials.username}
        )
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_EXPIRES_MIN)
    # Usar el ID del usuario (UUID) como subject en el token
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    logger.info(f"Login exitoso para usuario: {user.display_name or user.email} (ID={user.id})")
    return {"access_token": access_token, "token_type": "bearer"}

