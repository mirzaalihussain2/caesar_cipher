from flask import Flask
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
    
    return app