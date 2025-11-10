"""
Gestores de excepciones para FastAPI
"""
import logging
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

from app.core.exceptions import AppException, DatabaseError
from app.core.logging_config import get_logger

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Maneja excepciones personalizadas de la aplicación.
    
    Formato de respuesta:
    {
        "error": {
            "message": "Mensaje de error",
            "type": "NotFoundError",
            "details": {...}
        }
    }
    """
    logger.error(
        f"Excepción de aplicación: {exc.__class__.__name__} - {exc.message}",
        extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
                "details": exc.details,
            }
        }
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Maneja errores de validación de Pydantic.
    
    Formato de respuesta:
    {
        "error": {
            "message": "Error de validación",
            "type": "ValidationError",
            "details": {
                "errors": [...]
            }
        }
    }
    """
    errors = exc.errors()
    logger.warning(
        f"Error de validación en {request.url.path}: {errors}",
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Error de validación en los datos enviados",
                "type": "ValidationError",
                "details": {
                    "errors": errors
                }
            }
        }
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    Maneja excepciones HTTP estándar de Starlette/FastAPI.
    
    Formato de respuesta:
    {
        "error": {
            "message": "Mensaje de error",
            "type": "HTTPException",
            "details": {}
        }
    }
    """
    logger.warning(
        f"Excepción HTTP {exc.status_code}: {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "HTTPException",
                "details": {}
            }
        }
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Maneja excepciones de SQLAlchemy (base de datos).
    
    Convierte excepciones de SQLAlchemy en DatabaseError para mantener
    el formato consistente y no exponer detalles internos de la BD.
    """
    # Log completo para debugging
    logger.exception(
        f"Error de base de datos en {request.url.path}: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": exc.__class__.__name__,
        }
    )
    
    # Determinar mensaje según el tipo de error
    if isinstance(exc, IntegrityError):
        message = "Error de integridad en la base de datos (posible duplicado o violación de restricción)"
    elif isinstance(exc, OperationalError):
        message = "Error de conexión con la base de datos"
    else:
        message = "Error en la base de datos"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": message,
                "type": "DatabaseError",
                "details": {
                    "exception_type": exc.__class__.__name__
                }
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Maneja cualquier excepción no capturada.
    
    Este es el gestor "catch-all" que captura TODAS las excepciones que no
    hayan sido manejadas por los gestores más específicos, incluyendo:
    - Excepciones de librerías externas (requests, httpx, etc.)
    - Excepciones de Python estándar (ValueError, KeyError, etc.)
    - Cualquier otra excepción no prevista
    
    Formato de respuesta:
    {
        "error": {
            "message": "Error interno del servidor",
            "type": "InternalServerError",
            "details": {}
        }
    }
    """
    logger.exception(
        f"Excepción no manejada en {request.url.path}: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": exc.__class__.__name__,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Error interno del servidor",
                "type": "InternalServerError",
                "details": {}
            }
        }
    )

