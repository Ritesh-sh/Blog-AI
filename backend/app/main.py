"""
FastAPI Application - Main Entry Point
Orchestrates the complete blog generation pipeline.
"""

import logging
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.models import (
    BlogGenerationRequest,
    BlogGenerationResponse,
    ErrorResponse,
    KeywordData,
    ContentAnalysis,
    BlogContent,
    ImageData
)
from app.config import init_settings, setup_logging, get_settings
from app.core.url_validator import URLValidator
from app.core.content_extractor import ContentExtractor
from app.core.text_cleaner import TextCleaner
from app.core.keyword_extractor import KeywordExtractor
from app.core.topic_analyzer import TopicAnalyzer
from app.core.prompt_builder import PromptBuilder
from app.core.blog_generator import BlogGenerator
from app.core.seo_postprocessor import SEOPostProcessor
from app.core.image_fetcher import ImageFetcher
from app.auth import get_current_user, log_user_action, TokenData
from app.db import get_blogs_collection
from bson import ObjectId

logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Initialize settings and logging at startup
    settings = init_settings()
    setup_logging(settings)
    
    logger.info("Starting AI Blog Generator API...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Gemini Model: {settings.gemini_model}")
    
    # Initialize MongoDB connection if configured
    if settings.mongodb_uri:
        try:
            from app.db import check_mongo_connection
            if await check_mongo_connection():
                logger.info("MongoDB Atlas connection established")
            else:
                logger.warning("MongoDB Atlas connection failed - DB features disabled")
        except Exception as e:
            logger.warning(f"MongoDB initialization skipped: {e}")
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down AI Blog Generator API...")
    if settings.mongodb_uri:
        try:
            from app.db import close_mongo_connection
            await close_mongo_connection()
        except Exception:
            pass


