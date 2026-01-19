"""
Gradio Frontend Interface - Simplified for compatibility.
All images are embedded directly in HTML to avoid Gradio component issues.
Production-ready with environment-driven configuration.
"""

import os
import gradio as gr
import requests
from typing import Dict, Tuple

# Import settings lazily to avoid initialization at import time
def get_api_url() -> str:
    """Get API URL from environment or default."""
    return os.getenv("API_URL", "http://localhost:8000")

def get_app_settings():
    """Get app settings lazily."""
    try:
        from app.config import get_settings
        return get_settings()
    except ImportError:
        return None

# API endpoint (configurable via environment)
API_URL = get_api_url()


def format_blog_output(response: Dict, include_meta: bool) -> Tuple[str, str, str]:
    """
    Format blog response for display with all images embedded in HTML.
    
    Args:
        response: API response dictionary
        include_meta: Whether to include meta description
        
    Returns:
        Tuple of (blog_html, keywords_text, analysis_text)
    """
    if not response.get('success', False):
        error = response.get('error', 'Unknown error')
        return f"<h3 style='color: red;'>Error: {error}</h3>", "", ""
    
    blog = response.get('blog', {})
    keywords = response.get('keywords', {})
    analysis = response.get('analysis', {})
    
    # Extract featured image
    featured_image = blog.get('featured_image')
    featured_html = ""
    
    if featured_image and featured_image.get('url'):
        featured_url = featured_image.get('url') or featured_image.get('url_small', '')
        photographer = featured_image.get('photographer', 'Unknown')
        photographer_url = featured_image.get('photographer_url', '#')
        alt_text = featured_image.get('alt_text', blog.get('title', 'Featured image'))
        
        featured_html = f'''
        <div style='text-align: center; margin: 25px 0;'>
            <img 
                src="{featured_url}" 
                alt="{alt_text}" 
                loading="lazy"
                style='max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'
            />
            <p style='text-align: center; font-size: 12px; color: #666; margin-top: 8px;'>
                Photo by <a href="{photographer_url}?utm_source=ai_blog&utm_medium=referral" target="_blank" style="color: #3498db;">{photographer}</a> 
                on <a href="https://unsplash.com/?utm_source=ai_blog&utm_medium=referral" target="_blank" style="color: #3498db;">Unsplash</a>
            </p>
        </div>
        '''
    
    # Format blog as HTML
    blog_html = f"""
    <div style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;'>
        <h1 style='color: #2c3e50; font-size: 2em; margin-bottom: 10px;'>{blog.get('title', 'Untitled')}</h1>
        
        {'<div style="background: linear-gradient(135deg, #EEF2FF, #E0E7FF); padding: 18px; border-radius: 14px; margin: 22px 0; border-left: 5px solid #4F46E5;"><strong style="color: #4F46E5; font-size: 15px;">📝 Meta Description</strong><br/><em style="color: #1E293B; font-style: normal; font-size: 15px; line-height: 1.6; display: block; margin-top: 6px;">' + blog.get('meta_description', '') + '</em></div>' if include_meta and blog.get('meta_description') else ''}
        
        {featured_html}
        
        <div style='margin: 20px 0;'>
            <h2 style='color: #34495e;'>Introduction</h2>
            <p style='line-height: 1.8; color: #333;'>{blog.get('introduction', '')}</p>
        </div>
    """
    
    # Add sections
    for section in blog.get('sections', []):
        blog_html += f"""
        <div style='margin: 25px 0;'>
            <h2 style='color: #34495e;'>{section.get('heading', '')}</h2>
            <p style='line-height: 1.8; color: #333;'>{section.get('content', '')}</p>
        </div>
        """
    
    # Add conclusion and CTA
    blog_html += f"""
        <div style='margin: 20px 0;'>
            <h2 style='color: #34495e;'>Conclusion</h2>
            <p style='line-height: 1.8; color: #333;'>{blog.get('conclusion', '')}</p>
        </div>
        
        <div style='background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;'>
            <strong style='font-size: 1.1em;'>{blog.get('cta', '')}</strong>
        </div>
    """
    
    # Add additional images gallery inline
    additional_images = blog.get('additional_images', [])
    if additional_images:
        blog_html += """
        <div style='margin-top: 30px; padding-top: 20px; border-top: 2px solid #ecf0f1;'>
            <h3 style='color: #2c3e50;'>🖼️ Related Images</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;'>
        """
        
        for img in additional_images[:4]:  # Limit to 4 images
            img_url = img.get('url_small') or img.get('url', '')
            alt_text = img.get('alt_text', 'Related image')
            photographer = img.get('photographer', '')
            photographer_url = img.get('photographer_url', '#')
            
            if img_url:
                blog_html += f'''
                <div style='text-align: center;'>
                    <img src="{img_url}" alt="{alt_text}" 
                         loading="lazy"
                         style='width: 100%; height: 150px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
                    />
                    <p style='font-size: 11px; color: #888; margin-top: 5px;'>
                        📷 <a href="{photographer_url}?utm_source=ai_blog&utm_medium=referral" target="_blank" style="color: #666;">{photographer}</a>
                    </p>
                </div>
                '''
        
        blog_html += "</div></div>"
    
    # Add footer stats
    blog_html += f"""
        <div style='margin-top: 30px; padding-top: 20px; border-top: 2px solid #ecf0f1;'>
            <p><strong>Tags:</strong> {', '.join(blog.get('tags', []))}</p>
            <p><strong>Word Count:</strong> {response.get('word_count', 'N/A')} words</p>
            <p><strong>Processing Time:</strong> {response.get('processing_time', 'N/A')}s</p>
        </div>
    </div>
    """
    
    # Format keywords
    primary_kw = keywords.get('primary_keywords', [])
    secondary_kw = keywords.get('secondary_keywords', [])
    density = keywords.get('keyword_density', {})
    
    keywords_text = f"""**Primary Keywords:**
{', '.join(primary_kw) if primary_kw else 'None extracted'}

**Secondary Keywords:**
{', '.join(secondary_kw) if secondary_kw else 'None extracted'}

**Keyword Density:**
"""
    for kw, d in list(density.items())[:10]:
        keywords_text += f"- {kw}: {d*100:.2f}%\n"
    
    # Format analysis
    analysis_text = f"""**Summary:**
{analysis.get('summary', 'No summary available')}

**Detected Intent:** {analysis.get('intent', 'N/A').upper()}

**Main Topics:**
{', '.join(analysis.get('topics', [])) if analysis.get('topics') else 'None detected'}

**Content Length:** {analysis.get('content_length', 'N/A')} characters
"""
    
    return blog_html, keywords_text, analysis_text


