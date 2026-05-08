# db/seed.py
from sqlalchemy.orm import Session

from db.models import LLMProvider


def seed_data(db: Session):
    if not db.query(LLMProvider).first():
        providers = [
            LLMProvider(name="OpenAI", base_url="https://api.openai.com/v1"),
            LLMProvider(name="Deepseek", base_url="https://api.deepseek.com/v1"),
            LLMProvider(
                name="Gemini",
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
            LLMProvider(name="Groq", base_url="https://api.groq.com/openai/v1"),
            LLMProvider(name="Together AI", base_url="https://api.together.xyz/v1"),
            LLMProvider(
                name="Fireworks", base_url="https://api.fireworks.ai/inference/v1"
            ),
            LLMProvider(name="Cerebras", base_url="https://api.cerebras.ai/v1"),
            LLMProvider(name="SambaNova", base_url="https://api.sambanova.ai/v1"),
            LLMProvider(name="Perplexity", base_url="https://api.perplexity.ai"),
            LLMProvider(name="xAI", base_url="https://api.x.ai/v1"),
        ]

        db.add_all(providers)
        db.commit()
