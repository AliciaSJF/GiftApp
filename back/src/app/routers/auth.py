import httpx
from fastapi import APIRouter, Query, HTTPException, status
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from typing import Optional
from datetime import timedelta

from app.core.config import settings
from app.core.dependencies import UserServiceDep
from app.core.logging_config import get_logger
from app.core.security import create_access_token

from app.schemas import user as user_schema

router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger(__name__)



@router.post("/register"
, response_model=user_schema.User)
def register(user: user_schema.UserRegister, user_service: UserServiceDep):
    """Registra un nuevo usuario"""
    logger.info(f"Intentando registrar usuario: {user.username} ({user.email})")
    new_user = user_service.create_user(user)
    logger.info(f"Usuario registrado exitosamente: ID={new_user.id}, username={new_user.username}")
    return new_user

