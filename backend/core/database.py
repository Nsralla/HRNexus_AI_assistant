from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set!")
    raise ValueError("DATABASE_URL must be set in environment variables")

# Validate DATABASE_URL format
try:
    parsed = urlparse(DATABASE_URL)
    if not parsed.scheme or not parsed.hostname:
        logger.warning("DATABASE_URL format may be invalid. Expected: postgresql://user:password@host:port/dbname")
except Exception as e:
    logger.warning(f"Could not parse DATABASE_URL: {e}")

logger.info(f"Initializing database connection...")
logger.info(f"Database host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'}")

# Detect if using Supabase pooler and adjust settings accordingly
is_pooler = "pooler.supabase.com" in DATABASE_URL if DATABASE_URL else False

try:
    if is_pooler:
        # For ANY Supabase Pooler (Session or Transaction): Use NullPool
        # This prevents "{:shutdown, :db_termination}" errors by letting Supabase handle ALL pooling
        from sqlalchemy.pool import NullPool
        logger.info("Using Supabase pooler with NullPool (no SQLAlchemy connection pooling)")
        engine = create_engine(
            DATABASE_URL,
            poolclass=NullPool,  # No SQLAlchemy pooling - Supabase pooler handles connections
            connect_args={
                "connect_timeout": 10,
            }
        )
    else:
        # For direct connection: Use SQLAlchemy's connection pooling
        logger.info("Using direct connection with SQLAlchemy connection pooling")
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            pool_timeout=30,
            connect_args={
                "connect_timeout": 10,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            }
        )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
