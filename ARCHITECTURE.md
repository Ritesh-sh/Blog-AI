# System Architecture Documentation

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Gradio Web UI (Port 7860)                       │   │
│  │  • URL Input  • Tone Selection  • Word Count Slider          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ HTTP POST
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND (Port 8000)                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   API Layer (main.py)                        │   │
│  │  Endpoints: /generate-blog, /estimate-cost, /health         │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            │                                         │
│  ┌─────────────────────────▼───────────────────────────────────┐   │
│  │                  ORCHESTRATION LAYER                         │   │
│  │  Pipeline: Validation → Extraction → Analysis → Generation  │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
┌──────────────────┐                    ┌──────────────────┐
│  LOCAL NLP       │                    │  EXTERNAL APIs    │
│  PROCESSING      │                    │                   │
│  • KeyBERT       │                    │  • OpenAI         │
│  • SentTrans.    │                    │  • Google Gemini  │
│  (No API cost)   │                    │  (API cost)       │
└──────────────────┘                    └──────────────────┘
```

---

## 🔄 Request Flow Diagram

```
┌──────────┐
│  START   │
└────┬─────┘
     │
     ▼
┌────────────────────────┐
│ 1. URL Validation      │──────► Check format (http/https)
│    (url_validator.py)  │        Check accessibility (HEAD request)
└────┬───────────────────┘        Validate domain
     │ ✓ Valid
     ▼
┌────────────────────────┐
│ 2. Content Extraction  │──────► Try newspaper3k (article parser)
│ (content_extractor.py) │        Fallback: BeautifulSoup
└────┬───────────────────┘        Extract: title, text, meta
     │ 5000-10000 chars
     ▼
┌────────────────────────┐
│ 3. Text Cleaning       │──────► Remove URLs, emails
│    (text_cleaner.py)   │        Normalize whitespace
└────┬───────────────────┘        Remove special chars
     │ Cleaned text
     ▼
┌────────────────────────┐
│ 4. Keyword Extraction  │──────► KeyBERT with embeddings
│ (keyword_extractor.py) │        Categorize: primary/secondary
└────┬───────────────────┘        Calculate density
     │ Keywords list
     ▼
┌────────────────────────┐
│ 5. Topic Analysis      │──────► Detect intent (service/product/blog)
│  (topic_analyzer.py)   │        Generate summary (extractive)
└────┬───────────────────┘        Extract main topics
     │ Analysis data
     ▼
┌────────────────────────┐
│ 6. Prompt Building     │──────► Structure prompt with all data
│  (prompt_builder.py)   │        Include keywords, topics, tone
└────┬───────────────────┘        Set word count target
     │ Optimized prompt
     ▼
┌────────────────────────┐
│ 7. Blog Generation     │──────► Call LLM API (OpenAI/Gemini)
│  (blog_generator.py)   │        Parse JSON response
└────┬───────────────────┘        Retry on failure (3x)
     │ Generated blog
     ▼
┌────────────────────────┐
│ 8. SEO Post-Processing │──────► Validate meta description
│ (seo_postprocessor.py) │        Check keyword density
└────┬───────────────────┘        Calculate SEO score
     │ Final blog + analysis
     ▼
┌────────────────────────┐
│    JSON Response       │──────► Return to user
│ (BlogGenerationResp.)  │
└────┬───────────────────┘
     │
     ▼
┌──────────┐
│   END    │
└──────────┘
```

---

## 📦 Module Architecture

### Core Modules (app/core/)

```
┌─────────────────────────────────────────────────────────────┐
│                      CORE MODULES                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ url_validator    │  │ content_extractor│                │
│  │ • validate()     │  │ • extract()      │                │
│  │ • check_access() │  │ • newspaper3k    │                │
│  └──────────────────┘  │ • beautifulsoup  │                │
│                        └──────────────────┘                │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ text_cleaner     │  │ keyword_extractor│                │
│  │ • clean()        │  │ • extract_kw()   │                │
│  │ • normalize()    │  │ • KeyBERT        │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ topic_analyzer   │  │ prompt_builder   │                │
│  │ • analyze()      │  │ • build_prompt() │                │
│  │ • detect_intent()│  │ • template       │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ blog_generator   │  │ seo_postproc.    │                │
│  │ • generate()     │  │ • process()      │                │
│  │ • OpenAI/Gemini  │  │ • validate_seo() │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Between Modules

