from sqlalchemy.orm import Session

from db.models import LLMModel, LLMProvider

PROVIDERS_DEFAULT_DATA = [
    {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": [
            {"name": "gpt-4o", "ctx_window": 128000},
            {"name": "gpt-4o-mini", "ctx_window": 128000},
            {"name": "gpt-4.1", "ctx_window": 1048576},
            {"name": "gpt-4.1-mini", "ctx_window": 1048576},
        ],
    },
    {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "models": [
            {"name": "deepseek-v4-pro", "ctx_window": 1000000},
            {"name": "deepseek-v4-flash", "ctx_window": 1000000},
        ],
    },
    {
        "name": "Gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "models": [
            {"name": "gemini-2.5-pro", "ctx_window": 1000000},
            {"name": "gemini-2.5-flash", "ctx_window": 1000000},
            {"name": "gemini-3-flash", "ctx_window": 1000000},
            {"name": "gemini-3.1-pro", "ctx_window": 1000000},
        ],
    },
    {"name": "Ollama", "base_url": "http://localhost:11434/v1", "models": []},
    {"name": "OpenAI Compatible", "base_url": "http://localhost:8080/v1", "models": []},
]


def seed_data(db: Session):
    if db.query(LLMProvider).first():
        return

    for p_data in PROVIDERS_DEFAULT_DATA:
        provider = LLMProvider(
            name=p_data["name"],
            base_url=p_data["base_url"],
        )
        db.add(provider)
        db.flush()

        for m_data in p_data["models"]:
            model = LLMModel(
                provider_id=provider.id,
                name=m_data["name"],
                ctx_window=m_data["ctx_window"],
            )
            db.add(model)

    db.commit()
