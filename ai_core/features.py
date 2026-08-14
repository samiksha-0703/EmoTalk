import librosa
import numpy as np
from config import SAMPLE_RATE, DURATION, N_MFCC

def extract_features(file_path):
    audio, sr = librosa.load(
        file_path,
        sr=SAMPLE_RATE,
        duration=DURATION,
        res_type="kaiser_fast",
        backend="audioread"   
    )

    if len(audio) < sr * DURATION:
        audio = np.pad(audio, (0, sr * DURATION - len(audio)))
    else:
        audio = audio[: sr * DURATION]

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=N_MFCC
    )

    return np.mean(mfcc.T, axis=0)
