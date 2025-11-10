-- ============================================
-- Script completo para configurar PostgreSQL
-- ============================================
-- Ejecutar como superusuario (postgres)

-- 1. Crear el usuario (si no existe)
-- Opción A: Crear usuario con contraseña

-- Opción B: Crear usuario con más permisos (recomendado para desarrollo)
CREATE USER alicia WITH 
    PASSWORD 'alicia123'
    CREATEDB
    CREATEROLE;

-- 2. Crear la base de datos y asignarla al usuario
CREATE DATABASE archetype
    WITH 
    OWNER = alicia
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TEMPLATE = template0;

-- 3. Conceder todos los privilegios al usuario sobre la base de datos
GRANT ALL PRIVILEGES ON DATABASE dbname TO user;

-- 4. Conectarse a la base de datos y conceder privilegios en el esquema público
\c dbname
GRANT ALL ON SCHEMA public TO user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO user;

-- Verificar
\l dbname
\du user

