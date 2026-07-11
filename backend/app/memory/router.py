from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
):
    return save_memory(
        db=db,
        user_id=1,  # Temporary until JWT integration
        memory=memory,
    )