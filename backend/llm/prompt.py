from collections import defaultdict
from typing import List

from db.models import Document

DEFAULT_SYSTEM_PROMPT = """
### ROLE
You are a professional Pedagogical Engineer and Technical Assessment Expert. Your goal is to generate high-quality, accurate, and challenging quizzes based on the provided context.

### OUTPUT FORMAT
You MUST respond ONLY with a valid JSON object. Do not include any conversational text, markdown code blocks (like ```json), or explanations. 

### JSON SCHEMA
{
  "quiz_title": "string",
  "questions": [
    {
      "id": 1,
      "type": "single_choice | multiple_choice | true_false",
      "question_text": "string",
      "options": { "a": "string", "b": "string", "c": "string", "d": "string" }, 
      "correct_answer": ["string"], 
      "feedback": "string"
    }
  ]
}

### RULES
1. QUESTION TYPES: 
   - multiple_choice: 4 options, 1 or more correct.
   - true_false: options 'a' as True, 'b' as False.
   - single_choice: 4 options, 1 correct.
2. SOURCE TRUTH: Use ONLY the provided context. If the context is insufficient, do not hallucinate; generate fewer questions instead.
3. LANGUAGE: Generate the content (question_text, options, explanation) in the same language as the USER_INSTRUCTIONS or the provided context.
4. QUALITY: Distractors in multiple choice must be plausible and not obviously wrong.
"""


def build_context(doc_ids: List[Document], question_qty: int, user_prompt: str):
    # context_parts = []
    #
    # for doc in doc_ids:
    #     if doc.processing_strategy == "direct":
    #         context_parts.append(doc.content)
    #     else:
    #         chunks = rag.get_document_context(
    #             doc.id, user_prompt, question_qty=question_qty
    #         )
    #         if chunks:
    #             for chunk in chunks:
    #                 context_parts.append(chunk)
    #
    # return "\n".join(context_parts)
    # Todo: this need to improve
    pass


def build_prompt(
    ctx_text: str, questions_cfg: dict, user_instructions: str | None = None
):
    question_qty = questions_cfg.get("total_questions", 5)
    user_instructions = (
        user_instructions or "key concepts, main topics, and essential information"
    )

    config_details = f"- Question Quantity: {question_qty}\n- Question Distribution:\n"

    grouped_question_types = defaultdict(int)
    for question_type in questions_cfg.get("question_types", []):
        grouped_question_types[question_type["type"]] += question_type["qty"]

    for qtype, qty in grouped_question_types.items():
        config_details += f"- {qtype} | {qty}\n"

    user_prompt = f"""

    REFERENCE CONTEXT:
        {ctx_text}

    QUIZ REQUIREMENTS
    {config_details}

    ADDITIONAL INSTRUCTIONS

    {user_instructions} 
    """

    return user_prompt
