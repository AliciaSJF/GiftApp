"""
Configuración de la sesión de base de datos
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

logger = logging.getLogger(__name__)

# Verificar que psycopg esté disponible
try:
    import psycopg
    logger.debug(f"psycopg v3 disponible: {psycopg.__version__}")
except ImportError:
    logger.warning("psycopg v3 no está disponible. Asegúrate de tener psycopg[binary] instalado.")

# Crear el motor de la base de datos
# Forzar el uso de psycopg (versión 3) para Python 3.13+
database_url = settings.DATABASE_URL
original_url = database_url

# Normalizar la URL para usar psycopg v3
if database_url.startswith("postgresql://"):
    # Reemplazar postgresql:// por postgresql+psycopg:// para usar psycopg v3
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql+psycopg2://"):
    # Si ya especifica psycopg2, cambiar a psycopg v3
    database_url = database_url.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)
# Si ya tiene postgresql+psycopg://, dejarlo como está

if original_url != database_url:
    logger.info(f"URL de base de datos normalizada: {original_url} -> {database_url}")

engine = create_engine(
    database_url,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    echo=False,  # Silenciar queries SQL (siempre desactivado)
)

# Crear la clase base para los modelos
Base = declarative_base()

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependencia para obtener la sesión de base de datos.
    Uso en routers:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

