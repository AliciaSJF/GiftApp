"""
Utilidades de seguridad: autenticación y autorización
"""
from datetime import datetime, timedelta
import re
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
from app.core.config import settings
import base64

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_salt(length: int = 16) -> str:
    """Genera un salt para una contraseña codificada en base 64 de longitud length"""
    return base64.b64encode(secrets.token_bytes(length)).decode("utf-8")


def hash_password(password: str, salt: str) -> str:
    """Hashea una contraseña con un salt"""
    pepper = settings.PEPPER
    combined = "f{salt}{pepper}{password}"
    return pwd_context.hash(password, salt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def verify_password_strength(password: str) -> bool:
    # (?=.*[A-Z])    Debe tener al menos una mayúscula
    # (?=.*[a-z])    Debe tener al menos una minúscula
    # (?=.*[0-9])    Debe tener al menos un dígito
    # (?=.*[^a-zA-Z0-9]) Debe tener al menos un carácter no-alfanumérico (especial)
    # .{8,100}$      Debe tener entre 8 y 100 caracteres de longitud total
    
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,100}$"
    return re.search(pattern, password) is not None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRES_MIN)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica un token JWT"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

