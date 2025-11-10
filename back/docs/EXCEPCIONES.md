# Sistema de Excepciones y Gestión de Errores

## ⚠️ Importante: Formato de Respuestas

**Solo las respuestas de ERROR tienen formato estándar.** Las respuestas exitosas (200, 201, etc.) mantienen su formato normal según lo que devuelvas en cada endpoint.

### Respuestas de Error (Formato Estándar)
Todas las excepciones devuelven este formato:
```json
{
  "error": {
    "message": "Mensaje descriptivo del error",
    "type": "NombreDeLaExcepcion",
    "details": {...}
  }
}
```

### Respuestas Exitosas (Formato Libre)
Las respuestas exitosas pueden tener cualquier formato:
```json
// Ejemplo 1: Objeto simple
{"id": 1, "name": "Usuario"}

// Ejemplo 2: Lista
[{"id": 1}, {"id": 2}]

// Ejemplo 3: Objeto con estructura personalizada
{"data": {...}, "meta": {...}}
```

## ¿Se Manejan TODAS las Excepciones?

**✅ SÍ, todas las excepciones se manejan automáticamente.**

El sistema tiene un gestor "catch-all" que captura **cualquier excepción** que no haya sido manejada por los gestores más específicos:

```python
app.add_exception_handler(Exception, general_exception_handler)  # Catch-all
```

### Orden de Manejo (de más específico a más general)

1. **Excepciones personalizadas** (`AppException` y subclases)
   - `NotFoundError`, `AlreadyExistsError`, etc.
   - Formato: `{"error": {"message": "...", "type": "NotFoundError", ...}}`

2. **Errores de validación** (`RequestValidationError`)
   - Errores de Pydantic al validar request body/query params
   - Formato: `{"error": {"message": "...", "type": "ValidationError", ...}}`

3. **Excepciones HTTP** (`StarletteHTTPException`)
   - Excepciones HTTP estándar de FastAPI/Starlette
   - Formato: `{"error": {"message": "...", "type": "HTTPException", ...}}`

4. **Errores de SQLAlchemy** (`SQLAlchemyError`)
   - Errores de base de datos (IntegrityError, OperationalError, etc.)
   - Formato: `{"error": {"message": "...", "type": "DatabaseError", ...}}`

5. **Cualquier otra excepción** (`Exception` - catch-all)
   - Excepciones de librerías externas (requests, httpx, etc.)
   - Excepciones de Python estándar (ValueError, KeyError, AttributeError, etc.)
   - Cualquier otra excepción no prevista
   - Formato: `{"error": {"message": "Error interno del servidor", "type": "InternalServerError", ...}}`

### Ejemplos de Excepciones que se Manejan Automáticamente

#### Excepciones de Librerías Externas

```python
# requests
import requests
response = requests.get("https://api.example.com")  # Si falla, se maneja automáticamente

# httpx
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")  # Si falla, se maneja

# psycopg (PostgreSQL)
# Si hay un error de conexión o SQL, se captura como SQLAlchemyError

# Cualquier otra librería
# Todas las excepciones no manejadas van al catch-all
```

#### Excepciones de Python Estándar

```python
# ValueError
data = int("no es un número")  # Se maneja automáticamente

# KeyError
d = {}
value = d["key_inexistente"]  # Se maneja automáticamente

# AttributeError
obj = None
obj.metodo()  # Se maneja automáticamente

# Cualquier otra excepción de Python
```

## Excepciones Personalizadas

El proyecto incluye excepciones personalizadas para manejar errores comunes de forma consistente.

### Excepciones Disponibles

#### `NotFoundError`
Recurso no encontrado (404)

```python
from app.core.exceptions import NotFoundError

raise NotFoundError(resource="Usuario", identifier=user_id)
# Respuesta: {"error": {"message": "Usuario no encontrado (ID: 123)", "type": "NotFoundError", "details": {...}}}
```

#### `AlreadyExistsError`
Recurso que ya existe (400)

```python
from app.core.exceptions import AlreadyExistsError

raise AlreadyExistsError(resource="Usuario", field="email", value="user@example.com")
# Respuesta: {"error": {"message": "Usuario con email 'user@example.com' ya existe", "type": "AlreadyExistsError", "details": {...}}}
```

#### `ValidationError`
Error de validación (422)

```python
from app.core.exceptions import ValidationError

raise ValidationError(message="El campo es requerido", field="email")
# Respuesta: {"error": {"message": "El campo es requerido", "type": "ValidationError", "details": {"field": "email"}}}
```

#### `AuthenticationError`
Error de autenticación (401)

```python
from app.core.exceptions import AuthenticationError

raise AuthenticationError(message="Credenciales incorrectas")
# Respuesta: {"error": {"message": "Credenciales incorrectas", "type": "AuthenticationError", "details": {}}}
```

#### `AuthorizationError`
Error de autorización/permisos (403)

```python
from app.core.exceptions import AuthorizationError

raise AuthorizationError(message="No tienes permisos para esta acción")
```

#### `DatabaseError`
Error de base de datos (500)

```python
from app.core.exceptions import DatabaseError

raise DatabaseError(message="Error al conectar con la base de datos")
```

#### `ConflictError`
Conflicto de estado (409)

```python
from app.core.exceptions import ConflictError

raise ConflictError(message="El usuario tiene items asociados y no puede ser eliminado")
```

## Formato de Respuesta de Error

**Todas las excepciones** (personalizadas, validación, HTTP, SQLAlchemy, generales) devuelven un formato consistente:

