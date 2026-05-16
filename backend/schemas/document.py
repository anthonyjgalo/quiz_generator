from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentCreatePaste(BaseModel):
    name: str
    content: str


class DocumentRead(BaseModel):
    id: int
    name: str
    source_type: str
    format: str
    char_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
