"""
Keyword Extractor Module
Extracts important keywords from text using KeyBERT (local NLP, no LLM required).
Identifies primary and secondary keywords with their relevance scores.
"""

import logging
from typing import List, Tuple, Dict
from keybert import KeyBERT
from app.config import settings

logger = logging.getLogger(__name__)


class KeywordExtractor:
    """Extracts keywords using KeyBERT and sentence transformers."""
    
    def __init__(self):
        """Initialize KeyBERT with lightweight embedding model."""
        try:
            # Use lightweight model for cost optimization
            self.model = KeyBERT(model=settings.embedding_model)
            logger.info(f"KeyBERT initialized with model: {settings.embedding_model}")
        except Exception as e:
            logger.error(f"Failed to initialize KeyBERT: {str(e)}")
            raise
    
    def extract_keywords(
        self, 
        text: str, 
        top_n: int = 15,
        keyphrase_ngram_range: Tuple[int, int] = (1, 2),
        use_maxsum: bool = True,
        diversity: float = 0.5
    ) -> List[Tuple[str, float]]:
        """
        Extract keywords from text using KeyBERT.
        
        Args:
            text: Input text
            top_n: Number of keywords to extract
            keyphrase_ngram_range: Range of n-grams (1,1) for single words, (1,2) for 1-2 word phrases
            use_maxsum: Use Max Sum Similarity for diversity
            diversity: Diversity of results (0.0 = similar, 1.0 = diverse)
            
        Returns:
            List of (keyword, score) tuples
        """
        try:
            if not text or len(text.strip()) < 50:
                logger.warning("Text too short for keyword extraction")
                return []
            
            # Extract keywords
            keywords = self.model.extract_keywords(
                text,
                keyphrase_ngram_range=keyphrase_ngram_range,
                stop_words='english',
                top_n=top_n,
                use_maxsum=use_maxsum,
                diversity=diversity
            )
            
            logger.info(f"Extracted {len(keywords)} keywords")
            return keywords
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {str(e)}")
            return []
    
    def categorize_keywords(
        self, 
        keywords: List[Tuple[str, float]], 
        primary_threshold: float = 0.3
    ) -> Dict[str, List[str]]:
        """
        Categorize keywords into primary and secondary based on relevance score.
        
        Args:
            keywords: List of (keyword, score) tuples
            primary_threshold: Minimum score for primary keywords
            
        Returns:
            Dictionary with 'primary' and 'secondary' keyword lists
        """
        primary = []
        secondary = []
        
        for keyword, score in keywords:
            if score >= primary_threshold:
                primary.append(keyword)
            else:
                secondary.append(keyword)
        
        return {
            'primary': primary[:5],  # Top 5 primary
            'secondary': secondary[:10]  # Top 10 secondary
        }
    
    def calculate_keyword_density(
        self, 
        text: str, 
        keywords: List[str]
    ) -> Dict[str, float]:
        """
        Calculate keyword density (frequency) in text.
        
        Args:
            text: Original text
            keywords: List of keywords to check
            
        Returns:
            Dictionary mapping keyword to density (0.0-1.0)
        """
        text_lower = text.lower()
        words = text_lower.split()
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        density = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = text_lower.count(keyword_lower)
            density[keyword] = round(count / total_words, 4)
        
        return density
    
    def extract_and_categorize(self, text: str) -> Dict:
        """
        Complete keyword extraction pipeline.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with categorized keywords and density info
        """
        # Extract keywords
        keywords = self.extract_keywords(text)
        
        if not keywords:
            return {
                'primary_keywords': [],
                'secondary_keywords': [],
                'keyword_density': {},
                'all_keywords': []
            }
        
        # Categorize
        categorized = self.categorize_keywords(keywords)
        
        # Calculate density
        all_keywords = categorized['primary'] + categorized['secondary']
        density = self.calculate_keyword_density(text, all_keywords)
        
        result = {
            'primary_keywords': categorized['primary'],
            'secondary_keywords': categorized['secondary'],
            'keyword_density': density,
            'all_keywords': [kw for kw, score in keywords]
        }
        
        logger.info(f"Keywords extracted - Primary: {len(result['primary_keywords'])}, "
                   f"Secondary: {len(result['secondary_keywords'])}")
        
        return result


# Convenience function
def extract_keywords(text: str) -> Dict:
    """
    Extract keywords from text (convenience function).
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with keyword data
    """
    extractor = KeywordExtractor()
    return extractor.extract_and_categorize(text)
