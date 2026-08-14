import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Calendar.css";

export default function Calendar() {
  const navigate = useNavigate();

  const [currentDate, setCurrentDate] = useState(new Date());
  const [entriesByDate, setEntriesByDate] = useState({});

  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // ================= FETCH EMOTION HISTORY =================
  useEffect(() => {
    fetch("http://127.0.0.1:8000/emotion-history")
      .then((res) => res.json())
      .then((data) => {
        const map = {};

        data.forEach((item) => {
          //  date to YYYY-MM-DD
          const normalizedDate = new Date(item.date)
            .toISOString()
            .split("T")[0];

          map[normalizedDate] = true;
        });

        console.log("📅 Calendar entries:", map);
        setEntriesByDate(map);
      })
      .catch((err) => {
        console.error("Failed to load emotion history", err);
      });
  }, []);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const monthName = currentDate.toLocaleString("default", {
    month: "long",
  });

  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const handlePrevMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1));
  };

  // ================= RENDER DATES =================
  const renderDates = () => {
    const cells = [];

    // Empty cells
    for (let i = 0; i < firstDayOfMonth; i++) {
      cells.push(<div key={`empty-${i}`} />);
    }

    // Actual days
    for (let day = 1; day <= daysInMonth; day++) {
      const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(
        day
      ).padStart(2, "0")}`;

      const hasEntry = entriesByDate[dateKey];

      cells.push(
        <div
          key={day}
          className={`date-cell ${hasEntry ? "clickable" : ""}`}
          onClick={() => hasEntry && navigate(`/history/${dateKey}`)}
        >
          <span className="date-number">{day}</span>
          {hasEntry && <span className="dot" />}
        </div>
      );
    }

    return cells;
  };

  return (
    <div className="calendar-page">
      <div className="calendar-header">
        <h2>Your Journey</h2>
        <p>Track your emotional well-being over time</p>
      </div>

      <div className="calendar-card">
        <div className="month-row">
          <button className="nav-btn" onClick={handlePrevMonth}>
            ‹
          </button>

          <h3>
            {monthName} {year}
          </h3>

          <button className="nav-btn" onClick={handleNextMonth}>
            ›
          </button>
        </div>

        <div className="weekdays">
          {days.map((day) => (
            <span key={day}>{day}</span>
          ))}
        </div>

        <div className="dates-grid">{renderDates()}</div>
      </div>

      <div className="legend">
        <span className="legend-dot" />
        <span>Day with entry</span>
      </div>
    </div>
  );
}
