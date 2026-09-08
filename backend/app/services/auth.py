# -*- coding: utf-8 -*-
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import User

ITERATIONS = 100000

def hash_password(password: str) -> str:
    """
    NIST-recommended PBKDF2-HMAC-SHA256 password hashing with unique salt.
    Format: pbkdf2_sha256$<salt_hex>$<hash_hex>
    """
    salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        ITERATIONS
    ).hex()
    return f"pbkdf2_sha256${salt}${pw_hash}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Timing-safe constant-time password verification.
    """
    if not stored_hash or not stored_hash.startswith("pbkdf2_sha256$"):
        return False
    try:
        parts = stored_hash.split("$")
        if len(parts) != 3:
            return False
        salt = parts[1]
        expected_hash = parts[2]
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            ITERATIONS
        ).hex()
        return hmac.compare_digest(computed_hash, expected_hash)
    except Exception:
        return False

def generate_session_token() -> str:
    """
    Generates a cryptographically random, URL-safe 48-character bearer token.
    """
    return secrets.token_urlsafe(36)

def generate_reset_token() -> str:
    """
    Generates a 6-digit or secure token for password reset.
    """
    return secrets.token_hex(16)

def get_user_by_token(token: str, db: Session) -> Optional[User]:
    """
    Resolves user by active auth_token.
    """
    if not token:
        return None
    return db.query(User).filter(User.auth_token == token).first()

def get_user_by_email(email: str, db: Session) -> Optional[User]:
    """
    Resolves user by case-insensitive email.
    """
    if not email:
        return None
    return db.query(User).filter(User.email == email.strip().lower()).first()
