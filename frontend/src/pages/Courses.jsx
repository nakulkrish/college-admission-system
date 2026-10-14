import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getCourses } from "../services/api";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchCourses() {
      try {
        const data = await getCourses();
        setCourses(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchCourses();
  }, []);

  if (loading) return <p>Loading courses...</p>;
  if (error) return <div className="toast">{error}</div>;

  return (
    <div>
      <h2 style={{ marginBottom: "1rem" }}>Available Courses</h2>
      {courses.map((course) => (
        <div key={course.id} className="glass-card">
          <h3>{course.name}</h3>
          <p>{course.description || "No description provided."}</p>
          <p>
            <strong>Seats:</strong> {course.seats}
          </p>
          <p>
            <strong>Fee:</strong> ${course.fee.toFixed(2)}
          </p>
          <p>
            <strong>Eligibility GPA:</strong> {course.eligibility_min_gpa}
          </p>
          <Link className="btn" to={`/apply/${course.id}`}>
            Apply
          </Link>
        </div>
      ))}
    </div>
  );
}
