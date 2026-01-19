"""
SEO Post-Processor Module
Post-processes generated blog content to improve SEO and readability.
Ensures keyword coverage, validates meta descriptions, and optimizes structure.
"""

import logging
import re
from typing import Dict, List
from collections import Counter

logger = logging.getLogger(__name__)


class SEOPostProcessor:
    """Post-processes blog content for SEO optimization."""
    
    def __init__(self):
        # SEO best practices
        self.meta_description_min = 150
        self.meta_description_max = 160
        self.title_max_length = 60
        self.min_word_count = 300
        self.keyword_density_min = 0.005  # 0.5%
        self.keyword_density_max = 0.025  # 2.5%
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)
    
    def get_full_text(self, blog_data: Dict) -> str:
        """
        Extract all text from blog structure.
        
        Args:
            blog_data: Blog content dictionary
            
        Returns:
            Complete blog text
        """
        text_parts = [
            blog_data.get('title', ''),
            blog_data.get('introduction', ''),
            blog_data.get('conclusion', ''),
        ]
        
        # Add section content
        for section in blog_data.get('sections', []):
            text_parts.append(section.get('heading', ''))
            text_parts.append(section.get('content', ''))
        
        return ' '.join(text_parts)
    
    def check_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """
        Check keyword density in content.
        
        Args:
            text: Full blog text
            keywords: List of keywords to check
            
        Returns:
            Dictionary of keyword densities
        """
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        densities = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count occurrences (including multi-word keywords)
            count = text_lower.count(keyword_lower)
            density = count / total_words
            densities[keyword] = round(density, 4)
        
        return densities
    
    def validate_meta_description(self, meta_description: str) -> Dict:
        """
        Validate meta description length and quality.
        
        Args:
            meta_description: Meta description text
            
        Returns:
            Validation results
        """
        length = len(meta_description)
        
        result = {
            'length': length,
            'is_valid': self.meta_description_min <= length <= self.meta_description_max,
            'issue': None
        }
        
        if length < self.meta_description_min:
            result['issue'] = f"Too short (minimum {self.meta_description_min} chars)"
        elif length > self.meta_description_max:
            result['issue'] = f"Too long (maximum {self.meta_description_max} chars, will be truncated)"
        
        return result
    
    def validate_title(self, title: str) -> Dict:
        """
        Validate title length for SEO.
        
        Args:
            title: Blog title
            
        Returns:
            Validation results
        """
        length = len(title)
        
        result = {
            'length': length,
            'is_valid': length <= self.title_max_length,
            'issue': None
        }
        
        if length > self.title_max_length:
            result['issue'] = f"Too long (maximum {self.title_max_length} chars for optimal SEO)"
        
        return result
    
    def check_heading_structure(self, blog_data: Dict) -> Dict:
        """
        Check if heading structure is proper (H1 -> H2 -> H3).
        
        Args:
            blog_data: Blog content dictionary
            
        Returns:
            Structure validation results
        """
        sections = blog_data.get('sections', [])
        
        result = {
            'has_h1': bool(blog_data.get('title')),
            'h2_count': len(sections),
            'is_valid': True,
            'recommendations': []
        }
        
        if not result['has_h1']:
            result['is_valid'] = False
            result['recommendations'].append("Add an H1 title")
        
        if result['h2_count'] < 3:
            result['recommendations'].append("Add more H2 sections (3-5 recommended)")
        elif result['h2_count'] > 7:
            result['recommendations'].append("Consider consolidating sections (3-7 H2s optimal)")
        
        return result
    
    def generate_readability_score(self, text: str) -> Dict:
        """
        Simple readability assessment.
        Based on average sentence length and word length.
        
        Args:
            text: Text to analyze
            
        Returns:
            Readability metrics
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = re.findall(r'\b\w+\b', text)
        
        if not sentences or not words:
            return {'score': 'N/A', 'level': 'unknown'}
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple scoring
        if avg_sentence_length < 15 and avg_word_length < 5:
            level = 'easy'
        elif avg_sentence_length < 20 and avg_word_length < 6:
            level = 'medium'
        else:
            level = 'complex'
        
        return {
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 1),
            'level': level
        }
    
    def process(self, blog_data: Dict, keywords: List[str]) -> Dict:
        """
        Complete SEO post-processing pipeline.
        
        Args:
            blog_data: Generated blog content
            keywords: Target keywords for SEO
            
        Returns:
            Dictionary with processed blog and SEO analysis
        """
        # Get full text
        full_text = self.get_full_text(blog_data)
        word_count = self.count_words(full_text)
        
        # Validate components
        meta_validation = self.validate_meta_description(blog_data.get('meta_description', ''))
        title_validation = self.validate_title(blog_data.get('title', ''))
        heading_structure = self.check_heading_structure(blog_data)
        
        # Check keyword density
        keyword_densities = self.check_keyword_density(full_text, keywords)
        
        # Generate readability score
        readability = self.generate_readability_score(full_text)
        
        # SEO recommendations
        recommendations = []
        
        if word_count < self.min_word_count:
            recommendations.append(f"Content is short ({word_count} words). Aim for {self.min_word_count}+ words.")
        
        if not meta_validation['is_valid']:
            recommendations.append(f"Meta description issue: {meta_validation['issue']}")
        
        if not title_validation['is_valid']:
            recommendations.append(f"Title issue: {title_validation['issue']}")
        
        # Check keyword usage
        low_density_keywords = [kw for kw, density in keyword_densities.items() 
                               if density < self.keyword_density_min]
        if low_density_keywords:
            recommendations.append(f"Keywords underused: {', '.join(low_density_keywords[:3])}")
        
        recommendations.extend(heading_structure.get('recommendations', []))
        
        result = {
            'blog': blog_data,
            'seo_analysis': {
                'word_count': word_count,
                'keyword_densities': keyword_densities,
                'meta_description': meta_validation,
                'title': title_validation,
                'heading_structure': heading_structure,
                'readability': readability,
                'recommendations': recommendations,
                'seo_score': self._calculate_seo_score(
                    meta_validation, title_validation, 
                    heading_structure, word_count, keyword_densities
                )
            }
        }
        
        logger.info(f"SEO post-processing complete - Score: {result['seo_analysis']['seo_score']}/100")
        
        return result
    
    def _calculate_seo_score(
        self, 
        meta_val: Dict, 
        title_val: Dict, 
        heading_struct: Dict, 
        word_count: int,
        keyword_densities: Dict
    ) -> int:
        """
        Calculate overall SEO score (0-100).
        
        Returns:
            SEO score
        """
        score = 0
        
        # Meta description (20 points)
        if meta_val['is_valid']:
            score += 20
        
        # Title (15 points)
        if title_val['is_valid']:
            score += 15
        
        # Heading structure (15 points)
        if heading_struct['is_valid'] and 3 <= heading_struct['h2_count'] <= 7:
            score += 15
        
        # Word count (25 points)
        if word_count >= 800:
            score += 25
        elif word_count >= 500:
            score += 15
        elif word_count >= self.min_word_count:
            score += 10
        
        # Keyword usage (25 points)
        if keyword_densities:
            good_keywords = [d for d in keyword_densities.values() 
                           if self.keyword_density_min <= d <= self.keyword_density_max]
            score += int((len(good_keywords) / len(keyword_densities)) * 25)
        
        return min(score, 100)


# Convenience function
def postprocess_blog(blog_data: Dict, keywords: List[str]) -> Dict:
    """
    Post-process blog for SEO (convenience function).
    
    Args:
        blog_data: Generated blog content
        keywords: Target keywords
        
    Returns:
        Processed blog with SEO analysis
    """
    processor = SEOPostProcessor()
    return processor.process(blog_data, keywords)
