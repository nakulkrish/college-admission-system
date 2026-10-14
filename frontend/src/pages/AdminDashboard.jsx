import React, { useEffect, useState } from "react";
import { getAllApplications, updateApplicationStatus } from "../services/api";

export default function AdminDashboard() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const fetchApplications = async () => {
    try {
      const data = await getAllApplications();
      setApplications(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  const handleStatusChange = async (id, newStatus) => {
    try {
      await updateApplicationStatus(id, newStatus);
      setToast(`Application ${id} status updated to ${newStatus}`);
      fetchApplications();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Loading applications...</p>;
  if (error) return <div className="toast">{error}</div>;

  return (
    <div>
      <h2 style={{ marginBottom: "1rem" }}>Admin Dashboard - All Applications</h2>
      {toast && <div className="toast">{toast}</div>}
      <table className="table glass-card">
        <thead>
          <tr>
            <th>ID</th>
            <th>Student ID</th>
            <th>Course ID</th>
            <th>GPA</th>
            <th>Status</th>
            <th>Merit Score</th>
            <th>Submitted At</th>
            <th>Change Status</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((app) => (
            <tr key={app.id}>
              <td>{app.id}</td>
              <td>{app.student_id}</td>
              <td>{app.course_id}</td>
              <td>{app.gpa}</td>
              <td>{app.status}</td>
              <td>{app.merit_score ? app.merit_score.toFixed(2) : "-"}</td>
              <td>{new Date(app.created_at).toLocaleString()}</td>
              <td>
                <select
                  value={app.status}
                  onChange={(e) => handleStatusChange(app.id, e.target.value)}
                >
                  <option value="PENDING">PENDING</option>
                  <option value="APPROVED">APPROVED</option>
                  <option value="REJECTED">REJECTED</option>
                  <option value="REQUEST_CORRECTION">REQUEST_CORRECTION</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
