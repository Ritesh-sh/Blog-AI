# 🤖 AI Blog Generator

An end-to-end AI system that generates SEO-optimized blog posts from website URLs using local NLP and LLM APIs.

## 📋 Overview

This system takes a website URL as input and generates a complete, SEO-friendly blog post by:
1. Extracting and cleaning website content
2. Analyzing keywords and topics using local NLP (no LLM costs)
3. Understanding website intent and context
4. Generating high-quality blog content using LLM APIs
5. Post-processing for SEO optimization

## 🚀 Features

- **URL Validation**: Checks URL format and accessibility
- **Smart Content Extraction**: Extracts main content, filters noise
- **Local NLP Analysis**: KeyBERT for keywords, sentence transformers for topics
- **Intent Detection**: Identifies website type (service, product, blog, etc.)
- **LLM Integration**: Supports OpenAI and Google Gemini
- **SEO Optimization**: Meta descriptions, keyword density, heading structure
- **Cost Optimization**: Efficient prompts, content truncation, model selection
- **REST API**: FastAPI backend with comprehensive endpoints
- **Simple UI**: Gradio interface for easy testing

## 📁 Project Structure

```
blog/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   ├── models.py                  # Pydantic models
│   └── core/
│       ├── url_validator.py       # URL validation
│       ├── content_extractor.py   # Web scraping
│       ├── text_cleaner.py        # Text preprocessing
│       ├── keyword_extractor.py   # KeyBERT integration
│       ├── topic_analyzer.py      # Topic analysis
│       ├── prompt_builder.py      # Prompt engineering
│       ├── blog_generator.py      # LLM integration
│       └── seo_postprocessor.py   # SEO optimization
├── ui/
│   └── gradio_app.py              # Gradio frontend
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- pip

### Setup

1. **Clone the repository** (or you're already here!)

2. **Create virtual environment**:
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download NLP models** (first run will auto-download):
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

5. **Configure environment**:
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
# Windows: notepad .env
# Linux/Mac: nano .env
```

### Environment Variables

Edit `.env` file:

```env
# Choose LLM provider
LLM_PROVIDER=openai  # or "gemini"

# OpenAI (if using)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Google Gemini (if using)
GEMINI_API_KEY=your-gemini-key-here
GEMINI_MODEL=gemini-1.5-flash

# App settings
MAX_CONTENT_LENGTH=10000
REQUEST_TIMEOUT=30
```

## 🎯 Usage

### Option 1: Run API Server + UI (Recommended)

**Terminal 1 - Start FastAPI Backend**:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Gradio UI**:
```bash
python ui/gradio_app.py
```

Then open: `http://localhost:7860`

### Option 2: API Only

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: `http://localhost:8000/docs`

### Option 3: Python Integration

```python
from app.core.url_validator import validate_url
from app.core.content_extractor import extract_content
from app.core.keyword_extractor import extract_keywords
from app.core.topic_analyzer import analyze_topics
from app.core.prompt_builder import build_blog_prompt
from app.core.blog_generator import generate_blog

# Complete pipeline
url = "https://example.com"

# Validate
is_valid, error = validate_url(url)

# Extract content
content = extract_content(url)

# Analyze
keywords = extract_keywords(content['text'])
analysis = analyze_topics(content['text'], content['title'])

# Generate
prompt = build_blog_prompt(url, content, analysis, keywords)
blog = generate_blog(prompt)
```

## 📡 API Endpoints

### POST `/generate-blog`

Generate a blog post from URL.

**Request:**
```json
{
  "url": "https://example.com",
  "tone": "professional",
  "word_count": 800,
  "include_meta": true
}
```

**Response:**
```json
{
  "success": true,
  "blog": {
    "title": "Blog Title (H1)",
    "meta_description": "SEO description",
    "introduction": "Opening paragraph...",
    "sections": [
      {
        "heading": "Section 1",
        "content": "Section content..."
      }
    ],
    "conclusion": "Closing paragraph...",
    "cta": "Call to action",
    "tags": ["tag1", "tag2"]
  },
  "keywords": {
    "primary_keywords": ["keyword1", "keyword2"],
    "secondary_keywords": ["keyword3", "keyword4"],
    "keyword_density": {"keyword1": 0.015}
  },
  "analysis": {
    "summary": "Brief summary",
    "intent": "service",
    "topics": ["topic1", "topic2"],
    "content_length": 5000
  },
  "word_count": 850,
  "generated_at": "2026-01-18T10:30:00",
  "processing_time": 12.5
}
```

### POST `/estimate-cost`

Estimate API cost before generation.

