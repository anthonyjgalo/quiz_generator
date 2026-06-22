from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreatePaste(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    content: str = Field(min_length=200, max_length=50_000)


class DocumentRead(BaseModel):
    id: int
    name: str
    source_type: str
    format: str
    char_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
