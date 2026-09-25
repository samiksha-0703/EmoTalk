"""
Custom TensorFlow Model Loader

Loads the locally-trained CNN+LSTM emotion recognition model (emotion_model.h5)
and its LabelEncoder (label_encoder.pkl) from backend/models/.

This module mirrors the interface of hf_model_loader.py so that routes.py
can swap between them without any changes — just set MODEL_TYPE in .env.
"""
import logging
import pickle

import librosa
import numpy as np

from app.core.config import MODEL_PATH, ENCODER_PATH, SAMPLE_RATE, DURATION, N_MFCC

logger = logging.getLogger(__name__)


class CustomEmotionModel:
    """
    Singleton wrapper around the locally-trained TF/Keras SER model.

    Usage:
        emotion, confidence = model_loader.predict(audio_path)
    """

    def __init__(self):
        self.model = None
        self.encoder = None
        self.is_loaded = False
        self._load()

    def _load(self):
        """Load the .h5 model and .pkl label encoder from backend/models/."""
        # Lazy import — only pull in TensorFlow if this loader is actually used
        try:
            from tensorflow.keras.models import load_model as keras_load_model
        except ImportError:
            logger.error(
                "TensorFlow is not installed. "
                "Install it with: pip install tensorflow"
            )
            return

        if not MODEL_PATH.exists():
            logger.error(
                f"Custom model file not found: {MODEL_PATH}\n"
                "To fix:\n"
                "  1. Run ai_core/train.py to train the model, OR\n"
                "  2. Copy emotion_model.h5 into backend/models/\n"
                "  Alternatively, set MODEL_TYPE=huggingface in your .env"
            )
            return

        if not ENCODER_PATH.exists():
            logger.error(
                f"Label encoder file not found: {ENCODER_PATH}\n"
                "To fix:\n"
                "  1. Run ai_core/train.py — it saves label_encoder.pkl, OR\n"
                "  2. Copy label_encoder.pkl into backend/models/"
            )
            return

        try:
            self.model = keras_load_model(str(MODEL_PATH))
            logger.info(f"✅ Custom model loaded from {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load model from {MODEL_PATH}: {e}")
            return

        try:
            with open(ENCODER_PATH, "rb") as f:
                self.encoder = pickle.load(f)
            logger.info(f"✅ Label encoder loaded from {ENCODER_PATH}")
        except Exception as e:
            logger.error(f"Failed to load label encoder from {ENCODER_PATH}: {e}")
            self.model = None
            return

        self.is_loaded = True
        logger.info("✅ Custom CNN+LSTM emotion model ready")

    def load_model(self):
        """Compatibility shim — loading happens in __init__."""
        return self.is_loaded, None if self.is_loaded else "Model not loaded"

    def _extract_features(self, audio_path: str) -> np.ndarray:
        """
        Extract mean-MFCC features matching the training pipeline.

        Output shape: (1, N_MFCC, 1) = (1, 40, 1) — batch + channel dims
        for the Conv1D input layer.
        """
        audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE, duration=DURATION)

        target_length = int(sr * DURATION)
        if len(audio) < target_length:
            audio = np.pad(audio, (0, target_length - len(audio)), mode="constant")
        else:
            audio = audio[:target_length]

        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
        features = np.mean(mfcc.T, axis=0)       # shape: (40,)
        features = features[np.newaxis, :, np.newaxis]  # shape: (1, 40, 1)
        return features

    def predict(self, audio_path: str) -> tuple[str, float]:
        """
        Predict the emotion in an audio file.

        Args:
            audio_path: Path to the audio file (.wav).

        Returns:
            (emotion_label, confidence) where confidence is in [0, 1].

        Raises:
            RuntimeError: If the model is not loaded.
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Custom model is not loaded. "
                "Check backend/models/ for emotion_model.h5 and label_encoder.pkl."
            )

        features = self._extract_features(audio_path)
        probs = self.model.predict(features, verbose=0)[0]   # shape: (num_classes,)
        idx = int(np.argmax(probs))
        emotion = self.encoder.inverse_transform([idx])[0]
        confidence = float(probs[idx])

        return emotion, confidence


# Global singleton — imported by routes when MODEL_TYPE=custom
model_loader = CustomEmotionModel()
