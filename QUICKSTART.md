# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1️⃣ Backend Setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY and MONGODB_URL
```

### 2️⃣ Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

The frontend will run at `http://localhost:5173` and communicate with the backend at `http://localhost:8000`.

Terminal 1 (Backend):
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```powershell
python ui\gradio_app.py
```

Open browser: `http://localhost:7860`

**Option B: API Only**

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

### Step 4: Test the System

Open Gradio UI at `http://localhost:7860` and:
1. Enter URL: `https://www.python.org`
2. Select tone: `Professional`
3. Set word count: `800`
4. Click "Generate Blog"

Wait 10-20 seconds for your blog!

---

## 📋 System Requirements

### Minimum
- Python 3.9+
- 4GB RAM
- 2GB disk space
- Internet connection

### Recommended
- Python 3.10+
- 8GB RAM
- 5GB disk space
- Good internet connection

---

## 💰 Cost Optimization Guide

### 1. Choose the Right Model

| Provider | Model | Cost per Blog | Quality | Speed |
|----------|-------|---------------|---------|-------|
| **Gemini** | gemini-1.5-flash | $0.0001 | Good | Fast |
| **OpenAI** | gpt-3.5-turbo | $0.002 | Very Good | Fast |
| **OpenAI** | gpt-4o-mini | $0.005 | Excellent | Medium |
| **OpenAI** | gpt-4 | $0.10 | Best | Slow |

**Recommendation**: Use `gemini-1.5-flash` for MVP/testing, `gpt-3.5-turbo` for production.

### 2. Optimize Content Length

```env
# In .env file
MAX_CONTENT_LENGTH=10000  # Default
```

Lower this to reduce input tokens:
- `5000` - Fast, cheap, may miss details
- `10000` - Balanced (recommended)
- `15000` - Thorough, more expensive

### 3. Batch Processing

Generate multiple blogs in bulk during off-peak hours to maximize efficiency.

### 4. Caching Strategy

For repeated URLs:
```python
# Enable FAISS caching in .env
USE_FAISS_CACHE=true
```

This caches extracted content and keywords locally.

### 5. Cost Monitoring

```python
# Check estimated cost before generation
import requests

response = requests.post(
    "http://localhost:8000/estimate-cost",
    params={"url": "https://example.com", "word_count": 800}
)
print(response.json())
```

### 6. Budget Calculator

For 1000 blogs per month:

| Model | Cost per Blog | Monthly Cost |
|-------|---------------|--------------|
| Gemini Flash | $0.0001 | **$0.10** |
| GPT-3.5 Turbo | $0.002 | **$2.00** |
| GPT-4o Mini | $0.005 | **$5.00** |
| GPT-4 | $0.10 | **$100.00** |

---

## 🐛 Common Issues & Solutions

### Issue 1: "No module named 'app'"

**Solution:**
```powershell
# Make sure you're in the project root
cd "c:\Users\Sharma ji\OneDrive\Desktop\placement\blog"

# Run with python -m
python -m uvicorn app.main:app --reload
```

### Issue 2: "API key not configured"

**Solution:**
```powershell
# Check if .env exists
if (Test-Path .env) { "File exists" } else { "File missing" }

# Verify content
Get-Content .env

# Make sure no extra spaces
# Correct: OPENAI_API_KEY=sk-abc123
# Wrong: OPENAI_API_KEY = sk-abc123
```

### Issue 3: "Module 'sentence_transformers' not found"

**Solution:**
```powershell
# Reinstall specific package
pip install sentence-transformers --upgrade
```

### Issue 4: "Connection refused" when UI tries to connect to API

**Solution:**
```powershell
# Make sure API is running first
# Check if port 8000 is in use
netstat -ano | findstr :8000

# If nothing shows, start the API:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Issue 5: "Content extraction failed"

**Reasons:**
- Website blocks scraping (check robots.txt)
- Website requires JavaScript (try different URL)
- Website is down (verify manually)

**Solution:**
```python
# Try a different, more scraper-friendly URL
# Good examples:
# - https://www.python.org
# - https://www.tensorflow.org
# - https://en.wikipedia.org/wiki/Python_(programming_language)

