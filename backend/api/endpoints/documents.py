from fastapi import APIRouter, Depends, UploadFile, status
from schemas.document import DocumentCreatePaste, DocumentRead
from services.document import DocumentService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentRead])
def get_documents(db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    return document_service.get_all()


@router.get("/{document_id}", response_model=DocumentRead)
def get_document_by_id(document_id: int, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    return document_service.get_or_404(document_id)


@router.post(
    "/upload", response_model=DocumentRead, status_code=status.HTTP_201_CREATED
)
def create_document_by_upload(file: UploadFile, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    return document_service.create_document_by_upload(file)


@router.post("/paste", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document_by_paste(
    doc_create: DocumentCreatePaste, db: Session = Depends(get_db)
):
    document_service = DocumentService(db)
    return document_service.create_document_by_paste(doc_create)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    document_service.delete_document(document_id)
