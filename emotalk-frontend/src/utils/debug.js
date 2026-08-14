/**
 * Debug Utilities
 * 
 * Lightweight debugging helpers for development.
 * Use these in browser console or components for debugging.
 * 
 * TODO: Remove or disable in production build
 */

/**
 * Test API connection
 * 
 * Usage in browser console:
 *   import { testApiConnection } from './utils/debug';
 *   testApiConnection();
 */
export async function testApiConnection() {
  console.log("🔍 Testing API connection...");
  
  try {
    const response = await fetch("http://127.0.0.1:8000/health");
    const data = await response.json();
    
    if (data.status === "healthy") {
      console.log("✅ API connection successful");
      console.log("   Model loaded:", data.model_loaded);
      console.log("   Version:", data.version);
      return true;
    } else {
      console.warn("⚠️ API responded but status is not healthy");
      return false;
    }
  } catch (error) {
    console.error("❌ API connection failed:", error.message);
    console.error("   Check if backend is running on http://127.0.0.1:8000");
    return false;
  }
}

/**
 * Test debug endpoint
 */
export async function testDebugEndpoint() {
  console.log("🔍 Testing debug endpoint...");
  
  try {
    const response = await fetch("http://127.0.0.1:8000/debug/status");
    const data = await response.json();
    
    console.log("✅ Debug endpoint response:", data);
    return data;
  } catch (error) {
    console.error("❌ Debug endpoint failed:", error.message);
    return null;
  }
}

/**
 * Log current API configuration
 */
export function logApiConfig() {
  const config = {
    baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
    apiPrefix: "/api/v1",
  };
  
  console.log("📋 Current API Configuration:", config);
  return config;
}

/**
 * Test emotion prediction with sample data
 * Note: This is a mock test, actual prediction requires audio file
 */
export function testPredictionFlow() {
  console.log("🔍 Testing prediction flow...");
  console.log("   1. Check API connection");
  console.log("   2. Verify model is loaded");
  console.log("   3. Test prediction endpoint accessibility");
  
  testApiConnection().then((connected) => {
    if (connected) {
      console.log("✅ Ready for prediction");
      console.log("   Use the app UI to record and analyze emotion");
    } else {
      console.error("❌ Cannot test prediction - API not connected");
    }
  });
}

// Auto-run in development mode
if (import.meta.env.DEV) {
  console.log("🐛 Debug utilities loaded");
  console.log("   Available functions:");
  console.log("   - testApiConnection()");
  console.log("   - testDebugEndpoint()");
  console.log("   - logApiConfig()");
  console.log("   - testPredictionFlow()");
}