# Avoid:
# - Social media sites (Facebook, LinkedIn)
# - Sites with heavy JavaScript (SPAs)
# - Sites that block bots
```

### Issue 6: Model download timeout

**Solution:**
```powershell
# Pre-download models manually
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# If still fails, download directly
pip install --no-cache-dir sentence-transformers
```

---

## 🧪 Testing the System

### Test 1: URL Validator

```powershell
python -c "from app.core.url_validator import validate_url; print(validate_url('https://www.python.org'))"
```

Expected: `(True, '')`

### Test 2: Content Extraction

```powershell
python -c "from app.core.content_extractor import extract_content; c = extract_content('https://www.python.org'); print(f'Extracted {len(c[\"text\"])} chars')"
```

Expected: `Extracted XXXX chars`

### Test 3: Keyword Extraction

```powershell
python -c "from app.core.keyword_extractor import extract_keywords; k = extract_keywords('Python is a high-level programming language'); print(k['primary_keywords'])"
```

### Test 4: Full API Test

```powershell
# Start API first, then in another terminal:
curl -X POST "http://localhost:8000/generate-blog" -H "Content-Type: application/json" -d "{\"url\":\"https://www.python.org\",\"tone\":\"professional\",\"word_count\":800,\"include_meta\":true}"
```

---

## 📊 Performance Benchmarks

Based on testing (your results may vary):

| Stage | Time | Can Optimize? |
|-------|------|---------------|
| URL Validation | 0.5s | ✅ Already fast |
| Content Extraction | 2-3s | ⚠️ Depends on website |
| Text Cleaning | 0.1s | ✅ Already fast |
| Keyword Extraction | 1-2s | ✅ Could cache |
| Topic Analysis | 1-2s | ✅ Could cache |
| Prompt Building | 0.1s | ✅ Already fast |
| LLM Generation | 5-15s | ⚠️ Depends on API |
| SEO Processing | 0.5s | ✅ Already fast |
| **Total** | **10-25s** | |

**Bottlenecks:**
1. LLM API call (5-15s) - Unavoidable
2. Content extraction (2-3s) - Can cache

**Optimization Opportunities:**
- Cache extracted content for repeated URLs
- Use async/background tasks for non-critical operations
- Batch process multiple blogs

---

## 🔐 Security Checklist

Before deployment:

- [ ] Never commit `.env` file to git
- [ ] Use environment variables for API keys
- [ ] Add rate limiting to API endpoints
- [ ] Configure CORS properly (not `*` in production)
- [ ] Add API authentication
- [ ] Use HTTPS in production
- [ ] Validate all user inputs
- [ ] Set up logging and monitoring
- [ ] Add request size limits
- [ ] Implement proper error handling

---

## 📈 Next Steps

### For Learning/Portfolio:
1. ✅ Successfully generate your first blog
2. Test with different websites
3. Try different tones and word counts
4. Add to your portfolio with screenshots
5. Document learnings in blog post

### For Production:
1. Add user authentication
2. Implement caching (Redis)
3. Add database for storing blogs
4. Set up monitoring (Sentry, DataDog)
5. Add rate limiting
6. Deploy to cloud (AWS, GCP, Azure)
7. Set up CI/CD pipeline
8. Add comprehensive testing

### For Optimization:
1. Implement FAISS caching
2. Add async processing with Celery
3. Optimize prompt engineering
4. Fine-tune keyword extraction
5. Add more LLM providers
6. Implement A/B testing for prompts

---

## 🎓 Learning Resources

### Python & FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### NLP & ML
- [KeyBERT Guide](https://maartengr.github.io/KeyBERT/)
- [Sentence Transformers](https://www.sbert.net/)

### LLM APIs
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini Docs](https://ai.google.dev/docs)

### SEO Best Practices
- [Google SEO Guide](https://developers.google.com/search/docs)
- [Moz SEO Guide](https://moz.com/beginners-guide-to-seo)

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Dependencies listed in requirements.txt
- [ ] Documentation complete
- [ ] Security checklist complete

### Deployment
- [ ] Choose hosting platform
- [ ] Set up CI/CD
- [ ] Configure monitoring
- [ ] Set up logging
- [ ] Add health checks
- [ ] Configure auto-scaling
- [ ] Set up backups

### Post-Deployment
- [ ] Monitor errors
- [ ] Track performance
- [ ] Monitor API costs
- [ ] Collect user feedback
- [ ] Plan improvements

---

**Need Help?** Check the main README.md or open an issue!
