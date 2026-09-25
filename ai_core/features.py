"""
Feature extraction for the EmoTalk custom CNN+LSTM model.

Extracts a mean-MFCC vector of shape (N_MFCC,) = (40,) per audio file.
This shape must match what the model was trained on — do NOT change
without re-training the model.
"""
import numpy as np
import librosa

from config import SAMPLE_RATE, DURATION, N_MFCC


def extract_features(file_path: str) -> np.ndarray:
    """
    Load an audio file and return a mean-MFCC feature vector.

    Args:
        file_path: Path to a .wav audio file.

    Returns:
        np.ndarray of shape (N_MFCC,) = (40,) — the mean of MFCC
        coefficients across time frames.

    Raises:
        Exception: If the file cannot be loaded or processed.
    """
    # Load audio — fixed duration, standard sample rate
    # Note: 'backend' / 'res_type' args removed — librosa >= 0.10 uses
    # sndfile by default which is faster and doesn't need those kwargs.
    audio, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Pad if shorter than target duration, trim if longer
    target_length = int(sr * DURATION)
    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), mode="constant")
    else:
        audio = audio[:target_length]

    # Extract MFCC and average across time → shape (N_MFCC,)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    return np.mean(mfcc.T, axis=0)   # shape: (40,)
