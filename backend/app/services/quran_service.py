"""
Service layer for Quran RAG operations.
Wraps the existing QuranRetrieval and QuranLLMExplainer classes.
"""

import sys
import os
from typing import Dict, Any, Optional
import time

# Add parent directory to path to import existing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from quran_retrieval2 import QuranRetrieval
from llm_explainer import QuranLLMExplainer
from app.config import settings


class QuranService:
    """Service for handling Quran queries using RAG pipeline."""
    
    def __init__(self):
        """Initialize the service with lazy loading."""
        self._retrieval: Optional[QuranRetrieval] = None
        self._explainer: Optional[QuranLLMExplainer] = None
    
    @property
    def retrieval(self) -> QuranRetrieval:
        """Lazy load retrieval system."""
        if self._retrieval is None:
            # Use absolute paths - check project root first
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            # If files not in project root, try current directory
            json_path = os.path.join(base_path, settings.QURAN_JSON_PATH)
            index_path = os.path.join(base_path, settings.FAISS_INDEX_PATH)
            metadata_path = os.path.join(base_path, settings.QURAN_METADATA_PATH)
            
            # Fallback to current directory if not found
            if not os.path.exists(json_path):
                json_path = settings.QURAN_JSON_PATH
            if not os.path.exists(index_path):
                index_path = settings.FAISS_INDEX_PATH
            if not os.path.exists(metadata_path):
                metadata_path = settings.QURAN_METADATA_PATH
            
            self._retrieval = QuranRetrieval(
                json_path=json_path,
                index_path=index_path,
                metadata_path=metadata_path
            )
        return self._retrieval
    
    @property
    def explainer(self) -> QuranLLMExplainer:
        """Lazy load LLM explainer."""
        if self._explainer is None:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")
            self._explainer = QuranLLMExplainer(api_key=settings.OPENAI_API_KEY)
        return self._explainer
    
    def answer_query(
        self,
        query: str,
        k: int = 5,
        score_threshold: Optional[float] = None,
        window: int = 1
    ) -> Dict[str, Any]:
        """
        Answer a query using the RAG pipeline.
        
        Returns:
            Dictionary with answer, citations, and metadata
        """
        start_time = time.time()
        
        # Get citation bundle
        citation_bundle = self.retrieval.retrieve_citation_bundle(
            query=query,
            k=k,
            score_threshold=score_threshold,
            window=window
        )
        
        # Generate explanation
        answer = self.explainer.explain(citation_bundle)
        
        processing_time = time.time() - start_time
        
        return {
            "query": query,
            "answer": answer,
            "citations": citation_bundle.get("results", []),
            "has_answer": citation_bundle.get("has_answer", False),
            "processing_time": processing_time
        }


# Global service instance (singleton pattern)
quran_service = QuranService()

