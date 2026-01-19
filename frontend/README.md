# AI Blog Generator - React Frontend

Modern React frontend for the AI Blog Generator API.

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_ENV=development
PORT=3000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   │   └── Layout.jsx  # Main layout with sidebar
│   ├── pages/          # Page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Generate.jsx
│   │   ├── History.jsx
│   │   ├── HistoryDetail.jsx
│   ├── lib/            # API and auth helpers
│   │   ├── api.js
│   │   └── auth.js
│   └── index.css       # Global styles
├── package.json        # Node dependencies
├── vite.config.js      # Vite config
├── tailwind.config.js  # Tailwind config
└── README.md           # Frontend documentation
│   │   ├── Generate.jsx
│   │   └── History.jsx
│   ├── lib/            # Utilities
│   │   ├── api.js      # Axios API client
│   │   └── auth.js     # Auth token helpers
│   ├── App.jsx         # Root component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── Dockerfile
```

## Features

- 🔐 JWT Authentication (Login/Register)
- 📝 Blog Generation from URL
- 📊 User Dashboard
- 📜 Generation History
- 🎨 Responsive Design
- ⚡ Fast Development with Vite

## Docker

```bash
# Build
docker build -t blog-frontend .

# Run
docker run -p 3000:3000 blog-frontend
```

## API Integration

The frontend expects the backend to be running at `VITE_API_BASE_URL` (default: `http://localhost:8000`).

Required backend endpoints:
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/history` - User history
- `POST /generate-blog` - Generate blog
- `GET /health` - Health check
