import { useState } from "react";

function toDateKey(iso) {
  return iso.split("T")[0]; // YYYY-MM-DD
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString();
}

export default function CalendarView({ history }) {
  const [selectedDate, setSelectedDate] = useState(null);

  // group history by date
  const byDate = history.reduce((acc, item) => {
    const key = toDateKey(item.date);
    acc[key] = acc[key] || [];
    acc[key].push(item);
    return acc;
  }, {});

  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const selectedEntries = selectedDate ? byDate[selectedDate] || [] : [];

  return (
    <>
      {/* Calendar Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, 1fr)",
          gap: 10,
        }}
      >
        {[...Array(daysInMonth)].map((_, i) => {
          const day = i + 1;
          const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(
            day
          ).padStart(2, "0")}`;

          const hasEntry = Boolean(byDate[dateKey]);

          return (
            <div
              key={dateKey}
              onClick={() => hasEntry && setSelectedDate(dateKey)}
              style={{
                height: 70,
                border: "1px solid #ccc",
                borderRadius: 8,
                padding: 6,
                cursor: hasEntry ? "pointer" : "default",
                background:
                  selectedDate === dateKey ? "#eef6ff" : "white",
                position: "relative",
              }}
            >
              <div>{day}</div>

              {hasEntry && (
                <span
                  style={{
                    width: 10,
                    height: 10,
                    background: "green",
                    borderRadius: "50%",
                    position: "absolute",
                    bottom: 6,
                    right: 6,
                  }}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Details Panel */}
      {selectedDate && (
        <div style={{ marginTop: 30 }}>
          <h3>Emotions on {selectedDate}</h3>

          {selectedEntries.map((item, index) => (
            <div
              key={index}
              style={{
                padding: 10,
                border: "1px solid #ddd",
                borderRadius: 6,
                marginBottom: 10,
              }}
            >
              <strong>Emotion:</strong> {item.emotion} <br />
              <strong>Confidence:</strong>{" "}
              {(item.confidence * 100).toFixed(2)}% <br />
              <strong>Time:</strong> {formatTime(item.date)}
            </div>
          ))}
        </div>
      )}
    </>
  );
}
