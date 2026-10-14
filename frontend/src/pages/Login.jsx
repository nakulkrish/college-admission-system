import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login({ email, password });
      navigate("/courses");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="glass-card" style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h2 style={{ marginBottom: "1rem", textAlign: "center" }}>Student Login</h2>
      {error && <div className="toast">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input className="input-field" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input className="input-field" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button className="btn" type="submit" style={{ width: "100%" }}>
          Login
        </button>
      </form>
    </div>
  );
}
