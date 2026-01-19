"""
URL Validator Module
Validates URL format and checks accessibility before processing.
"""

import logging
import re
from typing import Tuple
from urllib.parse import urlparse
import requests
from app.config import settings

logger = logging.getLogger(__name__)


class URLValidator:
    """Validates and checks URL accessibility."""
    
    def __init__(self):
        self.timeout = settings.request_timeout
        # Common patterns to exclude
        self.excluded_domains = ['localhost', '127.0.0.1', '0.0.0.0']
    
    def validate_url_format(self, url: str) -> Tuple[bool, str]:
        """
        Validate URL format and structure.
        
        Args:
            url: URL string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Basic format check
            if not url or not isinstance(url, str):
                return False, "URL must be a non-empty string"
            
            # Parse URL
            parsed = urlparse(str(url))
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False, "URL must start with http:// or https://"
            
            # Check if domain exists
            if not parsed.netloc:
                return False, "Invalid URL: missing domain"
            
            # Check for excluded domains (localhost, etc.)
            if any(excluded in parsed.netloc.lower() for excluded in self.excluded_domains):
                return False, f"Local URLs are not supported"
            
            logger.info(f"URL format validation passed: {url}")
            return True, ""
            
        except Exception as e:
            logger.error(f"URL format validation error: {str(e)}")
            return False, f"Invalid URL format: {str(e)}"
    
    def check_accessibility(self, url: str) -> Tuple[bool, str, int]:
        """
        Check if URL is accessible via HTTP request.
        
        Args:
            url: URL to check
            
        Returns:
            Tuple of (is_accessible, error_message, status_code)
        """
        try:
            # Send HEAD request first (faster)
            response = requests.head(
                str(url),
                timeout=self.timeout,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            status_code = response.status_code
            
            # Check if successful (2xx or 3xx)
            if 200 <= status_code < 400:
                logger.info(f"URL accessible: {url} (Status: {status_code})")
                return True, "", status_code
            else:
                return False, f"HTTP {status_code}: URL not accessible", status_code
                
        except requests.exceptions.Timeout:
            return False, "Request timeout: URL took too long to respond", 0
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Unable to reach URL", 0
        except requests.exceptions.TooManyRedirects:
            return False, "Too many redirects", 0
        except Exception as e:
            logger.error(f"Accessibility check error: {str(e)}")
            return False, f"Error checking URL: {str(e)}", 0
    
    def validate(self, url: str) -> Tuple[bool, str]:
        """
        Complete URL validation: format and accessibility.
        
        Args:
            url: URL to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Step 1: Validate format
        is_valid_format, format_error = self.validate_url_format(url)
        if not is_valid_format:
            return False, format_error
        
        # Step 2: Check accessibility
        is_accessible, access_error, status_code = self.check_accessibility(url)
        if not is_accessible:
            return False, access_error
        
        logger.info(f"URL validation successful: {url}")
        return True, ""


# Convenience function
def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate a URL (convenience function).
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = URLValidator()
    return validator.validate(url)
