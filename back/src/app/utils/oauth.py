"""
Utilidades para OAuth 2.0 y PKCE (Proof Key for Code Exchange)
"""
import base64
import hashlib
import os
import secrets


def b64url_encode(data: bytes) -> str:
    """
    Codifica bytes en Base64 URL-safe sin padding.
    
    Args:
        data: Bytes a codificar
        
    Returns:
        String codificado en Base64 URL-safe
    """
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_code_verifier() -> str:
    """
    Genera un code_verifier para PKCE (RFC 7636).
    Recomendado: 43-128 caracteres. Usamos 64.
    
    Returns:
        Code verifier aleatorio en Base64 URL-safe
    """
    return b64url_encode(os.urandom(64))


def generate_code_challenge(verifier: str) -> str:
    """
    Genera el code_challenge a partir del code_verifier usando SHA256.
    
    Args:
        verifier: Code verifier generado previamente
        
    Returns:
        Code challenge en Base64 URL-safe
    """
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return b64url_encode(digest)


def generate_state() -> str:
    """
    Genera un state aleatorio para proteger contra CSRF.
    
    Returns:
        Token aleatorio URL-safe
    """
    return secrets.token_urlsafe(24)


def generate_nonce() -> str:
    """
    Genera un nonce aleatorio para OpenID Connect.
    
    Returns:
        Token aleatorio URL-safe
    """
    return secrets.token_urlsafe(24)

