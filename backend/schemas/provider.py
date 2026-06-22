from pydantic import BaseModel, ConfigDict, Field


class LLMProviderRead(BaseModel):
    id: int
    name: str
    base_url: str

    model_config = ConfigDict(from_attributes=True)


class LLMModelRead(BaseModel):
    id: int
    name: str
    provider_id: int
    ctx_window: int

    model_config = ConfigDict(from_attributes=True)


class LLMModelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    ctx_window: int = Field(gt=0)
    provider_id: int | None = None
