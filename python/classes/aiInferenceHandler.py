import pickle
import torch
from classes.handler import Handler
from classes.request import Request
from classes.response import Response
from typing import Dict, Any

class AIInferenceHandler(Handler):
    def __init__(self, model_path: str, label_decoder_path: str):
        super().__init__()
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print(f"Loading model on {self.device}...")
        
        # Load the model
        self.model = torch.jit.load(model_path, map_location=self.device)
        self.model.eval()
        if torch.cuda.is_available():
            self.model.to(self.device)
        
        # Load label decoder
        with open(label_decoder_path, 'rb') as f:
            self.label_decoder = pickle.load(f)
        
        print("Model and label decoder loaded successfully")
        
        # Cache dictionary - in production use Redis
        self.cache = {}
    
    def _get_cache_key(self, request: Request) -> str:
        # Create a simple hash of the image data for cache key
        image_hash = hash(request.image_data.tobytes())
        return f"inference:{image_hash}"
    
    def handle(self, request: Request) -> Response:
        # Check cache first
        cache_key = self._get_cache_key(request)
        cached_result = self.cache.get(cache_key)
        
        if cached_result:
            print(f"Cache hit for inference")
            response = Response(True, cached_result, "Inference result retrieved from cache")
            response.from_cache = True
            return response
        
        try:
            # Move tensor to appropriate device
            input_tensor = request.processed_image.to(self.device).unsqueeze(0)
            
            # Run inference
            with torch.no_grad():
                output = self.model(input_tensor)
                _, predicted = torch.max(output, 1)
                predicted = predicted.cpu().numpy()[0]
            
            # Decode prediction
            character = self.label_decoder(predicted)
            
            # Store in cache
            result = {
                'character': character,
                'confidence': float(output.softmax(1)[0][predicted].item())
            }
            self.cache[cache_key] = result
            
            print(f"Inference successful: {character}")
            return Response(True, result, "Inference successful")
        
        except Exception as e:
            return Response(False, None, f"Inference failed: {str(e)}")
