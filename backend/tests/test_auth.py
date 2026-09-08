# -*- coding: utf-8 -*-
import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth import hash_password, verify_password

client = TestClient(app)

def test_password_hashing_and_verification():
    raw_pw = "SecureKisan@2026"
    hashed = hash_password(raw_pw)
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(raw_pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False
    assert verify_password("", hashed) is False

def test_signup_duplicate_and_login_flow():
    email = f"farmer_{uuid.uuid4().hex[:8]}@krishiai.org"
    password = "KisanPassword123"

    # 1. Sign up new farmer
    signup_payload = {
        "name": "Ramesh Gowda",
        "email": email,
        "phone": "+919876543210",
        "password": password,
        "preferred_language": "kn"
    }
    signup_resp = client.post("/auth/signup", json=signup_payload)
    assert signup_resp.status_code == 200
    signup_data = signup_resp.json()
    assert "token" in signup_data
    assert signup_data["user"]["name"] == "Ramesh Gowda"
    assert signup_data["user"]["email"] == email.lower()
    token = signup_data["token"]

    # 2. Prevent duplicate email registration
    dup_resp = client.post("/auth/signup", json=signup_payload)
    assert dup_resp.status_code == 400
    assert "already exists" in dup_resp.json()["detail"].lower()

    # 3. Test Login with wrong password -> HTTP 401
    bad_login = client.post("/auth/login", json={"email": email, "password": "WrongPassword"})
    assert bad_login.status_code == 401
    assert "invalid email or password" in bad_login.json()["detail"].lower()

    # 4. Test Login with correct password -> HTTP 200
    good_login = client.post("/auth/login", json={"email": email, "password": password})
    assert good_login.status_code == 200
    login_data = good_login.json()
    assert "token" in login_data
    assert login_data["user"]["email"] == email.lower()
    active_token = login_data["token"]

    # 5. Test /auth/me with Bearer token
    me_resp = client.get("/auth/me", headers={"Authorization": f"Bearer {active_token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["name"] == "Ramesh Gowda"

    # 6. Test /auth/me without token -> HTTP 401
    unauth_resp = client.get("/auth/me")
    assert unauth_resp.status_code == 401

def test_forgot_and_reset_password():
    email = f"reset_{uuid.uuid4().hex[:8]}@krishiai.org"
    old_pw = "OldPassword123"
    new_pw = "NewPassword456"

    # Signup
    client.post("/auth/signup", json={"name": "Suresh", "email": email, "password": old_pw})

    # Request password reset
    forgot_resp = client.post("/auth/forgot-password", json={"email": email})
    assert forgot_resp.status_code == 200
    reset_token = forgot_resp.json().get("reset_token")
    assert reset_token is not None

    # Reset password with token
    reset_resp = client.post("/auth/reset-password", json={
        "email": email,
        "token": reset_token,
        "new_password": new_pw
    })
    assert reset_resp.status_code == 200

    # Old password no longer works
    assert client.post("/auth/login", json={"email": email, "password": old_pw}).status_code == 401

    # New password works
    assert client.post("/auth/login", json={"email": email, "password": new_pw}).status_code == 200

def test_upload_image_validation():
    # Attempt to upload an invalid file extension (.txt)
    resp = client.post(
        "/upload-image",
        files={"file": ("malicious.txt", b"malicious executable text", "text/plain")}
    )
    assert resp.status_code == 400
    assert "invalid image format" in resp.json()["detail"].lower()
