from classes.request import Request
from classes.response import Response
from classes.handler import Handler
from typing import Optional, Dict, Any
import redis 

class AuthHandler(Handler):
    def __init__(self):
        super().__init__()
        # init Redis client
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0) 
    
    def _validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        # Check if token exists in Redis
        return self.redis_client.get(token) 
    
    def handle(self, request: Request) -> Response:
        # Check if token exists
        if not request.token:
            return Response(False, None, "Authentication token is required")
        
        # Validate token
        authResponse = self._validate_token(request.token)

        if not authResponse:
            return Response(False, None, "Invalid or expired token")


        print(f"Authentication successful for user with token: {request.token}")
        return self.do_next(request)