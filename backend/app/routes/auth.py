"""
Authentication API Routes.
Provides registration, login, logout, and history endpoints.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from app.auth import (
    UserCreate, UserLogin, UserResponse, Token, TokenData,
    create_access_token, authenticate_user, create_user,
    get_current_user, log_user_action, get_user_history
)
from app.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, password, optional name)
        
    Returns:
        Created user data (without password)
    """
    settings = get_settings()
    
    if not settings.mongodb_uri:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User registration not available (database not configured)"
        )
    
    user = await create_user(user_data)
    await log_user_action(user["id"], "register")
    logger.info(f"New user registered: {user['email']}")
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user.get("name"),
        created_at=user["created_at"]
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT token.
    
    Args:
        credentials: User login data (email, password)
        
    Returns:
        JWT access token
    """
    settings = get_settings()
    
    if not settings.mongodb_uri:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authentication not available (database not configured)"
        )
    
    user = await authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        user_id=user["id"],
        email=user["email"],
        expires_delta=timedelta(minutes=settings.jwt_expiry_minutes)
    )
    
    await log_user_action(user["id"], "login")
    logger.info(f"User logged in: {user['email']}")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_expiry_minutes * 60
    )


@router.post("/logout")
async def logout(current_user: TokenData = Depends(get_current_user)):
    """
    Logout user (record logout event).
    
    Note: For stateless JWT, client should discard token.
    Server records logout event for audit purposes.
    """
    await log_user_action(current_user.user_id, "logout")
    logger.info(f"User logged out: {current_user.email}")
    
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=TokenData)
async def get_me(current_user: TokenData = Depends(get_current_user)):
    """
    Get current authenticated user info.
    
    Returns:
        Current user's token data
    """
    return current_user


@router.get("/history")
async def get_history(
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get current user's action history.
    
    Args:
        limit: Maximum number of records to return (default 50)
        
    Returns:
        List of history records
    """
    settings = get_settings()
    
    if not settings.mongodb_uri:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="History not available (database not configured)"
        )
    
    history = await get_user_history(current_user.user_id, limit)
    return history
