"""
Configuración avanzada de logging con colores y trazabilidad mejorada
"""
import logging
import sys
from typing import Optional

import colorlog


def setup_logging(debug: bool = False) -> None:
    """
    Configura el sistema de logging con:
    - Colores para diferentes niveles
    - Formato detallado con clase/módulo
    - Silenciamiento de bibliotecas ruidosas
    - Mejor trazabilidad
    """
    # Nivel base según modo debug
    root_level = logging.DEBUG if debug else logging.INFO
    
    # Crear handler con colores
    handler = colorlog.StreamHandler(sys.stdout)
    handler.setLevel(root_level)
    
    # Formato detallado con colores
    # Formato: [FECHA] [NIVEL] [MÓDULO.CLASE] [FUNCIÓN:LÍNEA] - MENSAJE
    formatter = colorlog.ColoredFormatter(
        fmt=(
            "%(log_color)s%(bold)s[%(asctime)s]%(reset)s "
            "%(log_color)s%(levelname)-8s%(reset)s "
            "%(cyan)s[%(name)s]%(reset)s "
            "%(blue)s%(funcName)s:%(lineno)d%(reset)s "
            "- %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    
    handler.setFormatter(formatter)
    
    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(root_level)
    root_logger.handlers = [handler]  # Reemplazar handlers existentes
    
    # Silenciar bibliotecas ruidosas
    _silence_noisy_libraries(debug)
    
    # Configurar loggers específicos de la aplicación
    _configure_app_loggers(debug)


def _silence_noisy_libraries(debug: bool) -> None:
    """Silencia bibliotecas que generan muchos logs innecesarios"""
    
    # SQLAlchemy - completamente silenciado (solo CRITICAL)
    # Silenciar todos los loggers de SQLAlchemy
    sqlalchemy_loggers = [
        "sqlalchemy",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "sqlalchemy.dialects",
        "sqlalchemy.orm",
        "sqlalchemy.dialects.postgresql",
        "sqlalchemy.dialects.postgresql.psycopg",
        "sqlalchemy.dialects.postgresql.psycopg2",
    ]
    for logger_name in sqlalchemy_loggers:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL)
        logging.getLogger(logger_name).propagate = False  # Evitar propagación
    
    # Uvicorn - solo información importante
    uvicorn_level = logging.DEBUG if debug else logging.INFO
    logging.getLogger("uvicorn").setLevel(uvicorn_level)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)  # Silenciar access logs
    logging.getLogger("uvicorn.error").setLevel(uvicorn_level)
    
    # HTTPX - solo errores
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # HTTPCore - solo errores
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # Passlib - solo errores
    logging.getLogger("passlib").setLevel(logging.WARNING)
    
    # Cryptography - solo errores
    logging.getLogger("cryptography").setLevel(logging.WARNING)
    
    # Pydantic - solo errores
    logging.getLogger("pydantic").setLevel(logging.WARNING)
    
    # Alembic - mantener INFO para ver migraciones
    logging.getLogger("alembic").setLevel(logging.INFO)
    
    # Watchfiles (usado por uvicorn --reload) - silenciar
    logging.getLogger("watchfiles").setLevel(logging.WARNING)


def _configure_app_loggers(debug: bool) -> None:
    """Configura loggers específicos de la aplicación"""
    
    # Logger principal de la app
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Loggers por módulo para mejor organización
    logging.getLogger("app.core").setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger("app.db").setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger("app.routers").setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger("app.services").setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger("app.repositories").setLevel(logging.DEBUG if debug else logging.INFO)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Obtiene un logger configurado.
    
    Uso recomendado:
        logger = get_logger(__name__)
        logger.info("Mensaje informativo")
        logger.error("Error ocurrido")
    
    Args:
        name: Nombre del logger (normalmente __name__ del módulo)
    
    Returns:
        Logger configurado con el sistema de logging
    """
    if name is None:
        # Intentar obtener el nombre del módulo que llama
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get("__name__", "app")
        else:
            name = "app"
    
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin para agregar logging fácilmente a cualquier clase.
    
    Ejemplo:
        class MiClase(LoggerMixin):
            def mi_metodo(self):
                self.logger.info("Ejecutando método")
                self.logger.error("Error en método")
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Retorna un logger con el nombre de la clase"""
        class_name = self.__class__.__module__ + "." + self.__class__.__name__
        return logging.getLogger(class_name)

