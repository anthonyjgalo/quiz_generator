from typing import List

from fastapi import APIRouter, Depends
from schemas.workspace import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate
from services.workspace import WorkspaceService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=List[WorkspaceRead])
def get_workspaces(db: Session = Depends(get_db)):
    workspace_service = WorkspaceService(db)
    return workspace_service.get_all()


@router.get("/{workspace_id}", response_model=WorkspaceRead)
def get_workspace_by_id(workspace_id: int, db: Session = Depends(get_db)):
    workspace_service = WorkspaceService(db)
    w = workspace_service.get_or_404(workspace_id)
    print(f"w.documents = {w.documents}")
    return w


@router.post("", response_model=WorkspaceRead)
def create_workspace(workspace_create: WorkspaceCreate, db: Session = Depends(get_db)):
    workspace_service = WorkspaceService(db)
    return workspace_service.create_workspace(workspace_create)


@router.put("/{workspace_id}")
def update_workspace(
    workspace_id: int, workspace_update: WorkspaceUpdate, db: Session = Depends(get_db)
):
    workspace_service = WorkspaceService(db)
    workspace_service.update_workspace(workspace_id, workspace_update)


@router.delete("/{workspace_id}")
def delete_workspace(workspace_id: int, db: Session = Depends(get_db)):
    workspace_service = WorkspaceService(db)
    workspace_service.delete(workspace_id)
