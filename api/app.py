from fastapi import FastAPI

from . import records_router

app = FastAPI(docs_url="/ui")
app.include_router(records_router)


@app.get("/ping", tags=["Health"], include_in_schema=False)
async def ping():
    """Simple ping endpoint"""
    return {"pong": True}
