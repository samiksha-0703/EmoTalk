import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getEmotionHistory } from "../services/historyApi";
import "./History.css";

const emotionMap = {
  happy: { y: 6, emoji: "😄" },
  calm: { y: 5, emoji: "😌" },
  neutral: { y: 4, emoji: "😐" },
  surprised: { y: 3, emoji: "😲" },
  sad: { y: 2, emoji: "😢" },
  fearful: { y: 1, emoji: "😨" },
  angry: { y: 0, emoji: "😡" },
};

const getDayPhase = (dateStr) => {
  const h = new Date(dateStr).getHours();
  if (h >= 5 && h < 12) return { label: "Morning", icon: "🌅" };
  if (h >= 12 && h < 17) return { label: "Afternoon", icon: "🌞" };
  if (h >= 17 && h < 21) return { label: "Evening", icon: "🌆" };
  return { label: "Night", icon: "🌙" };
};

export default function HistoryByDate() {
  const { date } = useParams();
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);

  useEffect(() => {
    getEmotionHistory()
      .then((data) => {
        const filtered = data
          .filter(
            (item) =>
              new Date(item.date).toISOString().split("T")[0] === date
          )
          .sort((a, b) => new Date(a.date) - new Date(b.date));

        setRecords(filtered);
      });
  }, [date]);

  return (
    <div className="graph-page">
      <button className="back-btn" onClick={() => navigate(-1)}>
        ← Calendar
      </button>

      <h2>Mood Graph</h2>
      <p className="subtitle">Emotion transitions throughout the day</p>

      {records.length === 0 ? (
        <p className="empty">No emotional records found.</p>
      ) : (
        <div className="graph-container">
          {/* GRAPH */}
          <svg width="100%" height="300" viewBox="0 0 600 300">
            <defs>
              <linearGradient id="moodGradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#6c63ff" />
                <stop offset="50%" stopColor="#42a5f5" />
                <stop offset="100%" stopColor="#26c6da" />
              </linearGradient>
            </defs>

            {/* GRID */}
            {[0, 1, 2, 3, 4, 5, 6].map((lvl) => (
              <line
                key={lvl}
                x1="40"
                x2="580"
                y1={260 - lvl * 35}
                y2={260 - lvl * 35}
                stroke="#eef0ff"
              />
            ))}

            {/* ANIMATED LINE */}
            <polyline
              className="mood-line"
              fill="none"
              stroke="url(#moodGradient)"
              strokeWidth="4"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={records
                .map((item, i) => {
                  const x = 60 + i * (480 / (records.length - 1 || 1));
                  const y = 260 - emotionMap[item.emotion].y * 35;
                  return `${x},${y}`;
                })
                .join(" ")}
            />

            {/* EMOJI POINTS */}
            {records.map((item, i) => {
              const x = 60 + i * (480 / (records.length - 1 || 1));
              const y = 260 - emotionMap[item.emotion].y * 35;
              return (
                <text
                  key={i}
                  x={x}
                  y={y}
                  fontSize="22"
                  textAnchor="middle"
                  className="emoji-point"
                  style={{ animationDelay: `${i * 0.15 + 0.6}s` }}
                >
                  {emotionMap[item.emotion].emoji}
                </text>
              );
            })}
          </svg>

          {/* DAY PHASES */}
          <div className="day-phase-row">
            {records.map((item, i) => {
              const phase = getDayPhase(item.date);
              return (
                <div key={i} className="day-phase">
                  <span className="phase-icon">{phase.icon}</span>
                  <span className="phase-label">{phase.label}</span>
                </div>
              );
            })}
          </div>

          {/* TIME */}
          <div className="time-row">
            {records.map((item, i) => (
              <span key={i}>
                {new Date(item.date).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
