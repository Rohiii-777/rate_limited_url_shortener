# app/rate_limiter.py

import redis
from fastapi import Request
from app.exceptions import http_error
from starlette.status import HTTP_429_TOO_MANY_REQUESTS, HTTP_403_FORBIDDEN
from app.exceptions import CustomHttpException
from app.services.metrics import ip_block_counter

r = redis.Redis(host="redis_cache", port=6379, db=0, decode_responses=True)

ANON_LIMIT = 10  # per minute
AUTH_LIMIT = 30  # per minute
BLOCK_DURATION = 600  # 10 minutes

def get_ip(request: Request):
    return request.client.host

def get_limit_key(ip: str, user_id: str = None):
    return f"rate:{user_id or ip}"

def get_block_key(ip: str):
    return f"blocked:{ip}"

def is_blocked(ip: str):
    return r.exists(get_block_key(ip))

def increment_and_check(ip: str, user_id: str = None):
    key = get_limit_key(ip, user_id)
    limit = AUTH_LIMIT if user_id else ANON_LIMIT

    current = r.incr(key)
    if current == 1:
        r.expire(key, 60)  # 60s window

    if current > limit:
        # Block the IP if over limit
        r.setex(get_block_key(ip), BLOCK_DURATION, 1)
        return False
    return True

async def rate_limiter(request: Request, user_id: str = None):
    ip = get_ip(request)

    if is_blocked(ip):
        ip_block_counter.inc()
        raise CustomHttpException("Too many requests. IP blocked temporarily.", HTTP_403_FORBIDDEN)

    ok = increment_and_check(ip, user_id)
    if not ok:
        ip_block_counter.inc()
        raise CustomHttpException("Rate limit exceeded", HTTP_429_TOO_MANY_REQUESTS)
