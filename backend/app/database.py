"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

# Create database engine
# Use NullPool for Supabase to avoid connection pool issues
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        poolclass=NullPool,  # Disable connection pooling for Supabase
        connect_args={
            "sslmode": "require"  # Supabase requires SSL
        }
    )
except Exception as e:
    print(f"⚠ Database engine creation error: {e}")
    # Fallback without SSL (for local development)
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        poolclass=NullPool
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

