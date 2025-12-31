from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import logging
import time

from core.database import engine, Base
from routers import auth, chat, documents

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables with retry logic
    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to create database tables (attempt {attempt}/{max_retries})...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            break
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to create tables on attempt {attempt}: {error_msg}")

            # Check for authentication errors - don't retry these
            if "Circuit breaker open" in error_msg or "authentication errors" in error_msg.lower():
                logger.error("=" * 60)
                logger.error("AUTHENTICATION ERROR: Circuit breaker is open due to too many failed auth attempts")
                logger.error("This means your DATABASE_URL credentials are incorrect or need URL encoding.")
                logger.error("")
                logger.error("SOLUTIONS:")
                logger.error("  1. Verify your password in Supabase dashboard")
                logger.error("  2. If password contains special characters, URL-encode them:")
                logger.error("     - $ becomes %24")
                logger.error("     - @ becomes %40")
                logger.error("     - : becomes %3A")
                logger.error("     - / becomes %2F")
                logger.error("     - # becomes %23")
                logger.error("  3. Wait 5-10 minutes for circuit breaker to reset")
                logger.error("  4. Check DATABASE_URL format: postgresql://user:password@host:port/dbname")
                logger.error("=" * 60)
                # Don't retry auth errors - they won't succeed
                logger.error("Stopping retries for authentication errors. Please fix DATABASE_URL and restart.")
                break

            # Check for specific Supabase errors
            if "db_termination" in error_msg or "shutdown" in error_msg:
                logger.error("SUPABASE ERROR: Database pooler is terminating connections. This usually means:")
                logger.error("  1. Database is paused (free tier) - Check Supabase dashboard")
                logger.error("  2. Wrong pooler type - Try Transaction Pooler (port 6543) instead of Session Pooler (port 5432)")
                logger.error("  3. Too many connections - Using NullPool to avoid connection pooling conflicts")

            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("Max retries reached. Application will start but database may not be ready.")
                logger.error("Please check: 1) Supabase database status, 2) DATABASE_URL is correct, 3) Using Transaction Pooler")
                # Don't raise - let the app start and handle DB errors per request

    yield
    # Shutdown: Dispose of the engine connection pool
    engine.dispose()
    logger.info("Database connection pool disposed")

# Create FastAPI app with lifespan
app = FastAPI(
    title="HR Nexus API",
    description="AI-powered HR Assistant with RAG",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - Must be added before routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        "https://hr-nexus-ai-assistant-nuar.vercel.app",
        "https://hr-nexus-ai-assistant-nuar.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "HR Nexus API is running"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to HR Nexus API",
        "docs": "/docs",
        "health": "/health"
    }