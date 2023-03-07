# https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html
# https://docs.aiohttp.org/en/stable/web_advanced.html#cleanup-context

import os
import time

import redis.asyncio as redis
from aiohttp import web


async def redis_context(app: web.Application):
    app["redis"] = await redis.from_url(os.environ["REDIS_URL"])
    yield
    await app["redis"].close()


def add_redis_context(app: web.Application):
    app.cleanup_ctx.append(redis_context)


async def rate_exceeded(
    client: redis.Redis, key: str, per_second=10, interval=1
) -> bool:
    """
    Проверка превышения частоты запросов на интервале времени.

    :param redis.Redis client:
        Инстанс асинхронного клиента Redis.
    :param str key:
        Ключ для подсчёта запросов, (IP-адрес или ID пользователя).
    :param int per_second:
        Допустимое число запросов в секунду.
    :param int interval:
        Интервал времени храненния запросов, в секундах.
    """
    now = time.time_ns()
    await client.zremrangebyscore(key, 0, now - interval * 1e9)
    if await client.zcard(key) < per_second * interval:
        await client.zadd(key, {now: now})
        return False
    return True
