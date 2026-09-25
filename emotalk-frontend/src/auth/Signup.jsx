import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { signup as signupApi } from "../services/authApi";
import "./Auth.css";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // Call the real backend — returns { access_token, token_type }
      const data = await signupApi(email, password);

      // Immediately log the user in after signup (token is returned on registration)
      login(email, data.access_token);

      navigate("/", { replace: true });
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Signup failed. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      {/* Brand */}
      <div className="brand">
        <div className="leaf-icon">
          <svg
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M5 21c14 0 14-16 14-16S5 5 5 21z" />
            <path d="M5 21c4-4 8-6 14-16" />
          </svg>
        </div>
        <h1 className="brand-name">Emotalk</h1>
      </div>

      {/* Card */}
      <div className="auth-card">
        <h2>Create account</h2>
        <p className="subtitle">Start tracking your emotional journey</p>

        {error && (
          <div className="auth-error" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
          />

          <input
            type="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        {/* Switch */}
        <p className="switch-text">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
}
