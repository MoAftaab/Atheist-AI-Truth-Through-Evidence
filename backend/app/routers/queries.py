"""
Query endpoints for Quran Q&A.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import User, QueryHistory
from app.schemas import QueryRequest, QueryResponse, QueryHistoryResponse, VerseCitation
from app.auth import get_current_user_optional
from app.services.quran_service import quran_service
from app.services.cache_service import cache_service

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_quran(
    query_request: QueryRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Query the Quran using RAG pipeline.
    Public endpoint - works with or without authentication.
    """
    # Check cache first
    cached_result = cache_service.get(
        query_request.query,
        query_request.k,
        query_request.score_threshold,
        query_request.window
    )
    
    if cached_result:
        # Convert cached result to response format
        citations = [VerseCitation(**c) for c in cached_result.get("citations", [])]
        return QueryResponse(
            query=cached_result["query"],
            answer=cached_result["answer"],
            citations=citations,
            has_answer=cached_result["has_answer"],
            processing_time=cached_result.get("processing_time")
        )
    
    # Process query
    try:
        result = quran_service.answer_query(
            query=query_request.query,
            k=query_request.k,
            score_threshold=query_request.score_threshold,
            window=query_request.window
        )
        
        # Cache the result
        cache_service.set(
            query_request.query,
            query_request.k,
            query_request.score_threshold,
            query_request.window,
            result
        )
        
        # Convert citations to schema format
        citations = [VerseCitation(**c) for c in result.get("citations", [])]
        
        # Save to query history if user is authenticated
        if current_user:
            query_history = QueryHistory(
                user_id=current_user.id,
                query=query_request.query,
                answer=result["answer"],
                citations=json.dumps([c.dict() for c in citations], default=str)
            )
            db.add(query_history)
            db.commit()
        
        return QueryResponse(
            query=result["query"],
            answer=result["answer"],
            citations=citations,
            has_answer=result["has_answer"],
            processing_time=result.get("processing_time")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/history", response_model=List[QueryHistoryResponse])
async def get_query_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get query history for the authenticated user.
    Requires authentication.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    history = db.query(QueryHistory)\
        .filter(QueryHistory.user_id == current_user.id)\
        .order_by(QueryHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return history



