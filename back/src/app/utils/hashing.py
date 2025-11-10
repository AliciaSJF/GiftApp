"""
Utilidades para hashing de contraseñas
"""
from app.core.security import get_password_hash


def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt.
    
    Ejemplo:
        hashed = hash_password("mi_contraseña_secreta")
    """
    return get_password_hash(password)

