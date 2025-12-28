"""
Script to create .env file with database connection.
Run this once to set up your environment variables.

Usage:
    # Activate virtual environment first
    .\venv\Scripts\activate  # Windows
    # or
    source venv/bin/activate  # Linux/Mac
    
    # Then run this script
    python setup_env.py
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with database connection."""
    env_path = Path(__file__).parent / ".env"
    
    # Database URL - Get from user input or environment variable
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("\n📝 Database Configuration")
        print("Enter your PostgreSQL database URL (e.g., postgresql://user:password@host:port/database)")
        print("Note: If password contains special characters like @, use URL encoding (%40 for @)")
        database_url = input("DATABASE_URL: ").strip()
        if not database_url:
            print("⚠ Warning: DATABASE_URL not provided. You'll need to set it manually in .env")
            database_url = "postgresql://user:password@localhost:5432/database"
    
    # OpenAI API Key (from llm_explainer.py - now moved to env)
    openai_key = input("Enter your OpenAI API key: ").strip()
    
    env_content = f"""# API Settings
SECRET_KEY=your-secret-key-change-in-production-generate-a-random-string-here
API_V1_PREFIX=/api/v1

# Database - Supabase PostgreSQL
# Note: @ in password is URL-encoded as %40
DATABASE_URL={database_url}

# Redis (optional - leave empty if not using)
REDIS_URL=

# OpenAI API Key
OPENAI_API_KEY={openai_key}

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Quran Data Paths (relative to project root)
QURAN_JSON_PATH=quran_full_formatted.json
FAISS_INDEX_PATH=quran_faiss.index
QURAN_METADATA_PATH=quran_metadata.json
"""
    
    if env_path.exists():
        print(f"⚠ .env file already exists at {env_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✓ Created .env file at {env_path}")
    print("✓ Database URL configured")
    print("✓ OpenAI API key configured")
    print("\n⚠ IMPORTANT: Change SECRET_KEY to a random string for production!")
    print("   You can generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
    print("\n✓ Environment setup complete!")

if __name__ == "__main__":
    create_env_file()

