from typing import Dict, Any

class Request:
    def __init__(self, token: str, payload: Dict[str, Any]):
        self.token = token
        self.payload = payload
        self.image_data = None      # Will be set by InputValidationHandler
        self.processed_image = None  # Will be set by DataPrepHandler
        self.metadata = {}  # For additional data