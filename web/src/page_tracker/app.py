"""
Simple Flask App with Redis Page Views
This Flask app demonstrates a simple web page that tracks
and displays the number of times the page has been viewed
using Redis as the backend data store.
It uses the `lru_cache` decorator to memoize the
Redis connection for efficient reuse.
Author: zakaria
"""

import os
from functools import lru_cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """
    Display Page Views

    This route displays the number of times the page has been viewed.
    It increments the page views count in Redis.

    Returns:
        str: Page view count or an error message
    """
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{thinking face}", 500
    return f"This page has been seen {page_views} times."


@lru_cache
def redis():
    """
    Get Redis Connection

    This function establishes a connection to Redis using the URL specified
    in the environment variable REDIS_URL.
    If no URL is provided, it defaults to connecting to a local Redis server.

    Returns:
        Redis: Redis connection object
    """
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
