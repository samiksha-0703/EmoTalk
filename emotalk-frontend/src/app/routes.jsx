import { Routes, Route, Navigate } from "react-router-dom";
import Login from "../auth/Login";
import Signup from "../auth/Signup";
import Home from "../pages/Home";
import Calendar from "../pages/Calendar";
import Report from "../pages/Report";
import WeeklyReport from "../pages/WeeklyReport"; // ✅ ADD
import ProtectedRoute from "./ProtectedRoute";
import Resources from "../pages/Resources";
import EmotionHistoryDay from "../pages/EmotionHistoryDay";

export default function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />

      <Route
        path="/calendar"
        element={
          <ProtectedRoute>
            <Calendar />
          </ProtectedRoute>
        }
      />

      <Route
        path="/report"
        element={
          <ProtectedRoute>
            <Report />
          </ProtectedRoute>
        }
      />

      {/* ✅ WEEKLY REPORT ROUTE */}
      <Route
        path="/weekly-report"
        element={
          <ProtectedRoute>
            <WeeklyReport />
          </ProtectedRoute>
        }
      />

      <Route
        path="/resources"
        element={
          <ProtectedRoute>
            <Resources />
          </ProtectedRoute>
        }
      />

      <Route
        path="/history/:date"
        element={
          <ProtectedRoute>
            <EmotionHistoryDay />
          </ProtectedRoute>
        }
      />

      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
