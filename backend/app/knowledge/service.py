from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.knowledge.chunker import DocumentChunker
from app.knowledge.parser import DocumentParser
from app.knowledge.repository import DocumentRepository
from app.knowledge.schemas import (
    DocumentCreate,
    DocumentListResponse,
    DocumentResponse,
)
from app.knowledge.storage import StorageService


class DocumentService:

    # =====================================================
    # Upload Document
    # =====================================================

    @staticmethod
    async def upload_document(
        db: Session,
        user_id: int,
        title: str,
        file: UploadFile,
    ) -> dict:

        # -----------------------------
        # Save uploaded file
        # -----------------------------

        storage_path, size = await StorageService.save_file(file)

        # -----------------------------
        # Save document metadata
        # -----------------------------

        document = DocumentRepository.create(
            db=db,
            user_id=user_id,
            title=title,
            filename=file.filename,
            content_type=file.content_type,
            size=size,
            storage_path=storage_path,
        )

        # -----------------------------
        # Extract text
        # -----------------------------

        extracted_text = DocumentParser.parse(
            storage_path,
            file.content_type,
        )

        # -----------------------------
        # Split into chunks
        # -----------------------------

        chunks = DocumentChunker.split(
            extracted_text
        )

        # -----------------------------
        # Save chunks
        # -----------------------------

        for index, chunk in enumerate(chunks):

            DocumentRepository.create_chunk(
                db=db,
                document_id=document.id,
                chunk_index=index,
                content=chunk,
            )

        return {
            "document": DocumentResponse.model_validate(document),
            "text": extracted_text,
            "chunks": len(chunks),
        }

    # =====================================================
    # Create Metadata Only
    # =====================================================

    @staticmethod
    def create_document(
        db: Session,
        user_id: int,
        data: DocumentCreate,
    ) -> DocumentResponse:

        document = DocumentRepository.create(
            db=db,
            user_id=user_id,
            title=data.title,
            filename=data.filename,
            content_type=data.content_type,
            size=data.size,
            storage_path=data.storage_path,
        )

        return DocumentResponse.model_validate(document)

    # =====================================================
    # Get Document
    # =====================================================

    @staticmethod
    def get_document(
        db: Session,
        document_id: int,
    ) -> DocumentResponse | None:

        document = DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )

        if document is None:
            return None

        return DocumentResponse.model_validate(document)

    # =====================================================
    # List Documents
    # =====================================================

    @staticmethod
    def list_documents(
        db: Session,
        user_id: int,
    ) -> DocumentListResponse:

        documents = DocumentRepository.get_all_by_user(
            db=db,
            user_id=user_id,
        )

        return DocumentListResponse(
            documents=[
                DocumentResponse.model_validate(document)
                for document in documents
            ]
        )

    # =====================================================
    # Delete Document
    # =====================================================

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int,
    ) -> bool:

        document = DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )

        if document is None:
            return False

        DocumentRepository.delete(
            db=db,
            document=document,
        )

        return True