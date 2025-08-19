import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Firebase configuration
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase_key.json')
    
    # Groq configuration
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GROQ_MODEL = os.environ.get('GROQ_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
    
    # Application settings
    FLASHCARDS_PER_SET = int(os.environ.get('FLASHCARDS_PER_SET', '8'))
    MAX_TOPIC_LENGTH = int(os.environ.get('MAX_TOPIC_LENGTH', '200'))
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present."""
        required_vars = ['GROQ_API_KEY', 'FIREBASE_PROJECT_ID']
        missing_vars = []
        
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Check if Firebase credentials file exists
        firebase_key_path = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase_key.json')
        if not os.path.exists(firebase_key_path):
            raise FileNotFoundError(f"Firebase credentials file not found: {firebase_key_path}")
        
        return True
