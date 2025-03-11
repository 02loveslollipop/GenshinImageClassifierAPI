from classes.request import Request
from classes.response import Response
from classes.handler import Handler
from typing import Optional, Dict, Any
import redis
from classes.config import Config

class AuthHandler(Handler):
    def __init__(self):
        super().__init__()
        config = Config()
        self.redis_client = redis.Redis(
            host=config['redis']['host'], 
            port=config['redis']['port'],
            decode_responses=True,
            password=config['redis']['password']
        )
    
    def _validate_token(self, token: str) -> bool:
        # Check if API hash exists and is enabled
        return self.redis_client.hget(token, "enabled") == "true"
    
    def handle(self, request: Request) -> Response:
        if not request.token:
            return Response(False, None, "Authentication token is required")
        
        if not self._validate_token(request.token):
            return Response(False, None, "Invalid or disabled API key")

        print(f"Authentication successful for API key: {request.token}")
        return self.do_next(request)