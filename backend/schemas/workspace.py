from pydantic import BaseModel, ConfigDict


class WorkspaceCreate(BaseModel):
    name: str
    document_ids: list[int]


class WorkspaceUpdate(BaseModel):
    name: str | None = None


class WorkspaceRead(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
