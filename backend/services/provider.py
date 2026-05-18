from db.models import LLMModel, LLMProvider
from schemas.provider import LLMModelCreate
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.base import BaseService


class ProviderService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session, LLMProvider)

    def get_llm_models_by_provider(self, provider_id: int):
        return self.session.scalars(
            select(LLMModel).where(LLMModel.provider_id == provider_id)
        ).all()

    def create_llm_model_by_provider(
        self, provider_id: int, llm_model_create: LLMModelCreate
    ):
        model = LLMModel(**llm_model_create.model_dump(), provider_id=provider_id)
        self.session.add(model)
        self.session.commit()
        return model
