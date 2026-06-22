from fastapi import APIRouter, Depends, status
from schemas.provider import LLMModelCreate, LLMModelRead, LLMProviderRead
from services.provider import ProviderService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=list[LLMProviderRead])
def get_llm_providers(db: Session = Depends(get_db)):
    provider_service = ProviderService(db)
    return provider_service.get_all()


@router.get("/{provider_id}/models", response_model=list[LLMModelRead])
def get_llm_models_by_provider(provider_id: int, db: Session = Depends(get_db)):
    provider_service = ProviderService(db)
    return provider_service.get_llm_models_by_provider(provider_id)


@router.post(
    "/{provider_id}/models",
    response_model=LLMModelRead,
    status_code=status.HTTP_201_CREATED,
)
def create_llm_model_by_provider(
    provider_id: int, llm_model_create: LLMModelCreate, db: Session = Depends(get_db)
):
    provider_service = ProviderService(db)
    return provider_service.create_llm_model_by_provider(provider_id, llm_model_create)
