"""
Content Extractor Module
Extracts main textual content from web pages using BeautifulSoup and newspaper3k.
Focuses on article content while filtering out navigation, ads, and boilerplate.
"""

import logging
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from app.config import settings

logger = logging.getLogger(__name__)


class ContentExtractor:
    """Extracts meaningful content from web pages."""
    
    def __init__(self):
        self.timeout = settings.request_timeout
        self.max_length = settings.max_content_length
    
    def extract_with_newspaper(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract content using newspaper3k library.
        Best for article-style content and blogs.
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary with extracted content or None
        """
        try:
            article = Article(str(url))
            article.download()
            article.parse()
            
            # Extract metadata
            content = {
                'title': article.title or '',
                'text': article.text or '',
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else None,
                'top_image': article.top_image or '',
                'meta_description': article.meta_description or '',
                'meta_keywords': article.meta_keywords,
            }
            
            if content['text']:
                logger.info(f"Successfully extracted content using newspaper3k: {len(content['text'])} chars")
                return content
            
            return None
            
        except Exception as e:
            logger.warning(f"Newspaper extraction failed: {str(e)}")
            return None
    
    def extract_with_beautifulsoup(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract content using BeautifulSoup.
        More flexible, works for various page types.
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary with extracted content or None
        """
        try:
            # Fetch page
            response = requests.get(
                str(url),
                timeout=self.timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 
                                'aside', 'form', 'iframe', 'noscript']):
                element.decompose()
            
            # Extract title
            title = ''
            if soup.title:
                title = soup.title.string or ''
            elif soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            
            # Extract meta description
            meta_desc = ''
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag and meta_tag.get('content'):
                meta_desc = meta_tag['content']
            
            # Extract main content
            # Priority: article, main, div with specific classes
            main_content = None
            for tag in ['article', 'main', ['div', {'class': ['content', 'post', 'entry']}]]:
                if isinstance(tag, list):
                    main_content = soup.find(tag[0], tag[1])
                else:
                    main_content = soup.find(tag)
                if main_content:
                    break
            
            # Fallback to body
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                # Extract paragraphs
                paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li'])
                text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
                content = {
                    'title': title,
                    'text': text,
                    'meta_description': meta_desc,
                    'authors': [],
                    'publish_date': None,
                    'top_image': '',
                    'meta_keywords': [],
                }
                
                if text:
                    logger.info(f"Successfully extracted content using BeautifulSoup: {len(text)} chars")
                    return content
            
            return None
            
        except Exception as e:
            logger.warning(f"BeautifulSoup extraction failed: {str(e)}")
            return None
    
    def extract(self, url: str) -> Dict[str, str]:
        """
        Extract content from URL using multiple methods.
        Tries newspaper3k first, falls back to BeautifulSoup.
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary with extracted content
            
        Raises:
            ValueError: If content extraction fails
        """
        # Try newspaper3k first (better for articles)
        content = self.extract_with_newspaper(url)
        
        # Fallback to BeautifulSoup
        if not content or not content.get('text'):
            content = self.extract_with_beautifulsoup(url)
        
        # Validate extraction
        if not content or not content.get('text'):
            raise ValueError("Failed to extract content from URL")
        
        # Truncate if too long (cost optimization)
        if len(content['text']) > self.max_length:
            logger.info(f"Truncating content from {len(content['text'])} to {self.max_length} chars")
            content['text'] = content['text'][:self.max_length]
        
        logger.info(f"Content extraction complete: {len(content['text'])} chars")
        return content


# Convenience function
def extract_content(url: str) -> Dict[str, str]:
    """
    Extract content from URL (convenience function).
    
    Args:
        url: URL to extract from
        
    Returns:
        Dictionary with extracted content
    """
    extractor = ContentExtractor()
    return extractor.extract(url)
