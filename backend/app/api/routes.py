"""
API Routes for EmoTalk

Handles all HTTP endpoints for emotion prediction, history, and reports.
Uses service layer for business logic separation.

TODO: Add rate limiting
TODO: Add request logging
TODO: Add API versioning support
"""
import logging
import tempfile
import os
from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, Any, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

from app.core.hf_model_loader import model_loader
from app.core.config import (
    MAX_FILE_SIZE_MB,
    ALLOWED_AUDIO_TYPES,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_EXPIRATION_MINUTES,
    API_V1_PREFIX,
)
from app.services.database import (
    get_history,
    save_emotion,
    create_user,
    get_user_by_email,
)
from app.services.gemini import (
    generate_daily_insight,
    generate_weekly_insight,
)


# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_PREFIX}/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


# -------------------------
# AUTHENTICATION ROUTES
# -------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

logger = logging.getLogger(__name__)
router = APIRouter()


# =========================
# RESPONSE MODELS
# =========================
class PredictionResponse(BaseModel):
    """Response model for emotion prediction."""
    emotion: str
    confidence: float


class ErrorResponse(BaseModel):
    """Error response model."""
    error: bool
    details: str

# ===============================
# 🎤 PREDICT EMOTION
# ===============================
@router.post("/auth/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    """Register a new user and return a JWT token."""
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed = hash_password(user.password)
    success = create_user(user.email, hashed)
    if not success:
        # should not happen because we just checked, but handle literally
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create user")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login", response_model=TokenResponse)
def login(user: UserCreate):
    """Authenticate existing user and return a JWT token."""
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Predict emotion from audio file.
    
    Accepts audio files (wav, webm, mp3, m4a) up to 10MB.
    Returns predicted emotion and confidence score.
    """
    request_start_time = datetime.utcnow()
    
    # Validate model is loaded
    if not model_loader.is_loaded:
        logger.error("Prediction attempted but model not loaded")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not loaded. Please check server logs."
        )
    
    # Validate file type
    if file.content_type and file.content_type not in ALLOWED_AUDIO_TYPES:
        # Also allow files without content-type (some clients don't send it)
        if file.content_type:
            logger.warning(f"Rejected file with content-type: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_AUDIO_TYPES)}"
            )
    
    # Validate file size
    contents = await file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    
    if file_size_mb > MAX_FILE_SIZE_MB:
        logger.warning(f"File too large: {file_size_mb:.2f}MB")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE_MB}MB"
        )
    
    # Save to temporary file for processing
    tmp_path = None
    try:
        # Create temp file with appropriate extension
        suffix = ".wav"  # librosa can handle various formats
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        
        logger.info(f"Processing audio: {file.filename or 'unnamed'} ({file_size_mb:.2f}MB)")

        prediction_start = datetime.utcnow()
        emotion, confidence = model_loader.predict(tmp_path)
        prediction_time = (datetime.utcnow() - prediction_start).total_seconds()
        logger.debug(f"Model prediction took {prediction_time:.2f}s")
        
        total_time = (datetime.utcnow() - request_start_time).total_seconds()
        logger.info(
            f"✅ Prediction: {emotion} ({confidence:.1%} confidence) "
            f"| Time: {total_time:.2f}s | File: {file_size_mb:.2f}MB"
        )
        
        # Save to database
        try:
            save_emotion(
                emotion,
                confidence,
                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            )
            logger.debug("Emotion saved to database")
        except Exception as db_error:
            # Log but don't fail the request if DB save fails
            logger.error(f"Failed to save emotion to database: {db_error}")
        
        return {
            "emotion": emotion,
            "confidence": confidence
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio file: {str(e)}"
        )
    finally:
        # Clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {e}")

