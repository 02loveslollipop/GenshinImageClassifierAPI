from typing import Any

class Response:
    def __init__(self, success: bool, data: Any = None, message: str = ""):
        self.success = success
        self.data = data
        self.message = message
        self.from_cache = False

    def to_dict(self):
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message,
            'from_cache': self.from_cache
        }
