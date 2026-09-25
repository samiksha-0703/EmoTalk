import { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ ADD
import { getDailyReport } from "../services/historyApi";
import "./Report.css";

const emotionConfig = {
  happy: { emoji: "😄", color: "#22c55e" },
  calm: { emoji: "😌", color: "#06b6d4" },
  neutral: { emoji: "😐", color: "#9ca3af" },
  surprised: { emoji: "😲", color: "#f59e0b" },
  sad: { emoji: "😢", color: "#3b82f6" },
  fearful: { emoji: "😨", color: "#8b5cf6" },
  angry: { emoji: "😡", color: "#ef4444" },
  disgust: { emoji: "🤢", color: "#10b981" },
};

export default function Report() {
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [message, setMessage] = useState("");

  const navigate = useNavigate(); // ✅ ADD

  const generateReport = async () => {
    setLoading(true);
    setReport(null);
    setMessage("Generating your daily report…");

    try {
      const data = await getDailyReport();

      if (data.error || !data.report) {
        setMessage("⚠️ Unable to generate report right now.");
        return;
      }

      setReport(data.report);
      setMessage("✅ Your daily report is ready");
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Unable to generate report right now.");
    } finally {
      setLoading(false);
    }
  };

  const emotion = report?.dominantEmotion || "neutral";
  const { emoji, color } =
    emotionConfig[emotion] || emotionConfig.neutral;

  return (
    <div className="daily-report-page">
      <h2>Daily Emotional Report</h2>
      <p className="subtitle">
        A personalized summary of today’s emotional patterns
      </p>

      <button
        className="generate-btn"
        onClick={generateReport}
        disabled={loading}
      >
        {loading ? "Generating…" : "Generate Daily Report"}
      </button>

      {message && <p className="status">{message}</p>}

      {report && (
        <div className="report-card fade-in">
          {/* DOMINANT EMOTION */}
          <div
            className="emotion-card"
            style={{ borderLeft: `6px solid ${color}` }}
          >
            <span className="emotion-emoji">{emoji}</span>
            <div>
              <h4>Dominant Emotion</h4>
              <p className="emotion-name" style={{ color }}>
                {emotion}
              </p>
            </div>
          </div>

          {/* INSIGHT */}
          <div className="info-card insight">
            <h4>🧠 Emotional Insight</h4>
            <p>{report.insight}</p>
          </div>

          {/* SUGGESTION */}
          <div className="info-card suggestion">
            <h4>💡 Recommended Action</h4>
            <p>{report.suggestion}</p>
          </div>

          {/* ✅ WEEKLY REPORT BUTTON */}
          <button
            className="weekly-btn"
            onClick={() => navigate("/weekly-report")}
          >
            View Weekly Report →
          </button>
        </div>
      )}
    </div>
  );
}