# ===============================
# 📜 EMOTION HISTORY
# ===============================
@router.get("/emotion-history")
def emotion_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get all emotion history records.
    
    Returns list of all recorded emotions with timestamps and confidence scores.
    """
    try:
        history = get_history()
        return {"data": history, "count": len(history)}
    except Exception as e:
        logger.error(f"Error fetching emotion history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching emotion history"
        )

# ===============================
# DAILY REPORT
# ===============================
@router.get("/daily-report")
def daily_report(current_user: Dict[str, Any] = Depends(get_current_user)):
    history = get_history()
    today = datetime.utcnow().date().isoformat()

    today_records = [
        h for h in history if h["date"].startswith(today)
    ]

    if not today_records:
        return {"error": True, "details": "No emotions recorded today."}

    emotions = [r["emotion"] for r in today_records]
    counts = Counter(emotions)
    dominant = counts.most_common(1)[0][0]

    summary = f"Emotion counts: {dict(counts)}. Dominant: {dominant}"

    try:
        ai_text = generate_daily_insight(summary)

        insight = ""
        suggestion = ""

        lower = ai_text.lower()
        if "suggestion" in lower:
            parts = ai_text.split("Suggestion", 1)
            insight = parts[0].replace("Insight", "").strip(":\n ")
            suggestion = parts[1].strip(":\n ")
        else:
            insight = ai_text.strip()
            suggestion = "Take a few moments to reflect and care for yourself."

        if not insight:
            insight = "Your emotions today show meaningful patterns."
        if not suggestion:
            suggestion = "Consider gentle self-care and mindful pauses."

        return {
            "report": {
                "dominantEmotion": dominant,
                "insight": insight,
                "suggestion": suggestion
            }
        }

    except Exception as e:
        logger.warning(f"Gemini API error for daily report: {str(e)}")
        return {
            "report": {
                "dominantEmotion": dominant,
                "insight": "Your emotions today showed meaningful patterns.",
                "suggestion": "Take a few moments to rest and reflect."
            }
        }

# ===============================
# WEEKLY REPORT
# ===============================
@router.get("/weekly-report")
def weekly_report(current_user: Dict[str, Any] = Depends(get_current_user)):
    history = get_history()
    today = datetime.utcnow().date()

    days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    daily_summary = []
    all_emotions = []

    for day in days:
        day_str = day.isoformat()
        day_records = [
            h for h in history if h["date"].startswith(day_str)
        ]

        if not day_records:
            daily_summary.append({
                "date": day_str,
                "emotion": "neutral"
            })
            continue

        emotions = [r["emotion"] for r in day_records]
        dominant_day = Counter(emotions).most_common(1)[0][0]

        daily_summary.append({
            "date": day_str,
            "emotion": dominant_day
        })

        all_emotions.extend(emotions)

    if not all_emotions:
        return {"error": True, "details": "No emotions recorded this week."}

    counts = Counter(all_emotions)
    dominant = counts.most_common(1)[0][0]

    summary = f"Weekly emotion trend: {daily_summary}. Overall counts: {dict(counts)}."

    try:
        ai_text = generate_weekly_insight(summary)

        insight = ""
        suggestion = ""

        lower = ai_text.lower()
        if "suggestion" in lower:
            parts = ai_text.split("Suggestion", 1)
            insight = parts[0].replace("Insight", "").strip(":\n ")
            suggestion = parts[1].strip(":\n ")
        else:
            insight = ai_text.strip()
            suggestion = "Maintain routines that support balance."

        if not insight:
            insight = "Your emotions this week show repeating patterns."
        if not suggestion:
            suggestion = "Maintain routines that support emotional balance."

        return {
            "report": {
                "dominantEmotion": dominant,
                "distribution": dict(counts),
                "weeklyTrend": daily_summary,
                "insight": insight,
                "suggestion": suggestion
            }
        }

    except Exception as e:
        logger.warning(f"Gemini API error for weekly report: {str(e)}")
        return {
            "report": {
                "dominantEmotion": dominant,
                "distribution": dict(counts),
                "weeklyTrend": daily_summary,
                "insight": "Your emotions this week show repeating patterns.",
                "suggestion": "Maintain routines that support balance."
            }
        }
