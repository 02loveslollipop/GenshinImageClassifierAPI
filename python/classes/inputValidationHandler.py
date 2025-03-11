from PIL import Image
import io
import base64
from classes.handler import Handler
from classes.request import Request
from classes.response import Response

class InputValidationHandler(Handler):
    def handle(self, request: Request) -> Response:
        # Check if image data exists
        if 'image' not in request.payload:
            return Response(False, None, "Image data is required")
        
        try:
            # Decode base64 image
            image_data = base64.b64decode(request.payload['image'])
            image = Image.open(io.BytesIO(image_data))
            
            # Verify it's an image
            if image.format not in ['JPEG', 'PNG', 'GIF']:
                return Response(False, None, "Invalid image format. Supported formats: JPEG, PNG, GIF")
            
            # Store image in request
            request.image_data = image
            print(f"Image validation successful: {image.format} {image.size}")
            
            return self.do_next(request)
        except Exception as e:
            return Response(False, None, f"Image validation failed: {str(e)}")