```json
{
  "error": {
    "message": "Mensaje descriptivo del error",
    "type": "NombreDeLaExcepcion",
    "details": {
      "resource": "Usuario",
      "identifier": 123
    }
  }
}
```

**Nota:** Este formato solo aplica a errores. Las respuestas exitosas mantienen su formato normal.

## Gestores de Excepciones

El sistema incluye gestores automáticos para:

1. **Excepciones personalizadas** (`AppException` y subclases)
   - Formato consistente
   - Logging automático
   - Status code correcto

2. **Errores de validación** (`RequestValidationError`)
   - Errores de Pydantic
   - Lista de campos con errores

3. **Excepciones HTTP** (`HTTPException`)
   - Excepciones estándar de FastAPI/Starlette

4. **Errores de SQLAlchemy** (`SQLAlchemyError`)
   - Errores de base de datos
   - Mensajes específicos según el tipo (IntegrityError, OperationalError, etc.)
   - No expone detalles internos de la BD

5. **Excepciones generales** (`Exception` - catch-all)
   - Captura cualquier error no manejado
   - Logging completo con traceback
   - Respuesta genérica para no exponer detalles internos

## Ejemplos de Uso

### En Routers

```python
from app.core.exceptions import NotFoundError, AlreadyExistsError

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise NotFoundError(resource="Usuario", identifier=user_id)
    return user
```

### En Servicios

```python
from app.core.exceptions import NotFoundError, DatabaseError

def update_user(db: Session, user_id: int, data: dict):
    user = get_user(db, user_id)
    if not user:
        raise NotFoundError(resource="Usuario", identifier=user_id)
    
    try:
        # operación de BD
        return user_repository.update(db, user, values=data)
    except SQLAlchemyError as e:
        # Esto se manejará automáticamente por database_exception_handler
        raise  # O puedes convertirlo a DatabaseError si quieres más control
```

### Con Detalles Adicionales

```python
from app.core.exceptions import ValidationError

if not email_valid:
    raise ValidationError(
        message="El email no es válido",
        field="email",
        details={
            "field": "email",
            "value": email,
            "reason": "Formato inválido"
        }
    )
```

## Ventajas del Sistema

1. **Consistencia**: Todas las respuestas de error tienen el mismo formato
2. **Trazabilidad**: Los errores se registran automáticamente con contexto
3. **Claridad**: Mensajes descriptivos y detalles útiles
4. **Mantenibilidad**: Fácil agregar nuevas excepciones
5. **Seguridad**: Errores internos no se exponen al cliente
6. **Cobertura Total**: TODAS las excepciones se manejan, incluso las no previstas

## Agregar Nueva Excepción

### ✅ Pasos Simples

1. **Crea la clase en `src/app/core/exceptions.py`** heredando de `AppException`:
```python
class MiNuevaExcepcion(AppException):
    """Descripción de la excepción"""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=400,  # O el código HTTP apropiado
            details=details or {}
        )
```

2. **¡Ya está!** El gestor de excepciones la manejará automáticamente.

### ¿Por qué funciona automáticamente?

En `main.py` está registrado el gestor para `AppException`:
```python
app.add_exception_handler(AppException, app_exception_handler)
```

Como todas las excepciones personalizadas heredan de `AppException`, FastAPI las captura automáticamente y las formatea con el formato estándar.

### Ejemplo Completo

```python
# 1. Crear la excepción en exceptions.py
class RateLimitError(AppException):
    """Error cuando se excede el límite de peticiones"""
    
    def __init__(self, message: str = "Límite de peticiones excedido", details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=429,  # Too Many Requests
            details=details or {}
        )

# 2. Usarla en tu código
from app.core.exceptions import RateLimitError

if requests_count > limit:
    raise RateLimitError(
        message=f"Has excedido el límite de {limit} peticiones",
        details={"limit": limit, "current": requests_count}
    )
```

**No necesitas registrar nada más.** El sistema la manejará automáticamente.

## Logging Automático

Todas las excepciones se registran automáticamente con:
- Tipo de excepción
- Mensaje
- Status code
- Detalles
- Path y método HTTP
- Traceback completo (para excepciones no manejadas)

### Ejemplo de Log

```
[2024-01-15 10:30:45] ERROR    [app.core.exception_handlers] general_exception_handler:186 - Excepción no manejada en /api/v1/users/123: division by zero
```

## Mejores Prácticas

1. **Usa excepciones específicas**: `NotFoundError` en lugar de `AppException` genérico
2. **Incluye contexto**: Agrega detalles útiles en el parámetro `details`
3. **Mensajes claros**: Mensajes que ayuden al usuario/cliente a entender el error
4. **No expongas detalles internos**: Usa `DatabaseError` genérico en lugar de mostrar el error SQL real
5. **Confía en el catch-all**: No necesitas manejar manualmente todas las excepciones de librerías externas

## Preguntas Frecuentes

### ¿Qué pasa si una librería externa lanza una excepción?

Se maneja automáticamente por el gestor `general_exception_handler`. Se registra con traceback completo en los logs, pero al cliente se le devuelve un mensaje genérico "Error interno del servidor" para no exponer detalles internos.

### ¿Puedo agregar gestores para otras librerías?

Sí, puedes agregar gestores específicos en `main.py` antes del catch-all:

```python
from requests.exceptions import RequestException

async def requests_exception_handler(request: Request, exc: RequestException):
    # Tu lógica personalizada
    pass

app.add_exception_handler(RequestException, requests_exception_handler)
```

### ¿Cómo veo los detalles completos de un error?

Los detalles completos (incluyendo traceback) se registran en los logs. Revisa los logs de la aplicación para debugging.

