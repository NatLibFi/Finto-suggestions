"""
Creates a WSGI app instance for the server (Gunicorn)
"""

import os

from app import create_app


config_object = os.environ.get('APP_CONFIG_OBJECT', 'config.DevelopmentConfig')

connexion_app = create_app(config_object)  # connexion instance
flask_app = connexion_app.app  # flask app instance
