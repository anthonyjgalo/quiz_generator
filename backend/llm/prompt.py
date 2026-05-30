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
3. LANGUAGE: Generate the content (question_text, options, explanation) in the same language as the provided context.
4. QUALITY: Distractors in multiple choice must be plausible and not obviously wrong.
5. DIFFICULTY LEVEL: Adhere strictly to the level specified in QUIZ REQUIREMENTS. Adapt cognitive complexity based on the chosen value: basic | intermediate | advanced.
"""


def build_prompt(
    ctx_text: str,
    questions_cfg: dict,
    difficulty_level: str,
    user_instructions: str | None = None,
):
    question_qty = questions_cfg.get("total_questions", 5)

    config_details = f"- Total Questions: {question_qty}\n"
    config_details += f"- Difficulty Level: {difficulty_level}\n"
    config_details += "- Questions Distribution:\n"

    # grouped_question_types = defaultdict(int)
    # for question_type, question_qty in questions_cfg.items():
    #     grouped_question_types[question_type] += question_qty

    for qtype, qty in questions_cfg.get("question_types", {}).items():
        config_details += f"\t* {qtype}: {qty}\n"

    user_prompt = f"""
REFERENCE CONTEXT: {ctx_text}

QUIZ REQUIREMENTS
{config_details}

{f"ADDITIONAL INSTRUCTIONS \n\n {user_instructions}" if user_instructions else ""}"""

    return user_prompt
