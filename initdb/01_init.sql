-- Crea el rol (usuario de aplicación)
CREATE ROLE giftapp LOGIN PASSWORD '?PW&kks(%;[JM?^bmO)' NOSUPERUSER NOCREATEDB NOCREATEROLE;

-- Crea la base de datos principal
CREATE DATABASE giftapp OWNER giftapp;

-- Ajustes de codificación y zona horaria
ALTER DATABASE giftapp SET client_encoding TO 'UTF8';
ALTER DATABASE giftapp SET timezone TO 'Europe/Madrid';

-- Conéctate a la nueva base
\connect giftapp

-- Extensiones útiles
CREATE EXTENSION IF NOT EXISTS pgcrypto;
