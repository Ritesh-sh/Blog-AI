"""
Image Fetcher Module
Fetches relevant images for blog posts from Unsplash API.
"""

import logging
import requests
from typing import List, Dict, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class ImageFetcher:
    """Fetches relevant images for blog content."""
    
    def __init__(self):
        """Initialize ImageFetcher with Unsplash API."""
        self.unsplash_access_key = getattr(settings, 'unsplash_access_key', '')
        self.base_url = "https://api.unsplash.com"
        self.timeout = 10
        
        if not self.unsplash_access_key:
            logger.warning("Unsplash API key not set. Image fetching will be disabled.")
    
    def fetch_images(
        self,
        keywords: List[str],
        num_images: int = 3,
        orientation: str = "landscape"
    ) -> List[Dict[str, str]]:
        """
        Fetch relevant images based on keywords.
        
        Args:
            keywords: List of search keywords
            num_images: Number of images to fetch (default: 3)
            orientation: Image orientation - landscape, portrait, or squarish
            
        Returns:
            List of image dictionaries with url, alt_text, photographer, etc.
        """
        if not self.unsplash_access_key:
            logger.warning("No Unsplash API key - returning empty image list")
            return []
        
        try:
            # Use top 3 keywords for search
            search_query = " ".join(keywords[:3]) if keywords else "blog post"
            logger.info(f"Searching Unsplash for images: '{search_query}'")
            
            # Call Unsplash search API
            response = requests.get(
                f"{self.base_url}/search/photos",
                params={
                    "query": search_query,
                    "per_page": num_images,
                    "orientation": orientation,
                    "content_filter": "high"  # Family-friendly content
                },
                headers={
                    "Authorization": f"Client-ID {self.unsplash_access_key}"
                },
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Unsplash API error: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                logger.warning(f"No images found for query: '{search_query}'")
                return []
            
            # Parse image data
            images = []
            for img in results[:num_images]:
                images.append({
                    "url": img["urls"]["regular"],
                    "url_small": img["urls"]["small"],
                    "url_thumb": img["urls"]["thumb"],
                    "alt_text": img.get("alt_description") or img.get("description") or search_query,
                    "photographer": img["user"]["name"],
                    "photographer_url": img["user"]["links"]["html"],
                    "download_location": img["links"]["download_location"]
                })
            
            logger.info(f"Successfully fetched {len(images)} images from Unsplash")
            return images
            
        except requests.exceptions.Timeout:
            logger.error("Unsplash API request timed out")
            return []
        except Exception as e:
            logger.error(f"Error fetching images from Unsplash: {str(e)}")
            return []
    
    def get_featured_image(self, keywords: List[str]) -> Optional[Dict[str, str]]:
        """
        Get a single featured image for the blog post.
        
        Args:
            keywords: List of keywords for search
            
        Returns:
            Single image dictionary or None
        """
        images = self.fetch_images(keywords, num_images=1)
        return images[0] if images else None
