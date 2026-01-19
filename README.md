# 🤖 AI Blog Generator

An end-to-end full-stack AI system that generates SEO-optimized blog posts from website URLs or topics using Google Gemini and local NLP models.

## 📋 Overview

This project has evolved into a full-stack application featuring a modern React frontend and a robust FastAPI backend. It automates the blog writing process by:
1.  **Extracting Content**: Smartly scraping and cleaning content from source URLs.
2.  **Analyzing Intent**: Using local NLP (KeyBERT) to understand keywords and topics.
3.  **Generating Content**: Leveraging Google Gemini Pro/Flash for high-quality writing.
4.  **Managing Data**: Storing user history and generated blogs in MongoDB.

## 🚀 Features

-   **Full-Stack Architecture**: React (Vite) Frontend + FastAPI Backend.
-   **AI Integration**: Google Gemini for text generation.
-   **Local NLP**: KeyBERT & Sentence Transformers for cost-effective analysis.
-   **Authentication**: Secure user signup/login with JWT.
-   **History Tracking**: Save and retrieve past generated blogs.
-   **SEO Optimization**: Automatic meta description and tag generation.
-   **Legacy Support**: Includes a standalone Gradio UI (in `ui/` folder).

## 📁 Project Structure

```
blog/
├── backend/                # 🐍 FastAPI Backend
│   ├── app/                # Application logic (Auth, DB, Core AI)
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # ⚛️ React Frontend
│   ├── src/                # Components, Pages, Hooks
│   └── package.json        # Node dependencies
└── README.md               # This documentation
```

## 🛠️ Installation & Setup

### Prerequisites

-   **Python 3.9+**
-   **Node.js 16+**
-   **MongoDB Atlas** URI (for database)
-   **Google Gemini** API Key

### 1️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
# Activate it (Windows: .\venv\Scripts\activate, Mac/Linux: source venv/bin/activate)

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY and MONGODB_URL
```

### 2️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run at `http://localhost:5173` and communicate with the backend at `http://localhost:8000`.

## 📡 API Endpoints (Backend)

-   `POST /api/auth/register`: Register new user
-   `POST /api/auth/token`: Login (Get Token)
-   `POST /api/generate`: Generate blog from URL
-   `GET /api/history`: Get user's generation history


## 🧪 Optional: Gradio UI (Legacy)

If you want a simple Python-only interface for quick testing, you can use the legacy Gradio app (if present):

```bash
# From the backend directory
cd backend
python ui/gradio_app.py
```

## 📄 License

This project is created for educational and portfolio purposes.
