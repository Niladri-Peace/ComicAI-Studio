from flask import Flask, jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Server is running!"

@app.route('/status')
def status():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    try:
        logger.info("Starting minimal server...")
        app.run(port=5002, debug=False)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}", exc_info=True)
