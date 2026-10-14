import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../services/api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register({ email, password, full_name: fullName });
      navigate("/login");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="glass-card" style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h2 style={{ marginBottom: "1rem", textAlign: "center" }}>Student Registration</h2>
      {error && <div className="toast">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label>
          Full Name
          <input className="input-field" type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
        </label>
        <label>
          Email
          <input className="input-field" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input className="input-field" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button className="btn" type="submit" style={{ width: "100%" }}>
          Register
        </button>
      </form>
    </div>
  );
}