# Initialize FastAPI app
app = FastAPI(
    title="AI Blog Generator API",
    description="Generate SEO-optimized blog posts from website URLs using AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - use settings for allowed origins
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router
from app.routes.auth import router as auth_router
app.include_router(auth_router)

# Initialize components (singleton pattern for better performance)
url_validator = URLValidator()
content_extractor = ContentExtractor()
text_cleaner = TextCleaner()
keyword_extractor = KeywordExtractor()
topic_analyzer = TopicAnalyzer()
prompt_builder = PromptBuilder()
blog_generator = BlogGenerator()
seo_postprocessor = SEOPostProcessor()
image_fetcher = ImageFetcher()


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "service": "AI Blog Generator API",
        "version": "1.0.0",
        "status": "operational",
        "gemini_model": settings.gemini_model
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


@app.post(
    "/generate-blog",
    response_model=BlogGenerationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def generate_blog(request: BlogGenerationRequest, current_user: TokenData = Depends(get_current_user)):
    """
    Generate SEO-optimized blog post from website URL.
    
    This endpoint orchestrates the complete pipeline:
    1. URL validation
    2. Content extraction
    3. Text cleaning
    4. Keyword extraction (local NLP)
    5. Topic analysis (local NLP)
    6. Prompt building
    7. Blog generation (LLM)
    8. SEO post-processing
    
    Args:
        request: BlogGenerationRequest with URL and parameters
        
    Returns:
        BlogGenerationResponse with generated blog and analysis
    """
    start_time = time.time()
    url = str(request.url)
    
    try:
        logger.info(f"Starting blog generation for URL: {url}")
        
        # Step 1: Validate URL
        logger.info("Step 1/8: Validating URL...")
        is_valid, error_msg = url_validator.validate(url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"URL validation failed: {error_msg}")
        
        # Step 2: Extract content
        logger.info("Step 2/8: Extracting content...")
        try:
            content_data = content_extractor.extract(url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Content extraction failed: {str(e)}")
        
        # Step 3: Clean text
        logger.info("Step 3/8: Cleaning text...")
        cleaned_text = text_cleaner.clean(content_data['text'])
        if not cleaned_text:
            raise HTTPException(status_code=400, detail="No usable content found after cleaning")
        
        # Step 4: Extract keywords (local NLP)
        logger.info("Step 4/8: Extracting keywords...")
        keyword_data = keyword_extractor.extract_and_categorize(cleaned_text)
        
        # Step 5: Analyze topics (local NLP)
        logger.info("Step 5/8: Analyzing topics...")
        analysis_data = topic_analyzer.analyze(
            cleaned_text,
            title=content_data.get('title', ''),
            keywords=keyword_data.get('primary_keywords', [])
        )
        
        # Step 6: Build prompt
        logger.info("Step 6/8: Building prompt...")
        prompt = prompt_builder.build_prompt(
            url=url,
            title=content_data.get('title', ''),
            summary=analysis_data['summary'],
            intent=analysis_data['intent'],
            primary_keywords=keyword_data['primary_keywords'],
            secondary_keywords=keyword_data['secondary_keywords'],
            topics=analysis_data['topics'],
            tone=request.tone,
            word_count=request.word_count
        )
        
        # Step 7: Generate blog (LLM call)
        logger.info("Step 7/9: Generating blog with LLM...")
        try:
            blog_data = blog_generator.generate(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Blog generation failed: {str(e)}")
        
        # Step 8: Fetch images
        logger.info("Step 8/9: Fetching relevant images...")
        featured_image = None
        additional_images = []
        
        if settings.unsplash_access_key:
            try:
                # Get featured image
                featured_image_data = image_fetcher.get_featured_image(
                    keywords=keyword_data['primary_keywords']
                )
                if featured_image_data:
                    featured_image = ImageData(**featured_image_data)
                
                # Get additional images for sections
                additional_images_data = image_fetcher.fetch_images(
                    keywords=keyword_data['primary_keywords'],
                    num_images=3
                )
                additional_images = [ImageData(**img) for img in additional_images_data]
                logger.info(f"Fetched {len(additional_images)} images successfully")
            except Exception as e:
                logger.warning(f"Image fetching failed (non-critical): {str(e)}")
        else:
            logger.warning("Unsplash API key not configured - skipping image fetch")
        
        # Step 9: SEO post-processing (if requested)
        logger.info("Step 9/9: Post-processing for SEO...")
        all_keywords = keyword_data['primary_keywords'] + keyword_data['secondary_keywords']
        processed_result = seo_postprocessor.process(blog_data, all_keywords)
        
        # Add images to blog content
        processed_result['blog']['featured_image'] = featured_image
        processed_result['blog']['additional_images'] = additional_images
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Build response
        blog_content = BlogContent(**processed_result['blog'])
        word_count_value = processed_result['seo_analysis']['word_count']
        processing_time_value = round(processing_time, 2)

        response = BlogGenerationResponse(
            success=True,
            blog=blog_content,
            keywords=KeywordData(
                primary_keywords=keyword_data['primary_keywords'],
                secondary_keywords=keyword_data['secondary_keywords'],
                keyword_density=keyword_data['keyword_density']
            ),
            analysis=ContentAnalysis(
                summary=analysis_data['summary'],
                intent=analysis_data['intent'],
                topics=analysis_data['topics'],
                content_length=analysis_data['content_length']
            ),
            word_count=word_count_value,
            processing_time=processing_time_value
        )

        logger.info(f"Blog generation completed in {processing_time:.2f}s")
        logger.info(f"SEO Score: {processed_result['seo_analysis']['seo_score']}/100")

        blog_doc = {
            "user_id": current_user.user_id,
            "url": url,
            "title": blog_content.title,
            "generated_at": datetime.utcnow(),
            "blog": blog_content.dict(),
            "keywords": response.keywords.dict(),
            "analysis": response.analysis.dict(),
            "word_count": word_count_value,
            "processing_time": processing_time_value,
        }

        blogs_collection = get_blogs_collection()
        insert_result = await blogs_collection.insert_one(blog_doc)
        blog_id = str(insert_result.inserted_id)

        await log_user_action(
            current_user.user_id,
            "generate_blog",
            {
                "url": url,
                "title": blog_content.title,
                "blog_id": blog_id
            }
        )

        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/blogs/{blog_id}", response_model=BlogGenerationResponse)
async def get_blog(blog_id: str, current_user: TokenData = Depends(get_current_user)):
    """Retrieve a previously generated blog for the authenticated user."""
    try:
        oid = ObjectId(blog_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid blog ID")

    collection = get_blogs_collection()
    doc = await collection.find_one({"_id": oid, "user_id": current_user.user_id})
    if doc is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    return BlogGenerationResponse(
        success=True,
        blog=BlogContent(**doc["blog"]),
        keywords=KeywordData(**doc["keywords"]),
        analysis=ContentAnalysis(**doc["analysis"]),
        word_count=doc.get("word_count", 0),
        processing_time=doc.get("processing_time", 0.0),
        generated_at=doc.get("generated_at", datetime.utcnow())
    )


@app.post("/estimate-cost")
async def estimate_cost(url: str, word_count: int = 800):
    """
    Estimate API cost for generating a blog.
    
    Args:
        url: Website URL
        word_count: Target word count
        
    Returns:
        Cost estimation in USD
    """
    try:
        # Rough estimation
        prompt_length = 2000  # Average prompt length
        output_length = word_count * 6  # Rough char estimate
        
        generator = BlogGenerator()
        estimated_cost = generator.estimate_cost(prompt_length, output_length)
        
        return {
            "url": url,
            "word_count": word_count,
            "estimated_cost_usd": round(estimated_cost, 4),
            "provider": "Google Gemini",
            "model": generator.model
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=exc.detail,
            details=f"Status code: {exc.status_code}"
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal server error",
            details=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.app_env == "development"
    )