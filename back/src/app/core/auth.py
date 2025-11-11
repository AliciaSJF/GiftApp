"""
Módulo de autenticación y autorización.

Contiene la lógica para obtener y validar usuarios autenticados desde tokens JWT.
"""
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.core.security import decode_access_token
from app.db.models.user import User
from app.db.session import get_db
from app.repositories.user_repository import UserRepository

logger = get_logger(__name__)

# Esquema de seguridad para tokens Bearer
security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db),
) -> User:
    """
    Obtiene el usuario actual desde el token JWT.
    
    Extrae el token del header Authorization, lo decodifica y obtiene
    el usuario correspondiente de la base de datos.
    
    Args:
        credentials: Credenciales HTTP Bearer del request
        session: Sesión de base de datos (inyectada automáticamente)
        
    Returns:
        User: Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    
    # Decodificar el token
    payload = decode_access_token(token)
    if payload is None:
        logger.warning("Intento de acceso con token inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener el subject (user_id) del token
    user_id_str = payload.get("sub")
    if not user_id_str:
        logger.warning("Token sin subject (sub)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta subject",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convertir a UUID
    try:
        user_id = UUID(user_id_str) if isinstance(user_id_str, str) else user_id_str
    except (ValueError, TypeError):
        logger.warning(f"Subject inválido en token: {user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: subject inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener el usuario de la base de datos usando el repositorio
    user_repository = UserRepository(session)
    user = user_repository.get(user_id)
    if user is None:
        logger.warning(f"Usuario no encontrado: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica que el usuario actual esté activo.
    
    Args:
        current_user: Usuario actual (inyectado por get_current_user)
        
    Returns:
        User: Usuario activo y autenticado
        
    Raises:
        HTTPException: Si el usuario no está activo
    """
    if not current_user.is_active:
        logger.warning(f"Intento de acceso de usuario inactivo: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    session: Session = Depends(get_db),
) -> Optional[User]:
    """
    Obtiene el usuario actual si hay un token válido (opcional).
    
    A diferencia de get_current_user, esta función no lanza excepción si no hay token.
    Útil para endpoints que pueden funcionar tanto autenticados como anónimos.
    
    Args:
        credentials: Credenciales HTTP Bearer (opcional)
        session: Sesión de base de datos
        
    Returns:
        User | None: Usuario si hay token válido, None en caso contrario
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(credentials, session)
    except HTTPException:
        return None
