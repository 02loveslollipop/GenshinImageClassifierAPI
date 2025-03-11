from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from classes.handler import Handler
from classes.authHandler import AuthHandler
from classes.rateLimitHandler import RateLimitHandler
from classes.inputValidationHandler import InputValidationHandler
from classes.dataPreparationHandler import DataPrepHandler
from classes.aiInferenceHandler import AIInferenceHandler
from classes.genshinDataSet import GenshinDataSet
from classes.config import Config
from classes.request import Request
from classes.response import Response


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
config = Config()

# Initialize handlers
auth_handler = AuthHandler()
rate_limit_handler = RateLimitHandler()
validation_handler = InputValidationHandler()
data_prep_handler = DataPrepHandler()
ai_handler = AIInferenceHandler(
    model_path='models/torchScript200epoch.pt',
    label_decoder_path='models/labelDecoder.pkl'
)

# Chain them together
auth_handler.set_next(rate_limit_handler)
rate_limit_handler.set_next(validation_handler)
validation_handler.set_next(data_prep_handler)
data_prep_handler.set_next(ai_handler)

@app.route('/api/classify', methods=['POST'])
def classify_image():
    try:
        print("Received request for classification.")
        token = request.headers.get('X-API-Key', '')
        payload = request.get_json()
        
        # Create request object
        api_request = Request(
            token=token,
            payload=payload
        )
        
        # Start the chain
        response = auth_handler.handle(api_request)
        print(f"Response after auth: {response.to_dict()}")
        return jsonify(response.to_dict())
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'data': None,
            'message': f"Server error: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)