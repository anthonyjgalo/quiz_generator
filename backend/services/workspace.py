from db.models import Document, Workspace
from fastapi import HTTPException
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.base import BaseService


class WorkspaceService(BaseService[Workspace]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Workspace)

    def create_workspace(self, workspace_create: WorkspaceCreate):
        # TODO: improve this method
        documents = self.session.scalars(
            select(Document).where(Document.id.in_(workspace_create.document_ids))
        ).all()

        found_ids = {doc.id for doc in documents}
        missing = set(workspace_create.document_ids) - found_ids

        if missing:
            raise HTTPException(
                400,
                f"Documents with ids {missing} that are being attempted to be used do not exist.",
            )

        workspace = Workspace(name=workspace_create.name, documents=documents)

        self.session.add(workspace)
        self.session.commit()

        return workspace

    def update_workspace(self, workspace_id: int, workspace_update: WorkspaceUpdate):
        # TODO: improve this method
        workspace = self.get_or_404(workspace_id)
        if workspace_update.name:
            workspace.name = workspace_update.name

        if workspace_update.document_ids is not None:
            documents = self.session.scalars(
                select(Document).where(Document.id.in_(workspace_update.document_ids))
            ).all()

            found_ids = {doc.id for doc in documents}
            missing = set(workspace_update.document_ids) - found_ids

            if missing:
                raise HTTPException(
                    400,
                    f"Documents with ids {missing} that are being attempted to be used do not exist.",
                )

            workspace.documents = list(documents)

        self.session.commit()
