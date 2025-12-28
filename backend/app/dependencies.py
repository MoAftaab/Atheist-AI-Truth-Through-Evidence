"""
FastAPI dependencies.
"""

from app.database import get_db
from app.auth import get_current_user_optional
from app.models import User
from typing import Optional
from sqlalchemy.orm import Session

def get_optional_user(
    db: Session = None,
    current_user: Optional[User] = None
) -> Optional[User]:
    """Dependency to get optional user (for public endpoints)."""
    return current_user


