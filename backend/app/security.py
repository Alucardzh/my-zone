'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 15:08:17
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 17:12:01
 # @ Description:
'''


__all__ = [
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "get_current_user",
]

from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
from app.db.models import User
from .config import jwt_config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


JWT_SECRET = jwt_config.secret_key_value
JWT_ALGORITHM = jwt_config.algorithm
ACCESS_TOKEN_EXPIRE_SECONDS = jwt_config.access_token_expire_seconds


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """解码 JWT Token"""
    try:
        payload = jwt.decode(
            token, jwt_config.secret_key_value,
            algorithms=[jwt_config.algorithm]
        )
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, password_hash: str) -> bool:
    """_summary_

    Args:
        plain_password (str): _description_
        password_hash (str): _description_

    Returns:
        bool: _description_
    """
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    """_summary_

    Args:
        password (str): _description_

    Returns:
        str: _description_
    """
    return pwd_context.hash(password)


def create_access_token(subject: str,
                        expires_delta: Optional[timedelta] = None) -> str:
    """_summary_

    Args:
        subject (str): _description_
        expires_delta (Optional[timedelta], optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    if expires_delta is None:
        expires_delta = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """_summary_

    Args:
        token (str, optional): Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: _description_
        credentials_exception: _description_
        credentials_exception: _description_

    Returns:
        User: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    try:
        user = await User.get(username=username)
    except DoesNotExist as exc:
        raise credentials_exception from exc
    return user
