from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.document import DocumentRead


class WorkspaceCreate(BaseModel):
    name: str
    document_ids: list[int] = []


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    document_ids: list[int] | None = None


class WorkspaceRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    documents: list[DocumentRead]

    model_config = ConfigDict(from_attributes=True)
