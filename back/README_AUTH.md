# Configuración de Autenticación

## Variables de Entorno Requeridas

Para que la autenticación funcione correctamente, necesitas configurar las siguientes variables en tu archivo `.env`:

```env
# OAuth Google
GOOGLE_CLIENT_ID=tu_client_id_de_google
GOOGLE_CLIENT_SECRET=tu_client_secret_de_google
OAUTH_GOOGLE_REDIRECT_URI=http://localhost:8000/auth/oauth/callback/google
FRONTEND_URL=http://localhost:3000

# JWT
JWT_SECRET=tu_secret_key_muy_seguro
JWT_ACCESS_EXPIRES_MIN=30
JWT_REFRESH_EXPIRES_DAYS=7
```

## Configuración de Google OAuth

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ (o Google Identity)
4. Ve a "Credenciales" y crea un "ID de cliente OAuth 2.0"
5. Configura las URLs de redirección autorizadas:
   - `http://localhost:8000/auth/oauth/callback/google` (desarrollo)
   - Tu URL de producción (producción)
6. Copia el Client ID y Client Secret a tu archivo `.env`

## Flujo de Autenticación

### Login con Usuario/Contraseña
1. Usuario ingresa username/email y contraseña
2. Frontend envía petición a `/users/login`
3. Backend valida credenciales y devuelve JWT token
4. Frontend guarda token en localStorage

### Login con Google OAuth
1. Usuario hace clic en "Continuar con Google"
2. Frontend redirige a `/auth/oauth/google/start`
3. Backend redirige a Google para autenticación
4. Usuario autoriza en Google
5. Google redirige a `/auth/oauth/callback/google`
6. Backend intercambia código por tokens y crea/obtiene usuario
7. Backend redirige a frontend con token: `FRONTEND_URL/oauth/callback?token=...`
8. Frontend guarda token en localStorage

## Endpoints

- `POST /users/login` - Login con usuario/contraseña
- `POST /users/` - Registro de nuevo usuario
- `GET /auth/oauth/google/start` - Inicia OAuth con Google
- `GET /auth/oauth/callback/google` - Callback de OAuth (manejado por backend)

