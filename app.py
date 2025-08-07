import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import base64
from modules.story_generator import StoryGenerator
from modules.image_generator import LocalImageGenerator
from modules.comic_composer import ComicComposer
import time

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
try:
    logger.info("Initializing StoryGenerator...")
    story_generator = StoryGenerator()
    
    logger.info("Initializing ImageGenerator...")
    image_generator = LocalImageGenerator()
    
    logger.info("Initializing ComicComposer...")
    comic_composer = ComicComposer()
except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    raise

@app.route('/')
def index():
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    try:
        # Special handling for temp directory
        if path.startswith('temp/'):
            directory = os.path.join('static', 'temp')
            filename = os.path.basename(path)
            logger.info(f"Serving temp file: {filename} from {directory}")
            return send_from_directory(directory, filename)
            
        logger.info(f"Serving static file: {path}")
        return send_from_directory('static', path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_comic():
    print("DEBUG: /generate endpoint was called")
    try:
        data = request.get_json()
        print('DEBUG: Received data:', data)
        if not data:
            print('DEBUG: No data provided')
            return jsonify({'error': 'No data provided'}), 400
            
        prompt = data.get('prompt', '').strip()
        print('DEBUG: Prompt:', prompt)
        if not prompt:
            print('DEBUG: Prompt is required')
            return jsonify({'error': 'Prompt is required'}), 400
            
        style = data.get('style', 'manga')
        quality = data.get('quality', 'standard')
        print('DEBUG: Style:', style, 'Quality:', quality)
        
        logger.info(f"Received generate request")
        logger.info(f"Processing request - Prompt: {prompt}, Style: {style}, Quality: {quality}")
        
        # Get requested number of panels (pages)
        # Generate story
        logger.info("Generating story...")
        try:
            story, visual_context = story_generator.generate(prompt)
            print('DEBUG: Story:', story)
            print('DEBUG: Visual context:', visual_context)
        except Exception as e:
            print('DEBUG: Exception during story generation:', e)
            import traceback; traceback.print_exc()
            return jsonify({'error': f'Exception: {str(e)}'}), 500
        if not story or not visual_context:
            print('DEBUG: Story or visual_context is empty')
            return jsonify({'error': 'Failed to generate story'}), 500
        logger.info(f"Story generated successfully: {story}")
        
        # Generate images for each panel
        logger.info("Generating panels...")
        panels = []
        errors = []
        
        for i, (text, context) in enumerate(zip(story, visual_context)):
            try:
                logger.info(f"Generating panel {i+1}/{len(story)}")
                image, metadata = image_generator.generate_image(text, context, style)
                
                # Check if we got an error image
                if 'error' in metadata:
                    errors.append(f"Panel {i+1}: {metadata['error']}")
                    continue
                
                # Convert PIL Image to base64 string
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                panels.append({
                    'image': img_str,
                    'text': text,
                    'metadata': metadata
                })
                logger.info(f"Panel {i+1} generated successfully")
                
            except Exception as e:
                error_msg = f"Panel {i+1}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        if not panels:
            return jsonify({
                'success': False,
                'error': 'Failed to generate any panels. ' + '; '.join(errors)
            }), 500
            
        # Compose the final comic
        logger.info("Composing final comic...")
        comic_image = comic_composer.compose_comic(panels, story[:len(panels)], style, quality)
        if not comic_image:
            return jsonify({'error': 'Failed to compose final comic'}), 500
        
        # Ensure temp directory exists
        os.makedirs('static/temp', exist_ok=True)
        
        # Save the image to a temporary file
        temp_filename = f"comic_{int(time.time())}.png"
        temp_path = os.path.join('static', 'temp', temp_filename)
        try:
            # Ensure the image is in RGB mode before saving
            if comic_image.mode != 'RGB':
                comic_image = comic_image.convert('RGB')
            
            # Save with explicit permissions
            comic_image.save(temp_path, 'PNG', optimize=True)
            
            # Verify the file was saved
            if not os.path.exists(temp_path):
                raise Exception("Failed to save comic file")
                
            # Log success
            logger.info(f"Comic saved successfully to {temp_path}")
            
            # Return the URL with a cache-busting parameter
            return jsonify({
                'success': True,
                'panels': panels,
                'story': story,
                'image_url': f'/static/temp/{temp_filename}?t={int(time.time())}',
                'warnings': errors if errors else None
            })
        
        except Exception as e:
            logger.error(f"Error saving comic: {str(e)}")
            return jsonify({'error': 'Failed to save comic'}), 500
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in generate_comic: {error_msg}", exc_info=True)
        return jsonify({
            'error': error_msg,
            'message': 'An error occurred while generating your comic. Please try again.'
        }), 500

@app.route('/download')
def download_comic():
    try:
        return send_from_directory('static/temp', 'comic.png', as_attachment=True, download_name='comic.png')
    except Exception as e:
        logger.error(f"Error serving comic for download: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting application...")
        # Ensure the static and temp directories exist
        os.makedirs('static', exist_ok=True)
        os.makedirs('static/temp', exist_ok=True)
        
        # Start the Flask app with production settings
        logger.info("Starting Flask server on port 5002...")
        app.config['TEMPLATES_AUTO_RELOAD'] = False
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(
            host='127.0.0.1',
            port=5002,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}", exc_info=True)
