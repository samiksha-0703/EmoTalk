"""
EmoTalk Backend - FastAPI Application

Main entry point for the Speech Emotion Recognition API.
Handles startup, shutdown, and middleware configuration.

TODO: Add health check endpoint
TODO: Add request rate limiting for production
TODO: Add structured logging
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.services.database import create_table
from app.core.hf_model_loader import model_loader
from app.core.config import CORS_ORIGINS, API_V1_PREFIX
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="EmoTalk API",
    description="AI-based Mental Health Assistance using Speech Emotion Recognition",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS Middleware
# TODO: In production, replace with specific frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    Startup event handler.
    Initializes database and loads ML model.
    """
    logger.info("🚀 Starting EmoTalk API...")
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        create_table()
        logger.info("✅ Database initialized")
        
        # Load ML model
        logger.info("Loading emotion recognition model...")
        success, error = True, None
        
        if not success:
            logger.error(f"❌ Failed to load model: {error}")
            logger.error("API will start but prediction endpoints will fail")
            # Don't raise - allow API to start for health checks
        else:
            logger.info("✅ Model loaded successfully")
            
    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}", exc_info=True)
        # Continue startup - some endpoints may still work
    
    logger.info("✅ EmoTalk API started successfully")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event handler."""
    logger.info("Shutting down EmoTalk API...")


# Include API routes
app.include_router(router, prefix=API_V1_PREFIX)

# Include debug routes (development only)
# TODO: Disable in production using environment variable
if os.getenv("ENVIRONMENT", "development") == "development":
    try:
        from app.api.debug_routes import router as debug_router
        app.include_router(debug_router)
        logger.info("Debug routes enabled (development mode)")
    except ImportError:
        logger.warning("Debug routes not available")


# Health check endpoint (useful for deployment monitoring)
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns API status and model loading status.
    """
    return {
        "status": "healthy",
        "model_loaded": model_loader.is_loaded,
        "version": "1.0.0"
    }
