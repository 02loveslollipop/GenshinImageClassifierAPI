from PIL import Image
from torchvision import transforms
from classes.handler import Handler
from classes.request import Request
from classes.response import Response

class DataPrepHandler(Handler):
    def __init__(self):
        super().__init__()
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.0189, 0.0177, 0.0192], std=[0.0098, 0.0097, 0.0094])
        ])
    
    def handle(self, request: Request) -> Response:
        try:
            # Make sure image is RGB
            image = request.image_data.convert('RGB')
            
            # Apply transformations
            processed_image = self.transform(image)
            request.processed_image = processed_image
            
            print("Image pre-processing successful")
            return self.do_next(request)
        except Exception as e:
            return Response(False, None, f"Data preparation failed: {str(e)}")