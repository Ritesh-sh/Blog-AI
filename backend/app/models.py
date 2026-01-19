"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal
from datetime import datetime


class BlogGenerationRequest(BaseModel):
    """Request model for blog generation endpoint."""
    
    url: HttpUrl = Field(..., description="Website URL to generate blog from")
    tone: Literal["professional", "casual", "technical", "conversational"] = Field(
        default="professional",
        description="Tone of the generated blog"
    )
    word_count: int = Field(
        default=800,
        ge=300,
        le=2000,
        description="Target word count for the blog (300-2000)"
    )
    include_meta: bool = Field(
        default=True,
        description="Include meta description and SEO elements"
    )


class KeywordData(BaseModel):
    """Extracted keyword information."""
    
    primary_keywords: List[str] = Field(description="Main keywords (top 5)")
    secondary_keywords: List[str] = Field(description="Supporting keywords (top 10)")
    keyword_density: dict = Field(description="Keyword frequency mapping")


class ContentAnalysis(BaseModel):
    """Website content analysis result."""
    
    summary: str = Field(description="Brief summary of website content")
    intent: Literal["service", "product", "blog", "informational", "commercial"] = Field(
        description="Detected website intent"
    )
    topics: List[str] = Field(description="Main topics identified")
    content_length: int = Field(description="Extracted content length in characters")


class ImageData(BaseModel):
    """Image data model."""
    
    url: str = Field(description="Full-size image URL")
    url_small: str = Field(description="Small image URL")
    url_thumb: str = Field(description="Thumbnail URL")
    alt_text: str = Field(description="Alt text for accessibility and SEO")
    photographer: str = Field(description="Photographer name")
    photographer_url: str = Field(description="Photographer profile URL")


class BlogContent(BaseModel):
    """Generated blog structure."""
    
    title: str = Field(description="Blog post title (H1)")
    meta_description: str = Field(description="SEO meta description (150-160 chars)")
    introduction: str = Field(description="Opening paragraph")
    sections: List[dict] = Field(
        description="List of sections with heading and content"
    )
    conclusion: str = Field(description="Closing paragraph")
    cta: str = Field(description="Call-to-action")
    tags: List[str] = Field(description="Suggested tags")
    featured_image: Optional[ImageData] = Field(default=None, description="Featured image for blog header")
    additional_images: List[ImageData] = Field(default=[], description="Additional images for blog sections")


class BlogGenerationResponse(BaseModel):
    """Response model for successful blog generation."""
    
    success: bool = True
    blog: BlogContent
    keywords: KeywordData
    analysis: ContentAnalysis
    word_count: int
    generated_at: datetime = Field(default_factory=datetime.now)
    source_url: Optional[str] = Field(default=None, description="Original website URL")
    processing_time: float = Field(description="Time taken in seconds")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = False
    error: str = Field(description="Error message")
    details: Optional[str] = Field(default=None, description="Additional error details")
