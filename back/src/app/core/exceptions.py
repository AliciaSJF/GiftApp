"""
Excepciones personalizadas comunes de la aplicación

Para crear una nueva excepción:
1. Crea una clase que herede de AppException
2. Define el __init__ con los parámetros que necesites
3. Llama a super().__init__() con message, status_code y details
4. ¡Ya está! El gestor automático la manejará

Ejemplo:
    class MiExcepcion(AppException):
        def __init__(self, message: str, details: Optional[dict] = None):
            super().__init__(
                message=message,
                status_code=400,
                details=details or {}
            )
"""
from typing import Optional, Any


class AppException(Exception):
    """
    Excepción base para todas las excepciones de la aplicación.
    
    Todas las excepciones que hereden de esta clase serán manejadas
    automáticamente por el gestor de excepciones en main.py.
    """
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """Recurso no encontrado"""
    
    def __init__(self, resource: str, identifier: Any, details: Optional[dict] = None):
        message = f"{resource} no encontrado"
        if identifier is not None:
            message += f" (ID: {identifier})"
        super().__init__(
            message=message,
            status_code=404,
            details=details or {"resource": resource, "identifier": identifier}
        )


class AlreadyExistsError(AppException):
    """Recurso que ya existe"""
    
    def __init__(self, resource: str, field: str, value: Any, details: Optional[dict] = None):
        message = f"{resource} con {field} '{value}' ya existe"
        super().__init__(
            message=message,
            status_code=400,
            details=details or {"resource": resource, "field": field, "value": value}
        )


class ValidationError(AppException):
    """Error de validación"""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=422,
            details=details or ({"field": field} if field else {})
        )


class AuthenticationError(AppException):
    """Error de autenticación"""
    
    def __init__(self, message: str = "Credenciales incorrectas", details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=401,
            details=details or {}
        )


class AuthorizationError(AppException):
    """Error de autorización (permisos insuficientes)"""
    
    def __init__(self, message: str = "No tienes permisos para realizar esta acción", details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=403,
            details=details or {}
        )


class DatabaseError(AppException):
    """Error relacionado con la base de datos"""
    
    def __init__(self, message: str = "Error en la base de datos", details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=500,
            details=details or {}
        )


class ConflictError(AppException):
    """Conflicto de estado (ej: intentar eliminar un recurso en uso)"""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=409,
            details=details or {}
        )
