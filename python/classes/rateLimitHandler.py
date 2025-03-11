import redis
import time
from classes.request import Request
from classes.response import Response
from classes.handler import Handler
from typing import Dict
from classes.config import Config

class RateLimitHandler(Handler):
    def __init__(self, limit_per_minute: Dict[str, int] = None):
        super().__init__()
        config = Config()
        self.limit_request = 10
        self.window_minutes = config['settings']['window_minutes']
        self.redis_client = redis.Redis(
            host=config['redis']['host'], 
            port=config['redis']['port'],
            decode_responses=True,
            password=config['redis']['password']
        )
    
    def handle(self, request: Request) -> Response:
        api_key = request.token
        
        # Check if API exists
        if not self.redis_client.exists(api_key):
            return Response(False, None, "API key not found or disabled")

        # Get all request entries
        current_requests = len(self.redis_client.hgetall(api_key))-1
        
        if current_requests >= self.limit_request:
            return Response(
                False, 
                None, 
                f"Rate limit exceeded. Max {self.limit_request} requests per {self.window_minutes} minutes."
            )
        
        # Add new request entry with TTL
        timestamp = str(int(time.time()))
        request_field = f"req_{timestamp}"
        
        # Use pipeline to ensure atomic operations
        with self.redis_client.pipeline() as pipe:
            pipe.hset(api_key, request_field, timestamp)
            pipe.hexpire(api_key, self.window_minutes * 60, request_field)
            pipe.execute()
        
        print(f"Rate limit check passed for API key: {api_key}: {current_requests + 1}/{self.limit_request}")
        return self.do_next(request)
