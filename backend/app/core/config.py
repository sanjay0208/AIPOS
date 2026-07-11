from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================
    # Application
    # ==========================
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str

    # ==========================
    # JWT
    # ==========================
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==========================
    # AI
    # ==========================
    AI_PROVIDER: str = "mock"
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()