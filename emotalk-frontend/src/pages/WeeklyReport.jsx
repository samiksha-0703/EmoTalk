import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getWeeklyReport } from "../services/historyApi";
import "./WeeklyReport.css";

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

const emotionLevel = {
  angry: 0,
  fearful: 1,
  sad: 2,
  neutral: 3,
  surprised: 4,
  calm: 5,
  happy: 6,
};

export default function WeeklyReport() {
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const generateWeeklyReport = async () => {
    setLoading(true);
    setMessage("Generating your weekly report…");
    setReport(null);

    try {
      const data = await getWeeklyReport();

      if (data.error || !data.report) {
        setMessage("⚠️ Unable to generate weekly report.");
        return;
      }

      setReport(data.report);
      setMessage("✅ Your weekly report is ready");
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Backend not connected");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weekly-report-page">
      <h2>Weekly Emotional Report</h2>
      <p className="weekly-report-subtitle">
        Emotional patterns from the last 7 days
      </p>

      <button
        className="generate-btn"
        onClick={generateWeeklyReport}
        disabled={loading}
      >
        {loading ? "Generating…" : "Generate Weekly Report"}
      </button>

      {message && <p className="status">{message}</p>}

      {report && (
        <>
          {/* SUMMARY */}
          <div className="weekly-summary-card">
            <div className="weekly-dominant">
              <span className="emoji">
                {emotionEmojiMap[report.dominantEmotion] || "🙂"}
              </span>
              <div className="emotion-name">
                {report.dominantEmotion}
              </div>
            </div>

            <div className="weekly-distribution">
              <h4>Emotion Distribution</h4>
              <div className="distribution-list">
                {Object.entries(report.distribution).map(([emo, count]) => (
                  <div key={emo} className="distribution-item">
                    {emotionEmojiMap[emo] || "🙂"}
                    <br />
                    {emo}: {count}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 📈 WEEKLY EMOTION GRAPH */}
          <div className="weekly-graph-card">
            <h4>Weekly Emotion Trend</h4>

            <svg width="100%" height="240" viewBox="0 0 700 240">
              {/* GRID */}
              {[0, 1, 2, 3, 4, 5, 6].map((lvl) => (
                <line
                  key={lvl}
                  x1="40"
                  x2="660"
                  y1={200 - lvl * 25}
                  y2={200 - lvl * 25}
                  stroke="#eef0ff"
                />
              ))}

              {/* LINE */}
              <polyline
                fill="none"
                stroke="#6366f1"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={report.weeklyTrend
                  .map((d, i) => {
                    const x = 60 + i * (560 / 6);
                    const y = 200 - emotionLevel[d.emotion] * 25;
                    return `${x},${y}`;
                  })
                  .join(" ")}
              />

              {/* EMOJIS */}
              {report.weeklyTrend.map((d, i) => {
                const x = 60 + i * (560 / 6);
                const y = 200 - emotionLevel[d.emotion] * 25;
                return (
                  <text
                    key={i}
                    x={x}
                    y={y}
                    fontSize="22"
                    textAnchor="middle"
                  >
                    {emotionEmojiMap[d.emotion] || "🙂"}
                  </text>
                );
              })}
            </svg>

            {/* DAY LABELS */}
            <div className="weekly-day-row">
              {report.weeklyTrend.map((d, i) => (
                <span key={i}>
                  {new Date(d.date).toLocaleDateString("en-US", {
                    weekday: "short",
                  })}
                </span>
              ))}
            </div>
          </div>

          {/* INSIGHT */}
          <div className="weekly-info-card">
            <h4>🧠 Weekly Insight</h4>
            <p>{report.insight}</p>
          </div>

          {/* SUGGESTION */}
          <div className="weekly-info-card">
            <h4>💡 Weekly Suggestion</h4>
            <p>{report.suggestion}</p>
          </div>

          {/* NAVIGATION */}
          <div
            className="weekly-back-btn"
            onClick={() => navigate("/report")}
          >
            ← Back to Daily Report
          </div>
        </>
      )}
    </div>
  );
}
