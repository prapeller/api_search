import logging
from abc import ABC, abstractmethod

from redis.asyncio import Redis
from redis.exceptions import RedisError

from core import config

logger = logging.getLogger(__name__)


class Cache(ABC):

    @abstractmethod
    def set_cache(self, cache_key, data):
        pass

    @abstractmethod
    def get_cache(self, cache_key):
        pass


class RedisCache(Cache):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_cache(self, cache_key, data):
        try:
            logger.info(f'set to cache by {cache_key=:} {data=:}')
            await self.redis.set(cache_key, data, config.REDIS_CACHE_EXPIRES_IN_SECONDS)
        except RedisError as e:
            logger.warning(f'failed to set data to cache for {cache_key=:}: {e}')

    async def get_cache(self, cache_key) -> str | None:
        try:
            logger.info(f'get data from cache by {cache_key=:}')
            return await self.redis.get(cache_key)
        except RedisError as e:
            logger.warning(f'failed to get data from cache for {cache_key=:}: {e}')
            return None
