"""
Configuración de la aplicación usando variables de entorno
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Aplicación
    APP_NAME: str = "Wishy"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    APP_BASE_URL: Optional[str] = None
    
    # Base de datos
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/dbname"
    
    # OAuth Google
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    OAUTH_GOOGLE_REDIRECT_URI: Optional[str] = None
    
    # Frontend URL (para redirecciones OAuth)
    FRONTEND_URL: Optional[str] = None
    
    # JWT
    JWT_SECRET: str
    JWT_ACCESS_EXPIRES_MIN: int = 30
    JWT_REFRESH_EXPIRES_DAYS: int = 7
    ALGORITHM: str = "HS256"
    

    # Password
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 100
    PEPPER: str
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # Ignorar variables extra en el .env
    )


# Instancia global de configuración
settings = Settings()
logger.info("Configuración cargada correctamente")
