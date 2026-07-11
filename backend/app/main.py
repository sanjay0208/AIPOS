from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

from app.database.base import Base
from app.database.session import engine

# Import models so SQLAlchemy knows about them
from app.database.models.user import User
from app.database.models.memory import Memory

logger = setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Personal Operating System",
)

# Create database tables (Development only)
Base.metadata.create_all(bind=engine)

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