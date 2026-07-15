from pathlib import Path

from docx import Document
from pypdf import PdfReader


class DocumentParser:
    """
    Universal document parser.
    """

    @staticmethod
    def parse(
        file_path: str,
        content_type: str,
    ) -> str:

        if content_type == "application/pdf":
            return DocumentParser.parse_pdf(file_path)

        if (
            content_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return DocumentParser.parse_docx(file_path)

        if content_type == "text/plain":
            return DocumentParser.parse_txt(file_path)

        if content_type == "text/markdown":
            return DocumentParser.parse_markdown(file_path)

        return ""

    @staticmethod
    def parse_pdf(
        file_path: str,
    ) -> str:

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    @staticmethod
    def parse_docx(
        file_path: str,
    ) -> str:

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    @staticmethod
    def parse_txt(
        file_path: str,
    ) -> str:

        return Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore",
        )

    @staticmethod
    def parse_markdown(
        file_path: str,
    ) -> str:

        return Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore",
        )