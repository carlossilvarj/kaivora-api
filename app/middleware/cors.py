"""
CORS middleware configuration for Kaivora API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def setup_cors(app: FastAPI) -> None:
    """
    Setup CORS middleware for the FastAPI application
    
    Args:
        app (FastAPI): FastAPI application instance
    """
    
    logger.info("Setting up CORS middleware")
    logger.info(f"Allowed origins: {settings.CORS_ORIGINS}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-API-Key",
            "Origin",
            "Cache-Control",
            "Pragma"
        ],
        expose_headers=[
            "Content-Length",
            "Content-Type",
            "X-Total-Count",
            "X-Page-Count"
        ]
    )
    
    logger.info("CORS middleware configured successfully")
