# HR Nexus - AI-Powered HR Assistant

An intelligent HR assistant powered by LLMs, RAG (Retrieval-Augmented Generation), and LangGraph for advanced agentic workflows. The system provides real-time HR support with access to company documentation, employee data, and web search capabilities.

## 🎯 Overview

HR Nexus is a comprehensive AI assistant that helps employees and HR staff with:
- **Intelligent Q&A** about company policies and procedures
- **Employee Information** lookup and queries
- **Real-time Web Search** for up-to-date information
- **Custom Document Upload** to expand the knowledge base
- **Multi-tenant Architecture** for multiple companies
- **Conversational Memory** for context-aware responses

## ✨ Key Features

### 🤖 AI & LLM Capabilities
- **Advanced RAG Pipeline** with ChromaDB vector database
- **LangGraph Agentic Workflows** for multi-step reasoning
- **CrewAI Agents** for specialized task handling
- **OpenAI GPT-4** integration for intelligent responses
- **Cohere Embeddings** for semantic search
- **Streaming Responses** for real-time chat experience

### 💬 Chat & Conversation
- **Multi-turn Conversations** with persistent chat history
- **Context-aware Responses** using conversation history
- **Streaming Support** for token-by-token responses
- **Chat Management** (create, list, delete conversations)
- **Auto-naming** chats based on first message

### 📚 Knowledge Base & RAG
- **Document Upload** - Upload and embed custom documents (.txt, .md, .json, .csv, .pdf)
- **Vector Search** across all company documentation
- **Markdown Documentation** support for policies and guides
- **JSON Data Integration** for structured information
- **Real-time Web Search** via Tavily API
- **Semantic Search** with Cohere embeddings

### 🔐 Authentication & Security
- **JWT Token Authentication** with secure password hashing (bcrypt)
- **Multi-tenant Architecture** with company isolation
- **Role-based Access Control** 
- **Session Management** with automatic token refresh
- **Secure API Endpoints** with authentication middleware

### 📊 Data Management
- **PostgreSQL Database** (Supabase) for structured data
- **Employee Information** queries and management
- **Project & Sprint Tracking** integration
- **Jira Tickets** access and querying
- **Meeting Notes** retrieval
- **Service & Deployment** information

### 🎨 User Interface
- **Modern React UI** with Tailwind CSS
- **Responsive Design** for mobile and desktop
- **Dark Theme** sidebar with chat history
- **Animated Components** using Framer Motion
- **Guide Cards** for new users
- **File Upload Modal** with drag & drop
- **Real-time Upload Progress** tracking
- **Error Handling** with user-friendly messages

### 🔧 Developer Features
- **FastAPI Backend** with automatic API documentation
- **OpenAPI/Swagger** documentation at `/docs`
- **Modular Architecture** for easy extension
- **MCP (Model Context Protocol)** support
- **Comprehensive Logging** for debugging
- **Type Safety** with TypeScript (frontend) and Pydantic (backend)

## 🏗️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Router** for navigation
- **Axios** for API requests

### Backend
- **FastAPI** (Python 3.10+)
- **SQLAlchemy** ORM with PostgreSQL
- **LangChain** for LLM orchestration
- **LangGraph** for agentic workflows
- **CrewAI** for multi-agent systems
- **ChromaDB** for vector embeddings
- **Cohere** for embeddings
- **OpenAI GPT-4** for chat
- **Tavily** for web search
- **JWT** authentication with python-jose
- **Bcrypt** for password hashing

### Infrastructure
- **PostgreSQL** (Supabase) for data storage
- **ChromaDB** for vector embeddings (local)
- **Cohere API** for embeddings
- **OpenAI API** for LLM
- **Tavily API** for web search

## 📁 Project Structure

