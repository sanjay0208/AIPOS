from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.models.user import User
from app.database.session import get_db
from app.memory.schemas import MemoryCreate, MemoryResponse
from app.memory.service import save_memory

router = APIRouter(
    prefix="/memory",
    tags=["Memory"],
)


@router.post(
    "",
    response_model=MemoryResponse,
)
def create_memory(
    memory: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return save_memory(
        db=db,
        user_id=current_user.id,
        memory=memory,
    )