def generate_blog(url: str, tone: str, word_count: int, include_meta: bool) -> Tuple[str, str, str]:
    """
    Call API to generate blog post.
    
    Returns:
        Tuple of (blog_html, keywords_md, analysis_md)
    """
    if not url or not url.strip():
        return "<h3 style='color: orange;'>⚠️ Please enter a URL</h3>", "", ""
    
    try:
        # Call API
        response = requests.post(
            f"{API_URL}/generate-blog",
            json={
                "url": url.strip(),
                "tone": tone.lower(),
                "word_count": int(word_count),
                "include_images": True
            },
            timeout=180  # 3 minutes for complex pages
        )
        
        if response.status_code == 200:
            data = response.json()
            return format_blog_output(data, include_meta)
        else:
            try:
                error_detail = response.json().get('detail', response.text)
            except Exception:
                error_detail = response.text
            return f"<h3 style='color: red;'>❌ API Error ({response.status_code}): {error_detail}</h3>", "", ""
            
    except requests.exceptions.Timeout:
        return "<h3 style='color: orange;'>⏱️ Request timed out. The page might be too complex. Try again or use a simpler URL.</h3>", "", ""
    except requests.exceptions.ConnectionError:
        return "<h3 style='color: red;'>🔌 Cannot connect to API server. Make sure it's running at http://localhost:8000</h3>", "", ""
    except Exception as e:
        return f"<h3 style='color: red;'>❌ Error: {str(e)}</h3>", "", ""


