# Guía para Configurar la Base de Datos PostgreSQL

## Opción 1: Desde psql (Recomendado)

### Paso 1: Conectar como superusuario

```bash
# En Windows (si PostgreSQL está en el PATH)
psql -U postgres

# O especificando el host
psql -U postgres -h localhost
```

### Paso 2: Ejecutar los comandos SQL

```sql
-- 1. Crear el usuario
CREATE USER user WITH PASSWORD 'password';

-- 2. Dar permisos al usuario
ALTER USER user CREATEDB;

-- 3. Crear la base de datos
CREATE DATABASE dbname OWNER user;

-- 4. Conceder privilegios
GRANT ALL PRIVILEGES ON DATABASE dbname TO user;
```

### Paso 3: Conectarse a la nueva base de datos

```sql
\c dbname

-- Conceder privilegios en el esquema público
GRANT ALL ON SCHEMA public TO user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO user;
```

## Opción 2: Desde la terminal (una línea)

```bash
# Crear usuario
psql -U postgres -c "CREATE USER user WITH PASSWORD 'password' CREATEDB;"

# Crear base de datos
psql -U postgres -c "CREATE DATABASE dbname OWNER user;"

# Conceder privilegios
psql -U postgres -d dbname -c "GRANT ALL ON SCHEMA public TO user;"
```

## Opción 3: Usar el archivo SQL

```bash
# Ejecutar el script completo
psql -U postgres -f setup_database.sql
```

## Opción 4: Docker Compose (Más fácil)

Si usas Docker Compose, **no necesitas crear nada manualmente**. El servicio PostgreSQL crea automáticamente:

- El usuario: `user`
- La contraseña: `password`
- La base de datos: `dbname`

Solo ejecuta:

```bash
docker-compose up -d db
```

Y luego aplica las migraciones:

```bash
alembic upgrade head
```

## Verificar la configuración

```bash
# Verificar que el usuario existe
psql -U postgres -c "\du user"

# Verificar que la base de datos existe
psql -U postgres -c "\l dbname"

# Probar conexión con el nuevo usuario
psql -U user -d dbname -h localhost
```

## Notas Importantes

1. **Cambiar contraseñas en producción**: Las contraseñas por defecto (`password`) son solo para desarrollo.

2. **Si el usuario ya existe**: Si intentas crear un usuario que ya existe, obtendrás un error. Puedes usar:
   ```sql
   CREATE USER IF NOT EXISTS user WITH PASSWORD 'password';
   ```
   O simplemente omitir ese paso si ya existe.

3. **Si la base de datos ya existe**: Puedes usar:
   ```sql
   CREATE DATABASE dbname OWNER user;
   ```
   Esto fallará si ya existe, pero puedes verificar primero con `\l`.

## Después de crear la base de datos

Una vez creada la base de datos y el usuario, aplica las migraciones:

```bash
# Asegúrate de que tu .env tenga la DATABASE_URL correcta
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Aplicar migraciones
alembic upgrade head
```

Esto creará todas las tablas (users, items, etc.) en la base de datos.

