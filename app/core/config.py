from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance System API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Settings will automatically read from environment variables if they exist
    class Config:
        case_sensitive = True

settings = Settings()