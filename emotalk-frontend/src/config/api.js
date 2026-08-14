/**
 * API Configuration
 * 
 * Centralizes API endpoint configuration for easy environment switching.
 * 
 * TODO: Move to environment variables for production
 * TODO: Add API versioning support
 */

// Base API URL - defaults to localhost for development
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  apiPrefix: "/api/v1", // Match backend API prefix
  timeout: 30000, // 30 seconds for audio uploads
};

// Full API URL with prefix
export const API_BASE_URL = `${API_CONFIG.baseURL}${API_CONFIG.apiPrefix}`;

// API Endpoints
export const API_ENDPOINTS = {
  predict: "/predict",
  emotionHistory: "/emotion-history",
  dailyReport: "/daily-report",
  weeklyReport: "/weekly-report",
  // auth routes
  signup: "/auth/signup",
  login: "/auth/login",
};

