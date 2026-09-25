import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

const TOKEN_KEY = "auth_token";
const EMAIL_KEY = "auth_email";

export function AuthProvider({ children }) {
  // Read persisted session on first render — survives page refresh
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    const email = localStorage.getItem(EMAIL_KEY);
    // Only restore session if BOTH token and email are present
    return token && email ? { email } : null;
  });

  /**
   * Call after a successful login/signup API response.
   * Persists the JWT token and email to localStorage.
   *
   * @param {string} email
   * @param {string} token  - JWT access_token from the backend
   */
  const login = (email, token) => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(EMAIL_KEY, email);
    setUser({ email });
  };

  /** Remove session from both state and localStorage. */
  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(EMAIL_KEY);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
