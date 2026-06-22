from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class QuizAnswerRead(BaseModel):
    id: int
    user_answer: list
    question_id: int

    model_config = ConfigDict(from_attributes=True)


class QuizAnswerCreate(BaseModel):
    question_id: int
    user_answer: List[str]


class QuizAttemptCreate(BaseModel):
    answers: list[QuizAnswerCreate]


class QuizAttemptRead(BaseModel):
    id: int
    score: int
    created_at: datetime
    quiz_id: int
    answers: List[QuizAnswerRead]

    model_config = ConfigDict(from_attributes=True)
