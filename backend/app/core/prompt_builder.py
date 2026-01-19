"""
Prompt Builder Module
Constructs optimized prompts for LLM blog generation.
Combines extracted data (keywords, topics, intent) into structured prompts.
"""

import logging
from typing import Dict, List, Literal

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds structured prompts for blog generation."""
    
    # Base prompt template
    BLOG_GENERATION_TEMPLATE = """You are an expert SEO content writer. Generate a high-quality, original blog post based on the following information:

**SOURCE INFORMATION:**
Website URL: {url}
Website Title: {title}
Website Summary: {summary}
Website Intent: {intent}

**SEO KEYWORDS:**
Primary Keywords: {primary_keywords}
Secondary Keywords: {secondary_keywords}

**MAIN TOPICS:**
{topics}

**BLOG REQUIREMENTS:**
- Tone: {tone}
- Target Word Count: {word_count} words
- Include proper heading structure (H1, H2, H3)
- Make it SEO-optimized and engaging
- Write original content (do NOT copy from the source)
- Use keywords naturally throughout the content
- Include a compelling meta description (150-160 characters)
- Add a clear call-to-action at the end

**IMPORTANT INSTRUCTIONS:**
1. Create an engaging H1 title that includes primary keywords
2. Write a captivating introduction that hooks the reader
3. Organize content with clear H2 and H3 subheadings
4. Use the primary keywords {keyword_density_target}% throughout the content
5. Include actionable insights and value for readers
6. End with a strong conclusion and call-to-action
7. Generate a meta description optimized for search engines

**OUTPUT FORMAT:**
**OUTPUT FORMAT (IMPORTANT - READ CAREFULLY):**
- You MUST return ONLY a single valid JSON object. Do NOT include any explanatory text, headings, or markdown outside the JSON.
- The JSON must be parsable with a strict JSON parser (no trailing commas, use straight quotes, no comments).
- Return the JSON object exactly as shown below.
 
- Return a JSON object with the following structure:
{{
    "title": "Blog post title (H1)",
    "meta_description": "SEO meta description (150-160 chars)",
    "introduction": "Opening paragraph(s)",
    "sections": [
        {{"heading": "Section heading (H2)", "content": "Section content"}},
        {{"heading": "Another heading (H2)", "content": "Section content"}}
    ],
    "conclusion": "Closing paragraph(s)",
    "cta": "Call-to-action",
    "tags": ["tag1", "tag2", "tag3"]
}}

IMPORTANT: Do NOT include any text, explanation, or formatting outside the JSON object. Your entire response MUST be a single valid JSON object as shown above.
"""
    
    def __init__(self):
        pass
    
    def format_keywords(self, keywords: List[str]) -> str:
        """Format keyword list as comma-separated string."""
        return ", ".join(keywords) if keywords else "N/A"
    
    def format_topics(self, topics: List[str]) -> str:
        """Format topics as bullet points."""
        if not topics:
            return "- General content"
        return "\n".join([f"- {topic}" for topic in topics])
    
    def calculate_keyword_density_target(self, word_count: int) -> float:
        """
        Calculate target keyword density based on word count.
        Standard SEO practice: 1-2% for primary keywords.
        
        Args:
            word_count: Target word count
            
        Returns:
            Target keyword density as percentage
        """
        # For shorter content, slightly higher density is acceptable
        if word_count < 500:
            return 2.0
        elif word_count < 1000:
            return 1.5
        else:
            return 1.0
    
    def build_prompt(
        self,
        url: str,
        title: str,
        summary: str,
        intent: str,
        primary_keywords: List[str],
        secondary_keywords: List[str],
        topics: List[str],
        tone: Literal["professional", "casual", "technical", "conversational"],
        word_count: int
    ) -> str:
        """
        Build complete prompt for blog generation.
        
        Args:
            url: Source website URL
            title: Website title
            summary: Website summary
            intent: Detected intent (service, product, blog, etc.)
            primary_keywords: Primary SEO keywords
            secondary_keywords: Secondary SEO keywords
            topics: Main topics
            tone: Desired tone of blog
            word_count: Target word count
            
        Returns:
            Formatted prompt string
        """
        # Calculate keyword density target
        kw_density = self.calculate_keyword_density_target(word_count)
        
        # Format data
        prompt = self.BLOG_GENERATION_TEMPLATE.format(
            url=url,
            title=title or "N/A",
            summary=summary or "No summary available",
            intent=intent,
            primary_keywords=self.format_keywords(primary_keywords),
            secondary_keywords=self.format_keywords(secondary_keywords),
            topics=self.format_topics(topics),
            tone=tone,
            word_count=word_count,
            keyword_density_target=kw_density
        )
        
        logger.info(f"Built prompt with {len(prompt)} characters")
        logger.info(f"Target: {word_count} words, {len(primary_keywords)} primary keywords, tone: {tone}")
        
        return prompt
    
    def build_revision_prompt(self, original_blog: str, feedback: str) -> str:
        """
        Build prompt for blog revision based on feedback.
        
        Args:
            original_blog: Original blog content
            feedback: Revision feedback
            
        Returns:
            Revision prompt
        """
        prompt = f"""You are an expert content editor. Revise the following blog post based on the feedback provided.

**ORIGINAL BLOG:**
{original_blog}

**REVISION FEEDBACK:**
{feedback}

**INSTRUCTIONS:**
- Maintain the original structure and tone
- Apply the requested changes
- Ensure SEO optimization is maintained
- Keep the same output format (JSON)

Return the revised blog in the same JSON format as the original."""
        
        return prompt


# Convenience function
def build_blog_prompt(
    url: str,
    content_data: Dict,
    analysis_data: Dict,
    keyword_data: Dict,
    tone: str = "professional",
    word_count: int = 800
) -> str:
    """
    Build blog generation prompt (convenience function).
    
    Args:
        url: Source URL
        content_data: Extracted content data
        analysis_data: Topic analysis data
        keyword_data: Keyword extraction data
        tone: Blog tone
        word_count: Target word count
        
    Returns:
        Formatted prompt
    """
    builder = PromptBuilder()
    
    return builder.build_prompt(
        url=url,
        title=content_data.get('title', ''),
        summary=analysis_data.get('summary', ''),
        intent=analysis_data.get('intent', 'informational'),
        primary_keywords=keyword_data.get('primary_keywords', []),
        secondary_keywords=keyword_data.get('secondary_keywords', []),
        topics=analysis_data.get('topics', []),
        tone=tone,
        word_count=word_count
    )
