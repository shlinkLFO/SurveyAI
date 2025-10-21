"""
WSGI entry point for cPanel Passenger deployment
This file is required for cPanel Python app hosting
"""

import sys
import os

# Get the current directory
INTERP = os.path.expanduser("~/virtualenv/SurveyAIUIUC/3.9/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add the app directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI app
from main import app

# Passenger expects an 'application' object
application = app