```
URL String
    ↓
[url_validator] → Boolean + Error
    ↓
[content_extractor] → Dict{title, text, meta}
    ↓
[text_cleaner] → Cleaned String
    ↓
[keyword_extractor] → Dict{primary_kw, secondary_kw, density}
    ↓
[topic_analyzer] → Dict{summary, intent, topics}
    ↓
[prompt_builder] → Structured Prompt String
    ↓
[blog_generator] → Dict{title, sections, meta, etc}
    ↓
[seo_postprocessor] → Dict{blog, seo_analysis}
    ↓
BlogGenerationResponse (Pydantic Model)
```

---

## 🗄️ Data Models

### Pydantic Models (app/models.py)

```python
BlogGenerationRequest
├── url: HttpUrl
├── tone: Literal["professional", "casual", "technical", "conversational"]
├── word_count: int (300-2000)
└── include_meta: bool

BlogGenerationResponse
├── success: bool
├── blog: BlogContent
│   ├── title: str
│   ├── meta_description: str
│   ├── introduction: str
│   ├── sections: List[Dict]
│   │   ├── heading: str
│   │   └── content: str
│   ├── conclusion: str
│   ├── cta: str
│   └── tags: List[str]
├── keywords: KeywordData
│   ├── primary_keywords: List[str]
│   ├── secondary_keywords: List[str]
│   └── keyword_density: Dict[str, float]
├── analysis: ContentAnalysis
│   ├── summary: str
│   ├── intent: str
│   ├── topics: List[str]
│   └── content_length: int
├── word_count: int
├── generated_at: datetime
└── processing_time: float
```

---

## ⚙️ Configuration Architecture

```
Environment Variables (.env)
         ↓
    config.py (Pydantic Settings)
         ↓
    ┌────────────────────────┐
    │  Settings Singleton    │
    ├────────────────────────┤
    │ • LLM Provider         │
    │ • API Keys             │
    │ • Model Names          │
    │ • App Settings         │
    │ • Limits & Timeouts    │
    └────────────────────────┘
         ↓
    All Modules Access Settings
```

---

## 🔌 External Dependencies

### NLP Libraries (Local, No API Cost)

```
┌─────────────────────────────────────┐
│      KeyBERT                        │
│  Keyword extraction using BERT      │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Sentence Transformers              │
│  Embeddings: all-MiniLM-L6-v2       │
│  Size: ~80MB                        │
│  Fast, lightweight                  │
└─────────────────────────────────────┘
```

### LLM APIs (External, API Cost)

```
┌──────────────────┐      ┌──────────────────┐
│   OpenAI API     │      │  Google Gemini   │
├──────────────────┤      ├──────────────────┤
│ gpt-3.5-turbo    │      │ gemini-1.5-flash │
│ gpt-4o-mini      │      │ gemini-1.5-pro   │
│ gpt-4            │      │                  │
└──────────────────┘      └──────────────────┘
         ↓                         ↓
    blog_generator.py (abstraction layer)
```

### Web Scraping

```
┌──────────────────┐      ┌──────────────────┐
│  newspaper3k     │      │  BeautifulSoup4  │
├──────────────────┤      ├──────────────────┤
│ Article-focused  │      │ General HTML     │
│ Auto-cleanup     │      │ Flexible parser  │
│ First choice     │      │ Fallback         │
└──────────────────┘      └──────────────────┘
```

---

## 🔄 Async vs Sync Operations

