/**
 * Simple wrapper around fetch that automatically includes the JWT token
 * and handles JSON responses.
 */
const API_BASE = "/api";

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handleResponse(res) {
  const contentType = res.headers.get("content-type");
  const isJson = contentType && contentType.includes("application/json");
  const data = isJson ? await res.json() : null;
  if (!res.ok) {
    const error = (data && data.detail) || res.statusText;
    throw new Error(error);
  }
  return data;
}

/* Auth */
export async function register(user) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });
  return handleResponse(res);
}

export async function login(credentials) {
  const form = new URLSearchParams();
  form.append("username", credentials.email);
  form.append("password", credentials.password);
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
  const data = await handleResponse(res);
  // Store token and role
  localStorage.setItem("token", data.access_token);
  // Decode token payload (simple base64 decode, no verification)
  const payload = JSON.parse(atob(data.access_token.split(".")[1]));
  localStorage.setItem("role", payload.role);
  return data;
}

/* Courses */
export async function getCourses() {
  const res = await fetch(`${API_BASE}/courses/`, {
    headers: { ...getAuthHeaders() },
  });
  return handleResponse(res);
}

/* Applications */
export async function submitApplication(formData) {
  const res = await fetch(`${API_BASE}/applications/`, {
    method: "POST",
    headers: { ...getAuthHeaders() },
    body: formData,
  });
  return handleResponse(res);
}

export async function getMyApplications() {
  const res = await fetch(`${API_BASE}/applications/me`, {
    headers: { ...getAuthHeaders() },
  });
  return handleResponse(res);
}

/* Admin */
export async function getAllApplications() {
  const res = await fetch(`${API_BASE}/admin/applications`, {
    headers: { ...getAuthHeaders() },
  });
  return handleResponse(res);
}

export async function updateApplicationStatus(id, status) {
  const res = await fetch(`${API_BASE}/admin/applications/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ status }),
  });
  return handleResponse(res);
}

/* Utility */
export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
}
