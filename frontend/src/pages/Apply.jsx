import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getCourses, submitApplication } from "../services/api";

export default function Apply() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [gpa, setGpa] = useState("");
  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    async function fetchCourse() {
      try {
        const data = await getCourses();
        const found = data.find((c) => c.id === parseInt(courseId));
        setCourse(found);
      } catch (err) {
        setError(err.message);
      }
    }
    fetchCourse();
  }, [courseId]);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (!gpa) {
      setError("Please enter your GPA.");
      return;
    }
    const formData = new FormData();
    formData.append("course_id", courseId);
    formData.append("gpa", gpa);
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }
    try {
      await submitApplication(formData);
      setSuccess("Application submitted successfully!");
      setTimeout(() => navigate("/my-applications"), 1500);
    } catch (err) {
      setError(err.message);
    }
  };

  if (!course) return <p>Loading course details...</p>;

  return (
    <div className="glass-card" style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ marginBottom: "1rem" }}>Apply for {course.name}</h2>
      {error && <div className="toast">{error}</div>}
      {success && <div className="toast">{success}</div>}
      <form onSubmit={handleSubmit}>
        <label>
          GPA (0 - 4)
          <input className="input-field" type="number" step="0.01" min="0" max="4" value={gpa} onChange={(e) => setGpa(e.target.value)} required />
        </label>
        <label>
          Upload Documents (Mark sheets, ID, Photo, etc.)
          <input className="input-field" type="file" multiple onChange={handleFileChange} required />
        </label>
        <button className="btn" type="submit" style={{ width: "100%" }}>
          Submit Application
        </button>
      </form>
    </div>
  );
}
