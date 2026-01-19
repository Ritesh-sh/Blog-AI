"""
Text Cleaner Module
Cleans and normalizes extracted text for NLP processing.
Removes noise, normalizes whitespace, and prepares text for analysis.
"""

import logging
import re
from typing import List

logger = logging.getLogger(__name__)


class TextCleaner:
    """Cleans and normalizes extracted text."""
    
    def __init__(self):
        # Patterns to remove or normalize
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.multiple_spaces = re.compile(r'\s+')
        self.multiple_newlines = re.compile(r'\n\s*\n')
        self.special_chars = re.compile(r'[^\w\s.,!?;:\'\"-]')
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return self.url_pattern.sub('', text)
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses from text."""
        return self.email_pattern.sub('', text)
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace (multiple spaces and newlines)."""
        text = self.multiple_spaces.sub(' ', text)
        text = self.multiple_newlines.sub('\n\n', text)
        return text.strip()
    
    def remove_special_characters(self, text: str, keep_basic_punctuation: bool = True) -> str:
        """
        Remove special characters while optionally keeping punctuation.
        
        Args:
            text: Text to clean
            keep_basic_punctuation: If True, keeps .,!?;:'"-
        """
        if keep_basic_punctuation:
            # Only remove truly special chars (emojis, symbols, etc.)
            return self.special_chars.sub('', text)
        else:
            # Remove everything except alphanumeric and spaces
            return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    def remove_short_lines(self, text: str, min_length: int = 20) -> str:
        """
        Remove very short lines (likely navigation or boilerplate).
        
        Args:
            text: Text to clean
            min_length: Minimum character length for a line to keep
        """
        lines = text.split('\n')
        cleaned_lines = [line for line in lines if len(line.strip()) >= min_length]
        return '\n'.join(cleaned_lines)
    
    def clean(self, text: str, aggressive: bool = False) -> str:
        """
        Main cleaning pipeline.
        
        Args:
            text: Text to clean
            aggressive: If True, applies more aggressive cleaning
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Step 1: Remove URLs and emails
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        
        # Step 2: Remove special characters (keep basic punctuation)
        text = self.remove_special_characters(text, keep_basic_punctuation=True)
        
        # Step 3: Normalize whitespace
        text = self.normalize_whitespace(text)
        
        # Step 4: Remove very short lines (optional, for aggressive cleaning)
        if aggressive:
            text = self.remove_short_lines(text, min_length=30)
        
        # Step 5: Final normalization
        text = text.strip()
        
        logger.info(f"Text cleaned: {len(text)} chars remaining")
        return text
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences (simple approach).
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with NLTK)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def get_preview(self, text: str, max_chars: int = 200) -> str:
        """
        Get a preview of cleaned text.
        
        Args:
            text: Text to preview
            max_chars: Maximum characters in preview
            
        Returns:
            Preview string
        """
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."


# Convenience function
def clean_text(text: str, aggressive: bool = False) -> str:
    """
    Clean text (convenience function).
    
    Args:
        text: Text to clean
        aggressive: Apply aggressive cleaning
        
    Returns:
        Cleaned text
    """
    cleaner = TextCleaner()
    return cleaner.clean(text, aggressive=aggressive)