```
HRNexus_AI_assistant/
├── UI/                          # Frontend React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/           # Chat UI components
│   │   │   │   ├── ChatArea.tsx
│   │   │   │   ├── InputArea.tsx
│   │   │   │   ├── LeftSidebar.tsx
│   │   │   │   ├── DocumentUpload.tsx  # NEW: Upload modal
│   │   │   │   └── ...
│   │   │   ├── sections/       # Landing page sections
│   │   │   └── shared/         # Shared components
│   │   ├── pages/
│   │   │   ├── ChatPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── SignupPage.tsx
│   │   └── services/           # API services
│   │       ├── api.config.ts
│   │       ├── chat.service.tsx
│   │       ├── auth.service.ts
│   │       └── document.service.ts  # NEW: Document upload
│   └── package.json
│
├── backend/                     # FastAPI backend
│   ├── agents/                 # AI agents
│   │   ├── crew_ai.py          # CrewAI agent orchestration
│   │   ├── agent_config.yaml   # Agent configurations
│   │   └── streaming.py        # Streaming support
│   ├── core/                   # Core utilities
│   │   ├── auth.py             # JWT authentication
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database connection
│   │   └── mcp.py              # MCP protocol support
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── chat.py
│   │   ├── message.py
│   │   ├── message_feedback.py
│   │   └── document.py         # NEW: Document metadata
│   ├── routers/                # API routes
│   │   ├── auth.py             # Auth endpoints
│   │   ├── chat.py             # Chat endpoints
│   │   └── documents.py        # NEW: Document upload API
│   ├── services/               # Business logic
│   │   ├── chat_pipeline.py    # Main chat pipeline
│   │   ├── document_processor.py  # NEW: Document processing
│   │   ├── tavily_search_service.py  # Web search
│   │   └── *Service.py         # Data services
│   ├── tools/                  # LangChain tools
│   │   ├── format_tool.py
│   │   └── summary_tool.py
│   ├── prompts/                # AI prompts
│   │   ├── intent_classification.py
│   │   ├── general_conversation.py
│   │   ├── data_query.py
│   │   └── documentation_query.py
│   ├── sources/                # Data sources
│   │   ├── kb/                 # Knowledge base (markdown)
│   │   └── Json_files/         # Structured data
│   ├── uploads/                # NEW: Uploaded documents
│   ├── chroma_db/              # Vector database
│   ├── rag_data_loader.py      # RAG data loading
│   ├── main.py                 # FastAPI app
│   └── requirements.txt
│
├── database/                    # Database schema
│   ├── migrations/
│   └── schema.dbml
│
└── kb/                         # Knowledge base files
    ├── code_review_policy.md
    ├── deployment_process.md
    ├── dev_env_setup.md
    ├── escalation_policy.md
    ├── onboarding_guide.md
    └── team_structure.md
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **PostgreSQL** database (Supabase account)
- **API Keys**:
  - OpenAI API key
  - Cohere API key
  - Tavily API key (optional, for web search)

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```bash
   # Database
   DATABASE_URL=postgresql://user:password@host:port/database
   
   # JWT
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # OpenAI
   OPENAI_API_KEY=your-openai-api-key
   
   # Cohere (for embeddings)
   COHERE_API_KEY=your-cohere-api-key
   
   # Tavily (for web search)
   TAVILY_API_KEY=your-tavily-api-key
   
   # Optional
   UPLOAD_DIR=./uploads
   CHROMA_PERSIST_DIR=./chroma_db
   ```

4. **Initialize the vector database:**
   ```bash
   python rag_data_loader.py
   ```

5. **Run the server:**
   ```bash
   python3 -m uvicorn main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd UI
   npm install
   ```

2. **Create `.env` file (if needed):**
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

### Initial Data Setup (Optional)

The system comes with sample data in `backend/sources/Json_files/`:
- `employees.json` - Employee information
- `projects.json` - Project data
- `jira_tickets.json` - Jira tickets
- `meetings.json` - Meeting notes
- `services.json` - Service information
- `deployments.json` - Deployment history
- `sprints.json` - Sprint data

## 📖 Usage

### Basic Workflow

1. **Sign Up / Login**: Create an account or log in
2. **Start Chatting**: Ask questions about company policies, employees, or general topics
3. **Upload Documents**: Add custom documents to expand the knowledge base
4. **Web Search**: Ask questions that require real-time information
5. **Provide Feedback**: Rate responses with 👍/👎

### Example Queries

**HR Policies:**
- "What is our code review policy?"
- "How do I set up my development environment?"
- "What's the escalation process for critical bugs?"

**Employee Information:**
- "Who is on the backend team?"
- "List all senior developers"
- "Show me Sarah Johnson's contact information"

**Project Data:**
- "What projects is John working on?"
- "Show me all active projects"
- "What's the status of the Analytics Platform?"

**Web Search:**
- "What are the latest React 18 features?"
- "Current best practices for API security"
- "Latest news about AI developments"

### Document Upload

1. Click **"Upload Documents"** button in sidebar
2. Drag & drop files or click to browse
3. Supported formats: `.txt`, `.md`, `.json`, `.csv`, `.pdf`
4. Max file size: 10MB per file
5. Files are automatically:
   - Processed and chunked
   - Embedded with Cohere
   - Added to vector database
   - Searchable in chat

## 🔌 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login/json` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Chat Endpoints

