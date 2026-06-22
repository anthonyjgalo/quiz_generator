from typing import Generic, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseService(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    def get_or_404(self, id: int) -> ModelType:
        obj = self.session.get(self.model, id)

        if not obj:
            raise HTTPException(
                404, f"Record with id {id} not found in {self.model.__name__}"
            )

        return obj

    def get_all(self):
        return self.session.scalars(select(self.model)).all()

    def create(self, schema_create: BaseModel):
        create_dict = schema_create.model_dump()
        obj = self.model(**create_dict)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, id: int, schema_update: BaseModel):
        obj = self.get_or_404(id)
        update_dict = schema_update.model_dump(exclude_unset=True)

        for k, v in update_dict.items():
            setattr(obj, k, v)

        self.session.commit()

    def delete(self, id: int):
        obj = self.get_or_404(id)
        self.session.delete(obj)
        self.session.commit()
