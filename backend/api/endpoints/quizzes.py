from typing import List

from fastapi import APIRouter, Depends
from schemas.quiz import QuizGenerateRequest, QuizGenerationRead, QuizRead
from services.quiz import QuizService
from sqlalchemy.orm import Session

from api.deps import get_db

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("", response_model=List[QuizRead])
def get_quizzes(db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    return quiz_service.get_all()


@router.get("/{quiz_id}", response_model=QuizRead)
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    return quiz_service.get_or_404(quiz_id)


@router.post("", response_model=QuizRead)
def generate_quiz(quiz_gen_req: QuizGenerateRequest, db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    return quiz_service.generate_quiz(quiz_gen_req)


@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    quiz_service.delete(quiz_id)


@router.get("/{quiz_id}/generation", response_model=QuizGenerationRead)
def get_quiz_generation_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    return quiz_service.get_quiz_generations_by_quiz(quiz_id)


quiz_gen_router = APIRouter(prefix="/quiz-generations", tags=["quiz-generations"])


@quiz_gen_router.get("", response_model=List[QuizGenerationRead])
def get_quiz_generations(db: Session = Depends(get_db)):
    quiz_service = QuizService(db)
    return quiz_service.get_quiz_generations()
