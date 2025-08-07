import os
import sys
import logging
from app import app

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logger.info("Starting server...")
        # Ensure directories exist
        os.makedirs('static', exist_ok=True)
        os.makedirs('static/temp', exist_ok=True)
        
        # Configure Flask
        app.config['TEMPLATES_AUTO_RELOAD'] = False
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        
        # Start server
        app.run(
            host='127.0.0.1',
            port=5001,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        sys.exit(1)
