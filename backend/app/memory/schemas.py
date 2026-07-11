from pydantic import BaseModel


class MemoryCreate(BaseModel):
    content: str


class MemoryResponse(BaseModel):
    message: str
    content: str