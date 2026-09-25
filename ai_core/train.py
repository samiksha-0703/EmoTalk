"""
EmoTalk — Custom CNN+LSTM Model Training Script

Trains a Speech Emotion Recognition model on the RAVDESS dataset.

Usage:
    1. Download RAVDESS: https://zenodo.org/record/1188976
    2. Extract to:  ai_core/data/RAVDESS/
       Expected layout:
           data/RAVDESS/Actor_01/03-01-01-01-01-01-01.wav
           data/RAVDESS/Actor_02/...
    3. Run from the ai_core/ directory:
           python train.py

Output files (saved to ai_core/):
    emotion_model.h5     — trained Keras model
    label_encoder.pkl    — fitted sklearn LabelEncoder
"""
import os
import pickle
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

from config import EMOTION_MAP, TEST_SIZE, RANDOM_STATE
from features import extract_features
from model import build_model


# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "data", "RAVDESS")
MODEL_OUT = os.path.join(BASE_DIR, "emotion_model.h5")
ENCODER_OUT = os.path.join(BASE_DIR, "label_encoder.pkl")


# ── Validate dataset path ────────────────────────────────────────────────────
if not os.path.isdir(DATASET_PATH):
    raise FileNotFoundError(
        f"RAVDESS dataset not found at: {DATASET_PATH}\n"
        "Download from: https://zenodo.org/record/1188976\n"
        "Then extract it so the path above exists."
    )


# ── Feature extraction ───────────────────────────────────────────────────────
print("Extracting features from RAVDESS dataset...")
features, labels = [], []
skipped = 0

for actor_dir in sorted(os.listdir(DATASET_PATH)):
    actor_path = os.path.join(DATASET_PATH, actor_dir)
    if not os.path.isdir(actor_path):
        continue

    for filename in os.listdir(actor_path):
        if not filename.endswith(".wav"):
            continue

        # RAVDESS filename format: 03-01-{emotion}-01-01-01-01.wav
        parts = filename.split("-")
        if len(parts) < 3:
            skipped += 1
            continue

        emotion_code = parts[2]
        label = EMOTION_MAP.get(emotion_code)
        if label is None:
            skipped += 1
            continue

        file_path = os.path.join(actor_path, filename)
        try:
            mfcc = extract_features(file_path)
            features.append(mfcc)
            labels.append(label)
        except Exception as e:
            print(f"  ⚠ Skipping {filename}: {e}")
            skipped += 1

print(f"  Loaded {len(features)} samples, skipped {skipped}")
print(f"  Emotion distribution: {dict(Counter(labels))}")

if not features:
    raise RuntimeError("No features extracted. Check your dataset path and file format.")


# ── Prepare tensors ──────────────────────────────────────────────────────────
X = np.array(features)          # shape: (n_samples, N_MFCC)
y = np.array(labels)

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_onehot = to_categorical(y_encoded)

# Add channel dimension for Conv1D: (n_samples, N_MFCC, 1)
X = X[..., np.newaxis]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_onehot,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y_onehot,
)

print(f"\nTraining set: {len(X_train)} samples")
print(f"Test set:     {len(X_test)} samples")
print(f"Classes:      {list(encoder.classes_)}")


# ── Build & train ────────────────────────────────────────────────────────────
model = build_model(
    input_shape=(X_train.shape[1], 1),   # (N_MFCC, 1)
    num_classes=y_train.shape[1],
)
model.summary()

print("\nTraining...")
model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test, y_test),
)


# ── Save outputs ─────────────────────────────────────────────────────────────
model.save(MODEL_OUT)
print(f"\n✅ Model saved → {MODEL_OUT}")

with open(ENCODER_OUT, "wb") as f:
    pickle.dump(encoder, f)
print(f"✅ Label encoder saved → {ENCODER_OUT}")

print(
    "\nNext step: copy these files into backend/models/\n"
    f"  cp {MODEL_OUT} ../backend/models/emotion_model.h5\n"
    f"  cp {ENCODER_OUT} ../backend/models/label_encoder.pkl"
)
