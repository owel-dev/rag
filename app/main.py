from fastapi import FastAPI
import uvicorn
from app.api import main_router
from app.core import settings

app = FastAPI()

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app,
                host=settings.UVICORN_HOST,
                port=settings.UVICORN_PORT)
