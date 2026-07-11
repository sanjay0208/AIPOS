from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.chat.router import router as chat_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(chat_router)