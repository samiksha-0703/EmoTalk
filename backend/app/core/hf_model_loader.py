import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
from pydub import AudioSegment
import tempfile
import os

# 🔹 Set your FFmpeg and FFprobe paths here
FFMPEG_PATH = r"C:\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg-8.0.1-full_build\bin\ffprobe.exe"

# Make PyDub aware of the executables
AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH

class HuggingFaceEmotionModel:

    def __init__(self):
        self.model_name = "superb/wav2vec2-base-superb-er"
        print("Loading HuggingFace emotion model...")

        # Load HuggingFace feature extractor and model
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        self.model = AutoModelForAudioClassification.from_pretrained(self.model_name)
        self.labels = self.model.config.id2label

        # Track if model is ready
        self.is_loaded = True
        print("Model loaded successfully")

    def load_model(self):
        # Compatibility method if needed elsewhere
        return True, None

    def _load_audio(self, audio_path, target_sr=16000):
        """
        Load audio safely using PyDub → FFmpeg → librosa.
        Converts audio to mono 16kHz WAV.
        """
        if not os.path.isfile(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            # Load via PyDub (handles almost any format via FFmpeg)
            audio = AudioSegment.from_file(audio_path)
            audio = audio.set_channels(1).set_frame_rate(target_sr)

            # Export to a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
                audio.export(tmp_wav.name, format="wav")
                tmp_path = tmp_wav.name

            # Load WAV into librosa
            y, sr = librosa.load(tmp_path, sr=target_sr)
            # Cleanup temp file
            os.remove(tmp_path)
            return y, sr
        except Exception as e:
            raise RuntimeError(f"Failed to load audio via FFmpeg: {e}")

    def predict(self, audio_path):
        # Load audio
        audio, sr = self._load_audio(audio_path)

        # Prepare model input
        inputs = self.feature_extractor(
            audio,
            sampling_rate=sr,
            return_tensors="pt",
            padding=True
        )

        # Model prediction
        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_id = torch.argmax(logits).item()
        emotion = self.labels[predicted_id]
        confidence = torch.softmax(logits, dim=1)[0][predicted_id].item()

        return emotion, confidence

# 🔹 Create a global instance for your routes
model_loader = HuggingFaceEmotionModel()
