"""
Redis caching service for query results.
"""

import json
import hashlib
from typing import Optional, Dict, Any
from app.config import settings

# Try to import redis, but make it optional
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class CacheService:
    """Service for caching query results in Redis."""
    
    def __init__(self):
        """Initialize Redis connection if available."""
        self.redis_client: Optional[redis.Redis] = None
        if REDIS_AVAILABLE and settings.REDIS_URL:
            try:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
            except Exception as e:
                print(f"Redis connection failed: {e}. Caching disabled.")
                self.redis_client = None
    
    def _generate_cache_key(self, query: str, k: int, score_threshold: Optional[float], window: int) -> str:
        """Generate a cache key from query parameters."""
        key_string = f"{query}:{k}:{score_threshold}:{window}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, query: str, k: int, score_threshold: Optional[float], window: int) -> Optional[Dict[str, Any]]:
        """Get cached result if available."""
        if not self.redis_client:
            return None
        
        try:
            cache_key = f"quran_query:{self._generate_cache_key(query, k, score_threshold, window)}"
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            print(f"Cache get error: {e}")
        
        return None
    
    def set(self, query: str, k: int, score_threshold: Optional[float], window: int, result: Dict[str, Any]):
        """Cache a query result."""
        if not self.redis_client:
            return
        
        try:
            cache_key = f"quran_query:{self._generate_cache_key(query, k, score_threshold, window)}"
            self.redis_client.setex(
                cache_key,
                settings.CACHE_TTL,
                json.dumps(result, default=str)
            )
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def clear(self, pattern: str = "quran_query:*"):
        """Clear cache entries matching pattern."""
        if not self.redis_client:
            return
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Cache clear error: {e}")


# Global cache service instance
cache_service = CacheService()


