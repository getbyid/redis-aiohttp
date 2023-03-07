from asyncio import sleep

from aiohttp import web

from app.redis import rate_exceeded


async def delayed_response(request: web.Request):
    user = request.query.get("user")
    if not user:
        raise web.HTTPBadRequest(reason="User required")

    if await rate_exceeded(request.app["redis"], f"ratelimit:{user}"):
        raise web.HTTPTooManyRequests()

    delay = int(request.query.get("delay", "1"))
    await sleep(delay / 1000)

    return web.json_response({"delay": delay})
