from typing import List

import services.connection as llm_connection_service
from fastapi import APIRouter, Depends, HTTPException
from schemas.connection import ConnectionCreate, ConnectionRead, ConnectionUpdate
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/connections", tags=["providers"])


@router.get("", response_model=List[ConnectionRead])
def get_llm_connections(db: Session = Depends(get_db)):
    return llm_connection_service.get_llm_connections(db)


@router.get("/{connection_id}", response_model=ConnectionRead)
def get_llm_connection(connection_id: int, db: Session = Depends(get_db)):
    conn = llm_connection_service.get_llm_connection(connection_id, db)

    if not conn:
        raise HTTPException(404, "Not Found")

    return conn


@router.post("", response_model=ConnectionRead)
def create_llm_connection(conn_create: ConnectionCreate, db: Session = Depends(get_db)):
    return llm_connection_service.create_llm_connection(conn_create, db)


@router.put("/{connection_id}")
def update_llm_connection(
    connection_id: int, conn_update: ConnectionUpdate, db: Session = Depends(get_db)
):
    llm_connection_service.update_llm_connection(connection_id, conn_update, db)


@router.delete("/{connection_id}")
def delete_llm_connection(connection_id: int, db: Session = Depends(get_db)):
    llm_connection_service.delete_llm_connection(connection_id, db)


@router.get("/{connection_id}/test")
def test_llm_connection(connection_id: int, db: Session = Depends(get_db)):
    llm_connection_service.test_llm_connection(connection_id, db)
