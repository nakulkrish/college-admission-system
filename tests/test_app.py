import json

from fastapi.testclient import TestClient

from app.main import app  # The platform provides app with routers mounted under /api


client = TestClient(app)


def test_register_and_login():
    # Register a student
    response = client.post(
        "/api/auth/register",
        json={"email": "student@example.com", "password": "secret123", "full_name": "Student One"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "student@example.com"
    assert data["role"] == "student"

    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": "student@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    # Use token to list courses (none yet)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/courses/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_admin_course_creation_and_application_flow():
    # Register admin
    response = client.post(
        "/api/auth/register",
        json={"email": "admin@example.com", "password": "adminpass", "full_name": "Admin User"},
    )
    assert response.status_code == 200
    admin_id = response.json()["id"]

    # Manually promote to admin in DB (since registration defaults to student)
    from app.core.database import SessionLocal
    from app import models

    db = SessionLocal()
    admin_user = db.query(models.User).filter(models.User.id == admin_id).first()
    admin_user.role = models.UserRole.ADMIN
    db.commit()
    db.close()

    # Login as admin
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@example.com", "password": "adminpass"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a course
    course_payload = {
        "name": "Computer Science",
        "description": "BSc Computer Science",
        "seats": 30,
        "fee": 5000.0,
        "eligibility_min_gpa": 3.0,
    }
    response = client.post("/api/courses/", json=course_payload, headers=headers)
    assert response.status_code == 201
    course_id = response.json()["id"]

    # Register a student
    response = client.post(
        "/api/auth/register",
        json={"email": "applicant@example.com", "password": "applicant", "full_name": "Applicant"},
    )
    assert response.status_code == 200
    student_token = client.post(
        "/api/auth/login",
        data={"username": "applicant@example.com", "password": "applicant"},
    ).json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # Submit application with a dummy file
    files = [("files", ("transcript.pdf", b"dummy content", "application/pdf"))]
    data = {"course_id": str(course_id), "gpa": "3.5"}
    response = client.post(
        "/api/applications/",
        data=data,
        files=files,
        headers=student_headers,
    )
    assert response.status_code == 201
    app_id = response.json()["id"]
    assert response.json()["status"] == "submitted"

    # Admin lists all applications
    response = client.get("/api/admin/applications", headers=headers)
    assert response.status_code == 200
    apps = response.json()
    assert any(a["id"] == app_id for a in apps)

    # Admin updates status to SELECTED
    response = client.patch(
        f"/api/admin/applications/{app_id}",
        json={"status": "selected"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "selected"
