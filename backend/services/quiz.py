import json
from typing import List

from core.constants import (
    DEFAULT_USER_INSTRUCTIONS,
    MAX_DIRECT_CHARS,
    QUESTION_FIXED_LIMITS,
)
from core.exceptions import (
    EmptyWorkspaceError,
    InsufficientContextError,
    QuestionLimitError,
)
from db.models import (
    Document,
    LLMConnection,
    LLMModel,
    LLMProvider,
    Question,
    Quiz,
    QuizGeneration,
    Workspace,
)
from fastapi import HTTPException, status
from llm import prompt, rag
from llm.client import LLMService
from schemas.quiz import QuizGenerateRequest
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.base import BaseService


class QuizService(BaseService[Quiz]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Quiz)

    @staticmethod
    def _validate_question_qty(question_qty: int, content_len: int):
        if question_qty < 0:
            raise QuestionLimitError("The number of questions cannot be negative.")

        for (min_len, max_len), max_q in QUESTION_FIXED_LIMITS:
            if min_len <= content_len <= max_len:
                if question_qty > max_q:
                    raise QuestionLimitError(
                        "The number of questions does not fit in the content."
                    )
                return

        raise QuestionLimitError("Invalid number of questions")

    @staticmethod
    def _get_content_by_threshold(
        documents: List[Document],
        query_text: str,
        total_questions: int,
        direct_content_len: int,
    ):
        if direct_content_len <= MAX_DIRECT_CHARS:
            return "".join([doc.content for doc in documents])
        else:
            ctx_parts = []
            for doc in documents:
                doc_results = rag.get_document_context(
                    doc.id,
                    query_text,
                    total_questions,
                )

                if doc_results:
                    for doc_res in doc_results:
                        ctx_parts.append("\n".join(doc_res))

            if not ctx_parts:
                raise InsufficientContextError(
                    "A quiz cannot be generated if there is not enough context."
                )

            return "\n".join(ctx_parts)

    @staticmethod
    def _get_total_questions(question_dist: dict):
        return sum([qty for qty in question_dist.values()])

    def _get_workspace_documents(self, workspace_id: int):
        workspace = self.session.get(Workspace, workspace_id)

        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A quiz cannot be generated if there is no workspace.",
            )

        if not workspace.documents:
            raise EmptyWorkspaceError(
                "A quiz cannot be generated if there are no documents."
            )

        return workspace.documents

    def _get_llm_connection(self, llm_connection_id: int):
        llm_connection = self.session.get(LLMConnection, llm_connection_id)

        if not llm_connection or (llm_connection and not llm_connection.is_active):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A quiz cannot be generated if there is no LLM connection.",
            )

        return llm_connection

    def _get_llm_model(self, llm_model_id: int):
        llm_model = self.session.get(LLMModel, llm_model_id)
        assert llm_model is not None, "LLM Model must exist"
        return llm_model

    def _get_llm_provider(self, llm_provider_id: int):
        llm_provider = self.session.get(LLMProvider, llm_provider_id)
        assert llm_provider is not None, "LLM Provider must exist"
        return llm_provider

    @staticmethod
    def _create_questions(questions: List[dict], quiz_id: int):
        questions_obj = []
        for question in questions:
            new_question_obj = Question(
                **{
                    "type": question["type"],
                    "text": question["question_text"],
                    "feedback": question["feedback"],
                    "correct_answer": question["correct_answer"],
                    "options": question["options"],
                    "quiz_id": quiz_id,
                }
            )
            questions_obj.append(new_question_obj)

        return questions_obj

    def generate_quiz(self, gen_req: QuizGenerateRequest):
        documents = self._get_workspace_documents(gen_req.workspace_id)
        llm_connection = self._get_llm_connection(gen_req.connection_id)
        direct_content_len = sum([doc.char_count for doc in documents])
        total_questions = QuizService._get_total_questions(
            gen_req.question_distribution
        )
        QuizService._validate_question_qty(total_questions, direct_content_len)

        keywords = ",".join(gen_req.keywords or [])

        quiz_content = QuizService._get_content_by_threshold(
            documents,
            keywords or DEFAULT_USER_INSTRUCTIONS,
            total_questions,
            direct_content_len=direct_content_len,
        )

        questions_cfg = {
            "total_questions": total_questions,
            "question_types": gen_req.question_distribution,
        }

        user_prompt = prompt.build_prompt(
            ctx_text=quiz_content,
            questions_cfg=questions_cfg,
            difficulty_level=gen_req.difficulty_level,
            user_instructions=gen_req.user_instructions,
        )

        llm_model = self._get_llm_model(llm_connection.model_id)

        llm_service = LLMService(
            llm_connection.base_url, llm_connection.api_key, llm_model.name
        )

        llm_model_response = llm_service.call_api_model(
            system_prompt=prompt.DEFAULT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=gen_req.temperature,
            max_tokens=gen_req.max_tokens,
        )

        try:
            quiz_data = json.loads(llm_model_response or "")
        except (json.JSONDecodeError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The AI provider returned an empty or invalid response structure. Please try again.",
            )

        llm_provider = self._get_llm_provider(llm_model.provider_id)

        quiz_generation = QuizGeneration(
            model_name=llm_model.name,
            provider_name=llm_provider.name,
            user_instructions=gen_req.user_instructions,
            temperature=gen_req.temperature,
            max_tokens=gen_req.max_tokens,
            questions_config=questions_cfg,
            keywords=gen_req.keywords,
            difficulty_level=gen_req.difficulty_level,
        )

        self.session.add(quiz_generation)
        self.session.flush()

        quiz = Quiz(name=quiz_data["quiz_title"], quiz_generation_id=quiz_generation.id)

        self.session.add(quiz)
        self.session.flush()

        questions = self._create_questions(quiz_data["questions"], quiz.id)

        self.session.add_all(questions)
        self.session.commit()

        return quiz

    def get_quiz_generations_by_quiz(self, quiz_id: int):
        quiz = self.get_or_404(quiz_id)
        quiz_generation = self.session.get(QuizGeneration, quiz.quiz_generation_id)

        if not quiz_generation:
            raise HTTPException(
                status_code=404,
                detail=f"Quiz Generation with id {quiz.quiz_generation_id} not found",
            )
        return quiz_generation

    def get_quiz_generations(self):
        return self.session.scalars(select(QuizGeneration)).all()

    def delete(self, id: int):
        quiz_generation = self.get_quiz_generations_by_quiz(id)
        self.session.delete(quiz_generation)
        super().delete(id)
