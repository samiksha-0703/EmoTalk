"""
Prediction Service — Custom CNN+LSTM Feature Pipeline
------------------------------------------------------
NOTE: This file is the feature extraction reference for the custom
      CNN+LSTM model (ai_core/). It is NOT used when MODEL_TYPE=huggingface
      (the default). Switch to MODEL_TYPE=custom in .env to activate it.

This pipeline extracts MFCC + RMS time-series features shaped (130, 41)
which is the input format for the more detailed backend model variant.
The simpler training pipeline in ai_core/features.py uses mean-MFCC (40,).

TODO: Add support for real-time streaming prediction
TODO: Add audio quality validation
"""
import logging
import librosa
import numpy as np
import os

from app.core.config import SAMPLE_RATE, DURATION, N_MFCC, MAX_PAD_LEN
from app.core.model_loader import model_loader  # custom TF loader

logger = logging.getLogger(__name__)


# =========================
# FEATURE EXTRACTION (MFCC + RMS)
# =========================
def extract_features_from_file(file_path: str) -> np.ndarray:
    """
    Extract features from audio file.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Feature array with shape (1, MAX_PAD_LEN, 41)
        Features: 40 MFCC coefficients + 1 RMS energy
        
    Raises:
        Exception: If audio file cannot be processed
    """
    try:
        # Load audio file
        audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)
        
        # Process audio chunk
        return extract_features_from_chunk(audio, sr)
        
    except Exception as e:
        logger.error(f"Error extracting features from {file_path}: {str(e)}")
        raise


def extract_features_from_chunk(chunk: np.ndarray, sr: int) -> np.ndarray:
    """
    Extract MFCC and RMS features from audio chunk.
    
    This function matches the feature extraction used during model training.
    Any changes here must be reflected in the training pipeline.
    
    Args:
        chunk: Audio signal array
        sr: Sample rate
        
    Returns:
        Feature array with shape (1, MAX_PAD_LEN, 41)
    """
    # 1️⃣ Pad/trim to fixed duration
    max_len = int(sr * DURATION)
    if len(chunk) < max_len:
        chunk = np.pad(chunk, (0, max_len - len(chunk)), mode="constant")
    else:
        chunk = chunk[:max_len]
    
    # 2️⃣ Trim silence (removes leading/trailing silence)
    chunk, _ = librosa.effects.trim(chunk, top_db=20)
    
    # Re-pad after trimming to maintain duration
    if len(chunk) < max_len:
        chunk = np.pad(chunk, (0, max_len - len(chunk)), mode="constant")
    
    # 3️⃣ Normalize audio (scale to [-1, 1])
    chunk = librosa.util.normalize(chunk)
    
    # 4️⃣ Extract MFCC features (40 coefficients)
    mfcc = librosa.feature.mfcc(
        y=chunk,
        sr=sr,
        n_mfcc=N_MFCC,
        n_fft=2048,
        hop_length=512
    )
    mfcc = mfcc.T  # Transpose to (time_frames, 40)
    
    # Pad/trim MFCC to fixed length
    if mfcc.shape[0] < MAX_PAD_LEN:
        mfcc = np.pad(
            mfcc,
            ((0, MAX_PAD_LEN - mfcc.shape[0]), (0, 0)),
            mode="constant"
        )
    else:
        mfcc = mfcc[:MAX_PAD_LEN, :]
    
    # 5️⃣ Extract RMS energy (root mean square)
    rms = librosa.feature.rms(y=chunk, frame_length=2048, hop_length=512)[0]
    
    # Pad/trim RMS to match MFCC length
    if len(rms) < MAX_PAD_LEN:
        rms = np.pad(
            rms,
            (0, MAX_PAD_LEN - len(rms)),
            mode="constant"
        )
    else:
        rms = rms[:MAX_PAD_LEN]
    
    # 6️⃣ Combine features → (MAX_PAD_LEN, 41)
    features = np.hstack([mfcc, rms.reshape(-1, 1)])
    
    # 7️⃣ Add batch dimension → (1, MAX_PAD_LEN, 41)
    features = np.expand_dims(features, axis=0)
    
    return features


# =========================
# LONG AUDIO PREDICTION (Future Feature)
# =========================
def predict_long_audio(audio_path: str) -> list:
    """
    Predict emotions for long audio files by segmenting.
    
    This function processes audio in chunks and returns a timeline
    of emotions throughout the recording.
    
    TODO: This feature is not currently used but kept for future implementation.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        List of emotion predictions with timestamps
    """
    if not model_loader.is_loaded:
        raise RuntimeError("Model not loaded")
    
    try:
        audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        model = model_loader.model
        encoder = model_loader.encoder
        
        window_size = int(DURATION * sr)
        step_size = window_size
        timeline = []
        
        for i, start in enumerate(range(0, len(audio) - window_size + 1, step_size)):
            chunk = audio[start:start + window_size]
            features = extract_features_from_chunk(chunk, sr)
            
            probs = model.predict(features, verbose=0)[0]
            idx = np.argmax(probs)
            emotion = encoder.inverse_transform([idx])[0]
            confidence = float(probs[idx])
            
            timeline.append({
                "segment": i + 1,
                "start_sec": round(start / sr, 2),
                "end_sec": round((start + window_size) / sr, 2),
                "emotion": emotion,
                "confidence": round(confidence, 3)
            })
        
        return timeline
        
    except Exception as e:
        logger.error(f"Error predicting long audio: {str(e)}")
        raise
    finally:
        # Clean up temp file if it exists
        if os.path.exists(audio_path) and audio_path.startswith("/tmp"):
            try:
                os.remove(audio_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {e}")
