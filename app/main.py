from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.middleware import token_validation_middleware
from app.router import main_router
from app.core import settings

app = FastAPI()

app.include_router(main_router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용된 Origin 리스트
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 미들웨어 등록
app.middleware("http")(token_validation_middleware)

if __name__ == "__main__":
    uvicorn.run(app,
                host=settings.UVICORN_HOST,
                port=settings.UVICORN_PORT)
