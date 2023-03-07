import logging

from aiohttp import web

from app.handlers import delayed_response
from app.redis import add_redis_context

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    add_redis_context(app)
    app.add_routes([web.get("/", delayed_response)])

    web.run_app(app)
