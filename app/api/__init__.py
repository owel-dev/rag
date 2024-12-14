from fastapi import APIRouter
from app.api.endpoints import api_router

main_router = APIRouter()
main_router.include_router(api_router, prefix="/api/v1")
