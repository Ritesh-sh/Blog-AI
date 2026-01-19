
# Example API Requests and Responses

This document contains example requests and responses for the AI Blog Generator API (React frontend + FastAPI backend).

---

## Example 1: Generate Professional Blog (Tech Company)

### Request

```bash
POST http://localhost:8000/generate-blog
Content-Type: application/json

{
  "url": "https://www.tensorflow.org/",
  "tone": "technical",
  "word_count": 1000,
  "include_meta": true
}
```

### Expected Response Structure

```json
{
  "success": true,
  "blog": {
    "title": "TensorFlow: The Complete Guide to Machine Learning Framework",
    "meta_description": "Discover TensorFlow, Google's powerful open-source machine learning framework. Learn how TensorFlow simplifies ML model development with comprehensive tools and libraries.",
    "introduction": "TensorFlow has revolutionized the way developers and data scientists approach machine learning. As Google's flagship open-source framework, it provides a comprehensive ecosystem for building, training, and deploying ML models at scale...",
    "sections": [
      {
        "heading": "What is TensorFlow?",
        "content": "TensorFlow is an end-to-end open-source platform for machine learning..."
      },
      {
        "heading": "Key Features and Capabilities",
        "content": "TensorFlow offers a robust set of features that make it the framework of choice..."
      },
      {
        "heading": "Getting Started with TensorFlow",
        "content": "Starting your TensorFlow journey is straightforward with comprehensive documentation..."
      }
    ],
    "conclusion": "TensorFlow continues to be the leading framework for machine learning development, offering unmatched flexibility, scalability, and community support...",
    "cta": "Ready to build your first ML model? Visit tensorflow.org to get started with tutorials and documentation today!",
    "tags": ["TensorFlow", "Machine Learning", "AI", "Deep Learning", "Python"]
  },
  "keywords": {
    "primary_keywords": [
      "tensorflow",
      "machine learning",
      "deep learning",
      "neural networks",
      "ml framework"
    ],
    "secondary_keywords": [
      "google tensorflow",
      "keras",
      "model training",
      "ai development",
      "python ml",
      "tensorflow tutorial",
      "machine learning framework",
      "tensorflow models",
      "deep neural networks",
      "tensorflow api"
    ],
    "keyword_density": {
      "tensorflow": 0.0234,
      "machine learning": 0.0156,
      "deep learning": 0.0098,
      "neural networks": 0.0067,
      "ml framework": 0.0045
    }
  },
  "analysis": {
    "summary": "TensorFlow is Google's open-source machine learning framework designed for building and deploying ML models. The platform provides comprehensive tools for developers and researchers.",
    "intent": "informational",
    "topics": [
      "Machine Learning",
      "TensorFlow",
      "Deep Learning",
      "Neural Networks",
      "AI Development"
    ],
    "content_length": 8543
  },
  "word_count": 1024,
  "generated_at": "2026-01-18T10:30:00.123456",
  "processing_time": 14.52
}
```

---

## Example 2: Generate Casual Blog (E-commerce)

### Request

```bash
POST http://localhost:8000/generate-blog
Content-Type: application/json

{
  "url": "https://www.etsy.com/",
  "tone": "casual",
  "word_count": 600,
  "include_meta": true
}
```

### Expected Response Structure

```json
{
  "success": true,
  "blog": {
    "title": "Etsy: Your Go-To Marketplace for Unique Handmade Treasures",
    "meta_description": "Explore Etsy, the global marketplace for creative goods. Find one-of-a-kind handmade items, vintage treasures, and craft supplies from talented artisans worldwide.",
    "introduction": "Looking for something unique that you won't find anywhere else? Etsy is where creativity meets commerce! This vibrant online marketplace connects you with millions of talented makers and vintage collectors...",
    "sections": [
      {
        "heading": "What Makes Etsy Special?",
        "content": "Unlike mass-market retailers, Etsy is all about the personal touch..."
      },
      {
        "heading": "Shopping on Etsy: A Buyer's Guide",
        "content": "Navigating Etsy is a breeze! The platform makes it super easy to find exactly what you're looking for..."
      },
      {
        "heading": "Supporting Small Businesses",
        "content": "Every purchase on Etsy directly supports independent creators and small businesses..."
      }
    ],
    "conclusion": "Whether you're hunting for the perfect gift or want to treat yourself to something special, Etsy has endless options...",
    "cta": "Start exploring unique finds on Etsy today – your perfect handmade treasure is waiting!",
    "tags": ["Etsy", "Handmade", "Shopping", "Crafts", "Small Business"]
  },
  "keywords": {
    "primary_keywords": [
      "etsy",
      "handmade",
      "unique gifts",
      "artisan",
      "crafts"
    ],
    "secondary_keywords": [
      "vintage",
      "creative goods",
      "small business",
      "online marketplace",
      "custom items",
      "etsy shop",
      "handcrafted",
      "personalized gifts",
      "etsy sellers",
      "unique products"
    ],
    "keyword_density": {
      "etsy": 0.0289,
      "handmade": 0.0178,
      "unique gifts": 0.0134,
      "artisan": 0.0089,
      "crafts": 0.0067
    }
  },
  "analysis": {
    "summary": "Etsy is an online marketplace specializing in handmade, vintage, and unique creative goods. The platform connects buyers with independent sellers and artisans globally.",
    "intent": "commercial",
    "topics": [
      "E-commerce",
      "Handmade Products",
      "Vintage Items",
      "Creative Marketplace",
      "Small Business"
    ],
    "content_length": 6721
  },
  "word_count": 627,
  "generated_at": "2026-01-18T10:35:15.987654",
  "processing_time": 11.23
}
```

