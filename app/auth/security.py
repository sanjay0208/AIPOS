from datetime import datetime, timezone

from jose import jwt
from passlib.context import CryptContext

from app.auth.config import (
    ACCESS_TOKEN_EXPIRE,
    ALGORITHM,
    SECRET_KEY,
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE

    payload.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )