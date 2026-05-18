from typing import List

from fastapi import APIRouter, Depends
from schemas.provider import LLMModelCreate, LLMModelRead, LLMProviderRead
from services.provider import ProviderService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=List[LLMProviderRead])
def get_llm_providers(db: Session = Depends(get_db)):
    provider_service = ProviderService(db)
    return provider_service.get_all()


@router.get("/{provider_id}/models", response_model=List[LLMModelRead])
def get_llm_models_by_provider(provider_id: int, db: Session = Depends(get_db)):
    provider_service = ProviderService(db)
    return provider_service.get_llm_models_by_provider(provider_id)


@router.post("/{provider_id}/models", response_model=LLMModelRead)
def create_llm_model_by_provider(
    provider_id: int, llm_model_create: LLMModelCreate, db: Session = Depends(get_db)
):
    provider_service = ProviderService(db)
    return provider_service.create_llm_model_by_provider(provider_id, llm_model_create)
