import io
from typing import List

import llm.rag as rag_service
from core.exceptions import DocumentLinkedError
from db.models import Document, QuizGenerationDocument
from docx import Document as WordDocument
from fastapi import File, UploadFile
from pydantic import TypeAdapter
from pypdf import PdfReader
from schemas.document import DocumentCreatePaste, DocumentRead
from sqlalchemy import exists, select
from sqlalchemy.orm import Session
from utils.files import validate_file, validate_text_length


def get_documents(session: Session):
    documents = session.query(Document).all()
    list_adapter = TypeAdapter(List[DocumentRead])
    return list_adapter.validate_python(documents)


def get_document_by_id(document_id: int, session: Session):
    document = session.get(Document, document_id)

    if not document:
        return None

    return DocumentRead.model_validate(document)


def _process_pdf_file(content: bytes):
    pdf_stream = io.BytesIO(content)

    reader = PdfReader(pdf_stream)

    pages_texts = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text().strip()

        if page_text:
            page_text += f"\n -- Page {i + 1} --- \n"
            pages_texts.append(page_text)

    total_text = "".join(pages_texts)

    return total_text


def _process_docx_file(content: bytes):
    stream = io.BytesIO(content)
    doc = WordDocument(stream)

    doc_texts = []
    for para in doc.paragraphs:
        para_text = para.text.strip()

        if para_text:
            doc_texts.append(para_text)

    for table in doc.tables:
        for row in table.rows:
            cells_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if cells_texts:
                doc_texts.append(" | ".join(cells_texts))

    total_text = "\n\n".join(doc_texts)

    return total_text


def _process_txt_file(content: bytes):
    text = content.decode(errors="ignore")

    return text.strip()


def _process_file(file: UploadFile = File(...)):
    if not file.filename:
        raise ValueError("File must have a name")

    ext = validate_file(file.filename)

    content = file.file.read()

    if ext == "pdf":
        return (ext, _process_pdf_file(content))
    elif ext == "docx":
        return (ext, _process_docx_file(content))

    return (ext, _process_txt_file(content))


def create_document_by_paste(doc_create_paste: DocumentCreatePaste, session: Session):
    validate_text_length(doc_create_paste.content)

    doc_dict = {
        **doc_create_paste.model_dump(),
        "char_count": len(doc_create_paste.content),
    }
    document = Document(**doc_dict)

    session.add(document)
    session.flush()

    rag_service.save_document_content(document.id, document.content)

    session.commit()

    return DocumentRead.model_validate(document)


def create_document_by_upload(file: UploadFile, session: Session):
    format, text = _process_file(file)

    validate_text_length(text)

    document = Document(
        **{
            "name": file.filename,
            "source_type": "upload",
            "format": format,
            "content": text,
            "char_count": len(text),
        }
    )

    session.add(document)
    session.flush()
    rag_service.save_document_content(document.id, document.content)
    session.commit()

    return DocumentRead.model_validate(document)


def delete_document(document_id: int, session: Session):
    stmt = select(exists().where(QuizGenerationDocument.document_id == document_id))

    quiz_rel_exists = session.scalar(stmt)

    if quiz_rel_exists:
        raise DocumentLinkedError("The document is already being used in an quiz.")

    session.query(Document).where(Document.id == document_id).delete()
    rag_service.delete_document_content(document_id)

    session.commit()
