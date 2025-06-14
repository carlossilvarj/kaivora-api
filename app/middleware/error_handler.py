"""
Error handling middleware for Kaivora API
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
from typing import Union
from app.models.schemas import ErrorResponse

logger = logging.getLogger(__name__)

def setup_error_handlers(app: FastAPI) -> None:
    """
    Setup error handlers for the FastAPI application
    
    Args:
        app (FastAPI): FastAPI application instance
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handle HTTP exceptions
        
        Args:
            request (Request): FastAPI request object
            exc (HTTPException): HTTP exception
        
        Returns:
            JSONResponse: Formatted error response
        """
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        
        error_response = ErrorResponse(
            error="HTTP_ERROR",
            message=exc.detail,
            details={
                "status_code": exc.status_code,
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Handle request validation errors
        
        Args:
            request (Request): FastAPI request object
            exc (RequestValidationError): Validation exception
        
        Returns:
            JSONResponse: Formatted validation error response
        """
        logger.error(f"Validation Error: {exc.errors()}")
        
        # Format validation errors for better readability
        error_details = []
        for error in exc.errors():
            field_path = " -> ".join(str(x) for x in error.get("loc", []))
            error_details.append({
                "field": field_path,
                "message": error.get("msg", ""),
                "type": error.get("type", ""),
                "input": error.get("input")
            })
        
        error_response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Request validation failed",
            details={
                "validation_errors": error_details,
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.dict()
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """
        Handle value errors
        
        Args:
            request (Request): FastAPI request object
            exc (ValueError): Value error exception
        
        Returns:
            JSONResponse: Formatted error response
        """
        logger.error(f"Value Error: {str(exc)}")
        
        error_response = ErrorResponse(
            error="VALUE_ERROR",
            message=str(exc),
            details={
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Handle general exceptions
        
        Args:
            request (Request): FastAPI request object
            exc (Exception): General exception
        
        Returns:
            JSONResponse: Formatted error response
        """
        logger.error(f"Unexpected Error: {type(exc).__name__} - {str(exc)}")
        
        error_response = ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            details={
                "error_type": type(exc).__name__,
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.dict()
        )
    
    logger.info("Error handlers configured successfully")
