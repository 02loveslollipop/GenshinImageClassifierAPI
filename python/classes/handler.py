from classes.request import Request
from classes.response import Response
from interface.iHandler import IHandler
from abc import ABC, abstractmethod

class Handler(IHandler):
    
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass

    def do_next(self, request: Request) -> Response:
        if self.next_handler:
            return self.next_handler.handle(request)
        return Response(True, None, "End of chain reached")