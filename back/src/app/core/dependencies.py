"""
Dependencias de la aplicación usando Annotated para mejor tipado.

Este módulo centraliza todas las dependencias de FastAPI usando Annotated,
lo que mejora la legibilidad, el tipado y la mantenibilidad del código.

Uso:
    from app.core.dependencies import DBSession, CurrentUserDep, UserServiceDep

    @router.get("/items")
    def get_items(session: DBSession):
        ...
    
    @router.post("/items")
    def create_item(item: ItemCreate, user_service: UserServiceDep, current_user: CurrentUserDep):
        ...
"""
from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth import (
    get_current_active_user,
    get_current_user,
    get_optional_current_user,
)
from app.db.models.user import User
from app.db.session import get_db
from app.repositories.auth_identity_repository import AuthIdentityRepository
from app.repositories.item_repository import ItemRepository
from app.repositories.user_repository import UserRepository
from app.services.item_service import ItemService
from app.services.oauth_service import OAuthService
from app.services.user_service import UserService


# ============================================================================
# Dependencia de Sesión de Base de Datos
# ============================================================================

DBSession = Annotated[Session, Depends(get_db)]


# ============================================================================
# Dependencias de Autenticación
# ============================================================================

# Las funciones de autenticación están en core.auth.py
# Aquí solo creamos los tipos anotados para usar en routers

CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]
OptionalCurrentUserDep = Annotated[Optional[User], Depends(get_optional_current_user)]


# ============================================================================
# Dependencias de Repositorios
# ============================================================================

def get_user_repository(session: DBSession) -> UserRepository:
    """Dependencia para obtener el repositorio de usuarios."""
    return UserRepository(session)


def get_item_repository(session: DBSession) -> ItemRepository:
    """Dependencia para obtener el repositorio de items."""
    return ItemRepository(session)


def get_auth_identity_repository(session: DBSession) -> AuthIdentityRepository:
    """Dependencia para obtener el repositorio de identidades de autenticación."""
    return AuthIdentityRepository(session)


# ============================================================================
# Dependencias de Servicios
# ============================================================================

def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """Dependencia para obtener el servicio de usuarios."""
    return UserService(user_repository)


def get_item_service(
    item_repository: Annotated[ItemRepository, Depends(get_item_repository)],
) -> ItemService:
    """Dependencia para obtener el servicio de items."""
    return ItemService(item_repository)


def get_oauth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    auth_identity_repository: Annotated[AuthIdentityRepository, Depends(get_auth_identity_repository)],
) -> OAuthService:
    """Dependencia para obtener el servicio de OAuth."""
    return OAuthService(
        user_repository=user_repository,
        auth_identity_repository=auth_identity_repository,
    )


# ============================================================================
# Tipos Anotados para Servicios (para usar en routers)
# ============================================================================

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
OAuthServiceDep = Annotated[OAuthService, Depends(get_oauth_service)]
