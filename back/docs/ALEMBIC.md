# Guía de Alembic - Migraciones de Base de Datos

Alembic es una herramienta de migración de base de datos para SQLAlchemy. Permite gestionar cambios en el esquema de la base de datos de forma versionada y controlada.

## ¿Qué es Alembic?

Alembic te permite:
- **Versionar cambios** en el esquema de la base de datos
- **Aplicar migraciones** de forma controlada
- **Reversar cambios** si es necesario
- **Trabajar en equipo** con historial de cambios
- **Sincronizar** el esquema entre entornos (desarrollo, producción, etc.)

## Estructura de Alembic

```
alembic/
├── versions/          # Aquí se guardan las migraciones
│   └── 001_initial_migration.py
├── env.py            # Configuración del entorno
└── script.py.mako    # Plantilla para nuevas migraciones

alembic.ini           # Configuración principal
```

## Comandos Básicos

### 1. Ver el estado actual

```bash
alembic current
```

Muestra la versión actual de la base de datos.

### 2. Ver el historial de migraciones

```bash
alembic history
```

Muestra todas las migraciones disponibles.

### 3. Ver migraciones pendientes

```bash
alembic heads
```

Muestra la última migración disponible.

### 4. Crear una nueva migración

#### Migración automática (recomendado)

Alembic puede detectar automáticamente los cambios en tus modelos:

```bash
alembic revision --autogenerate -m "Descripción del cambio"
```

**Ejemplo:**
```bash
alembic revision --autogenerate -m "Agregar campo phone a usuarios"
```

#### Migración manual

Si necesitas más control, crea una migración vacía:

```bash
alembic revision -m "Descripción del cambio"
```

Luego edita el archivo generado en `alembic/versions/` para agregar los cambios manualmente.

### 5. Aplicar migraciones

#### Aplicar todas las migraciones pendientes

```bash
alembic upgrade head
```

#### Aplicar hasta una versión específica

```bash
alembic upgrade <revision_id>
```

**Ejemplo:**
```bash
alembic upgrade 001
```

#### Aplicar la siguiente migración

```bash
alembic upgrade +1
```

### 6. Reversar migraciones

#### Reversar todas las migraciones

```bash
alembic downgrade base
```

#### Reversar hasta una versión específica

```bash
alembic downgrade <revision_id>
```

**Ejemplo:**
```bash
alembic downgrade 001
```

#### Reversar la última migración

```bash
alembic downgrade -1
```

## Flujo de Trabajo Típico

### Escenario 1: Agregar un nuevo campo a un modelo

1. **Modificar el modelo** en `src/app/db/models/`:
   ```python
   class User(Base):
       # ... campos existentes ...
       phone = Column(String, nullable=True)  # Nuevo campo
   ```

2. **Crear la migración automática**:
   ```bash
   alembic revision --autogenerate -m "Agregar campo phone a usuarios"
   ```

3. **Revisar el archivo generado** en `alembic/versions/` para asegurarte de que es correcto.

4. **Aplicar la migración**:
   ```bash
   alembic upgrade head
   ```

### Escenario 2: Crear una nueva tabla

1. **Crear el modelo** en `src/app/db/models/nueva_tabla.py`

2. **Importar el modelo** en `src/app/db/models/__init__.py`:
   ```python
   from .nueva_tabla import NuevaTabla
   __all__ = ["User", "Item", "NuevaTabla"]
   ```

3. **Importar en `alembic/env.py`**:
   ```python
   from app.db.models import User, Item, NuevaTabla
   ```

4. **Crear la migración**:
   ```bash
   alembic revision --autogenerate -m "Crear tabla nueva_tabla"
   ```

5. **Aplicar la migración**:
   ```bash
   alembic upgrade head
   ```

## Buenas Prácticas

### 1. Revisa siempre las migraciones generadas

Alembic puede no detectar todos los cambios correctamente. Siempre revisa el archivo generado antes de aplicarlo.

### 2. Usa nombres descriptivos

```bash
# ✅ Bueno
alembic revision --autogenerate -m "Agregar índice a email de usuarios"

# ❌ Malo
alembic revision --autogenerate -m "cambio"
```

### 3. Una migración por cambio lógico

No mezcles múltiples cambios no relacionados en una sola migración.

### 4. Prueba las migraciones en desarrollo primero

Siempre prueba `upgrade` y `downgrade` en un entorno de desarrollo antes de aplicarlas en producción.

### 5. Haz backup antes de migraciones importantes

```bash
# Backup de PostgreSQL
pg_dump -U user -d dbname > backup.sql
```

## Resolución de Problemas

### Error: "Target database is not up to date"

Significa que hay migraciones pendientes. Aplica las migraciones:

```bash
alembic upgrade head
```

### Error: "Can't locate revision identified by 'xxx'"

Puede ocurrir si el historial de migraciones está desincronizado. Verifica el estado:

```bash
alembic current
alembic history
```

### La migración automática no detecta cambios

1. Asegúrate de que todos los modelos estén importados en `alembic/env.py`
2. Verifica que los modelos estén correctamente definidos
3. Usa `--autogenerate` con cuidado y revisa siempre el resultado

## Comandos Útiles Adicionales

### Ver el SQL que se ejecutará (sin aplicarlo)

```bash
alembic upgrade head --sql
```

### Marcar la base de datos como actualizada (sin ejecutar migraciones)

```bash
alembic stamp head
```

**⚠️ Usar con precaución**: Solo si estás seguro de que el esquema ya está actualizado.

### Mostrar información detallada

```bash
alembic current -v
alembic history -v
```

## Integración con Docker

Si usas Docker Compose, puedes ejecutar migraciones dentro del contenedor:

```bash
# Aplicar migraciones
docker-compose exec web alembic upgrade head

# Crear nueva migración
docker-compose exec web alembic revision --autogenerate -m "Descripción"
```

## Ejemplo Completo

```bash
# 1. Modificar un modelo (agregar campo)
# Editar src/app/db/models/user.py

# 2. Crear migración
alembic revision --autogenerate -m "Agregar campo phone a usuarios"

# 3. Revisar el archivo generado en alembic/versions/

# 4. Aplicar migración
alembic upgrade head

# 5. Verificar
alembic current
```

## Recursos Adicionales

- [Documentación oficial de Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial de Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

**Nota**: Las migraciones son críticas para la integridad de la base de datos. Siempre revisa y prueba antes de aplicar en producción.

