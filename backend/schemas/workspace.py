from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.document import DocumentRead


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    document_ids: list[int] = []


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    document_ids: list[int] | None = None


class WorkspaceRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    documents: list[DocumentRead]

    model_config = ConfigDict(from_attributes=True)
