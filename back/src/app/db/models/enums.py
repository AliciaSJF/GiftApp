"""
Tipos ENUM para la base de datos
"""
import enum
from sqlalchemy import Enum


class AuthProvider(str, enum.Enum):
    """Proveedores de autenticación"""
    GOOGLE = "google"
    FACEBOOK = "facebook"
    APPLE = "apple"
    GITHUB = "github"
    PASSWORD = "password"


class SubjectType(str, enum.Enum):
    """Tipo de sujeto (usuario o grupo)"""
    USER = "user"
    GROUP = "group"


class ListRole(str, enum.Enum):
    """Roles en una lista de deseos"""
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class ClaimStatus(str, enum.Enum):
    """Estado de un claim sobre un item"""
    INTERESTED = "interested"
    CLAIMED = "claimed"
    PURCHASED = "purchased"
    RELEASED = "released"
    CANCELLED = "cancelled"


class InviteStatus(str, enum.Enum):
    """Estado de una invitación"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"

