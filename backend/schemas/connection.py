from pydantic import BaseModel, ConfigDict, Field


class ConnectionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    base_url: str = Field(min_length=1, max_length=255)
    model_id: int
    api_key: str = Field(min_length=1, max_length=255)
    is_active: bool = True


class ConnectionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    base_url: str | None = Field(default=None, min_length=1, max_length=255)
    model_id: int | None = None
    api_key: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None


class ConnectionRead(BaseModel):
    id: int
    name: str
    base_url: str
    model_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
