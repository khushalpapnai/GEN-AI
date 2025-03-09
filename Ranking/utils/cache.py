import redis
import json
from typing import Optional
from config import settings


# Initialize Redis client
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # so redis returns str instead of bytes
)

KEY_PREFIX = "rank:locality:"


def cache_key(locality: str) -> str:
    return f"{KEY_PREFIX}{locality.strip().lower()}"


def get_cached_rank(locality: str) -> Optional[dict]:
    raw = redis_client.get(cache_key(locality))
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Cache corrupted or invalid, optionally delete the key
        redis_client.delete(cache_key(locality))
        return None


def set_cached_rank(locality: str, payload: dict, ttl: Optional[int] = None) -> None:
    if ttl is None:
        ttl = settings.REDIS_TTL_SECONDS
    redis_client.setex(cache_key(locality), ttl, json.dumps(payload, ensure_ascii=False))


def invalidate_locality(locality: str) -> None:
    redis_client.delete(cache_key(locality))
