"""
Debug Routes (Development Only)

Lightweight debugging endpoints for testing and verification.
These should be disabled or removed in production.

TODO: Add environment check to disable in production
TODO: Add authentication for debug endpoints
"""
import logging
from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.core.model_loader import model_loader
from app.core.config import MODEL_PATH, ENCODER_PATH, DB_PATH
from app.services.database import get_history
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/status")
async def debug_status():
    """
    Get detailed system status for debugging.
    
    Returns information about:
    - Model loading status
    - File paths
    - Database status
    - Recent predictions
    """
    try:
        # Check model files
        model_exists = MODEL_PATH.exists() if MODEL_PATH else False
        encoder_exists = ENCODER_PATH.exists() if ENCODER_PATH else False
        
        # Check database
        db_exists = DB_PATH.exists() if DB_PATH else False
        db_size = DB_PATH.stat().st_size if db_exists else 0
        
        # Get recent history
        history = get_history()
        recent_count = len(history[:5])  # Last 5 records
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "model": {
                "loaded": model_loader.is_loaded,
                "model_file_exists": model_exists,
                "encoder_file_exists": encoder_exists,
                "model_path": str(MODEL_PATH) if MODEL_PATH else None,
                "encoder_path": str(ENCODER_PATH) if ENCODER_PATH else None,
            },
            "database": {
                "exists": db_exists,
                "path": str(DB_PATH) if DB_PATH else None,
                "size_bytes": db_size,
                "recent_records": recent_count,
            },
            "recent_predictions": history[:5] if history else [],
        }
    except Exception as e:
        logger.error(f"Error in debug status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Debug status error: {str(e)}")


@router.get("/test-prediction")
async def test_prediction():
    """
    Test if prediction endpoint is accessible.
    Does not actually make a prediction.
    """
    return {
        "status": "ok",
        "model_loaded": model_loader.is_loaded,
        "message": "Prediction endpoint is accessible. Use POST /api/v1/predict with audio file to test.",
        "note": "This endpoint only checks accessibility, not actual prediction."
    }

