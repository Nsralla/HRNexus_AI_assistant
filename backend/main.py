from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import logging
import time

from core.database import engine, Base
from routers import auth, chat

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
            logger.error(f"Failed to create tables on attempt {attempt}: {str(e)}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("Max retries reached. Application will start but database may not be ready.")
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