import os
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

from config import EMOTION_MAP, TEST_SIZE
from features import extract_features
from model import build_model

 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "data", "RAVDESS") # change if needed

features, labels = [], []

for actor in os.listdir(DATASET_PATH):
    actor_path = os.path.join(DATASET_PATH, actor)
    for file in os.listdir(actor_path):
        emotion_code = file.split("-")[2]
        label = EMOTION_MAP[emotion_code]

        file_path = os.path.join(actor_path, file)
        mfcc = extract_features(file_path)

        features.append(mfcc)
        labels.append(label)

X = np.array(features)
y = np.array(labels)

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_onehot = to_categorical(y_encoded)

X = X[..., np.newaxis]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_onehot, test_size=TEST_SIZE, random_state=42, stratify=y_onehot
)

model = build_model(
    input_shape=(X_train.shape[1], 1),
    num_classes=y_train.shape[1]
)

model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

model.save("/content/ai_core/emotion_model.h5")

with open("/content/ai_core/label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

labels = []

for file in audio_files:
    labels.append(get_emotion(file))

from collections import Counter
print("Emotion distribution:", Counter(labels))
