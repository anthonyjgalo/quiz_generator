from pydantic import BaseModel, ConfigDict


class QuizGenerateRequest(BaseModel):
    workspace_id: int
    total_questions: int
    question_distribution: dict  # problem inconsistent
    system_prompt: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1000


class QuizRead(BaseModel):
    id: int
    name: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class QuizGenerationRead(BaseModel):
    id: int
    model_name: str
    provider_name: str
    system_prompt: str
    temperature: float
    max_tokens: int
    questions_config: dict
    created_at: str
    quiz_id: int

    model_config = ConfigDict(from_attributes=True)


class QuestionRead(BaseModel):
    id: int
    text: str
    type: str
    options: dict
    correct_answer: dict
    feedback: str
    quiz_id: int

    model_config = ConfigDict(from_attributes=True)
