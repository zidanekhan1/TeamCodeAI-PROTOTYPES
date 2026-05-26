import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional

from pydantic import BaseModel, Field


# ---------- Data Models ----------

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    name: str
    token: str


# ---------- Fake Database ----------

# In a real application, replace this with a proper database layer.
_FAKE_USER_DB: Dict[str, Dict[str, str]] = {
    "alice": {"hashed_password": hashlib.sha256("alicepass".encode()).hexdigest(), "name": "Alice Wonderland"},
    "bob": {"hashed_password": hashlib.sha256("bobpass".encode()).hexdigest(), "name": "Bob Builder"},
}

# Token store: maps token string to (username, expiry)
_TOKEN_DB: Dict[str, Dict[str, datetime]] = {}


# ---------- Utility Functions ----------

def _hash_password(password: str) -> str:
    """Return a SHA256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored hash."""
    return _hash_password(plain_password) == hashed_password


def _create_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a UUID4 token and store it with an expiry."""
    if expires_delta is None:
        expires_delta = timedelta(hours=1)
    expiry = datetime.utcnow() + expires_delta
    token = str(uuid.uuid4())
    _TOKEN_DB[token] = {"username": username, "expiry": expiry}
    return token


def _get_username_from_token(token: str) -> Optional[str]:
    """Retrieve username associated with a valid token."""
    data = _TOKEN_DB.get(token)
    if not data:
        return None
    if data["expiry"] < datetime.utcnow():
        # Token expired, remove it
        del _TOKEN_DB[token]
        return None
    return data["username"]


# ---------- Authentication Logic ----------

def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    """Validate user credentials against the fake database."""
    user_record = _FAKE_USER_DB.get(username)
    if not user_record:
        return None
    if not _verify_password(password, user_record["hashed_password"]):
        return None
    return {"username": username, "name": user_record["name"]}


def login_user(request: LoginRequest) -> LoginResponse:
    """Process login request and return user info with token."""
    user = authenticate_user(request.username, request.password)
    if not user:
        raise ValueError("Invalid username or password")
    token = _create_token(user["username"])
    return LoginResponse(name=user["name"], token=token)


def get_current_user(token: str) -> Optional[Dict[str, str]]:
    """Retrieve user information based on the provided token."""
    username = _get_username_from_token(token)
    if not username:
        return None
    user_record = _FAKE_USER_DB.get(username)
    if not user_record:
        return None
    return {"username": username, "name": user_record["name"]}


# ---------- Example Usage (for testing only) ----------
if __name__ == "__main__":
    # Simulate a login
    req = LoginRequest(username="alice", password="alicepass")
    try:
        resp = login_user(req)
        print("Login successful:", resp)
        # Validate token
        current = get_current_user(resp.token)
        print("Current user from token:", current)
    except ValueError as e:
        print("Login failed:", e)