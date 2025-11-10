"""
Router para endpoints de autenticación
"""
from fastapi import APIRouter
from app.core.logging_config import get_logger


router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger(__name__)


@router.post("/login")
def login(user_credentials: user_schema.UserLogin, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token JWT"""
    logger.info(f"Intento de login para usuario: {user_credentials.username}")
    user = user_service_module.authenticate_user(
        db, user_credentials.username, user_credentials.password
    )
    if not user:
        raise AuthenticationError(
            message="Credenciales incorrectas",
            details={"username": user_credentials.username}
        )