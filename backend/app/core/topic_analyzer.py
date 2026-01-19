"""
Topic Analyzer Module
Analyzes text to understand topics, intent, and generate summaries using local NLP.
Detects website intent (service, product, blog, etc.) and extracts main topics.
"""

import logging
from typing import List, Dict, Literal
from collections import Counter
import re
from sentence_transformers import SentenceTransformer
from app.config import settings

logger = logging.getLogger(__name__)


class TopicAnalyzer:
    """Analyzes topics and intent from text using embeddings and heuristics."""
    
    def __init__(self):
        """Initialize with sentence transformer for semantic analysis."""
        try:
            self.model = SentenceTransformer(settings.embedding_model)
            logger.info(f"TopicAnalyzer initialized with model: {settings.embedding_model}")
        except Exception as e:
            logger.error(f"Failed to initialize TopicAnalyzer: {str(e)}")
            raise
        
        # Intent detection keywords
        self.intent_patterns = {
            'service': ['service', 'solution', 'consulting', 'help', 'support', 'provide', 'offer'],
            'product': ['buy', 'shop', 'product', 'price', 'purchase', 'store', 'cart', 'order'],
            'blog': ['article', 'blog', 'post', 'guide', 'tutorial', 'learn', 'read'],
            'informational': ['about', 'information', 'learn', 'understand', 'explain', 'what is'],
            'commercial': ['pricing', 'plans', 'subscribe', 'premium', 'pro', 'enterprise']
        }
    
    def extract_topics_from_keywords(self, keywords: List[str], top_n: int = 5) -> List[str]:
        """
        Extract main topics from keyword list.
        
        Args:
            keywords: List of keywords
            top_n: Number of topics to return
            
        Returns:
            List of main topics
        """
        # Simple approach: use keywords as topics
        # Can be enhanced with clustering or topic modeling
        return keywords[:top_n]
    
    def detect_intent(self, text: str, title: str = "") -> Literal['service', 'product', 'blog', 'informational', 'commercial']:
        """
        Detect website intent based on content patterns.
        
        Args:
            text: Content text
            title: Page title (optional)
            
        Returns:
            Detected intent type
        """
        text_lower = (text + " " + title).lower()
        
        # Count intent-related keywords
        intent_scores = {}
        for intent, keywords in self.intent_patterns.items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            intent_scores[intent] = score
        
        # Get intent with highest score
        if max(intent_scores.values()) == 0:
            return 'informational'  # Default
        
        detected_intent = max(intent_scores, key=intent_scores.get)
        logger.info(f"Detected intent: {detected_intent} (scores: {intent_scores})")
        
        return detected_intent
    
    def generate_summary(self, text: str, max_sentences: int = 3) -> str:
        """
        Generate a brief summary of the text.
        Uses simple extractive summarization (first sentences + key sentences).
        
        Args:
            text: Input text
            max_sentences: Maximum sentences in summary
            
        Returns:
            Summary text
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return ""
        
        # Simple approach: take first few sentences (usually most important)
        # Can be enhanced with sentence scoring using embeddings
        summary_sentences = sentences[:max_sentences]
        summary = '. '.join(summary_sentences) + '.'
        
        logger.info(f"Generated summary: {len(summary)} chars")
        return summary
    
    def extract_main_entities(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract main entities/concepts from text.
        Simple approach using capitalized words and noun phrases.
        
        Args:
            text: Input text
            top_n: Number of entities to return
            
        Returns:
            List of entities
        """
        # Extract capitalized words (likely proper nouns/entities)
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Count frequency
        entity_counts = Counter(words)
        
        # Get most common
        entities = [entity for entity, count in entity_counts.most_common(top_n)]
        
        return entities
    
    def analyze(self, text: str, title: str = "", keywords: List[str] = None) -> Dict:
        """
        Complete topic analysis pipeline.
        
        Args:
            text: Input text
            title: Page title (optional)
            keywords: Pre-extracted keywords (optional)
            
        Returns:
            Dictionary with analysis results
        """
        # Detect intent
        intent = self.detect_intent(text, title)
        
        # Generate summary
        summary = self.generate_summary(text)
        
        # Extract topics (from keywords if provided)
        if keywords:
            topics = self.extract_topics_from_keywords(keywords)
        else:
            topics = self.extract_main_entities(text, top_n=5)
        
        result = {
            'summary': summary,
            'intent': intent,
            'topics': topics,
            'content_length': len(text)
        }
        
        logger.info(f"Topic analysis complete - Intent: {intent}, Topics: {len(topics)}")
        
        return result


# Convenience function
def analyze_topics(text: str, title: str = "", keywords: List[str] = None) -> Dict:
    """
    Analyze topics and intent (convenience function).
    
    Args:
        text: Input text
        title: Page title
        keywords: Pre-extracted keywords
        
    Returns:
        Dictionary with analysis results
    """
    analyzer = TopicAnalyzer()
    return analyzer.analyze(text, title, keywords)
