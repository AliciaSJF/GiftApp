"""
Router para endpoints de autenticación OAuth (Google, etc.)
"""
import httpx
from fastapi import APIRouter, Query, HTTPException, status
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from typing import Optional
from datetime import timedelta

from app.core.config import settings
from app.core.dependencies import DBSession, OAuthServiceDep
from app.core.logging_config import get_logger
from app.core.security import create_access_token
from app.utils.oauth import (
    generate_code_verifier,
    generate_code_challenge,
    generate_state,
    generate_nonce,
)

router = APIRouter(prefix="/auth/oauth", tags=["auth:oauth"])
logger = get_logger(__name__)

# === DEV ONLY ===
# Al no tener Redis ni sesión aún, guardamos el estado en memoria.
# Se pierde al reiniciar el servidor (suficiente para desarrollo).
# TODO: Migrar a Redis o sesión persistente en producción
_OAUTH_STORE: dict[str, dict] = {}  # state -> {"code_verifier": ..., "nonce": ...}

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"


@router.get("/google/start")
def oauth_start_google():
    """
    Inicia el flujo de login con Google (OIDC Authorization Code + PKCE).
    Redirige al consentimiento de Google.
    """
    logger.info("=== Endpoint /auth/oauth/google/start llamado ===")
    # 1) Generar PKCE + state + nonce
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state = generate_state()
    nonce = generate_nonce()

    # 2) Guardar temporalmente (DEV)
    _OAUTH_STORE[state] = {
        "code_verifier": code_verifier,
        "nonce": nonce,
    }

    # 3) Construir URL de autorización
    redirect_uri = settings.OAUTH_GOOGLE_REDIRECT_URI
    if not redirect_uri:
        raise ValueError("OAUTH_GOOGLE_REDIRECT_URI no está configurado")
    
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",  # Para refresh token (no lo usaremos ahora)
        "prompt": "consent",  # Fuerza el consentimiento en dev
    }
    url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    logger.info(f"Iniciando OAuth con Google, state={state[:8]}..., redirect_uri={redirect_uri}")
    # 4) Redirigir a Google
    return RedirectResponse(url=url)


@router.get("/callback/google")
async def oauth_callback_google(
    session: DBSession,
    oauth_service: OAuthServiceDep,
    code: str = Query(..., description="Código de autorización"),
    state: str = Query(..., description="State para validar CSRF"),
    error: Optional[str] = Query(None, description="Error de OAuth"),
):
    """
    Callback de OAuth de Google.
    Intercambia el código por tokens y crea/autentica al usuario.
    """
    # Validar que no haya error
    if error:
        logger.error(f"Error en callback de Google: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en autenticación OAuth: {error}",
        )

    # Validar state (protección CSRF)
    if state not in _OAUTH_STORE:
        logger.warning(f"State no encontrado o expirado: {state[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="State inválido o expirado",
        )

    stored_data = _OAUTH_STORE.pop(state)  # Usar y eliminar
    code_verifier = stored_data["code_verifier"]
    nonce = stored_data["nonce"]

    try:
        # 1) Intercambiar código por tokens
        logger.info("Intercambiando código por tokens...")
        token_data = await oauth_service.exchange_code_for_tokens(
            code=code,
            code_verifier=code_verifier,
            redirect_uri=str(settings.OAUTH_GOOGLE_REDIRECT_URI),
        )
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("No se recibió access_token")

        # 2) Obtener información del usuario
        logger.info("Obteniendo información del usuario de Google...")
        google_user_info = await oauth_service.get_google_user_info(access_token)

        # Validar nonce (opcional pero recomendado para OIDC)
        # En producción, deberías validar el ID token y su nonce

        # 3) Obtener o crear usuario
        logger.info(f"Procesando usuario: {google_user_info.get('email', 'sin email')}")
        user, auth_identity, is_new_user = (
            oauth_service.get_or_create_user_from_google(session, google_user_info)
        )

        # 4) Generar token JWT para nuestra aplicación

        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_EXPIRES_MIN
        )
        jwt_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        logger.info(
            f"Login OAuth exitoso: user_id={user.id}, "
            f"email={user.email}, is_new={is_new_user}"
        )

        # 5) Redirigir al frontend con el token
        # Redirigir a la página de callback del frontend con el token
        frontend_callback_url = f"{settings.FRONTEND_URL}/oauth/callback?token={jwt_token}"
        return RedirectResponse(url=frontend_callback_url)

    except httpx.HTTPStatusError as e:
        logger.error(f"Error HTTP al comunicarse con Google: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error al comunicarse con el proveedor OAuth",
        )
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.exception(f"Error inesperado en callback OAuth: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
