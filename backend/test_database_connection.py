"""
Test database connection script.
Run this to verify your Supabase PostgreSQL connection is working.

Usage:
    python test_database_connection.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.config import settings
from app.database import engine, Base
from app.models import User, QueryHistory
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

def test_database_connection():
    """Test database connection and operations."""
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    
    # Show connection string (masked password)
    db_url_display = settings.DATABASE_URL
    if "@" in db_url_display:
        # Mask password in display
        parts = db_url_display.split("@")
        if ":" in parts[0]:
            user_pass = parts[0].split(":")
            if len(user_pass) > 1:
                db_url_display = f"{user_pass[0]}:****@{parts[1]}"
    
    print(f"Database URL: {db_url_display}")
    print()
    
    # Test 1: Basic connection
    print("Test 1: Basic Connection")
    print("-" * 60)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Connected successfully!")
            print(f"  PostgreSQL version: {version[:50]}...")
    except OperationalError as e:
        print(f"✗ Connection failed: {e}")
        print("\nPossible issues:")
        print("  1. Database URL is incorrect")
        print("  2. Database server is not accessible")
        print("  3. Password encoding issue (check %40 for @)")
        print("  4. Firewall blocking connection")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Create tables
    print("\nTest 2: Table Creation")
    print("-" * 60)
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created/verified successfully")
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Insert test data
    print("\nTest 3: Insert Test Data")
    print("-" * 60)
    try:
        from sqlalchemy.orm import Session
        from app.database import SessionLocal
        
        db = SessionLocal()
        try:
            # Check if test user exists
            test_user = db.query(User).filter(User.email == "test@example.com").first()
            if test_user:
                print("✓ Test user already exists (skipping insert)")
            else:
                # Try to create a test user
                from app.auth import get_password_hash
                test_user = User(
                    email="test@example.com",
                    hashed_password=get_password_hash("testpass123")
                )
                db.add(test_user)
                db.commit()
                print("✓ Test user created successfully")
        except Exception as e:
            db.rollback()
            print(f"⚠ Insert test failed: {e}")
            print("  (This might be OK if tables don't exist yet)")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠ Insert test error: {e}")
    
    # Test 4: Query test
    print("\nTest 4: Query Test")
    print("-" * 60)
    try:
        from sqlalchemy.orm import Session
        from app.database import SessionLocal
        
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            print(f"✓ Query successful - Users in database: {user_count}")
        except Exception as e:
            print(f"⚠ Query error: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠ Query test error: {e}")
    
    print("\n" + "=" * 60)
    print("Database Connection Test Complete")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)


