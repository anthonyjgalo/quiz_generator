from datetime import datetime
from typing import List

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
        ForeignKey("llm_provider.id", ondelete="CASCADE"), nullable=False
    )
    ctx_window: Mapped[int] = mapped_column(Integer, nullable=False)


class LLMConnection(Base):
    __tablename__ = "llm_connection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    model_id: Mapped[int] = mapped_column(ForeignKey("llm_model.id"), nullable=False)


workspace_document = Table(
    "workspace_document",
    Base.metadata,
    Column(
        "workspace_id", ForeignKey("workspace.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "document_id", ForeignKey("document.id", ondelete="CASCADE"), primary_key=True
    ),
)

quiz_generation_document = Table(
    "quiz_generation_document",
    Base.metadata,
    Column(
        "quiz_generation_id",
        ForeignKey("quiz_generation.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("document_id", ForeignKey("document.id"), primary_key=True),
)


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(
        String(10), nullable=False, default="paste"
    )  # upload | paste
    format: Mapped[str] = mapped_column(String(10), default="txt", nullable=False)
    char_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    workspaces: Mapped[list["Workspace"]] = relationship(
        secondary=workspace_document, back_populates="documents"
    )
    quiz_generations: Mapped[list["QuizGeneration"]] = relationship(
        secondary=quiz_generation_document
    )


class Workspace(Base):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    documents: Mapped[list["Document"]] = relationship(
        secondary=workspace_document, back_populates="workspaces"
    )


class QuizGeneration(Base):
    __tablename__ = "quiz_generation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_instructions: Mapped[str] = mapped_column(Text, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_name: Mapped[str] = mapped_column(String(50), nullable=False)
    questions_config: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    keywords: Mapped[list | None] = mapped_column(JSON, default=list)
    difficulty_level: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # basic | intermediate | advanced


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    quiz_generation_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_generation.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    questions: Mapped[list["Question"]] = relationship()


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # single_choice | multiple_choice | True/False
    correct_answer: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    options: Mapped[dict] = mapped_column(JSON, nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False
    )
    answers: Mapped[List["QuestionAnswer"]] = relationship()


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_answer: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE"), nullable=False
    )
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_attempt.id", ondelete="CASCADE"), nullable=False
    )
