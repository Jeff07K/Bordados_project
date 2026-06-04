from passlib.context import CryptContext
import bcrypt
from typing import Optional

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña
    """
    # bcrypt tiene un límite de 72 caracteres
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña en texto plano coincide con el hash
    """
    plain_password = plain_password[:72]

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback usando bcrypt directamente por compatibilidad
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False


def get_password_hash(password: str) -> str:
    """Alias para hash_password (usado en algunos routers)"""
    return hash_password(password)


# Función opcional para verificar si el usuario existe (útil en routers)
def authenticate_user(email: str, password: str, user) -> Optional[dict]:
    if not user or not verify_password(password, user.contrasena_hash):
        return None
    return user