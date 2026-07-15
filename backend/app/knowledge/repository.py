from sqlalchemy.orm import Session

from app.database.models.document import Document


class DocumentRepository:

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
    ) -> list[Document]:

        return (
            db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.updated_at.desc())
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        document: Document,
    ) -> None:

        db.delete(document)
        db.commit()