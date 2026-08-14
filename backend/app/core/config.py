"""
Configuration settings for the EmoTalk backend.

This module centralizes all configuration values including:
- Model paths and audio processing parameters
- API settings
- Database configuration
- Environment-specific settings

TODO: Move sensitive values (like API keys) to environment variables in production.
"""
import os
from pathlib import Path

# Base directory: backend/
BASE_DIR = Path(__file__).parent.parent.parent

# =========================
# MODEL CONFIGURATION
# =========================
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "emotion_model.h5"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

# =========================
# AUDIO PROCESSING CONFIG
# =========================
SAMPLE_RATE = 22050  # Standard sample rate for speech processing
DURATION = 3.0  # Maximum audio duration in seconds
N_MFCC = 40  # Number of MFCC coefficients
MAX_PAD_LEN = 130  # Maximum sequence length for padding/trimming

# =========================
# API CONFIGURATION
# =========================
API_V1_PREFIX = "/api/v1"  # API version prefix for future compatibility

# CORS: In production, replace with specific frontend URL
# TODO: Move to environment variable for production
CORS_ORIGINS = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
    "http://127.0.0.1:5173",
]

# =========================
# DATABASE CONFIG
# =========================
DB_PATH = BASE_DIR / "emotion_history.db"

# =========================
# FILE UPLOAD CONFIG
# =========================
MAX_FILE_SIZE_MB = 10  # Maximum audio file size in MB
ALLOWED_AUDIO_TYPES = [
    "audio/wav",
    "audio/webm",
    "audio/mpeg",
    "audio/mp3",
    "audio/x-m4a",
]

# =========================
# GEMINI API CONFIG
# =========================
# TODO: Load from environment variable in production
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "models/gemini-2.5-flash"

# =========================
# AUTH / JWT CONFIG
# =========================
# Secret for signing JWT tokens. In production this should come from a
# secure environment variable and be rotated periodically.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
JWT_ALGORITHM = "HS256"
# Token validity period in minutes (default 1 day)
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
