from fastapi import APIRouter
from .endpoints import router

main_router = APIRouter()
main_router.include_router(router, prefix="/api/v1")
