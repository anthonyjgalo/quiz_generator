from api.endpoints.providers import router as llm_providers_router
from fastapi import FastAPI

API_PREFIX = "/api"

app = FastAPI(title="Quiz Generator")

app.include_router(llm_providers_router, prefix=API_PREFIX)


@app.get(API_PREFIX)
async def root():
    return {"msg": "API: Quiz Generator Working"}
