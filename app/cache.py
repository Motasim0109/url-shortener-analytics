from datetime import UTC, datetime

from pydantic import BaseModel
from redis import Redis

from app.config import settings

redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


class CachedShortLink(BaseModel):
    id: int
    destination_url: str
    expires_at: datetime | None


def short_link_cache_key(short_code: str) -> str:
    return f"short-link:{short_code}"


def get_cached_short_link(short_code: str) -> CachedShortLink | None:
    key = short_link_cache_key(short_code)
    cached_value = redis_client.get(key)

    if cached_value is None:
        return None

    return CachedShortLink.model_validate_json(cached_value)


def cache_short_link(short_code: str, short_link: CachedShortLink, ttl_seconds: int) -> None:
    key = short_link_cache_key(short_code)
    cached_value = short_link.model_dump_json()
    if short_link.expires_at is not None:
        seconds_until_expiry = int((short_link.expires_at - datetime.now(UTC)).total_seconds())
        if seconds_until_expiry <= 0:
            return
        ttl_seconds = min(ttl_seconds, seconds_until_expiry)
    redis_client.set(key, cached_value, ex=ttl_seconds)


def invalidate_short_link(short_code: str) -> None:
    key = short_link_cache_key(short_code)
    redis_client.delete(key)
