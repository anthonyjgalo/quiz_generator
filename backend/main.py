from api.endpoints.connections import router as llm_connections_router
from api.endpoints.documents import router as document_router
from api.endpoints.providers import router as llm_providers_router
from api.endpoints.workspaces import router as workspaces_router
from fastapi import FastAPI

API_PREFIX = "/api"

app = FastAPI(title="Quiz Generator")

app.include_router(llm_providers_router, prefix=API_PREFIX)
app.include_router(llm_connections_router, prefix=API_PREFIX)
app.include_router(document_router, prefix=API_PREFIX)
app.include_router(workspaces_router, prefix=API_PREFIX)


@app.get(API_PREFIX)
async def root():
    return {"msg": "API: Quiz Generator Working"}
