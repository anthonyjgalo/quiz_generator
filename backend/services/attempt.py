from typing import List

from db.models import QuestionAnswer, Quiz, QuizAttempt
from fastapi import HTTPException, status
from schemas.attempt import QuizAnswerCreate, QuizAttemptCreate
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.base import BaseService


class QuizAttemptService(BaseService[QuizAttempt]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, QuizAttempt)

    @staticmethod
    def _create_question_answers(
        attempt_id: int, attempt_answers: List[QuizAnswerCreate]
    ):
        question_answers = []
        for answer in attempt_answers:
            question_answer = QuestionAnswer(
                user_answer=answer.user_answer,
                question_id=answer.question_id,
                attempt_id=attempt_id,
            )
            question_answers.append(question_answer)
        return question_answers

    @staticmethod
    def _get_quiz_score(quiz: Quiz, attempt_answers: List[QuizAnswerCreate]):
        valid_answers = 0

        questions_map = {q.id: q for q in quiz.questions}

        for answer in attempt_answers:
            if not answer.user_answer:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Answer cannot be empty",
                )

            question = questions_map.get(answer.question_id)

            if not question:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Question with id {answer.question_id} is not part of the quiz questions",
                )

            user_answer = set(answer.user_answer)
            invalid_answer = user_answer - set(question.options.keys())

            if invalid_answer:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Invalid Answer {','.join(invalid_answer)}",
                )

            correct_answer = set(question.correct_answer)

            if user_answer == correct_answer:
                valid_answers += 1

        return round((valid_answers / len(quiz.questions)) * 100, 2)

    def create_quiz_attempt(self, quiz_id: int, attempt_create: QuizAttemptCreate):
        quiz = self.session.get(Quiz, quiz_id)

        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Quiz must exist to create an attempt",
            )

        if not attempt_create.answers or len(attempt_create.answers) != len(
            quiz.questions
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="The number of questions in the attempt must match the number in the quiz",
            )
        quiz_score = self._get_quiz_score(quiz, attempt_create.answers)

        quiz_attempt = QuizAttempt(score=quiz_score, quiz_id=quiz_id)

        self.session.add(quiz_attempt)
        self.session.flush()

        question_answers = self._create_question_answers(
            quiz_attempt.id, attempt_create.answers
        )

        self.session.add_all(question_answers)

        self.session.commit()

        return quiz_attempt

    def get_quiz_attempts_by_quiz(self, quiz_id: int):
        return self.session.scalars(
            select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
        ).all()

    def get_quiz_attempt_by_quiz_and_id(self, quiz_id: int, attempt_id: int):
        quiz_attempt = self.session.scalar(
            select(QuizAttempt).where(
                QuizAttempt.quiz_id == quiz_id, QuizAttempt.id == attempt_id
            )
        )

        if not quiz_attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz Attempt from quiz id {quiz_id} not found",
            )

        return quiz_attempt
