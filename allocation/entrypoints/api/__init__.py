"""
Allocation API module
"""

from flask import Flask
from flask_cors import CORS

from .namespaces import api
from .service_adapter import service


def load_configuration(app):
    """Load application configuration from the api configuration
    python module"""
    app.config.from_pyfile("../../../config/service_config.py")


def init_app(app):
    """Initialize extensions of flask"""
    api.init_app(app)
    service.init(app.config)
    CORS(app, resources={r"/*": {"origins": "*"}})


def create_app(load=True):
    """Factory for flask application
    Entry point function for WSGI servers
    """
    app = Flask(__name__)
    load_configuration(app)
    if load:
        init_app(app)
    return app
