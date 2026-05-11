from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class LLMProvider(Base):
    __tablename__ = "llm_provider"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)


class LLMModel(Base):
    __tablename__ = "llm_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    provider_id: Mapped[int] = mapped_column(
        ForeignKey("llm_provider.id"), nullable=False
    )
    ctx_window: Mapped[int] = mapped_column(Integer, nullable=False)


class LLMConnection(Base):
    __tablename__ = "llm_connection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    api_key: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    model_id: Mapped[int] = mapped_column(ForeignKey("llm_model.id"), nullable=False)


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(
        String(10), nullable=False, default="paste"
    )  # upload | paste
    format: Mapped[str] = mapped_column(String(10), nullable=False)
    char_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    processing_strategy: Mapped[str] = mapped_column(
        String(10), nullable=False, default="direct"
    )  # direct | chunked


class Workspace(Base):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)


class WorkspaceDocument(Base):
    __tablename__ = "workspace_document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspace.id"), nullable=False
    )
    document_id: Mapped[int] = mapped_column(ForeignKey("document.id"), nullable=False)


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class QuizGeneration(Base):
    __tablename__ = "quiz_generation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_instructions: Mapped[str] = mapped_column(Text, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_name: Mapped[str] = mapped_column(String(50), nullable=False)
    questions_config: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), nullable=False)


class QuizGenerationDocument(Base):
    __tablename__ = "quiz_generation_document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    generation_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_generation.id"), nullable=False
    )
    document_id: Mapped[int] = mapped_column(ForeignKey("document.id"), nullable=False)


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    correct_answer: Mapped[dict] = mapped_column(JSON, nullable=False)
    options: Mapped[dict] = mapped_column(JSON, nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), nullable=False)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), nullable=False)


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_answer: Mapped[dict] = mapped_column(JSON, nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_attempt.id"), nullable=False
    )
