import redis
from classes.request import Request
from classes.response import Response
from classes.handler import Handler
from typing import Dict

class RateLimitHandler(Handler):
    def __init__(self, limit_per_minute: Dict[str, int] = None):
        super().__init__()
        self.limit_per_minute = 10
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    
    def handle(self, request: Request) -> Response:
        # Get rate limit based on role
        
        # Create key for Redis
        rate_key = f"rate:{request.user_id}"
        
        # Check current count
        current = self.redis_client.get(rate_key)
        count = int(current) if current else 0
        
        if count >= self.limit_per_minute:
            return Response(False, None, f"Rate limit exceeded. Max {self.limit_per_minute} requests per minute.")
        
        # Increment count with 60-second expiry
        pipe = self.redis_client.pipeline()
        pipe.incr(rate_key)
        pipe.expire(rate_key, 60)
        pipe.execute()
        
        print(f"Rate limit check passed for user with token: {request.token}: {count+1}/{self.limit_per_minute}")
        return self.do_next(request)