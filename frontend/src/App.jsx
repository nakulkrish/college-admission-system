import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";

import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Courses from "./pages/Courses";
import Apply from "./pages/Apply";
import MyApplications from "./pages/MyApplications";
import AdminDashboard from "./pages/AdminDashboard";

function PrivateRoute({ children, adminOnly = false }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  if (adminOnly && role !== "ADMIN") {
    return <Navigate to="/courses" replace />;
  }
  return children;
}

export default function App() {
  const [authChecked, setAuthChecked] = useState(false);
  const navigate = useNavigate();

  // Simple effect to redirect root based on auth status
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/courses", { replace: true });
    } else {
      navigate("/login", { replace: true });
    }
    setAuthChecked(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!authChecked) {
    return null; // or a spinner
  }

  return (
    <div className="app-container">
      <Navbar />
      <main className="content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/courses"
            element={
              <PrivateRoute>
                <Courses />
              </PrivateRoute>
            }
          />
          <Route
            path="/apply/:courseId"
            element={
              <PrivateRoute>
                <Apply />
              </PrivateRoute>
            }
          />
          <Route
            path="/my-applications"
            element={
              <PrivateRoute>
                <MyApplications />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <PrivateRoute adminOnly={true}>
                <AdminDashboard />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/courses" replace />} />
        </Routes>
      </main>
    </div>
  );
}
