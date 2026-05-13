from pydantic import BaseModel, ConfigDict


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
    name: str
    ctx_window: int
