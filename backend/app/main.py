from fastapi import FastAPI
from app.database.models.message import Message
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

# Import models so Alembic can discover them
from app.database.models.conversation import Conversation
from app.database.models.memory import Memory
from app.database.models.user import User

logger = setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Personal Operating System",
)

# Register API routes
app.include_router(api_router)


@app.get("/", tags=["Root"])
async def root():
    logger.info("Root endpoint accessed")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "running",
    }