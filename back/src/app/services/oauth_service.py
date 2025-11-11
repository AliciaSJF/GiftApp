"""
Servicio de lógica de negocio para OAuth
"""
import httpx
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging_config import get_logger
from app.db.models.user import User
from app.db.models.auth_identity import AuthIdentity
from app.repositories.auth_identity_repository import AuthIdentityRepository
from app.repositories.user_repository import UserRepository

logger = get_logger(__name__)

# URLs de Google OAuth
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class OAuthService:
    """Servicio de lógica de negocio para OAuth."""

    def __init__(
        self,
        user_repository: UserRepository,
        auth_identity_repository: AuthIdentityRepository,
    ):
        """
        Inicializa el servicio con los repositorios necesarios.
        
        Args:
            user_repository: Repositorio de usuarios
            auth_identity_repository: Repositorio de identidades de autenticación
        """
        self.logger = logger
        self.user_repository = user_repository
        self.auth_identity_repository = auth_identity_repository

    async def exchange_code_for_tokens(
        self, code: str, code_verifier: str, redirect_uri: str
    ) -> Dict[str, Any]:
        """
        Intercambia el código de autorización por tokens de acceso.
        
        Args:
            code: Código de autorización recibido del callback
            code_verifier: Code verifier para PKCE
            redirect_uri: URI de redirección configurada
            
        Returns:
            Diccionario con tokens y datos del usuario
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": str(redirect_uri),
                    "code_verifier": code_verifier,
                },
            )
            response.raise_for_status()
            token_data = response.json()
            return token_data

    async def get_google_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Obtiene la información del usuario de Google usando el access token.
        
        Args:
            access_token: Token de acceso de Google
            
        Returns:
            Diccionario con información del usuario
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return response.json()

    def get_or_create_user_from_google(
        self, db: Session, google_user_info: Dict[str, Any]
    ) -> tuple[User, AuthIdentity, bool]:
        """
        Obtiene o crea un usuario basado en la información de Google.
        
        Args:
            db: Sesión de base de datos
            google_user_info: Información del usuario de Google
            
        Returns:
            Tupla con (User, AuthIdentity, is_new_user)
        """
        provider_user_id = google_user_info.get("id") or google_user_info.get("sub")
        if not provider_user_id:
            raise ValueError("No se pudo obtener el ID del usuario de Google")

        # Buscar si ya existe una identidad para este usuario de Google
        auth_identity = self.auth_identity_repository.get_by_provider_and_user_id(
            provider="google", provider_user_id=provider_user_id
        )

        if auth_identity:
            # Usuario existente
            user = db.get(User, auth_identity.user_id)
            if not user:
                raise ValueError("Usuario asociado a identidad no encontrado")

            # Actualizar información si es necesario
            update_data = {}
            if google_user_info.get("email") and not user.email:
                update_data["email"] = google_user_info["email"]
            if google_user_info.get("verified_email"):
                update_data["email_verified"] = google_user_info["verified_email"]
            if google_user_info.get("name") and not user.display_name:
                update_data["display_name"] = google_user_info["name"]
            if google_user_info.get("picture") and not user.avatar_url:
                update_data["avatar_url"] = google_user_info["picture"]
            if google_user_info.get("locale") and not user.locale:
                update_data["locale"] = google_user_info["locale"]

            if update_data:
                self.user_repository.update(user, values=update_data)

            return user, auth_identity, False

        # Usuario nuevo - crear usuario e identidad
        email = google_user_info.get("email")
        display_name = google_user_info.get("name") or email or "Usuario"

        # Verificar si ya existe un usuario con ese email
        existing_user = None
        if email:
            existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            # Usuario existe pero no tiene identidad de Google - vincular
            user = existing_user
        else:
            # Crear nuevo usuario (sin username ni hashed_password)
            user = User(
                email=email,
                email_verified=google_user_info.get("verified_email", False),
                display_name=display_name,
                avatar_url=google_user_info.get("picture"),
                locale=google_user_info.get("locale"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            self.logger.info(f"Usuario creado desde OAuth: ID={user.id}, email={email}")

        # Crear identidad de autenticación
        auth_identity = self.auth_identity_repository.create(
            user_id=user.id,
            provider="google",
            provider_user_id=provider_user_id,
            provider_email=email,
            email_verified=google_user_info.get("verified_email"),
        )
        self.logger.info(
            f"Identidad OAuth creada: provider=google, user_id={user.id}"
        )

        return user, auth_identity, True
