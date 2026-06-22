from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class QuizGenerateRequest(BaseModel):
    workspace_id: int
    connection_id: int
    question_distribution: dict
    user_instructions: str | None = None
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1_000, ge=1000)  # TODO: to validate
    keywords: List[str] | None
    difficulty_level: Literal["basic", "intermediate", "advanced"] = Field(
        default="basic"
    )


class QuizRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    questions: List["QuestionRead"]

    model_config = ConfigDict(from_attributes=True)


class QuizGenerationRead(BaseModel):
    id: int
    model_name: str
    provider_name: str
    user_instructions: str | None
    temperature: float
    max_tokens: int
    questions_config: dict
    created_at: datetime
    keywords: List[str] | None
    difficulty_level: str

    model_config = ConfigDict(from_attributes=True)


class QuestionRead(BaseModel):
    id: int
    text: str
    type: str
    options: dict
    correct_answer: List[str]
    feedback: str
    # quiz_id: int

    model_config = ConfigDict(from_attributes=True)