### Current Implementation (Sync)
```
Request → Process → Response
(Sequential, simple, sufficient for MVP)
```

### Future Optimization (Async)
```
Request
    ├──→ Validate (fast)
    ├──→ Extract (slow) ────────────┐
    ├──→ Clean (fast)               │
    ├──→ Keywords (medium) ─────────┤─→ Parallel
    ├──→ Topics (medium) ───────────┘
    ├──→ Build Prompt (fast)
    └──→ Generate (slow)
Response
```

---

## 📊 Performance Characteristics

### Time Complexity

| Operation | Time | Bottleneck |
|-----------|------|------------|
| URL Validation | O(1) | Network latency |
| Content Extract | O(n) | Website size |
| Text Cleaning | O(n) | Content length |
| Keyword Extract | O(n×m) | Text × vocab |
| Topic Analysis | O(n) | Content length |
| Prompt Building | O(1) | Template format |
| LLM Generation | O(?) | API queue |
| SEO Processing | O(n) | Content length |

**n** = content length  
**m** = vocabulary size

### Space Complexity

| Component | Memory | Notes |
|-----------|--------|-------|
| Embedding Model | ~80 MB | Loaded once |
| Request Data | ~50 KB | Per request |
| Generated Blog | ~20 KB | Per response |
| Total per Request | ~100 KB | Excluding model |

---

## 🛡️ Error Handling Strategy

```
┌─────────────────────────────────────────┐
│         Error Handling Layers           │
├─────────────────────────────────────────┤
│                                         │
│  1. Input Validation (Pydantic)        │
│     • Type checking                     │
│     • Range validation                  │
│     • Format validation                 │
│                                         │
│  2. Business Logic Errors              │
│     • URL validation errors             │
│     • Content extraction errors         │
│     • Return meaningful messages        │
│                                         │
│  3. API Errors (Retry Logic)           │
│     • Tenacity retry decorator          │
│     • Exponential backoff               │
│     • Max 3 attempts                    │
│                                         │
│  4. Global Exception Handler           │
│     • Catch unexpected errors           │
│     • Log to console/file               │
│     • Return 500 error                  │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Considerations

```
┌─────────────────────────────────────────┐
│         Security Measures               │
├─────────────────────────────────────────┤
│                                         │
│  ✓ API Keys in Environment Variables   │
│  ✓ Input Validation (Pydantic)         │
│  ✓ URL Format Validation               │
│  ✓ Request Timeout Limits              │
│  ✓ Content Length Limits               │
│  ✓ CORS Configuration                  │
│                                         │
│  ⚠ TODO for Production:                 │
│  • Rate Limiting                        │
│  • API Authentication                   │
│  • Request Signing                      │
│  • HTTPS Only                          │
│  • Input Sanitization                   │
│  • SQL Injection Prevention             │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📈 Scalability Path

### Current (MVP)
```
Single Instance
    └── Handles ~10 requests/minute
```

### Phase 1: Optimize
```
Single Instance + Caching
    └── Handles ~50 requests/minute
```

### Phase 2: Horizontal Scale
```
Load Balancer
    ├── Instance 1
    ├── Instance 2
    └── Instance N
    └── Redis Cache (shared)
    └── Handles ~500 requests/minute
```

### Phase 3: Distributed
```
API Gateway
    ├── Auth Service
    ├── Content Service (Extract & Clean)
    ├── NLP Service (Keywords & Topics)
    ├── Generation Service (LLM)
    └── Storage Service (Database)
    └── Message Queue (Async processing)
    └── Handles ~5000 requests/minute
```

---

This architecture is designed to be:
- ✅ **Modular**: Each component is independent
- ✅ **Testable**: Clear interfaces between modules
- ✅ **Scalable**: Can grow from MVP to production
- ✅ **Cost-Optimized**: Minimizes API calls
- ✅ **Maintainable**: Clean code structure
- ✅ **Extensible**: Easy to add new features
