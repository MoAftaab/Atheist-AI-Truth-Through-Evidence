# Atheist AI - Citation-Locked Quran Q&A System

<div align="center">

![Atheist AI](screenshot/logo.png)

**A Quran-centric, citation-locked Question Answering system that answers user questions only using the Quran itself, without hallucination, interpretation drift, or external religious commentary.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.0-000000?style=flat&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.2-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.6-336791?style=flat&logo=postgresql)](https://www.postgresql.org/)

</div>

## 🎯 Core Philosophy

**Truth Preservation**: Instead of letting an LLM freely generate answers (which often leads to invented explanations or mixing of sources), this system enforces a strict Retrieval-Augmented Generation (RAG) pipeline where every answer must be explicitly supported by Quranic verses retrieved from a verified dataset.

## 🖼️ Project Showcase

### Landing Page
![Landing Page](screenshot/landing%20page.png)
*Clean, minimalist landing page with bold typography and calligraphy-inspired design. Features hero section, feature cards, and call-to-action buttons.*

### Q&A Chat Interface
![Chat UI](screenshot/chatui.png)
*Modern conversational chat interface for asking questions about the Quran. User messages appear in black bubbles, assistant responses in white with citations.*

### Supporting Verses Display
![Supporting Verses](screenshot/supporting%20verses.png)
*Answer display with supporting Quranic verses. Shows Arabic text, translations, and relevance scores in an elegant card layout.*

## 📋 Table of Contents

- [Project Showcase](#️-project-showcase)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality
- **Citation-Locked Answers**: Every response is backed by explicit Quranic verse citations
- **Semantic Search**: FAISS-powered vector search for finding relevant verses
- **No Hallucinations**: Strict enforcement prevents LLM from inventing verses
- **Context-Aware**: Retrieves surrounding verses for better understanding
- **Fast Performance**: Redis caching and optimized query processing

### User Features
- **User Authentication**: Secure JWT-based login/register system
- **Query History**: Save and access your past questions (for authenticated users)
- **Beautiful UI**: Modern black & white minimalist design
- **Chat Interface**: Conversational Q&A experience
- **Responsive Design**: Works seamlessly on desktop and mobile

### Technical Features
- **RESTful API**: Well-documented FastAPI backend
- **Type Safety**: Full TypeScript support in frontend
- **Error Handling**: Comprehensive error handling and validation
- **Database Integration**: PostgreSQL for user data and query history
- **Caching Layer**: Redis for query result caching (optional)

## 🏗️ Architecture

### System Architecture

![Architecture Diagram](screenshot/architecture.png)
*Complete system architecture showing the flow from frontend to backend, RAG pipeline, and data storage layers.*

### Data Flow

1. **User Query** → Frontend sends query to `/api/v1/queries/query`
2. **Cache Check** → Backend checks Redis for cached result
3. **RAG Pipeline**:
   - Query embedded using Sentence Transformers
   - FAISS semantic search finds relevant verses
   - Context window added to verses
   - Citation bundle created
4. **LLM Generation** → OpenAI GPT-4o-mini generates answer from citations only
5. **Response** → Answer + citations returned to frontend
6. **Storage** → Query saved to database (if user authenticated)

## 🛠️ Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104.1 | Modern Python web framework with async support |
| **SQLAlchemy** | 2.0.23 | ORM for database operations |
| **PostgreSQL** | 17.6 | Relational database (Supabase) |
| **Redis** | 5.0.1 | Query result caching (optional) |
| **FAISS** | ≥1.8.0 | Vector similarity search |
| **Sentence Transformers** | 2.2.2 | Text embeddings (all-MiniLM-L6-v2) |
| **OpenAI** | ≥1.3.5 | GPT-4o-mini for answer generation |
| **JWT** | python-jose | Stateless authentication |
| **bcrypt** | ≥4.0.0 | Password hashing |
| **Pydantic** | 2.5.0 | Data validation |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.2.0 | React framework with SSR |
| **TypeScript** | 5.3.2 | Type safety |
| **Tailwind CSS** | 3.3.6 | Utility-first CSS framework |
| **Framer Motion** | 10.16.4 | Smooth animations |
| **React Query** | 5.8.4 | Data fetching and caching |
| **Axios** | 1.6.2 | HTTP client |
| **Lucide React** | 0.294.0 | Icon library |

### Infrastructure

- **Database**: Supabase PostgreSQL (cloud-hosted)
- **Cache**: Upstash Redis (optional, serverless)
- **Deployment**: 
  - Backend: Railway/Render
  - Frontend: Vercel

## 📁 Project Structure

```
atheist_rag/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── config.py           # Environment variables & settings
│   │   ├── models.py           # SQLAlchemy models (User, QueryHistory)
│   │   ├── schemas.py          # Pydantic schemas for validation
│   │   ├── database.py         # Database connection & session
│   │   ├── auth.py             # JWT authentication utilities
│   │   ├── dependencies.py     # FastAPI dependencies
│   │   ├── routers/
│   │   │   ├── auth.py         # /auth/login, /auth/register, /auth/me
│   │   │   ├── queries.py      # /queries/query, /queries/history
│   │   │   └── health.py       # /health check
│   │   └── services/
│   │       ├── quran_service.py    # RAG pipeline wrapper
│   │       └── cache_service.py    # Redis caching layer
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── run.py                  # Development server
│   ├── test_connections.py    # Backend testing script
│   └── setup_env.py            # Environment setup
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx      # Root layout
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── qa/
│   │   │   │   └── page.tsx     # Q&A chat interface
│   │   │   ├── login/
│   │   │   │   └── page.tsx     # Login page
│   │   │   ├── register/
│   │   │   │   └── page.tsx     # Register page
│   │   │   └── history/
│   │   │       └── page.tsx     # Query history
│   │   ├── components/
│   │   │   ├── Header.tsx       # Navigation header
│   │   │   ├── QueryInput.tsx  # Query input form
│   │   │   ├── AnswerDisplay.tsx # Answer display (legacy)
│   │   │   ├── VerseCard.tsx   # Verse citation card
│   │   │   ├── AuthForm.tsx    # Authentication form
│   │   │   └── LoadingSpinner.tsx
│   │   ├── lib/
│   │   │   ├── api.ts          # API client functions
│   │   │   └── auth.tsx        # Auth context & hooks
│   │   └── styles/
│   │       └── globals.css     # Global styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── next.config.js
│
├── quran_retrieval2.py         # FAISS-based retrieval system
├── llm_explainer.py            # LLM explanation layer
├── quran_faiss.index           # FAISS vector index
├── quran_full_formatted.json   # Quran data (ayahs)
├── quran_metadata.json          # Verse metadata
├── quran_texts.json             # Searchable texts
└── README.md                    # This file
```

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Endpoints

#### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "atheist-ai-api"
}
```

---

#### 2. User Registration

**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Validation error

---

#### 3. User Login

**POST** `/auth/login`

Authenticate and get access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Incorrect email or password

---

#### 4. Get Current User

**GET** `/auth/me`

Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token

---

#### 5. Query Quran

**POST** `/queries/query`

Query the Quran using RAG pipeline. **Public endpoint** - works with or without authentication.

**Request Body:**
```json
{
  "query": "What does the Quran say about fasting?",
  "k": 5,
  "score_threshold": 0.5,
  "window": 1
}
```

**Parameters:**
- `query` (string, required): The question to ask
- `k` (integer, optional, default: 5): Number of verses to retrieve
- `score_threshold` (float, optional): Minimum similarity score (0.0-1.0)
- `window` (integer, optional, default: 1): Context window size (number of surrounding verses)

**Response:** `200 OK`
```json
{
  "query": "What does the Quran say about fasting?",
  "answer": "The Quran mentions fasting in several verses. In Surah Al-Baqarah (2:183-185), it states that fasting is prescribed for believers as it was prescribed for those before them, so that they may become righteous. The verses explain that fasting is for a fixed number of days, and if anyone is ill or on a journey, they should fast the same number of days later. The month of Ramadan is specifically mentioned as the time when the Quran was revealed, and during this month, believers should fast from dawn until sunset.",
  "citations": [
    {
      "surah_number": 2,
      "surah_name_english": "Al-Baqarah",
      "ayah_number": 183,
      "text_simple": "يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ كَمَا كُتِبَ عَلَى الَّذِينَ مِن قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ",
      "translation_en_yusufali": "O ye who believe! Fasting is prescribed to you as it was prescribed to those before you, that ye may (learn) self-restraint,",
      "score": 0.8567,
      "context": [
        {
          "surah_number": 2,
          "surah_name_english": "Al-Baqarah",
          "ayah_number": 184,
          "text_simple": "...",
          "translation_en_yusufali": "..."
        }
      ]
    },
    {
      "surah_number": 2,
      "surah_name_english": "Al-Baqarah",
      "ayah_number": 185,
      "text_simple": "شَهْرُ رَمَضَانَ الَّذِي أُنزِلَ فِيهِ الْقُرْآنُ هُدًى لِّلنَّاسِ وَبَيِّنَاتٍ مِّنَ الْهُدَىٰ وَالْفُرْقَانِ",
      "translation_en_yusufali": "Ramadan is the (month) in which was sent down the Qur'an, as a guide to mankind, also clear (Signs) for guidance and judgment (Between right and wrong).",
      "score": 0.8234,
      "context": []
    }
  ],
  "has_answer": true,
  "processing_time": 1.234
}
```

**Error Responses:**
- `500 Internal Server Error`: Service error (check backend logs)

**Notes:**
- If `has_answer` is `false`, the answer will be: "The Qur'an does not explicitly address this question."
- Citations are sorted by relevance score (highest first)
- Processing time includes embedding, search, and LLM generation

---

#### 6. Get Query History

**GET** `/queries/history`

Get query history for authenticated user. **Requires authentication.**

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `skip` (integer, optional, default: 0): Number of records to skip
- `limit` (integer, optional, default: 50): Maximum number of records to return

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "query": "What does the Quran say about fasting?",
    "answer": "The Quran mentions fasting...",
    "citations": "[{\"surah_number\":2,...}]",
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "query": "What is the meaning of prayer?",
    "answer": "Prayer in the Quran...",
    "citations": null,
    "created_at": "2024-01-15T09:15:00Z"
  }
]
```

**Error Responses:**
- `401 Unauthorized`: Authentication required

---

### API Response Format

All successful responses follow this structure:

```json
{
  "data": {...},           // Response data
  "status": "success"      // Status indicator
}
```

Error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**HTTP Status Codes:**
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

## 🚀 Installation

### Option 1: Docker (Recommended)

See [DOCKER.md](DOCKER.md) for detailed Docker setup instructions.

**Quick start:**
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Option 2: Manual Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (or use Supabase)
- OpenAI API key
- Redis (optional, for caching)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
python setup_env.py
```

Or manually create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your-openai-api-key
REDIS_URL=redis://localhost:6379  # Optional
CORS_ORIGINS=http://localhost:3000
```

5. **Test backend:**
```bash
python test_connections.py
```

6. **Run backend server:**
```bash
python run.py
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Run development server:**
```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🎨 Design Philosophy

The UI follows a **bold black & white minimalist design**:

- **2px black borders** throughout
- **High contrast** for readability
- **No rounded corners** - sharp, geometric shapes
- **Bold typography** - font-black for headings
- **Calligraphy-inspired** decorative elements
- **Consistent design language** across all pages

## 🔒 Security Features

- **JWT Authentication**: Stateless token-based auth
- **Password Hashing**: bcrypt with 72-byte limit handling
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Pydantic schemas for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM
- **Environment Variables**: Secrets stored in `.env` (gitignored)

## 📊 Performance

- **Query Response Time**: < 2 seconds (uncached), < 100ms (cached)
- **Page Load Time**: < 1 second (Next.js SSR)
- **API Latency**: < 500ms (uncached), < 50ms (cached)
- **Caching**: Redis for frequent queries (1 hour TTL)

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_connections.py
```

### Frontend-Backend Integration
```bash
cd backend
python test_frontend_backend.py
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy

**Backend (Railway):**
1. Connect GitHub repository
2. Add PostgreSQL database
3. Set environment variables
4. Deploy!

**Frontend (Vercel):**
1. Import GitHub repository
2. Set `NEXT_PUBLIC_API_URL`
3. Deploy!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Mohammad Aftaab**

- LinkedIn: [mohammad-aftaab-b49a5624a](https://www.linkedin.com/in/mohammad-aftaab-b49a5624a/)
- GitHub: [@MoAftaab](https://github.com/MoAftaab)

## 🙏 Acknowledgments

- Quran data source: [quran.com](https://quran.com)
- Translation: Yusuf Ali
- Built with dedication to truth preservation

---

<div align="center">

**Built with ❤️ for truth preservation**

[Report Bug](https://github.com/MoAftaab/atheist_rag/issues) · [Request Feature](https://github.com/MoAftaab/atheist_rag/issues)

</div>

