from fastapi import FastAPI
import uvicorn

from app.middleware import token_validation_middleware
from app.router import main_router
from app.core import settings

app = FastAPI()

app.include_router(main_router)

# 미들웨어 등록
app.middleware("http")(token_validation_middleware)

if __name__ == "__main__":
    uvicorn.run(app,
                host=settings.UVICORN_HOST,
                port=settings.UVICORN_PORT)
