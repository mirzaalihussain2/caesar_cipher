from flask import Flask
from flask_cors import CORS
from config import Config
import logging

# Removes "ERROR:root:" from the start of each error log
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Running CORS in prod, as well as local
    CORS(app, resources={
        r"/*": {
            "origins": app.config['FRONTEND_URL'],
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Import routes
    from app.encrypt import bp as encrypt_bp
    from app.decrypt import bp as decrypt_bp
    
    app.register_blueprint(encrypt_bp)
    app.register_blueprint(decrypt_bp)

    @app.route('/', methods=['GET'])
    def api_endpoint():
        return {
            "message": "Hello, World!",
            "status": "success"
        }
    
    @app.after_request
    def after_request(response):
        app.logger.info(f"CORS Headers: {dict(response.headers)}")
        return response
    
    return app