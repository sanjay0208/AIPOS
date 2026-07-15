from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =====================================================
# Create Document
# =====================================================

class DocumentCreate(BaseModel):
    title: str
    filename: str
    content_type: str
    size: int
    storage_path: str


# =====================================================
# Document Response
# =====================================================

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    filename: str
    content_type: str
    size: int
    storage_path: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Upload Response
# =====================================================

class DocumentUploadResponse(BaseModel):
    document: DocumentResponse
    text: str
    chunks: int


# =====================================================
# List Response
# =====================================================

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]