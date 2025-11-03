"""
Videogames Chatbot - Main Application
AI-powered chatbot for Steam games with RAG capabilities using Claude
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import settings
from src.utils.logger import get_logger
from src.api.routes import router, initialize_services
from src.api.routes import chatbot_service, steam_service
from src import __version__

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info(f"Starting Videogames Chatbot API v{__version__}")
    logger.info(f"Environment: {settings.env}")
    logger.info(f"Debug mode: {settings.debug}")

    try:
        initialize_services()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Videogames Chatbot API")
    if chatbot_service:
        await chatbot_service.close()
    if steam_service:
        await steam_service.close()
    logger.info("All services closed")


# Create FastAPI app
app = FastAPI(
    title="Videogames Chatbot API",
    description="AI-powered chatbot for Steam games with RAG capabilities using Claude",
    version=__version__,
    debug=settings.debug,
    lifespan=lifespan,
)

# Configure CORS - Allow all origins for now (Railway + Vercel + local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Videogames Chatbot API",
        "version": __version__,
        "status": "running",
        "docs": "/docs",
        "api": "/api/v1",
    }


if __name__ == "__main__":
    import uvicorn
    import os

    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", settings.port))

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
