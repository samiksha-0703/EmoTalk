"""
HuggingFace Emotion Model Loader

Loads the wav2vec2-based Speech Emotion Recognition model from HuggingFace.
Handles audio conversion via FFmpeg (resolved from PATH or FFMPEG_PATH env var).
"""
import os
import logging
import shutil
import tempfile

import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
from pydub import AudioSegment

logger = logging.getLogger(__name__)


def _resolve_ffmpeg() -> tuple[str | None, str | None]:
    """
    Resolve FFmpeg and FFprobe executables in this order:
      1. FFMPEG_PATH / FFPROBE_PATH environment variables (explicit override)
      2. System PATH (standard installation — `ffmpeg` / `ffprobe` commands)

    Returns:
        (ffmpeg_path, ffprobe_path) — either both found, or both None.
    """
    # 1. Explicit env var override (useful on machines with non-standard installs)
    env_ffmpeg = os.getenv("FFMPEG_PATH")
    env_ffprobe = os.getenv("FFPROBE_PATH")

    if env_ffmpeg and env_ffprobe:
        if os.path.isfile(env_ffmpeg) and os.path.isfile(env_ffprobe):
            logger.info(f"FFmpeg resolved from env vars: {env_ffmpeg}")
            return env_ffmpeg, env_ffprobe
        else:
            logger.warning(
                f"FFMPEG_PATH/FFPROBE_PATH set in env but files not found at:\n"
                f"  ffmpeg  → {env_ffmpeg}\n"
                f"  ffprobe → {env_ffprobe}\n"
                "Falling back to system PATH."
            )

    # 2. System PATH lookup
    ffmpeg_in_path = shutil.which("ffmpeg")
    ffprobe_in_path = shutil.which("ffprobe")

    if ffmpeg_in_path and ffprobe_in_path:
        logger.info(f"FFmpeg resolved from PATH: {ffmpeg_in_path}")
        return ffmpeg_in_path, ffprobe_in_path

    # Neither found
    return None, None


def _configure_pydub() -> bool:
    """
    Point PyDub at the resolved FFmpeg executables.

    Returns:
        True if FFmpeg was found and configured, False otherwise.
    """
    ffmpeg_path, ffprobe_path = _resolve_ffmpeg()

    if ffmpeg_path is None:
        logger.error(
            "FFmpeg not found. Audio conversion will fail.\n"
            "To fix:\n"
            "  • Install FFmpeg and add it to your PATH, OR\n"
            "  • Set FFMPEG_PATH and FFPROBE_PATH in your .env file.\n"
            "  Download: https://ffmpeg.org/download.html"
        )
        return False

    AudioSegment.converter = ffmpeg_path
    AudioSegment.ffprobe   = ffprobe_path
    return True


# Configure PyDub once at module load
_FFMPEG_AVAILABLE = _configure_pydub()


class HuggingFaceEmotionModel:
    """
    Singleton wrapper around the wav2vec2 HuggingFace SER model.

    Usage:
        emotion, confidence = model_loader.predict(audio_path)
    """

    MODEL_NAME = "superb/wav2vec2-base-superb-er"

    def __init__(self):
        logger.info(f"Loading HuggingFace emotion model: {self.MODEL_NAME}")

        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForAudioClassification.from_pretrained(self.MODEL_NAME)
        self.labels = self.model.config.id2label
        self.is_loaded = True

        logger.info("✅ HuggingFace emotion model loaded successfully")

    def load_model(self):
        """Compatibility shim — model is loaded in __init__."""
        return True, None

    def _load_audio(self, audio_path: str, target_sr: int = 16000):
        """
        Load any audio format as mono 16 kHz using PyDub → FFmpeg → librosa.

        Raises:
            FileNotFoundError: If the audio file does not exist.
            RuntimeError: If FFmpeg is unavailable or conversion fails.
        """
        if not os.path.isfile(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if not _FFMPEG_AVAILABLE:
            raise RuntimeError(
                "FFmpeg is not available. Cannot convert audio.\n"
                "Install FFmpeg or set FFMPEG_PATH / FFPROBE_PATH in your .env file."
            )

        try:
            audio = AudioSegment.from_file(audio_path)
            audio = audio.set_channels(1).set_frame_rate(target_sr)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio.export(tmp.name, format="wav")
                tmp_path = tmp.name

            try:
                y, sr = librosa.load(tmp_path, sr=target_sr)
            finally:
                os.remove(tmp_path)

            return y, sr

        except (FileNotFoundError, RuntimeError):
            raise
        except Exception as exc:
            raise RuntimeError(f"Failed to load audio '{audio_path}': {exc}") from exc

    def predict(self, audio_path: str) -> tuple[str, float]:
        """
        Predict the emotion in an audio file.

        Args:
            audio_path: Path to the audio file (any FFmpeg-supported format).

        Returns:
            (emotion_label, confidence) where confidence is in [0, 1].
        """
        audio, sr = self._load_audio(audio_path)

        inputs = self.feature_extractor(
            audio,
            sampling_rate=sr,
            return_tensors="pt",
            padding=True,
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_id = torch.argmax(logits).item()
        emotion = self.labels[predicted_id]
        confidence = torch.softmax(logits, dim=1)[0][predicted_id].item()

        return emotion, confidence


# Global singleton — imported by routes and health check
model_loader = HuggingFaceEmotionModel()
