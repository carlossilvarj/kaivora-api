"""
Kaivora API – FastAPI Web Server
Main entry point for the application
"""

import uvicorn
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Run the server with Uvicorn
    # Configured for Replit deployment
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
