"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "postgresql://medicalcycle:medicalcycle@localhost:5432/medicalcycle_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Encryption
    ENCRYPTION_KEY: str = "your-encryption-key-32-chars-long"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MedicalCycle Cloud"
    PROJECT_VERSION: str = "0.1.0-alpha"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
