from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import UserRegister, UserResponse
from app.auth.service import register_user
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