from typing import List

from core.exceptions import ConnectionTestFailed
from db.models import LLMConnection
from openai import APIError, OpenAI
from pydantic import TypeAdapter
from schemas.connection import ConnectionCreate, ConnectionRead, ConnectionUpdate
from sqlalchemy import update
from sqlalchemy.orm import Session


def get_llm_connections(session: Session):
    connections = session.query(LLMConnection).all()
    list_adapter = TypeAdapter(List[ConnectionRead])

    return list_adapter.validate_python(connections)


def get_llm_connection(connection_id: int, session: Session):
    connection = session.get(LLMConnection, connection_id)

    if not connection:
        return None

    adapter = TypeAdapter(ConnectionRead)

    return adapter.validate_python(connection)


def create_llm_connection(conn_create: ConnectionCreate, session: Session):
    connection = LLMConnection(**conn_create.model_dump())

    session.add(connection)
    session.commit()

    conn_read = ConnectionRead.model_validate(connection)
    return conn_read


def update_llm_connection(
    connection_id: int, conn_update: ConnectionUpdate, session: Session
):
    stmt = (
        update(LLMConnection)
        .where(LLMConnection.id == connection_id)
        .values(**conn_update.model_dump(exclude_unset=True))
    )
    session.execute(stmt)
    session.commit()


def delete_llm_connection(connection_id: int, session: Session):
    session.query(LLMConnection).where(LLMConnection.id == connection_id).delete()

    session.commit()


def test_llm_connection(connection_id: int, session: Session):
    connection = session.query(LLMConnection).get(connection_id)

    if not connection:
        raise ConnectionTestFailed("The connection must exist to test it")

    if not connection.is_active:
        raise ConnectionTestFailed("The connection must be active to test it")

    openai = OpenAI(base_url=connection.base_url, api_key=connection.api_key)

    try:
        openai.models.list()
    except APIError as e:
        raise ConnectionTestFailed(f"API Error: {e.message}")
    except Exception as e:
        raise ConnectionTestFailed(f"Failed: {str(e)}")
