from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings


def generate_password_rest_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "sub": email,
        }, settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str:
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithm=["HS256"])
        return decode_token["email"]
    except jwt.JWTError:
        return None

