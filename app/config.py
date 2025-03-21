import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define the database file name
DATABASE_FILE = 'nexus.db'

# Set the SQLAlchemy database URI using SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE

# Load the secret key from environment variables for security purposes
SECRET_KEY = os.getenv('SQLALCHEMY_SECRET_KEY')

# Enables or disables the web reloader (LiveReloader) based on the configuration.
# Set WEB_RELOADER = True to enable automatic reloading during development.
# Defaults to False (disabled) if not set.
WEB_RELOADER = False
