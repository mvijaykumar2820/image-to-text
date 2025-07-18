from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
import os
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_api_key():
    """Get OCR.space API key from environment variable"""
    api_key = os.getenv('OCR_SPACE_API_KEY')
    if not api_key:
        raise ValueError("OCR_SPACE_API_KEY environment variable not set")
    return api_key

def process_image_with_ocr(image_data, is_file=True):
    """
    Process image with OCR.space API
    
    Args:
        image_data: Either file path (if is_file=True) or base64 string (if is_file=False)
        is_file: Boolean indicating if image_data is a file path or base64 string
    
    Returns:
        dict: OCR result containing extracted text and metadata
    """
    try:
        api_key = get_api_key()
        
        # OCR.space API endpoint
        url = 'https://api.ocr.space/parse/image'
        
        # Prepare the payload
        payload = {
            'apikey': api_key,
            'OCREngine': '2',  # Engine 2 is better for handwriting
            'isOverlayRequired': 'false',
            'filetype': 'AUTO',
            'detectOrientation': 'true',
            'isCreateSearchablePdf': 'false',
            'isSearchablePdfHideTextLayer': 'false',
            'scale': 'true',
            'isTable': 'false'
        }
        
        if is_file:
            # Send file directly
            with open(image_data, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, data=payload, timeout=30)
        else:
            # Send base64 encoded image
            payload['base64Image'] = f"data:image/jpeg;base64,{image_data}"
            response = requests.post(url, data=payload, timeout=30)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('IsErroredOnProcessing'):
            error_msg = result.get('ErrorMessage', 'Unknown OCR processing error')
            logger.error(f"OCR processing error: {error_msg}")
            return {'success': False, 'error': error_msg}
        
        # Extract text from all parsed results
        extracted_text = ""
        if result.get('ParsedResults'):
            for parsed_result in result['ParsedResults']:
                if parsed_result.get('ParsedText'):
                    extracted_text += parsed_result['ParsedText']
        
        if not extracted_text.strip():
            return {'success': False, 'error': 'No text could be extracted from the image'}
        
        return {
            'success': True,
            'text': extracted_text.strip(),
            'confidence': result.get('ParsedResults', [{}])[0].get('TextOverlay', {}).get('HasOverlay', False)
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return {'success': False, 'error': f'API request failed: {str(e)}'}
    except Exception as e:
        logger.error(f"Unexpected error during OCR processing: {str(e)}")
        return {'success': False, 'error': f'Processing error: {str(e)}'}

@app.route('/')
def index():
    """Serve the React app"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'frontend/build'), 'favicon.ico')

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory(os.path.join(app.root_path, 'frontend/build/static'), path)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and OCR processing"""
    try:
        logger.info("Upload request received")
        
        # Check if file is provided
        if 'file' not in request.files:
            logger.error("No file in request")
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        logger.info(f"File received: {file.filename}")
        
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            logger.error(f"File type not allowed: {file.filename}")
            return jsonify({'success': False, 'error': 'File type not allowed. Use PNG, JPG, JPEG, GIF, or BMP.'}), 400
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        logger.info(f"File saved to: {filepath}")
        
        # Process with OCR
        logger.info("Starting OCR processing")
        result = process_image_with_ocr(filepath, is_file=True)
        logger.info(f"OCR result: {result}")
        
        # Clean up the uploaded file
        try:
            os.remove(filepath)
            logger.info("Temp file cleaned up")
        except:
            pass
        
        if result['success']:
            return jsonify({
                'success': True,
                'text': result['text'],
                'message': 'Text extracted successfully!'
            })
        else:
            logger.error(f"OCR failed: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Upload processing error: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/upload-base64', methods=['POST'])
def upload_base64():
    """Handle base64 image upload and OCR processing"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
        
        # Extract base64 data (remove data:image/...;base64, prefix if present)
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Process with OCR
        result = process_image_with_ocr(image_data, is_file=False)
        
        if result['success']:
            return jsonify({
                'success': True,
                'text': result['text'],
                'message': 'Text extracted successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Base64 upload processing error: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        api_key = get_api_key()
        return jsonify({
            'status': 'healthy',
            'api_key_configured': bool(api_key)
        })
    except:
        return jsonify({
            'status': 'unhealthy',
            'api_key_configured': False
        }), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if API key is configured
    try:
        get_api_key()
        logger.info("OCR.space API key configured successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set the OCR_SPACE_API_KEY environment variable")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

