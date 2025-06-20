"""
Kaivora API Application Factory
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_error_handlers
from app.api.routes import api_router
from app.db.init_db import init_database

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    
    # Setup logging
    setup_logging()
    
    # Create FastAPI instance with metadata
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/api/v1/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Setup CORS middleware
    setup_cors(app)
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Root endpoint - redirect to docs
    @app.get("/", include_in_schema=False)
    async def root():
        """Redirect root path to API documentation"""
        return RedirectResponse(url="/docs")
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint for monitoring
        
        Returns:
            dict: Health status information
        """
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        }
    
    return app