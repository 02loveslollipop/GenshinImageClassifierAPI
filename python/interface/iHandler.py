from abc import ABC, abstractmethod
from classes.request import Request
from classes.response import Response

class IHandler(ABC):
    """Interface for the Chain of Responsibility pattern handlers"""
    
    @abstractmethod
    def set_next(self, handler: 'IHandler') -> 'IHandler':
        """Set the next handler in the chain"""
        pass
    
    @abstractmethod
    def handle(self, request: Request) -> Response:
        """Handle the request or pass it to the next handler"""
        pass