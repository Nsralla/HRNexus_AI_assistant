# HR Nexus - AI-Powered HR Assistant

An intelligent HR assistant application with RAG (Retrieval-Augmented Generation) capabilities, built for a bootcamp project.

## Tech Stack

### Frontend
- **React** with Vite
- **Tailwind CSS** for styling
- **React Router** for navigation

### Backend
- **FastAPI** (Python)
- **PostgreSQL** (Supabase) for data storage
- **ChromaDB** for vector embeddings
- **LangChain** + **OpenAI** for LLM integration
- **JWT** authentication with bcrypt password hashing

## Project Structure

```
HRAssistant/
├── UI/                 # Frontend React application
├── backend/            # FastAPI backend
│   ├── core/          # Core utilities (auth, database)
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API routes
│   └── schemas/       # Pydantic schemas
└── database/          # Database migrations and schema
```

## Features

- ✅ Multi-tenant architecture
- ✅ User authentication (register, login, JWT tokens)
- ✅ Secure password hashing with bcrypt
- ✅ PostgreSQL database with Supabase
- ✅ ChromaDB for document embeddings
- 🔄 Chat interface (in progress)
- 🔄 Document upload and RAG (in progress)

## Setup

### Backend

1. Create virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your credentials

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd UI
   npm install
   ```

2. Run development server:
   ```bash
   npm run dev
   ```

## Deployment

- **Frontend**: Vercel
- **Backend**: Render/Railway
- **Database**: Supabase (PostgreSQL)
- **Vector DB**: ChromaDB (runs with backend)

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

Bootcamp Project - Educational Use Only
