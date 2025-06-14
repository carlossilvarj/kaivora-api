"""
Configuration settings for Kaivora API
"""

import os
from typing import Optional

class Settings:
    """
    Application settings and configuration
    """
    
    # Project Information
    PROJECT_NAME: str = "Kaivora API"
    PROJECT_DESCRIPTION: str = "FastAPI web server for Kaivora project with comprehensive API endpoints"
    VERSION: str = "1.0.0"
    
    # Environment Configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
        "*"  # Allow all origins in development
    ]
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "kaivora-api-secret-key-change-in-production")
    
    # Database (for future use)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # External API Keys (if needed)
    API_KEY: Optional[str] = os.getenv("API_KEY")

# Create settings instance
settings = Settings()
