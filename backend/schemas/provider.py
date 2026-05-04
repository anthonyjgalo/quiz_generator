from pydantic import BaseModel, ConfigDict


class LLMProviderRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class LLMModelRead(BaseModel):
    id: int
    name: str
    provider_id: int

    model_config = ConfigDict(from_attributes=True)
