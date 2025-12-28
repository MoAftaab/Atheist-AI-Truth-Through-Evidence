"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password length and requirements."""
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        # Bcrypt has a 72-byte limit
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (maximum 72 bytes/characters)')
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# Query Schemas
class VerseCitation(BaseModel):
    surah_number: int
    surah_name_english: str
    ayah_number: int
    text_simple: str
    translation_en_yusufali: str
    score: float
    context: Optional[List[Dict[str, Any]]] = None


class QueryRequest(BaseModel):
    query: str
    k: int = 5
    score_threshold: Optional[float] = None
    window: int = 1


class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[VerseCitation]
    has_answer: bool
    processing_time: Optional[float] = None


class QueryHistoryResponse(BaseModel):
    id: int
    query: str
    answer: str
    citations: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

