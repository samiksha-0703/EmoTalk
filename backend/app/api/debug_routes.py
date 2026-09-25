"""
Debug Routes (Development Only)

Lightweight debugging endpoints for testing and verification.
These should be disabled or removed in production.

TODO: Add authentication for debug endpoints
"""
import logging
from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.core.hf_model_loader import model_loader, _FFMPEG_AVAILABLE
from app.core.config import DB_PATH
from app.services.database import get_connection

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/status")
async def debug_status():
    """
    Get detailed system status for debugging.

    Returns information about:
    - Model loading status (HuggingFace wav2vec2)
    - FFmpeg availability
    - Database status
    - Recent predictions
    """
    try:
        # Check database
        db_exists = DB_PATH.exists() if DB_PATH else False
        db_size = DB_PATH.stat().st_size if db_exists else 0

        # Count total records across all users (debug view — no user scope needed)
        total_records = 0
        recent_records = []
        if db_exists:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM emotions")
                total_records = cur.fetchone()[0]
                cur.execute("SELECT date, emotion, confidence FROM emotions ORDER BY date DESC LIMIT 5")
                recent_records = [
                    {"date": r[0], "emotion": r[1], "confidence": r[2]}
                    for r in cur.fetchall()
                ]
                conn.close()
            except Exception:
                pass

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "model": {
                "type": "HuggingFace wav2vec2",
                "name": model_loader.MODEL_NAME,
                "loaded": model_loader.is_loaded,
            },
            "ffmpeg": {
                "available": _FFMPEG_AVAILABLE,
            },
            "database": {
                "exists": db_exists,
                "path": str(DB_PATH) if DB_PATH else None,
                "size_bytes": db_size,
                "total_records": total_records,
            },
            "recent_predictions": recent_records,
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
        "ffmpeg_available": _FFMPEG_AVAILABLE,
        "message": "Prediction endpoint is accessible. Use POST /api/v1/predict with audio file to test.",
        "note": "This endpoint only checks accessibility, not actual prediction.",
    }
