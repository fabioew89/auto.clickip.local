import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present).
# Used for sensitive or environment-specific configurations (e.g., API keys, database URIs).
load_dotenv()

# Flask environment mode (development, production, testing).
# 'development' enables debug mode, auto-reload, and detailed error pages.
FLASK_ENV = 'development'

# Default port for the Flask development server.
# Can be overridden by environment variables or deployment settings (e.g., Heroku uses PORT env var).
PORT = 5000

# SQLite database filename.
# Stores application data in a local file (default: 'nexus.db').
DATABASE_FILE = 'nexus.db'

# SQLAlchemy database connection URI.
# Uses SQLite for local development (file-based database).
# Format: 'sqlite:///<database_file_path>'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE

# Secret key for Flask session encryption and security features.
# Loaded from environment variables for production safety.
# Warning: Never hardcode secrets in version control!
SECRET_KEY = os.getenv('SQLALCHEMY_SECRET_KEY')

# Enable/disable the LiveReload server for frontend development.
# True: Auto-refreshes browser on file changes (HTML/CSS/JS).
# False: Disabled (default for production).
WEB_RELOADER = False