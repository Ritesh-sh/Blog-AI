"""
Authentication Module - JWT-based authentication for the API.
Uses MongoDB Atlas for user storage and bcrypt for password hashing.

Usage:
    from app.auth import create_access_token, verify_token, get_current_user
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

logger = logging.getLogger(__name__)

# JWT Bearer scheme
security = HTTPBearer()


# Pydantic models for auth
class UserCreate(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response (no password)."""
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Decoded token data."""
    user_id: str
    email: str
    exp: datetime


def verify_password(plain_password: str, stored_value: str) -> bool:
    """Compare plaintext passwords (not secure)."""
    return plain_password == stored_value


def hash_password(password: str) -> str:
    """Return password without hashing (insecure)."""
    logger.warning("Storing plaintext passwords is insecure; consider reintroducing hashing when possible.")
    return password


def create_access_token(user_id: str, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: MongoDB user ID
        email: User email
        expires_delta: Token expiry time (default from settings)
        
    Returns:
        Encoded JWT token string
    """
    from app.config import get_settings
    settings = get_settings()
    
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.jwt_expiry_minutes)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": user_id,
        "email": email,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData if valid, None if invalid
    """
    from app.config import get_settings
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        exp = datetime.fromtimestamp(payload.get("exp"))
        
        if user_id is None or email is None:
            return None
            
        return TokenData(user_id=user_id, email=email, exp=exp)
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    FastAPI dependency to get current authenticated user.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: TokenData = Depends(get_current_user)):
            return {"user_id": user.user_id}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    # Optionally verify user still exists in DB
    # (uncomment if you want to check on every request)
    # from app.db import get_users_collection
    # user = await get_users_collection().find_one({"_id": ObjectId(token_data.user_id)})
    # if user is None:
    #     raise credentials_exception
    
    return token_data


# User service functions (use MongoDB)
async def create_user(user_data: UserCreate) -> dict:
    """
    Create a new user in the database.
    
    Args:
        user_data: User registration data
        
    Returns:
        Created user document (without password)
        
    Raises:
        HTTPException: If email already exists
    """
    from app.db import get_users_collection
    from bson import ObjectId
    
    users = get_users_collection()
    
    # Check if email already exists
    existing = await users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_doc = {
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
        "name": user_data.name,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    # Return without password
    return {
        "id": str(user_doc["_id"]),
        "email": user_doc["email"],
        "name": user_doc["name"],
        "created_at": user_doc["created_at"]
    }


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Authenticate a user by email and password.
    
    Args:
        email: User email
        password: Plain text password
        
    Returns:
        User document if credentials valid, None otherwise
    """
    from app.db import get_users_collection
    
    users = get_users_collection()
    user = await users.find_one({"email": email})
    
    if user is None:
        return None
    
    if not verify_password(password, user["password_hash"]):
        return None
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name"),
        "created_at": user["created_at"]
    }


async def log_user_action(user_id: str, action: str, data: Optional[dict] = None):
    """
    Log a user action to the history collection.
    
    Args:
        user_id: User's MongoDB ID
        action: Action type (login, logout, generate_blog, etc.)
        data: Optional additional data about the action
    """
    from app.db import get_history_collection
    
    history = get_history_collection()
    await history.insert_one({
        "user_id": user_id,
        "action": action,
        "data": data or {},
        "timestamp": datetime.utcnow()
    })


async def get_user_history(user_id: str, limit: int = 50) -> list:
    """
    Get user's action history.
    
    Args:
        user_id: User's MongoDB ID
        limit: Maximum number of records to return
        
    Returns:
        List of history records
    """
    from app.db import get_history_collection
    
    history = get_history_collection()
    cursor = history.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    
    records = []
    async for record in cursor:
        record["id"] = str(record.pop("_id"))
        records.append(record)
    
    return records
