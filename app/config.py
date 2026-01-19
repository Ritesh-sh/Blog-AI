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
    
    # LLM Provider Configuration
    llm_provider: str = "gemini"  # "gemini" or "openai"
    
    # Gemini Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3-flash-preview"
    
    # OpenAI Configuration (alternative provider)
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    
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
    unsplash_access_key: str = ""
    
    # MongoDB Atlas Configuration
    mongodb_uri: str = ""  # mongodb+srv://<user>:<pass>@cluster0.mongodb.net
    mongodb_db: str = "blog_generator"
    
    # JWT / Auth Configuration
    jwt_secret_key: str = "change-this-in-production-use-secrets-manager"
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
    
    # Validate LLM provider
    if _settings.llm_provider.lower() not in ("openai", "gemini"):
        logging.warning(f"Unknown LLM_PROVIDER: {_settings.llm_provider}. Defaulting to 'gemini'.")
        _settings.llm_provider = "gemini"
    
    # Warn on missing API keys
    if _settings.llm_provider.lower() == "openai" and not _settings.openai_api_key:
        logging.warning("LLM_PROVIDER=openai but OPENAI_API_KEY is not set.")
    if _settings.llm_provider.lower() == "gemini" and not _settings.gemini_api_key:
        logging.warning("LLM_PROVIDER=gemini but GEMINI_API_KEY is not set.")
    
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
