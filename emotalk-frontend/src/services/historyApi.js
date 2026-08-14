/**
 * Emotion History API Service
 * 
 * Handles fetching emotion history and reports.
 * 
 * TODO: Add pagination support
 * TODO: Add date range filtering
 */
import apiClient from "../api/client";
import { API_ENDPOINTS } from "../config/api";

/**
 * Get all emotion history records
 * 
 * @returns {Promise<Array>} List of emotion records
 * @throws {Error} If fetch fails
 */
export async function getEmotionHistory() {
  try {
    const response = await apiClient.get(API_ENDPOINTS.emotionHistory);
    // Handle both old format (array) and new format ({data, count})
    return response.data.data || response.data || [];
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.detail || "Failed to fetch history");
    }
    throw new Error("Unable to connect to server. Please check your connection.");
  }
}

/**
 * Get daily emotion report
 * 
 * @returns {Promise<Object>} Daily report with insights
 */
export async function getDailyReport() {
  try {
    const response = await apiClient.get(API_ENDPOINTS.dailyReport);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.details || "Failed to fetch daily report");
    }
    throw new Error("Unable to connect to server. Please check your connection.");
  }
}

/**
 * Get weekly emotion report
 * 
 * @returns {Promise<Object>} Weekly report with trends
 */
export async function getWeeklyReport() {
  try {
    const response = await apiClient.get(API_ENDPOINTS.weeklyReport);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.details || "Failed to fetch weekly report");
    }
    throw new Error("Unable to connect to server. Please check your connection.");
  }
}
  