- `POST /api/chat/` - Create new chat
- `GET /api/chat/` - List user's chats
- `GET /api/chat/{chat_id}` - Get chat details
- `PATCH /api/chat/{chat_id}` - Update chat title
- `DELETE /api/chat/{chat_id}` - Delete chat
- `POST /api/chat/message` - Send message (with streaming)
- `GET /api/chat/{chat_id}/messages` - Get chat messages
- `POST /api/chat/message/{message_id}/feedback` - Rate message

### Document Endpoints (NEW)

- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - List documents
- `GET /api/documents/{doc_id}` - Get document details
- `DELETE /api/documents/{doc_id}` - Delete document
- `GET /api/documents/stats/vectorstore` - Vector store statistics

### Interactive Documentation

Once the backend is running:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🎨 Features in Detail

### RAG Pipeline

The RAG (Retrieval-Augmented Generation) system:
1. Embeds user queries using Cohere
2. Searches ChromaDB for relevant context
3. Retrieves top-k most relevant chunks
4. Passes context to LLM for response generation
5. Streams response back to user

### Agentic Workflows

LangGraph orchestrates multi-step reasoning:
1. **Intent Classification** - Determines query type
2. **Tool Selection** - Chooses appropriate data sources
3. **Information Retrieval** - Fetches relevant data
4. **Response Generation** - Synthesizes final answer
5. **Streaming** - Delivers response in real-time

### Document Processing

Uploaded documents go through:
1. **Validation** - File type and size checks
2. **Text Extraction** - Content parsing
3. **Chunking** - Split into optimal sizes (1000 chars)
4. **Embedding** - Generate vector embeddings
5. **Storage** - Save to ChromaDB and PostgreSQL
6. **Indexing** - Make searchable immediately

## 🚢 Deployment

### Frontend (Vercel)

```bash
cd UI
npm run build
# Deploy to Vercel
```

### Backend (Render/Railway)

```bash
# Set environment variables in platform
# Deploy from GitHub repository
```

### Database (Supabase)

- PostgreSQL hosted on Supabase
- Automatic backups
- Connection pooling enabled

### Vector Database

- ChromaDB runs with backend
- Persisted to disk
- Backed up with application data

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd UI
npm run test
```

### Manual Testing

```bash
# Test document upload
python backend/test_document_upload_setup.py

# Test chat pipeline
python backend/test_chat_pipeline_web_search.py

# Test Tavily search
python backend/test_tavily.py
```

## 📊 Performance

- **Average Response Time**: 2-5 seconds
- **Streaming**: Token-by-token delivery
- **Vector Search**: <100ms for similarity search
- **Document Upload**: 1-3 seconds per MB
- **Concurrent Users**: Scales with backend instances

## 🛠️ Development

### Adding New Features

1. **Backend**: Add route in `routers/`, implement in `services/`
2. **Frontend**: Create component in `components/`, add to page
3. **Database**: Update models in `models/`, run migrations
4. **AI**: Modify prompts in `prompts/`, update agents

### Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Follow ESLint config
- **Commits**: Conventional commits format

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Check DATABASE_URL format
- Verify Supabase database is active
- Ensure connection pooling is configured

**Embedding API Error**
- Verify COHERE_API_KEY is set
- Check API quota/limits
- Ensure network connectivity

**Upload Fails**
- Check file size (max 10MB)
- Verify file type is supported
- Ensure uploads directory exists

**ChromaDB Error**
- Check chroma_db directory permissions
- Verify disk space available
- Try deleting and recreating vector store

## 📝 Documentation

- `CHAT_PIPELINE_WORKFLOW.md` - Chat system architecture
- `TAVILY_INTEGRATION.md` - Web search integration
- `DEPLOYMENT.md` - Deployment guide
- `PROJECT_PRESENTATION.md` - Project overview

## 🤝 Contributing

This is a bootcamp project. For educational purposes only.

## 📄 License

Educational Use Only - Bootcamp Project

## 🙏 Acknowledgments

- **LangChain** for LLM orchestration
- **CrewAI** for agent frameworks
- **Cohere** for embeddings
- **OpenAI** for GPT-4
- **FastAPI** for the amazing backend framework
- **React** for the frontend framework

---

**Built with ❤️ for HR teams everywhere**
