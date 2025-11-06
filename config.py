import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    # Construct MySQL Database URI
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    # We aren't using Flask-SQLAlchemy's event system, so disable this
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4  # Reduce bcrypt rounds for faster tests
    
    # Test database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'lab_management_test')
    
    # Session configuration for testing
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_session'
    PERMANENT_SESSION_LIFETIME = 31536000  # 1 year in seconds for testing