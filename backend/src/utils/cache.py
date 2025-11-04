import json
from typing import Optional, Any
from functools import wraps
import hashlib
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger()

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class CacheManager:
    """Cache manager with Redis backend (falls back to in-memory dict)."""

    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}

        if REDIS_AVAILABLE and settings.redis_url:
            try:
                self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
                self.redis_client.ping()
                logger.info("Redis cache connected successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed, using memory cache: {e}")
                self.redis_client = None
        else:
            logger.info("Using in-memory cache (Redis not available)")

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                return json.loads(value) if value else None
            else:
                return self.memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        try:
            ttl = ttl or settings.cache_ttl
            if self.redis_client:
                self.redis_client.setex(key, ttl, json.dumps(value))
            else:
                self.memory_cache[key] = value
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            else:
                self.memory_cache.pop(key, None)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def clear(self) -> bool:
        """Clear all cache."""
        try:
            if self.redis_client:
                self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False


# Global cache instance
cache_manager = CacheManager()


def cached(prefix: str = "default", ttl: Optional[int] = None):
    """Decorator to cache function results."""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = cache_manager._generate_key(prefix, *args, **kwargs)
            cached_result = cache_manager.get(cache_key)

            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result

            result = await func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = cache_manager._generate_key(prefix, *args, **kwargs)
            cached_result = cache_manager.get(cache_key)

            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result

            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            return result

        return async_wrapper if hasattr(func, "__await__") else sync_wrapper

    return decorator
