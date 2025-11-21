# HR Assistant - Bootcamp Deployment Guide

## Architecture Overview

```
┌──────────────────┐
│   Frontend (UI)  │  → Vercel/Netlify
│   React + Vite   │
└────────┬─────────┘
         │ HTTPS
         ↓
┌──────────────────┐
│  Backend (API)   │  → Render/Railway
│   FastAPI        │
└────┬────────┬────┘
     │        │
     ↓        ↓
┌─────────┐ ┌──────────┐
│PostgreSQL│ │ ChromaDB │
│ Supabase │ │ (local)  │
└──────────┘ └──────────┘
```

## 📋 What You Need

### 5 Essential Tables (PostgreSQL)
1. **users** - Authentication
2. **chats** - Conversation history
3. **messages** - Chat messages
4. **message_feedback** - Thumbs up/down
5. **documents** - File metadata

### Storage
- **Files**: `uploads/` folder on backend or Supabase Storage
- **Embeddings**: ChromaDB (runs with your backend)

---

## 🚀 Step-by-Step Deployment

### 1️⃣ Database Setup (Supabase - Free)

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Go to SQL Editor
4. Run: `database/migrations/001_bootcamp_schema.sql`
5. Copy connection string from Settings → Database

**Add to backend `.env`:**
```env
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
```

---

### 2️⃣ Backend Deployment (Render - Free)

#### Prepare Backend

Create `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
chromadb==0.4.18
langchain==0.1.0
openai==1.3.0
```

Create `Dockerfile` (optional):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Deploy on Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Web Service
4. Connect GitHub repo
5. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
6. Add environment variables:
   ```
   DATABASE_URL=postgresql://...
   JWT_SECRET=your-super-secret-key-change-this
   JWT_ALGORITHM=HS256
   OPENAI_API_KEY=sk-...
   ```

7. Deploy!

**Your API will be at**: `https://your-app.onrender.com`

---

### 3️⃣ Frontend Deployment (Vercel - Free)

1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repo (UI folder)
3. Framework: Vite
4. Root Directory: `UI`
5. Add environment variable:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```
6. Deploy!

**Update CORS in backend** (`main.py`):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local dev
        "https://your-frontend.vercel.app"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔐 Security Checklist

### ✅ Must Have
- [x] Hash passwords with `bcrypt`
- [x] Use JWT for authentication
- [x] Environment variables for secrets
- [x] CORS configured properly
- [x] HTTPS (automatic on Render/Vercel)

### ❌ Don't Need (for bootcamp)
- [ ] Rate limiting
- [ ] Advanced caching
- [ ] Load balancing
- [ ] Kubernetes

---

## 📝 Environment Variables

### Backend (Render)
```env
DATABASE_URL=postgresql://...
JWT_SECRET=random-secret-string-change-this
JWT_ALGORITHM=HS256
OPENAI_API_KEY=sk-...
CHROMA_PERSIST_DIR=./chroma_data
```

### Frontend (Vercel)
```env
VITE_API_URL=https://your-backend.onrender.com
```

---

## �� Testing Deployment

### 1. Test Backend
```bash
curl https://your-backend.onrender.com/health
# Should return: {"status": "ok"}
```

### 2. Test Frontend
Visit: `https://your-frontend.vercel.app`

### 3. Test Full Flow
1. Register a user
2. Upload a document
3. Ask a question
4. Verify RAG retrieval works

---

## 💾 Data Flow

```
1. User uploads PDF
   ↓
2. Backend saves to uploads/ folder
   ↓
3. Store metadata in documents table
   ↓
4. Split PDF into chunks
   ↓
5. Generate embeddings (OpenAI)
   ↓
6. Store embeddings in ChromaDB
   ↓
7. User asks question
   ↓
8. Query ChromaDB for relevant chunks
   ↓
9. Send to LLM with context
   ↓
10. Return answer + save to messages table
```

---

## 🐛 Common Issues

### "Connection refused"
- Check DATABASE_URL is correct
- Ensure Supabase database is active

### "CORS error"
- Add your frontend URL to allow_origins
- Check HTTPS (not HTTP)

### "ChromaDB not persisting"
- Set CHROMA_PERSIST_DIR in env vars
- Ensure directory has write permissions

### "Render service sleeping"
- Free tier sleeps after inactivity
- First request takes ~30 seconds
- Consider upgrading or using Railway

---

## 📊 Free Tier Limits

| Service | Limit |
|---------|-------|
| **Supabase** | 500MB database, 1GB bandwidth |
| **Render** | 750 hrs/month (sleeps after 15min) |
| **Vercel** | 100GB bandwidth |
| **OpenAI** | Pay-as-you-go ($5 credit for new users) |

---

## 🎯 Bootcamp Demo Tips

1. **Prepare sample documents** (3-5 PDFs about HR policies)
2. **Pre-seed questions** to show off RAG
3. **Show before/after** of uploaded documents
4. **Demonstrate chat history**
5. **Highlight feedback mechanism**

---

## 📚 Useful Commands

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd UI
npm install
npm run dev
```

### Database Migrations
```bash
# Connect to Supabase
psql "postgresql://..."

# Run migration
\i database/migrations/001_bootcamp_schema.sql

# Verify tables
\dt
```

---

## 🎓 What to Present

1. **Architecture diagram** (show this file)
2. **Live demo** (upload → query → response)
3. **Code walkthrough** (FastAPI routes, RAG pipeline)
4. **Database schema** (show tables)
5. **Challenges faced** (embedding costs, chunking strategy)

---

## 🔗 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Render Deployment](https://render.com/docs)
- [Vercel Deployment](https://vercel.com/docs)

---

## 📧 Quick Links

- Frontend: `https://[your-app].vercel.app`
- Backend API: `https://[your-app].onrender.com`
- API Docs: `https://[your-app].onrender.com/docs`
- Database: Supabase Dashboard

---

**Good luck with your bootcamp presentation! 🚀**
