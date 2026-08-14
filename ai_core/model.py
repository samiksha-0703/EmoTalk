from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout

def build_model(input_shape, num_classes):
    model = Sequential([
        Conv1D(128, 5, activation="relu", padding="same", input_shape=input_shape),
        MaxPooling1D(2),
        Dropout(0.2),

        Conv1D(256, 5, activation="relu", padding="same"),
        MaxPooling1D(2),
        Dropout(0.2),

        LSTM(128),
        Dropout(0.3),

        Dense(128, activation="relu"),
        Dropout(0.3),

        Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model
