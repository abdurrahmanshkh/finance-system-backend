from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance System API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    # Using SQLite for local development. This creates a file named finance.db in the root directory.
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./finance.db"

    class Config:
        case_sensitive = True

settings = Settings()