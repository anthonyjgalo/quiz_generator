from typing import List

from fastapi import APIRouter, Depends
from schemas.connection import ConnectionCreate, ConnectionRead, ConnectionUpdate
from services.connection import ConnectionService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/connections", tags=["providers"])


@router.get("", response_model=List[ConnectionRead])
def get_llm_connections(db: Session = Depends(get_db)):
    connection_service = ConnectionService(db)
    return connection_service.get_all()


@router.get("/{connection_id}", response_model=ConnectionRead)
def get_llm_connection_by_id(connection_id: int, db: Session = Depends(get_db)):
    connection_service = ConnectionService(db)
    return connection_service.get_or_404(connection_id)


@router.post("", response_model=ConnectionRead)
def create_llm_connection(conn_create: ConnectionCreate, db: Session = Depends(get_db)):
    connection_service = ConnectionService(db)
    return connection_service.create(conn_create)


@router.put("/{connection_id}")
def update_llm_connection(
    connection_id: int, conn_update: ConnectionUpdate, db: Session = Depends(get_db)
):
    connection_service = ConnectionService(db)
    connection_service.update(connection_id, conn_update)


@router.delete("/{connection_id}")
def delete_llm_connection(connection_id: int, db: Session = Depends(get_db)):
    connection_service = ConnectionService(db)
    connection_service.delete(connection_id)


@router.get("/{connection_id}/test")
def test_llm_connection(connection_id: int, db: Session = Depends(get_db)):
    connection_service = ConnectionService(db)
    connection_service.test_llm_connection(connection_id)
