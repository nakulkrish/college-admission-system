import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../services/api";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <nav className="navbar glass-card">
      <div className="logo">
        <Link to="/" style={{ color: "var(--accent)", fontWeight: "bold", fontSize: "1.2rem", textDecoration: "none" }}>
          College Admission
        </Link>
      </div>
      <div className="nav-links">
        {token ? (
          <>
            <Link to="/courses">Courses</Link>
            <Link to="/my-applications">My Applications</Link>
            {role === "ADMIN" && <Link to="/admin">Admin</Link>}
            <button className="btn" onClick={handleLogout} style={{ marginLeft: "1rem" }}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
