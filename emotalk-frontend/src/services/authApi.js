import apiClient from "../api/client";
import { API_ENDPOINTS } from "../config/api";

/**
 * Call backend signup endpoint and return token data.
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{access_token:string,token_type:string}>}
 */
export async function signup(email, password) {
  const resp = await apiClient.post(API_ENDPOINTS.signup, { email, password });
  return resp.data;
}

/**
 * Call backend login endpoint and return token data.
 * @param {string} email
 * @param {string} password
 */
export async function login(email, password) {
  const resp = await apiClient.post(API_ENDPOINTS.login, { email, password });
  return resp.data;
}
