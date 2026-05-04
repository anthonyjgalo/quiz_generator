from pydantic import BaseModel, ConfigDict


class AnswerRead(BaseModel):
    id: int
    user_answer: dict
    question_id: int
    attempt_id: int

    model_config = ConfigDict(from_attributes=True)


class AnswerCreate(BaseModel):
    question_id: int
    user_answer: dict


class AttemptCreate(BaseModel):
    score: int
    answers: list[AnswerCreate]


class AttemptRead(BaseModel):
    id: int
    score: int
    created_at: str
    quiz_id: int

    model_config = ConfigDict(from_attributes=True)
