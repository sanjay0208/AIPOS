from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.models.user import User
from app.database.session import get_db

from app.knowledge.schemas import (
    DocumentCreate,
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadResponse,
)
from app.knowledge.service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Knowledge Base"],
)


# ==========================================================
# Upload Document
# ==========================================================

@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await DocumentService.upload_document(
        db=db,
        user_id=current_user.id,
        title=title,
        file=file,
    )


# ==========================================================
# Create Document Metadata
# ==========================================================

@router.post(
    "",
    response_model=DocumentResponse,
)
def create_document(
    data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DocumentService.create_document(
        db=db,
        user_id=current_user.id,
        data=data,
    )


# ==========================================================
# List Documents
# ==========================================================

@router.get(
    "",
    response_model=DocumentListResponse,
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DocumentService.list_documents(
        db=db,
        user_id=current_user.id,
    )


# ==========================================================
# Get Document
# ==========================================================

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = DocumentService.get_document(
        db=db,
        document_id=document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document


# ==========================================================
# Delete Document
# ==========================================================

@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    deleted = DocumentService.delete_document(
        db=db,
        document_id=document_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return {
        "message": "Document deleted successfully."
    }