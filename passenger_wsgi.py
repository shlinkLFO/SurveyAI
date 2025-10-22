"""
WSGI entry point for cPanel Passenger deployment
FastAPI is ASGI, so we need to wrap it for WSGI
"""
import sys
import os

# Add the app directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app
from main import app

# Use a2wsgi to wrap ASGI app for Passenger WSGI
from a2wsgi import ASGIMiddleware

# Passenger expects a WSGI 'application' object
application = ASGIMiddleware(app)

