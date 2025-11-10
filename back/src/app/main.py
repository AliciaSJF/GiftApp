"""
Aplicación principal FastAPI
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
    database_exception_handler,
)
from app.core.exceptions import AppException
from app.db.session import engine, Base, SessionLocal
from app.routers import users, items
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

# Configurar logging con colores y trazabilidad
setup_logging(debug=settings.DEBUG)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan para inicializar y probar la conexión a la base de datos.
    Se ejecuta al iniciar y cerrar la aplicación.
    """
    # Startup: Inicializar base de datos
    logger.info("Inicializando base de datos...")
    
    try:
        # Probar la conexión (las tablas se crean con Alembic)
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1"))
            result.scalar()
            logger.info("Conexión a la base de datos verificada correctamente")
            logger.info("Nota: Las migraciones de base de datos se gestionan con Alembic")
            
    except Exception as e:
        logger.error(f"Error al conectar con la base de datos: {e}")
        raise
    
    yield
    
    # Shutdown: Cerrar conexiones
    logger.info("Cerrando conexiones a la base de datos...")
    engine.dispose()
    logger.info("Conexiones cerradas")


# Crear la aplicación FastAPI con lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Registrar gestores de excepciones (orden importante: más específicas primero)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)  # Maneja errores de SQLAlchemy
app.add_exception_handler(Exception, general_exception_handler)  # Catch-all para todo lo demás

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy"}

