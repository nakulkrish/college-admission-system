import React, { useEffect, useState } from "react";
import { getMyApplications } from "../services/api";

export default function MyApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchApps() {
      try {
        const data = await getMyApplications();
        setApplications(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchApps();
  }, []);

  if (loading) return <p>Loading your applications...</p>;
  if (error) return <div className="toast">{error}</div>;

  return (
    <div>
      <h2 style={{ marginBottom: "1rem" }}>My Applications</h2>
      {applications.length === 0 ? (
        <p>No applications submitted yet.</p>
      ) : (
        <table className="table glass-card">
          <thead>
            <tr>
              <th>ID</th>
              <th>Course ID</th>
              <th>GPA</th>
              <th>Status</th>
              <th>Submitted At</th>
            </tr>
          </thead>
          <tbody>
            {applications.map((app) => (
              <tr key={app.id}>
                <td>{app.id}</td>
                <td>{app.course_id}</td>
                <td>{app.gpa}</td>
                <td>{app.status}</td>
                <td>{new Date(app.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
