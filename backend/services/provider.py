from typing import List

from db.models import LLMModel, LLMProvider
from pydantic import TypeAdapter
from schemas.provider import LLMModelCreate, LLMModelRead, LLMProviderRead
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_llm_providers(session: Session):
    llm_providers = session.query(LLMProvider).all()
    list_adapter = TypeAdapter(List[LLMProviderRead])
    return list_adapter.validate_python(llm_providers)


def get_llm_models_by_provider(provider_id: int, session: Session):
    stmt = select(LLMModel).where(LLMModel.provider_id == provider_id)
    llm_models = session.scalars(stmt).all()
    list_adapter = TypeAdapter(List[LLMModelRead])

    return list_adapter.validate_python(llm_models)


def create_llm_model_by_provider(
    provider_id: int, llm_model: LLMModelCreate, session: Session
):
    llm_model_dict = llm_model.model_dump()
    llm_model_dict["provider_id"] = provider_id
    model = LLMModel(**llm_model_dict)

    session.add(model)
    session.commit()

    model_read = LLMModelRead.model_validate(model)
    return model_read
