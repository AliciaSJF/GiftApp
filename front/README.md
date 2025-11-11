# GiftApp Frontend

Frontend de la aplicación GiftApp construido con React, TypeScript y Vite.

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# URL del backend API
VITE_API_URL=http://localhost:8000

# Ruta base de la API (opcional, por defecto vacío)
VITE_API_BASE_PATH=
```

### Instalación

```bash
npm install
```

### Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

### Build

```bash
npm run build
```

## Autenticación

La aplicación soporta dos métodos de autenticación:

1. **Usuario y contraseña**: Login tradicional con email/username y contraseña
2. **Google OAuth**: Autenticación mediante Google

El token JWT se almacena en `localStorage` y se incluye automáticamente en todas las peticiones a la API.

## Estructura

```
src/
├── components/     # Componentes reutilizables
├── pages/          # Páginas de la aplicación
├── services/        # Servicios de API
├── hooks/          # Custom hooks
├── types/          # Tipos TypeScript
└── utils/          # Utilidades
```

