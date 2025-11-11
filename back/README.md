# FastAPI Template

Plantilla base para proyectos FastAPI con estructura organizada y ejemplos mínimos funcionales.

## Estructura del Proyecto

```
fastapi-template/
├── src/
│   └── app/
│       ├── core/           # Configuración y seguridad
│       ├── db/
│       │   ├── models/     # Modelos SQLAlchemy (un archivo por modelo)
│       │   └── session.py  # Sesión y Base
│       ├── repositories/   # Acceso a datos
│       ├── routers/        # Endpoints de la API
│       ├── schemas/        # Schemas Pydantic
│       ├── services/       # Lógica de negocio
│       ├── utils/          # Utilidades
│       └── main.py         # Aplicación principal
├── tests/                  # Tests
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias
├── Dockerfile              # Configuración Docker
└── docker-compose.yml      # Docker Compose
```

## Características

- ✅ Estructura organizada y escalable
- ✅ Autenticación JWT
- ✅ Base de datos PostgreSQL con SQLAlchemy
- ✅ Alembic para migraciones de base de datos
- ✅ Lifespan para inicialización y verificación de BD
- ✅ Sistema de logging con colores y trazabilidad mejorada
- ✅ Sistema de excepciones personalizadas con gestores centralizados
- ✅ Schemas Pydantic para validación
- ✅ Separación de responsabilidades (routers, services, repositories, schemas)
- ✅ Repositorios dedicados para acceso a datos
- ✅ Configuración mediante variables de entorno
- ✅ Docker y Docker Compose con PostgreSQL
- ✅ Tests de ejemplo

## Instalación

### Opción 1: Instalación Local

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar .env con tus configuraciones
# Especialmente importante: DATABASE_URL y SECRET_KEY
```

4. Asegúrate de tener PostgreSQL corriendo localmente o usa Docker Compose

5. Aplicar migraciones de base de datos:
```bash
alembic upgrade head
```

6. Ejecutar la aplicación:

En Windows PowerShell:
```powershell
$env:PYTHONPATH="src"; uvicorn app.main:app --reload
```

En Linux/Mac:
```bash
PYTHONPATH=src uvicorn app.main:app --reload
```

**Nota**: 
- El lifespan de la aplicación verificará automáticamente la conexión a la base de datos al iniciar.
- Las migraciones de base de datos se gestionan con Alembic. Ver [ALEMBIC.md](ALEMBIC.md) para más información.

### Opción 2: Docker

1. Construir y ejecutar con Docker Compose:
```bash
docker-compose up --build
```

2. La aplicación estará disponible en: http://localhost:8000

## Uso

### Endpoints Disponibles

- `GET /` - Endpoint raíz
- `GET /health` - Verificación de salud
- `GET /docs` - Documentación interactiva (Swagger)
- `GET /redoc` - Documentación alternativa (ReDoc)

### API de Usuarios (`/users`)

- `POST /users/` - Crear usuario
- `GET /users/` - Listar usuarios
- `GET /users/{user_id}` - Obtener usuario
- `PUT /users/{user_id}` - Actualizar usuario
- `DELETE /users/{user_id}` - Eliminar usuario
- `POST /users/login` - Autenticación (obtener token)

### API de Items (`/items`)

- `POST /items/` - Crear item
- `GET /items/` - Listar items
- `GET /items/{item_id}` - Obtener item
- `PUT /items/{item_id}` - Actualizar item
- `DELETE /items/{item_id}` - Eliminar item

## Ejemplos de Uso

### Crear un usuario

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "username": "usuario",
    "password": "contraseña123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "contraseña123"
  }'
```

### Crear un item

```bash
curl -X POST "http://localhost:8000/items/?owner_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primer item",
    "description": "Descripción del item"
  }'
```

## Testing

Ejecutar tests:

```bash
pytest tests/
```

## Configuración

Las configuraciones se manejan mediante variables de entorno en el archivo `.env`:

### Base de Datos (PostgreSQL)

- `DATABASE_URL`: URL completa de conexión (ej: `postgresql://user:password@localhost:5432/dbname`)
- O usar variables individuales:
  - `POSTGRES_USER`: Usuario de PostgreSQL
  - `POSTGRES_PASSWORD`: Contraseña de PostgreSQL
  - `POSTGRES_SERVER`: Servidor (localhost o nombre del servicio en Docker)
  - `POSTGRES_PORT`: Puerto (por defecto 5432)
  - `POSTGRES_DB`: Nombre de la base de datos

### Aplicación

- `APP_NAME`: Nombre de la aplicación
- `SECRET_KEY`: Clave secreta para JWT (cambiar en producción)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token
- `CORS_ORIGINS`: Orígenes permitidos para CORS
- `DEBUG`: Modo debug (True/False)

### Lifespan

La aplicación incluye un lifespan que:
- Inicializa las tablas de la base de datos al arrancar
- Prueba la conexión a PostgreSQL antes de aceptar requests
- Cierra las conexiones correctamente al apagar la aplicación

## Migraciones de Base de Datos

Este proyecto usa **Alembic** para gestionar las migraciones de base de datos.

### Comandos Básicos

```bash
# Ver el estado actual
alembic current

# Crear una nueva migración (automática)
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Reversar última migración
alembic downgrade -1
```

Para una guía completa sobre cómo usar Alembic, consulta [ALEMBIC.md](ALEMBIC.md).

## Logging

El proyecto incluye un sistema de logging avanzado con:

- **Colores** para diferentes niveles de log
- **Trazabilidad mejorada** (módulo, clase, función, línea)
- **Bibliotecas silenciadas** (SQLAlchemy, Uvicorn, etc.)
- **Formato detallado** para fácil depuración

**Ejemplo de uso:**
```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Mensaje informativo")
logger.error("Error ocurrido")
```

Para más información, consulta [LOGGING.md](LOGGING.md).

## Sistema de Excepciones

El proyecto incluye un sistema completo de gestión de excepciones con:

- **Excepciones personalizadas** para errores comunes (NotFoundError, AlreadyExistsError, ValidationError, etc.)
- **Gestores centralizados** que formatean todas las respuestas de error de forma consistente
- **Logging automático** de todas las excepciones con contexto completo
- **Formato estándar** de respuesta de error

**Ejemplo de uso:**
```python
from app.core.exceptions import NotFoundError, AlreadyExistsError

# Recurso no encontrado
raise NotFoundError(resource="Usuario", identifier=user_id)

# Recurso duplicado
raise AlreadyExistsError(resource="Usuario", field="email", value=email)
```

Todas las excepciones se manejan automáticamente y devuelven respuestas en formato JSON consistente.

Para más información y ejemplos, consulta [EXCEPCIONES.md](EXCEPCIONES.md).

## Desarrollo