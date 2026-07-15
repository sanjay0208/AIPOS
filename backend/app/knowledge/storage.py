from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("storage/documents")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


class StorageService:

    @staticmethod
    async def save_file(
        file: UploadFile,
    ) -> tuple[str, int]:

        extension = Path(file.filename).suffix

        filename = f"{uuid4()}{extension}"

        destination = UPLOAD_DIR / filename

        content = await file.read()

        destination.write_bytes(content)

        return (
            str(destination),
            len(content),
        )