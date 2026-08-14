/**
 * Emotion Prediction API Service
 * 
 * Handles audio upload and emotion prediction.
 * 
 * TODO: Add progress tracking for large files
 * TODO: Add audio validation before upload
 */
import apiClient from "../api/client";
import { API_ENDPOINTS } from "../config/api";

/**
 * Predict emotion from audio blob URL
 * 
 * @param {string} audioBlobUrl - Blob URL of recorded audio
 * @returns {Promise<{emotion: string, confidence: number}>}
 * @throws {Error} If prediction fails
 */
export async function predictEmotion(audioBlobUrl) {
  try {
    // Convert blob URL to File object
    const response = await fetch(audioBlobUrl);
    const blob = await response.blob();
    
    // Determine file extension from blob type
    let extension = "webm";
    if (blob.type.includes("wav")) extension = "wav";
    else if (blob.type.includes("mpeg") || blob.type.includes("mp3")) extension = "mp3";
    else if (blob.type.includes("m4a")) extension = "m4a";

    const formData = new FormData();
    formData.append("file", blob, `audio.${extension}`);

    const result = await apiClient.post(
      API_ENDPOINTS.predict,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return result.data;
  } catch (error) {
    // Provide user-friendly error messages
    if (error.response) {
      const message = error.response.data?.detail || "Failed to analyze emotion";
      throw new Error(message);
    } else if (error.request) {
      throw new Error("Unable to connect to server. Please check your connection.");
    } else {
      throw new Error("An unexpected error occurred. Please try again.");
    }
  }
}
