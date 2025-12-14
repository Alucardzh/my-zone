'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 15:08:26
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 15:37:50
 # @ Description:
 '''

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from tortoise.exceptions import IntegrityError

from app.db.models import User
from app.schemas import UserCreate, UserLogin, Token
from app.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    )


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(payload: UserCreate) -> Token:
    """注册用户接口(不适用，仅保留)

    Args:
        payload (UserCreate): _description_

    Raises:
        HTTPException: _description_

    Returns:
        Token: _description_
    """
    try:
        user = await User.create(
            username=payload.username,
            password_hash=get_password_hash(payload.password),
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists") from exc

    token = create_access_token(subject=user.username)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin) -> Token:
    """登录接口

    Args:
        payload (UserLogin): _description_

    Raises:
        HTTPException: _description_

    Returns:
        Token: _description_
    """
    user = await User.get_or_none(username=payload.username)
    if user is None or not verify_password(payload.password,
                                           user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials")
    token = create_access_token(subject=user.username)
    return Token(access_token=token)


@router.get("/me")
async def me(user: User = Depends(get_current_user)) -> JSONResponse:
    """根据token查询当前用户信息

    Args:
        user (User, optional): Defaults to Depends(get_current_user).

    Returns:
        JSONResponse: _description_
    """
    return JSONResponse(
        content={"id": user.id, "username": user.username}, status_code=200)
