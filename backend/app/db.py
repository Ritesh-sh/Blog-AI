"""
MongoDB Atlas Database Connection Helper.
Provides async MongoDB client using Motor driver.

Environment:
    MONGODB_URI: MongoDB Atlas SRV connection string
                 Format: mongodb+srv://<user>:<pass>@cluster0.mongodb.net
    MONGODB_DB: Database name (default: blog_generator)

Usage:
    from app.db import get_mongo_db, get_mongo_client
    
    # Get database instance
    db = get_mongo_db()
    
    # Use collections
    users = db.users
    history = db.history
"""

import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

# Global client singleton
_mongo_client: Optional[AsyncIOMotorClient] = None


def get_mongo_client() -> AsyncIOMotorClient:
    """
    Get MongoDB Atlas client singleton.
    Uses TLS for secure connection to Atlas.
    
    Returns:
        AsyncIOMotorClient connected to Atlas cluster
        
    Raises:
        ValueError: If MONGODB_URI is not configured
    """
    global _mongo_client
    
    if _mongo_client is None:
        from app.config import get_settings
        settings = get_settings()
        
        if not settings.mongodb_uri:
            raise ValueError(
                "MONGODB_URI not configured. "
                "Set it in .env or environment variables. "
                "Format: mongodb+srv://<user>:<pass>@cluster0.mongodb.net"
            )
        
        _mongo_client = AsyncIOMotorClient(
            settings.mongodb_uri,
            tls=True,
            tlsAllowInvalidCertificates=False,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
        )
        logger.info("MongoDB Atlas client initialized")
    
    return _mongo_client


def get_mongo_db() -> AsyncIOMotorDatabase:
    """
    Get MongoDB database instance.
    
    Returns:
        AsyncIOMotorDatabase for the configured database name
    """
    from app.config import get_settings
    settings = get_settings()
    client = get_mongo_client()
    return client[settings.mongodb_db]


async def check_mongo_connection() -> bool:
    """
    Check if MongoDB connection is healthy.
    
    Returns:
        True if connection is working, False otherwise
    """
    try:
        client = get_mongo_client()
        await client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"MongoDB connection check failed: {e}")
        return False


async def close_mongo_connection():
    """Close MongoDB connection gracefully."""
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None
        logger.info("MongoDB connection closed")


# Collections helpers
def get_users_collection():
    """Get users collection."""
    return get_mongo_db().users


def get_history_collection():
    """Get history collection for user actions."""
    return get_mongo_db().history


def get_blogs_collection():
    """Get generated blogs collection."""
    return get_mongo_db().blogs
