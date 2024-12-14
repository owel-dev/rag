from fastapi import FastAPI
from app.api.endpoints import upload, query

app = FastAPI()

app.include_router(upload.router, prefix="/v1", tags=["upload"])
app.include_router(query.router, prefix="/v1", tags=["query"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)