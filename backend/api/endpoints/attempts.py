from fastapi import APIRouter, Depends, status
from schemas.attempt import QuizAttemptCreate, QuizAttemptRead
from services.attempt import QuizAttemptService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/quizzes", tags=["attempts"])


@router.get("/{quiz_id}/attempts", response_model=list[QuizAttemptRead])
def get_quiz_attempts_by_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz_attempt_service = QuizAttemptService(db)
    return quiz_attempt_service.get_quiz_attempts_by_quiz(quiz_id)


@router.get("/{quiz_id}/attempts/{attempt_id}", response_model=QuizAttemptRead)
def get_quiz_attempt_by_id(
    quiz_id: int, attempt_id: int, db: Session = Depends(get_db)
):
    quiz_attempt_service = QuizAttemptService(db)
    return quiz_attempt_service.get_quiz_attempt_by_quiz_and_id(quiz_id, attempt_id)


@router.post(
    "/{quiz_id}/attempts",
    response_model=QuizAttemptRead,
    status_code=status.HTTP_201_CREATED,
)
def create_quiz_attempt(
    quiz_id: int, attempt_create: QuizAttemptCreate, db: Session = Depends(get_db)
):
    quiz_attempt_service = QuizAttemptService(db)
    return quiz_attempt_service.create_quiz_attempt(quiz_id, attempt_create)
