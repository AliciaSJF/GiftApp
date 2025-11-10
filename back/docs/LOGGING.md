# Sistema de Logging - Guía de Uso

## Características

El sistema de logging incluye:

- ✅ **Colores** para diferentes niveles de log
- ✅ **Trazabilidad mejorada** con módulo, clase, función y línea
- ✅ **Bibliotecas silenciadas** (SQLAlchemy, Uvicorn, etc.)
- ✅ **Formato detallado** para fácil depuración

## Formato de los Logs

```
[2024-01-15 14:30:25] INFO     [app.routers.users] create_user:18 - Intentando crear usuario: alicia (alicia@example.com)
```

**Desglose:**
- `[2024-01-15 14:30:25]` - Fecha y hora
- `INFO` - Nivel (con color)
- `[app.routers.users]` - Módulo/clase
- `create_user:18` - Función y línea de código
- `- Mensaje` - Mensaje del log

## Niveles de Log y Colores

- 🔵 **DEBUG** (cyan) - Información detallada para depuración
- 🟢 **INFO** (verde) - Información general
- 🟡 **WARNING** (amarillo) - Advertencias
- 🔴 **ERROR** (rojo) - Errores
- ⚪ **CRITICAL** (rojo sobre blanco) - Errores críticos

## Cómo Usar el Logging

### Opción 1: Usando `get_logger()` (Recomendado)

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

def mi_funcion():
    logger.info("Mensaje informativo")
    logger.debug("Mensaje de debug")
    logger.warning("Advertencia")
    logger.error("Error ocurrido")
```

### Opción 2: Usando `LoggerMixin` en Clases

```python
from app.core.logging_config import LoggerMixin

class MiClase(LoggerMixin):
    def mi_metodo(self):
        self.logger.info("Mensaje desde la clase")
        self.logger.error("Error en la clase")
```

### Opción 3: Logger estándar de Python

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Mensaje")
```

## Ejemplos de Uso

### En Routers

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

@router.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    logger.info(f"Creando item: {item.title}")
    try:
        new_item = item_service.create_item(db, item)
        logger.info(f"Item creado exitosamente: ID={new_item.id}")
        return new_item
    except Exception as e:
        logger.error(f"Error al crear item: {e}", exc_info=True)
        raise
```

### En Servicios

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

def process_data(data: dict):
    logger.debug(f"Procesando datos: {data}")
    # ... lógica ...
    logger.info("Datos procesados correctamente")
```

### En Repositorios

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

def get_user(db: Session, user_id: int):
    logger.debug(f"Buscando usuario con ID: {user_id}")
    user = db.get(User, user_id)
    if user:
        logger.debug(f"Usuario encontrado: {user.username}")
    else:
        logger.warning(f"Usuario no encontrado: ID={user_id}")
    return user
```

## Bibliotecas Silenciadas

Las siguientes bibliotecas están configuradas para generar menos ruido:

- **SQLAlchemy** - Solo WARNING (o DEBUG si `DEBUG=True`)
- **Uvicorn Access** - Solo WARNING
- **HTTPX** - Solo WARNING
- **HTTPCore** - Solo WARNING
- **Passlib** - Solo WARNING
- **Cryptography** - Solo WARNING
- **Pydantic** - Solo WARNING
- **Watchfiles** - Solo WARNING

**Alembic** mantiene INFO para ver las migraciones.

## Configuración

El logging se configura automáticamente en `main.py`:

```python
from app.core.logging_config import setup_logging

setup_logging(debug=settings.DEBUG)
```

### Variables de Entorno

El nivel de logging se controla con:

```env
DEBUG=True   # Muestra logs DEBUG y silencia menos bibliotecas
DEBUG=False  # Solo INFO y superior, más bibliotecas silenciadas
```

## Mejores Prácticas

### 1. Usa el nivel apropiado

```python
# ✅ Correcto
logger.debug("Detalles técnicos para depuración")
logger.info("Evento importante del negocio")
logger.warning("Situación que requiere atención")
logger.error("Error que necesita corrección")

# ❌ Evitar
logger.info("Variable x = 5")  # Usa debug
logger.error("Usuario no encontrado")  # Usa warning si es esperado
```

### 2. Incluye contexto útil

```python
# ✅ Bueno
logger.info(f"Usuario autenticado: {user.username} (ID={user.id})")
logger.error(f"Error al procesar pedido {order_id}: {error}")

# ❌ Malo
logger.info("Usuario autenticado")
logger.error("Error")
```

### 3. Usa `exc_info=True` para excepciones

```python
try:
    # código
except Exception as e:
    logger.error(f"Error al procesar: {e}", exc_info=True)
    # Esto incluye el traceback completo
```

### 4. Logs estructurados para búsqueda

```python
# ✅ Fácil de buscar
logger.info(f"Pedido creado: order_id={order_id}, user_id={user_id}, total={total}")

# Permite buscar: "order_id=123" en los logs
```

## Trazabilidad

El formato incluye:

1. **Módulo/Clase**: `[app.routers.users]` - Dónde ocurre
2. **Función**: `create_user` - Qué función
3. **Línea**: `:18` - Línea exacta del código
4. **Timestamp**: `[2024-01-15 14:30:25]` - Cuándo ocurre

Esto facilita:
- Encontrar el código exacto que generó el log
- Rastrear el flujo de ejecución
- Depurar problemas rápidamente

## Ejemplo de Salida

```
[2024-01-15 14:30:25] INFO     [app.main] lifespan:26 - Inicializando base de datos...
[2024-01-15 14:30:25] INFO     [app.main] lifespan:33 - Conexión a la base de datos verificada correctamente
[2024-01-15 14:30:28] INFO     [app.routers.users] create_user:18 - Intentando crear usuario: alicia (alicia@example.com)
[2024-01-15 14:30:28] DEBUG    [app.services.user_service] create_user:36 - Creando usuario: alicia
[2024-01-15 14:30:28] INFO     [app.services.user_service] create_user:43 - Usuario creado: ID=1, username=alicia
[2024-01-15 14:30:28] INFO     [app.routers.users] create_user:40 - Usuario creado exitosamente: ID=1, username=alicia
```

## Personalización

Para personalizar el logging, edita `src/app/core/logging_config.py`:

- Cambiar colores: Modifica `log_colors` en el `ColoredFormatter`
- Cambiar formato: Modifica el `fmt` en el formatter
- Agregar más bibliotecas silenciadas: Agrega en `_silence_noisy_libraries()`
- Cambiar niveles: Modifica los `setLevel()` en las funciones de configuración

