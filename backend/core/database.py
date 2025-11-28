from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Detect if using Supabase pooler and adjust settings accordingly
is_pooler = "pooler.supabase.com" in DATABASE_URL if DATABASE_URL else False

if is_pooler:
    # For ANY Supabase Pooler (Session or Transaction): Use NullPool
    # This prevents "{:shutdown, :db_termination}" errors by letting Supabase handle ALL pooling
    from sqlalchemy.pool import NullPool
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,  # No SQLAlchemy pooling - Supabase pooler handles connections
        connect_args={
            "connect_timeout": 10,
        }
    )
else:
    # For direct connection: Use SQLAlchemy's connection pooling
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