def estimate_cost(url: str, word_count: int) -> str:
    """Estimate generation cost."""
    if not url or not url.strip():
        return "⚠️ Please enter a URL first"
    
    try:
        response = requests.post(
            f"{API_URL}/estimate-cost",
            params={"url": url.strip(), "word_count": int(word_count)},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            return f"""### 💰 Cost Estimation

| Parameter | Value |
|-----------|-------|
| **Provider** | {data.get('provider', 'Gemini').upper()} |
| **Model** | {data.get('model', 'N/A')} |
| **Estimated Cost** | ${data.get('estimated_cost', 0):.4f} USD |
| **Word Count** | {data.get('word_count', word_count)} words |

*Note: Actual cost may vary based on content complexity.*
"""
        else:
            return "❌ Could not estimate cost"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def check_api_health() -> str:
    """Check API server status."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return "✅ API server is running"
        return "⚠️ API server returned unexpected status"
    except Exception:
        return "❌ API server is not responding. Start it with: python -m uvicorn app.main:app --reload"


# Build Gradio Interface
with gr.Blocks(
    title="AI Blog Generator",
    theme=gr.themes.Soft(),
    css="""
    .main-title { text-align: center; margin-bottom: 20px; }
    .status-box { padding: 10px; border-radius: 8px; margin: 10px 0; }
    """
) as demo:
    
    gr.Markdown("""
    # 🤖 AI Blog Generator
    
    Generate SEO-optimized blog posts from any website URL using AI.
    Images are automatically fetched from Unsplash with proper attribution.
    
    ---
    """, elem_classes=["main-title"])
    
    # API Status
    with gr.Row():
        status_display = gr.Markdown(value=check_api_health())
        refresh_btn = gr.Button("🔄 Check API", size="sm")
    
    refresh_btn.click(fn=check_api_health, outputs=status_display)
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=2):
            url_input = gr.Textbox(
                label="Website URL",
                placeholder="https://example.com/article",
                info="Enter the URL of any webpage to generate a blog about"
            )
            
            with gr.Row():
                tone_input = gr.Dropdown(
                    choices=["Professional", "Casual", "Technical", "Conversational"],
                    value="Professional",
                    label="Writing Tone"
                )
                word_count_input = gr.Slider(
                    minimum=300,
                    maximum=2000,
                    value=800,
                    step=100,
                    label="Target Word Count"
                )
            
            include_meta_input = gr.Checkbox(
                value=True,
                label="Include SEO Meta Description"
            )
            
            with gr.Row():
                generate_btn = gr.Button("🚀 Generate Blog", variant="primary", size="lg")
                estimate_btn = gr.Button("💰 Estimate Cost", variant="secondary")
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### ℹ️ Quick Tips
            
            **Tone Options:**
            - 🎯 **Professional** - Business, formal
            - 😊 **Casual** - Friendly, relaxed
            - 🔧 **Technical** - Detailed, in-depth
            - 💬 **Conversational** - Personal, engaging
            
            **Word Count Guide:**
            - Short: 300-500 words
            - Medium: 500-1000 words
            - Long: 1000-2000 words
            
            **Images:**
            - Featured image at top
            - Related images at bottom
            - All lazy-loaded for speed
            - Photographer attribution included
            """)
    
    gr.Markdown("---")
    
    with gr.Tabs():
        with gr.TabItem("📝 Generated Blog"):
            blog_output = gr.HTML(
                label="Blog Post",
                value="<p style='color: #888; text-align: center; padding: 40px;'>Your generated blog will appear here...</p>"
            )
        
        with gr.TabItem("🔑 Keywords & SEO"):
            keywords_output = gr.Markdown(value="*Generate a blog to see keyword analysis*")
        
        with gr.TabItem("📊 Content Analysis"):
            analysis_output = gr.Markdown(value="*Generate a blog to see content analysis*")
        
        with gr.TabItem("💵 Cost Estimate"):
            cost_output = gr.Markdown(value="*Click 'Estimate Cost' to see pricing*")
    
    # Event handlers - simplified outputs (just 3 items, no Gallery or State)
    generate_btn.click(
        fn=generate_blog,
        inputs=[url_input, tone_input, word_count_input, include_meta_input],
        outputs=[blog_output, keywords_output, analysis_output]
    )
    
    estimate_btn.click(
        fn=estimate_cost,
        inputs=[url_input, word_count_input],
        outputs=cost_output
    )
    
    gr.Markdown("""
    ---
    
    ### 🛠️ Technical Stack
    
    | Component | Technology |
    |-----------|------------|
    | Backend | FastAPI + Python |
    | NLP | KeyBERT, SentenceTransformers |
    | LLM | Google Gemini (gemini-3-flash-preview) |
    | Images | Unsplash API (Free tier) |
    | Frontend | Gradio |
    
    ---
    
    **Note:** Make sure the FastAPI server is running: `uvicorn app.main:app --reload`
    """)


if __name__ == "__main__":
    print("Starting Gradio UI...")
    print(f"API endpoint: {API_URL}")
    print("Make sure the FastAPI backend is running")
    
    # Environment-driven launch configuration
    settings = get_app_settings()
    
    # Determine launch parameters based on environment
    if settings and settings.app_env == "production":
        # Production: no share, no debug, use allowed hosts
        server_name = settings.allowed_hosts[0] if settings.allowed_hosts else "0.0.0.0"
        server_port = int(os.getenv("PORT", 7860))
        share = False
        debug = False
    else:
        # Development: local access, debug enabled
        server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
        server_port = int(os.getenv("PORT", 7860))
        share = os.getenv("GRADIO_SHARE", "false").lower() == "true"
        debug = True
    
    print(f"Server: {server_name}:{server_port} | Share: {share} | Debug: {debug}")
    
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        debug=debug
    )
