"""
Configuration management for the blog generator application.
Loads environment variables and provides application settings.
Production-ready with MongoDB Atlas support and lazy initialization.
"""

from pydantic_settings import BaseSettings
import logging
from logging.handlers import RotatingFileHandler
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini Configuration (Google AI)
    gemini_api_key: str = ""  # Set in .env as GEMINI_API_KEY
    gemini_model: str = "gemini-3-flash-preview"
    
    # Application Settings
    app_env: str = "development"
    log_level: str = "INFO"
    log_file: Optional[str] = None  # e.g. /var/log/ai_blog/app.log
    max_content_length: int = 10000
    request_timeout: int = 30
    
    # Model Settings
    embedding_model: str = "all-MiniLM-L6-v2"
    use_faiss_cache: bool = False
    
    # Unsplash API (for images)
    unsplash_access_key: str = ""  # Set in .env as UNSPLASH_ACCESS_KEY
    
    # MongoDB Atlas Configuration
    mongodb_uri: str = ""  # Set in .env as MONGODB_URI
    mongodb_db: str = "blog_generator"  # Set in .env as MONGODB_DB if you want to override
    
    # JWT / Auth Configuration
    jwt_secret_key: str = ""  # Set in .env as JWT_SECRET_KEY
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    
    # Production / Security Settings
    cors_allowed_origins: List[str] = ["http://localhost:7860", "http://localhost:3000", "http://localhost:8000"]
    allowed_hosts: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    sentry_dsn: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings singleton (initialized lazily at app startup)
_settings: Optional[Settings] = None


def init_settings() -> Settings:
    """
    Initialize and validate settings. Call this during application startup.
    Warns on missing production secrets but doesn't crash for dev convenience.
    """
    global _settings
    _settings = Settings()
    
    # Warn on missing Gemini API key
    if not _settings.gemini_api_key:
        logging.warning("GEMINI_API_KEY is not set. Blog generation will fail.")
    
    # Warn on missing MongoDB URI in production
    if _settings.app_env == "production" and not _settings.mongodb_uri:
        logging.warning("APP_ENV=production but MONGODB_URI is not set. Database features disabled.")
    
    # Warn on default JWT secret in production
    if _settings.app_env == "production" and _settings.jwt_secret_key == "change-this-in-production-use-secrets-manager":
        logging.warning("Using default JWT_SECRET_KEY in production. Please set a secure secret!")
    
    return _settings


def get_settings() -> Settings:
    """
    Return initialized settings singleton.
    If not initialized, initializes now (lazy init for backward compatibility).
    """
    global _settings
    if _settings is None:
        return init_settings()
    return _settings


def setup_logging(s: Optional[Settings] = None):
    """
    Configure application logging with console and optional file handler.
    Call after init_settings() for best results.
    """
    if s is None:
        s = get_settings()
    
    level = getattr(logging, s.log_level.upper(), logging.INFO)
    handlers: List[logging.Handler] = []
    
    # Console handler (always enabled)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    handlers.append(stream_handler)
    
    # File handler (optional, for production)
    if s.log_file:
        try:
            file_handler = RotatingFileHandler(
                s.log_file,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            handlers.append(file_handler)
        except Exception as e:
            logging.warning(f"Failed to create log file handler: {e}")
    
    # Configure root logger
    logging.basicConfig(level=level, handlers=handlers, force=True)
    
    # Adjust uvicorn logger levels
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(level)


# Backward compatibility: expose settings at module level (lazy)
# Note: Prefer calling get_settings() in your code
settings = property(lambda self: get_settings())


class _SettingsProxy:
    """Proxy class to maintain backward compatibility with module-level settings."""
    def __getattr__(self, name):
        return getattr(get_settings(), name)


settings = _SettingsProxy()
