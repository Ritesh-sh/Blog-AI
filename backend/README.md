# AI Blog Generator - Backend

FastAPI backend for the AI Blog Generator with Gemini AI.

## Tech Stack

- **FastAPI** - Web framework
- **Google Gemini** - LLM for blog generation
- **MongoDB Atlas** - User data & history storage
- **Motor** - Async MongoDB driver
- **JWT** - Authentication
- **KeyBERT** - Keyword extraction
- **Unsplash API** - Blog images

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py         # Settings & environment config
│   ├── main.py           # FastAPI app entry point
│   ├── models.py         # Pydantic models
│   ├── db.py             # MongoDB Atlas connection
│   ├── auth.py           # JWT authentication
│   ├── routes/
│   │   └── auth.py       # Auth endpoints
│   └── core/
│       ├── blog_generator.py
│       ├── content_extractor.py
│       ├── keyword_extractor.py
│       ├── topic_analyzer.py
│       ├── prompt_builder.py
│       ├── seo_postprocessor.py
│       └── image_fetcher.py
├── ui/
│   └── gradio_app.py     # Gradio UI (optional)
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

## Quick Start

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables (copy from .env.example)
cp ../.env.example .env
# Edit .env with your API keys

# Run development server
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `MONGODB_URI` | MongoDB Atlas connection string | For auth/history |
| `JWT_SECRET_KEY` | Secret for JWT tokens | For auth |
| `UNSPLASH_ACCESS_KEY` | Unsplash API key | For images |

## API Endpoints

### Public
- `GET /` - API info
- `GET /health` - Health check
- `POST /generate-blog` - Generate blog from URL
- `POST /estimate-cost` - Estimate generation cost

### Protected (JWT required)
- `POST /auth/register` - Register user
- `POST /auth/login` - Login & get token
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get current user
- `GET /auth/history` - Get user history

## Docker

```bash
# Build
docker build -t blog-backend .

# Run
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e MONGODB_URI=your_uri \
  blog-backend
```

## Running with Gradio UI

```bash
python -m ui.gradio_app
```

Access at http://localhost:7860
