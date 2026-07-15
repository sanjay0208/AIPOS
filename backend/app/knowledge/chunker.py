from typing import List


class DocumentChunker:
    """
    Splits extracted document text into chunks.
    """

    CHUNK_SIZE = 1000

    OVERLAP = 200

    @staticmethod
    def split(
        text: str,
    ) -> List[str]:

        if not text.strip():
            return []

        chunks = []

        start = 0

        length = len(text)

        while start < length:

            end = min(
                start + DocumentChunker.CHUNK_SIZE,
                length,
            )

            chunk = text[start:end].strip()

            if chunk:

                chunks.append(chunk)

            start += (
                DocumentChunker.CHUNK_SIZE
                - DocumentChunker.OVERLAP
            )

        return chunks