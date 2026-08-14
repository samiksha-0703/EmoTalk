import { NavLink } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="bottom-navbar">
      {/* Home */}
      <NavLink to="/" className="nav-item">
        <svg viewBox="0 0 24 24" className="nav-icon">
          <path d="M3 9.5L12 3l9 6.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z" />
        </svg>
        <span className="label">Home</span>
      </NavLink>

      {/* Reports */}
      <NavLink to="/report" className="nav-item">
        <svg viewBox="0 0 24 24" className="nav-icon">
          <rect x="4" y="3" width="16" height="18" rx="2" />
          <line x1="8" y1="7" x2="16" y2="7" />
          <line x1="8" y1="11" x2="16" y2="11" />
          <line x1="8" y1="15" x2="13" y2="15" />
        </svg>
        <span className="label">Reports</span>
      </NavLink>

      {/* Calendar */}
      <NavLink to="/calendar" className="nav-item">
        <svg viewBox="0 0 24 24" className="nav-icon">
          <rect x="3" y="4" width="18" height="18" rx="2" />
          <line x1="16" y1="2" x2="16" y2="6" />
          <line x1="8" y1="2" x2="8" y2="6" />
          <line x1="3" y1="10" x2="21" y2="10" />
        </svg>
        <span className="label">Calendar</span>
      </NavLink>

      {/* 🔁 Resources  */}
      <NavLink to="/resources" className="nav-item">
        <svg viewBox="0 0 24 24" className="nav-icon">
          <path d="M4 4h12a4 4 0 0 1 4 4v12H8a4 4 0 0 0-4 4z" />
          <path d="M8 4v16" />
        </svg>
        <span className="label">Resources</span>
      </NavLink>
    </nav>
  );
}
