from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from core.database import engine, Base, get_db
from models import Company, User, Chat, Message, MessageFeedback, Document
from routers import auth

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="HR Nexus API",
    description="AI-powered HR Assistant with RAG",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

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