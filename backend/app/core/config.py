"""
Configuration settings for the EmoTalk backend.

This module centralizes all configuration values including:
- Model paths and audio processing parameters
- API settings
- Database configuration
- Environment-specific settings
"""
import os
import secrets
import logging
from pathlib import Path

from dotenv import load_dotenv

_logger = logging.getLogger(__name__)

# Base directory: backend/
BASE_DIR = Path(__file__).parent.parent.parent

# Load environment variables from backend/.env (local only, never committed).
# Values already present in the real environment take precedence over the file.
load_dotenv(BASE_DIR / ".env")

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

# CORS: allowed frontend origins.
# In production set CORS_ORIGINS as a comma-separated list in .env, e.g.:
#   CORS_ORIGINS=https://emotalk.yourdomain.com,https://www.emotalk.yourdomain.com
_cors_env = os.getenv("CORS_ORIGINS")
if _cors_env:
    CORS_ORIGINS = [origin.strip() for origin in _cors_env.split(",") if origin.strip()]
else:
    # Development defaults — Vite dev server
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:3000",
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
# MODEL SELECTION
# =========================
# Set MODEL_TYPE=custom in .env to use your locally-trained CNN+LSTM model.
# Set MODEL_TYPE=huggingface (default) to use wav2vec2 from HuggingFace.
# Note: 'custom' requires emotion_model.h5 + label_encoder.pkl in backend/models/
MODEL_TYPE = os.getenv("MODEL_TYPE", "huggingface").lower()

# =========================
# GEMINI API CONFIG
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "models/gemini-2.5-flash"

# =========================
# AUTH / JWT CONFIG
# =========================
_raw_jwt_secret = os.getenv("JWT_SECRET_KEY")

if _raw_jwt_secret:
    JWT_SECRET_KEY = _raw_jwt_secret
else:
    # No secret configured — generate a random one for this run.
    # IMPORTANT: tokens will be invalidated every time the server restarts.
    # Set JWT_SECRET_KEY in your .env file for persistent sessions.
    JWT_SECRET_KEY = secrets.token_hex(32)
    _logger.warning(
        "JWT_SECRET_KEY is not set in .env. "
        "A random key has been generated — all sessions will be lost on server restart. "
        "Add JWT_SECRET_KEY to backend/.env to fix this."
    )

JWT_ALGORITHM = "HS256"
# Token validity period in minutes (default 1 day)
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
