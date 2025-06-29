#!/bin/bash

# Change to the project directory
cd "$(dirname "$0")"

# Set environment variables
export FLASK_APP=src/main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the Flask application with auto-reload enabled
python3 src/main.py
