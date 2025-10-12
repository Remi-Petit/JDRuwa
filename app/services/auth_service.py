from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(subject: str) -> str:
    """
    Génère un JWT pour un utilisateur (subject = user.id)
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(subject), "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_access_token(token: str) -> str:
    """
    Vérifie le token et retourne le user_id (sub)
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload.get("sub")
