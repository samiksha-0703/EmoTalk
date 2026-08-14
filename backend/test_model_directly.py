import numpy as np
from app.core.model_loader import model, label_encoder

# Create RANDOM VALID INPUT with correct shape
fake_input = np.random.randn(1, 130, 120)

probs = model.predict(fake_input)[0]

print("Random input prediction:")
for emo, p in zip(label_encoder.classes_, probs):
    print(emo, round(float(p), 4))
