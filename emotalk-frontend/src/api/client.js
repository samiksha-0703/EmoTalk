/**
 * API Client
 * 
 * Centralized axios instance with interceptors for:
 * - Request/response logging
 * - Error handling
 * - Authentication (future)
 * 
 * TODO: Add request retry logic
 * TODO: Add request cancellation support
 */
import axios from "axios";
import { API_CONFIG, API_BASE_URL } from "../config/api";

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_CONFIG.timeout,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available (future feature)
    const token = localStorage.getItem("auth_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    }
    
    return config;
  },
  (error) => {
    console.error("[API Request Error]", error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.status);
    }
    return response;
  },
  (error) => {
    // Handle errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      if (status === 401) {
        // Unauthorized - clear auth and redirect
        localStorage.removeItem("auth_token");
        // TODO: Redirect to login
      }
      
      console.error(`[API Error] ${error.config?.url}`, {
        status,
        message: data?.detail || data?.message || "Unknown error",
      });
    } else if (error.request) {
      // Request made but no response received
      console.error("[API Error] No response received", error.request);
    } else {
      // Error setting up request
      console.error("[API Error] Request setup failed", error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;

