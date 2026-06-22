from db.models import Document, Workspace
from fastapi import HTTPException, status
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.base import BaseService


class WorkspaceService(BaseService[Workspace]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Workspace)

    def _get_documents(self, doc_ids: list[int]):
        documents = self.session.scalars(
            select(Document).where(Document.id.in_(doc_ids))
        ).all()

        found_ids = {doc.id for doc in documents}
        missing = set(doc_ids) - found_ids

        if missing:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Documents with ids {missing} that are being attempted to be used do not exist.",
            )

        return documents

    def create_workspace(self, workspace_create: WorkspaceCreate):
        documents = self._get_documents(workspace_create.document_ids)

        workspace = Workspace(name=workspace_create.name, documents=documents)

        self.session.add(workspace)
        self.session.commit()
        self.session.refresh(workspace)
        return workspace

    def update_workspace(self, workspace_id: int, workspace_update: WorkspaceUpdate):
        workspace = self.get_or_404(workspace_id)
        if workspace_update.name:
            workspace.name = workspace_update.name

        if workspace_update.document_ids is not None:
            documents = self._get_documents(workspace_update.document_ids)
            workspace.documents = list(documents)
        self.session.commit()
