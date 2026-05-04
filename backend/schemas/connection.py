from pydantic import BaseModel, ConfigDict


class ConnectionCreate(BaseModel):
    name: str
    model_id: int
    api_key: str
    base_url: str
    is_active: bool = True


class ConnectionUpdate(BaseModel):
    name: str | None = None
    model_id: int | None = None
    api_key: str | None = None
    base_url: str | None = None
    is_active: bool | None = None


class ConnectionRead(BaseModel):
    id: int
    name: str
    model_id: int
    base_url: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
