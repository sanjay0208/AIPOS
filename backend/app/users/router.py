from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.database.models.user import User
from app.auth.schemas import UserResponse
from app.users.service import get_user_profile

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return get_user_profile(current_user)