**Request:**
```
POST /estimate-cost?url=https://example.com&word_count=800
```

**Response:**
```json
{
  "url": "https://example.com",
  "word_count": 800,
  "estimated_cost_usd": 0.0024,
  "provider": "openai",
  "model": "gpt-3.5-turbo"
}
```

### GET `/health`

Health check endpoint.

## 💰 Cost Optimization Notes

### 1. **Model Selection**
- **OpenAI**: Use `gpt-3.5-turbo` (~$0.002/blog) instead of `gpt-4` (~$0.10/blog)
- **Gemini**: Use `gemini-1.5-flash` (~$0.0001/blog) - most cost-effective

### 2. **Content Truncation**
- Limit extracted content to 10,000 characters (configurable)
- Reduces input token costs

### 3. **Local NLP**
- Keywords extracted using KeyBERT (free, runs locally)
- Topic analysis using sentence-transformers (free)
- Only LLM call is for final blog generation

### 4. **Efficient Prompts**
- Structured prompts with clear instructions
- Request JSON output format (reduces tokens)
- Single API call per blog

### 5. **Caching** (Optional)
- Implement FAISS caching for repeated URLs
- Store extracted content to avoid re-scraping

**Estimated Costs Per Blog:**
- OpenAI GPT-3.5: $0.002 - $0.005
- Google Gemini Flash: $0.0001 - $0.0003
- OpenAI GPT-4: $0.08 - $0.15 (not recommended for MVP)

## 🧪 Testing

### Manual Testing with cURL

```bash
# Generate blog
curl -X POST "http://localhost:8000/generate-blog" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "tone": "professional",
    "word_count": 800,
    "include_meta": true
  }'

# Estimate cost
curl -X POST "http://localhost:8000/estimate-cost?url=https://example.com&word_count=800"
```

### Unit Tests (Future)

```bash
pytest tests/
```

## 🔧 Configuration Options

### LLM Providers

**OpenAI (Recommended for Quality)**:
- Models: `gpt-3.5-turbo`, `gpt-4o-mini`, `gpt-4`
- API Key: Get from https://platform.openai.com/

**Google Gemini (Recommended for Cost)**:
- Models: `gemini-1.5-flash`, `gemini-1.5-pro`
- API Key: Get from https://makersuite.google.com/

### Tone Options
- `professional`: Business, corporate style
- `casual`: Friendly, relaxed style
- `technical`: In-depth, detailed style
- `conversational`: Personal, engaging style

### Word Count
- Min: 300 words
- Max: 2000 words
- Recommended: 800-1200 for SEO

## 📊 Architecture Flow

```
User Input (URL)
    ↓
URL Validator → Validate format & accessibility
    ↓
Content Extractor → BeautifulSoup/newspaper3k
    ↓
Text Cleaner → Remove noise, normalize
    ↓
Keyword Extractor → KeyBERT (local)
    ↓
Topic Analyzer → SentenceTransformer (local)
    ↓
Prompt Builder → Structure LLM prompt
    ↓
Blog Generator → OpenAI/Gemini API call
    ↓
SEO Post-Processor → Validate & optimize
    ↓
JSON Response → Return to user
```

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "API key not configured"
```bash
# Check .env file exists
cat .env

# Verify API key is set
python -c "from app.config import settings; print(settings.openai_api_key)"
```

### Issue: "Content extraction failed"
- Some websites block scraping (check robots.txt)
- Try different URL from same domain
- Check if website is accessible manually

### Issue: "Sentence transformer download timeout"
```bash
# Manually download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## 🚀 Production Deployment

### Security Considerations
1. **API Keys**: Use environment variables, never commit
2. **CORS**: Configure `allow_origins` in `main.py`
3. **Rate Limiting**: Add rate limiting middleware
4. **Authentication**: Add API key authentication

### Scaling
1. **Async Processing**: Use background tasks for long operations
2. **Caching**: Implement Redis for content caching
3. **Load Balancing**: Deploy multiple instances behind load balancer
4. **Database**: Store generated blogs in PostgreSQL/MongoDB

### Deployment Options
- **Docker**: Containerize with Dockerfile
- **Cloud**: Deploy to AWS Lambda, Google Cloud Run, or Azure Functions
- **Traditional**: Deploy to VPS with nginx + gunicorn

## 📝 License

This is an educational project for demonstration purposes.

## 🤝 Contributing

This is a portfolio/internship project. Suggestions welcome!

## 📧 Contact

Built by an AI Engineer Intern as an MVP demonstration.

---

**Happy Blog Generating! 🎉**