---

## Example 3: Cost Estimation

### Request

```bash
POST http://localhost:8000/estimate-cost?url=https://example.com&word_count=800
```

### Response

```json
{
  "url": "https://example.com",
  "word_count": 800,
  "estimated_cost_usd": 0.0024,
  "provider": "openai",
  "model": "gpt-3.5-turbo"
}
```

---

## Example 4: Error Response (Invalid URL)

### Request

```bash
POST http://localhost:8000/generate-blog
Content-Type: application/json

{
  "url": "not-a-valid-url",
  "tone": "professional",
  "word_count": 800,
  "include_meta": true
}
```

### Response

```json
{
  "success": false,
  "error": "URL validation failed: URL must start with http:// or https://",
  "details": "Status code: 400"
}
```

---

## Example 5: Error Response (Content Extraction Failed)

### Request

```bash
POST http://localhost:8000/generate-blog
Content-Type: application/json

{
  "url": "https://example-blocked-site.com",
  "tone": "professional",
  "word_count": 800,
  "include_meta": true
}
```

### Response

```json
{
  "success": false,
  "error": "Content extraction failed: Failed to extract content from URL",
  "details": "Status code: 400"
}
```

---

## Example 6: Python Code Integration

```python
import requests

# API endpoint
API_URL = "http://localhost:8000"

# Prepare request
payload = {
    "url": "https://www.python.org/",
    "tone": "professional",
    "word_count": 800,
    "include_meta": True
}

# Make request
response = requests.post(f"{API_URL}/generate-blog", json=payload, timeout=120)

# Check response
if response.status_code == 200:
    data = response.json()
    
    # Access blog content
    print(f"Title: {data['blog']['title']}")
    print(f"Meta: {data['blog']['meta_description']}")
    print(f"\nIntroduction:\n{data['blog']['introduction']}")
    
    # Access keywords
    print(f"\nPrimary Keywords: {', '.join(data['keywords']['primary_keywords'])}")
    
    # Access analysis
    print(f"\nIntent: {data['analysis']['intent']}")
    print(f"Topics: {', '.join(data['analysis']['topics'])}")
    
    # Metrics
    print(f"\nWord Count: {data['word_count']}")
    print(f"Processing Time: {data['processing_time']}s")
else:
    print(f"Error: {response.json()['error']}")
```

---

## Example 7: JavaScript/Fetch Integration

```javascript
// API endpoint
const API_URL = 'http://localhost:8000';

// Prepare request
const payload = {
  url: 'https://www.python.org/',
  tone: 'professional',
  word_count: 800,
  include_meta: true
};

// Make request
fetch(`${API_URL}/generate-blog`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload),
})
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Title:', data.blog.title);
      console.log('Meta:', data.blog.meta_description);
      console.log('Keywords:', data.keywords.primary_keywords);
      console.log('Word Count:', data.word_count);
    } else {
      console.error('Error:', data.error);
    }
  })
  .catch(error => console.error('Request failed:', error));
```

---

## Notes

### Response Time
- Average: 10-20 seconds
- Depends on: URL complexity, content length, LLM API speed
- Timeout: 120 seconds

### SEO Scoring
The response includes an SEO score (0-100) based on:
- Meta description length (150-160 chars): 20 points
- Title length (< 60 chars): 15 points
- Heading structure (3-7 H2s): 15 points
- Word count (800+ words): 25 points
- Keyword density (0.5-2.5%): 25 points

### Keyword Density
- Optimal: 0.5% - 2.5% (0.005 - 0.025)
- Too low: < 0.5% (keyword not emphasized enough)
- Too high: > 2.5% (keyword stuffing, penalized by search engines)
