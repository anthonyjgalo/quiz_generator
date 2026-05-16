from typing import List

import services.document as document_service
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from schemas.document import DocumentCreatePaste, DocumentRead
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=List[DocumentRead])
def get_documents(db: Session = Depends(get_db)):
    return document_service.get_documents(db)


@router.get("/{document_id}", response_model=DocumentRead)
def get_document_by_id(document_id: int, db: Session = Depends(get_db)):
    document = document_service.get_document_by_id(document_id, db)

    if not document:
        raise HTTPException(404, detail="Not Found")

    return document


@router.post("/upload", response_model=DocumentRead)
def create_document_by_upload(file: UploadFile, db: Session = Depends(get_db)):
    return document_service.create_document_by_upload(file, db)


@router.post("/paste", response_model=DocumentRead)
def create_document_by_paste(
    doc_create: DocumentCreatePaste, db: Session = Depends(get_db)
):
    return document_service.create_document_by_paste(doc_create, db)


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    return document_service.delete_document(document_id, db)
