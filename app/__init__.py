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

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    setup_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/api/v1/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    setup_cors(app)
    setup_error_handlers(app)

    # Roteador principal da API
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        }

    return app
