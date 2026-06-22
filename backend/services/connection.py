from core.exceptions import ConnectionTestFailed
from db.models import LLMConnection
from openai import APIError, OpenAI
from sqlalchemy.orm import Session

from services.base import BaseService


class ConnectionService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session, LLMConnection)

    def test_llm_connection(self, connection_id: int):
        connection = self.get_or_404(connection_id)

        if not connection.is_active:
            raise ConnectionTestFailed("The connection must be active to test it")

        client = OpenAI(
            base_url=connection.base_url, api_key=connection.api_key, timeout=5.0
        )

        try:
            client.models.list()
        except APIError as e:
            raise ConnectionTestFailed(f"API Error: {e.message}")
        except Exception as e:
            raise ConnectionTestFailed(f"Failed: {str(e)}")
