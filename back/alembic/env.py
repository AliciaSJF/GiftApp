"""Configuración del entorno de Alembic."""
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Importar la configuración y los modelos
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.core.config import settings
from app.db.session import Base
# Importar todos los modelos para que Alembic los detecte
from app.db.models import (
    AuthIdentity,
    ContributionInvite,
    Group,
    GroupMember,
    Item,
    ItemACL,
    ItemActivity,
    ItemClaim,
    ItemContribution,
    Session,
    Tag,
    User,
    Wishlist,
    WishlistPermission,
    WishlistTag,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    """Obtiene la URL de la base de datos desde la configuración."""
    database_url = settings.DATABASE_URL
    
    # Normalizar la URL para usar psycopg (versión 3) para Python 3.13+
    if database_url.startswith("postgresql://"):
        # Reemplazar postgresql:// por postgresql+psycopg:// para usar psycopg v3
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql+psycopg2://"):
        # Si ya especifica psycopg2, cambiar a psycopg v3
        database_url = database_url.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)
    # Si ya tiene postgresql+psycopg://, dejarlo como está
    
    return database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

