from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ===========================
    # Application
    # ===========================
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str

    # ===========================
    # Database
    # ===========================
    DATABASE_URL: str

    # ===========================
    # JWT Authentication
    # ===========================
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()