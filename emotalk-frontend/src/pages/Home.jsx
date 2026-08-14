import { useState, useEffect } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import { predictEmotion } from "../services/emotionApi";
import "./Home.css";

/* 🔥 Emotion → Emoji mapping */
const emotionEmojiMap = {
  happy: "😄",
  calm: "😌",
  neutral: "😐",
  surprised: "😲",
  sad: "😢",
  fearful: "😨",
  angry: "😡",
  disgust: "🤢",
};

const emotionColors = {
  happy: "#FCD34D",
  calm: "#60A5FA",
  neutral: "#9CA3AF",
  surprised: "#FB923C",
  sad: "#3B82F6",
  fearful: "#A78BFA",
  angry: "#F87171",
  disgust: "#84CC16",
};

export default function Home() {
  const [emotion, setEmotion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recordingDuration, setRecordingDuration] = useState(0);

  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  } = useReactMediaRecorder({ audio: true });

  // Recording duration timer
  useEffect(() => {
    let interval = null;
    if (status === "recording") {
      interval = setInterval(() => {
        setRecordingDuration((prev) => prev + 1);
      }, 1000);
    } else {
      setRecordingDuration(0);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [status]);

  const handleMicClick = () => {
    if (status === "recording") {
      stopRecording();
    } else {
      setEmotion(null);
      setError(null);
      setRecordingDuration(0);
      startRecording();
    }
  };

  const handleAnalyze = async () => {
    if (!mediaBlobUrl) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await predictEmotion(mediaBlobUrl);
      setEmotion(result);
    } catch (err) {
      const errorMessage = err.message || "Failed to analyze emotion. Please try again.";
      setError(errorMessage);
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="home-page">
      {/* Header */}
      <div className="home-title">
        <h1>EmoTalk</h1>
        <p>How are you feeling today?</p>
      </div>

      {/* Center Content */}
      <div className="center-content">
        <p className="instruction-text">
          Press the microphone to start recording your voice journal entry.
          Share your thoughts, feelings, and experiences.
        </p>

        {/* MIC BUTTON */}
        <div className="mic-container">
          <button
            className={`mic-circle ${status === "recording" ? "recording" : ""} ${
              emotion ? "has-result" : ""
            }`}
            style={{
              backgroundColor: emotion
                ? emotionColors[emotion.emotion] || "#10b981"
                : undefined,
            }}
            onClick={handleMicClick}
            disabled={loading}
            aria-label={status === "recording" ? "Stop recording" : "Start recording"}
          >
            {status === "recording" ? (
              <div className="pulse-ring"></div>
            ) : emotion ? (
              <div className="emotion-emoji-large">
                {emotionEmojiMap[emotion.emotion] || "🙂"}
              </div>
            ) : (
              <svg
                width="36"
                height="36"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" y1="19" x2="12" y2="23" />
                <line x1="8" y1="23" x2="16" y2="23" />
              </svg>
            )}
          </button>

          {/* Recording Duration */}
          {status === "recording" && (
            <div className="recording-info">
              <div className="recording-duration">{formatDuration(recordingDuration)}</div>
              <div className="recording-waveform">
                {[...Array(20)].map((_, i) => (
                  <div
                    key={i}
                    className="wave-bar"
                    style={{
                      animationDelay: `${i * 0.1}s`,
                    }}
                  />
                ))}
              </div>
            </div>
          )}
        </div>

        <p className="tap-text">
          {status === "recording"
            ? "Tap to stop recording"
            : emotion
            ? "Tap to record again"
            : "Tap to start recording"}
        </p>

        {/* Audio Player & Analyze Button */}
        {mediaBlobUrl && !loading && (
          <div className="audio-section">
            <audio src={mediaBlobUrl} controls className="audio-player" />
            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={loading}
            >
              Analyze Emotion
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p className="loading-text">Analyzing your emotions...</p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="error-message" role="alert">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
            <button
              className="error-dismiss"
              onClick={() => setError(null)}
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        )}

        {/* 🌈 EMOTION RESULT */}
        {emotion && !loading && (
          <div
            className="emotion-result"
            style={{
              borderColor: emotionColors[emotion.emotion] || "#10b981",
            }}
          >
            <div className="emotion-emoji">
              {emotionEmojiMap[emotion.emotion] || "🙂"}
            </div>

            <div className="emotion-name">{emotion.emotion}</div>

            <div className="emotion-confidence">
              {(emotion.confidence * 100).toFixed(1)}% confidence
            </div>

            {/* Confidence Bar */}
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{
                  width: `${emotion.confidence * 100}%`,
                  backgroundColor: emotionColors[emotion.emotion] || "#10b981",
                }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
