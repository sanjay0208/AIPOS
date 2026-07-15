from sqlalchemy.orm import Session

from app.database.models.document import Document
from app.database.models.document_chunk import DocumentChunk


class DocumentRepository:

    # =====================================================
    # Documents
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        title: str,
        filename: str,
        content_type: str,
        size: int,
        storage_path: str,
    ) -> Document:

        document = Document(
            user_id=user_id,
            title=title,
            filename=filename,
            content_type=content_type,
            size=size,
            storage_path=storage_path,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: int,
    ) -> Document | None:

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.created_at.desc())
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        document: Document,
    ):

        db.delete(document)
        db.commit()

    # =====================================================
    # Chunks
    # =====================================================

    @staticmethod
    def create_chunk(
        db: Session,
        document_id: int,
        chunk_index: int,
        content: str,
    ) -> DocumentChunk:

        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            content=content,
        )

        db.add(chunk)
        db.commit()
        db.refresh(chunk)

        return chunk

    @staticmethod
    def update_chunk_vector(
        db: Session,
        chunk: DocumentChunk,
        vector_id: str,
    ) -> DocumentChunk:

        chunk.vector_id = vector_id

        db.commit()
        db.refresh(chunk)

        return chunk

    @staticmethod
    def list_chunks(
        db: Session,
        document_id: int,
    ) -> list[DocumentChunk]:

        return (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(DocumentChunk.chunk_index)
            .all()
        )