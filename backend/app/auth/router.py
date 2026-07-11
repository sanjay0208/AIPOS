from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.schemas import (
    UserRegister,
    UserResponse,
    UserLogin,
    Token,
)
from app.auth.service import (
    register_user,
    login_user,
)
from app.database.session import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    return register_user(db, user)


# ------------------------------------
# JSON Login (Frontend)
# ------------------------------------
@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=user.email,
        password=user.password,
    )


# ------------------------------------
# OAuth2 Login (Swagger)
# ------------------------------------
@router.post(
    "/token",
    response_model=Token,
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )