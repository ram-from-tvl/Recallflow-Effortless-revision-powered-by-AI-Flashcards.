import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import logging
import hashlib
import secrets
from datetime import datetime, timezone
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebaseConfig:
    """Firebase configuration and initialization."""
    
    def __init__(self):
        self.app = None
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK."""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Initialize Firebase Admin SDK
                cred_path = Config.FIREBASE_CREDENTIALS_PATH
                if not os.path.exists(cred_path):
                    logger.warning(f"Firebase credentials file not found: {cred_path}")
                    logger.warning("Running in development mode without Firebase")
                    self.app = None
                    self.db = None
                    return
                
                # Check if this is a dummy/test key
                with open(cred_path, 'r') as f:
                    key_content = f.read()
                    if 'DUMMY_PRIVATE_KEY_FOR_TESTING' in key_content:
                        logger.warning("Dummy Firebase key detected - running in development mode")
                        self.app = None
                        self.db = None
                        return
                
                cred = credentials.Certificate(cred_path)
                self.app = firebase_admin.initialize_app(cred, {
                    'projectId': Config.FIREBASE_PROJECT_ID,
                })
                logger.info("Firebase Admin SDK initialized successfully")
            else:
                self.app = firebase_admin.get_app()
                logger.info("Using existing Firebase Admin SDK instance")
            
            # Initialize Firestore
            self.db = firestore.client()
            logger.info("Firestore client initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to initialize Firebase: {str(e)}")
            logger.warning("Running in development mode without Firebase")
            self.app = None
            self.db = None
    
    def get_firestore_client(self):
        """Get Firestore client instance."""
        if self.db is None:
            logger.warning("Firestore not available - running in development mode")
            return None
        return self.db
    
    def verify_user_token(self, id_token):
        """Verify Firebase ID token and return user info."""
        if self.app is None:
            logger.warning("Firebase Auth not available - running in development mode")
            return None
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None
    
    def hash_password(self, password):
        """Hash a password with a random salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return salt + password_hash.hex()
    
    def verify_password(self, password, hashed_password):
        """Verify a password against its hash."""
        salt = hashed_password[:32]  # First 32 chars are the salt
        stored_hash = hashed_password[32:]  # Rest is the hash
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return password_hash.hex() == stored_hash
    
    def create_user(self, email, password, display_name=None):
        """Create a new user in Firestore with hashed password."""
        db = self.get_firestore_client()
        if not db:
            logger.error("Firestore not available")
            return None
        
        try:
            # Check if user already exists
            users_ref = db.collection('users')
            existing_users = users_ref.where('email', '==', email).limit(1).get()
            
            if existing_users:
                logger.warning(f"User already exists: {email}")
                return None
            
            # Create new user
            user_id = f"user_{secrets.token_hex(16)}"
            hashed_password = self.hash_password(password)
            
            user_data = {
                'user_id': user_id,
                'email': email,
                'display_name': display_name or email.split('@')[0],
                'password_hash': hashed_password,
                'created_at': datetime.now(timezone.utc),
                'last_login': None
            }
            
            # Save to Firestore
            db.collection('users').document(user_id).set(user_data)
            logger.info(f"User created successfully: {email}")
            
            # Return user data without password hash
            return {
                'user_id': user_id,
                'email': email,
                'display_name': user_data['display_name']
            }
            
        except Exception as e:
            logger.error(f"User creation failed: {str(e)}")
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password."""
        db = self.get_firestore_client()
        if not db:
            logger.error("Firestore not available")
            return None
        
        try:
            # Find user by email
            users_ref = db.collection('users')
            users = users_ref.where('email', '==', email).limit(1).get()
            
            if not users:
                logger.warning(f"User not found: {email}")
                return None
            
            user_doc = users[0]
            user_data = user_doc.to_dict()
            
            # Verify password
            if self.verify_password(password, user_data['password_hash']):
                # Update last login
                db.collection('users').document(user_data['user_id']).update({
                    'last_login': datetime.now(timezone.utc)
                })
                
                logger.info(f"User authenticated successfully: {email}")
                return {
                    'user_id': user_data['user_id'],
                    'email': user_data['email'],
                    'display_name': user_data['display_name']
                }
            else:
                logger.warning(f"Invalid password for user: {email}")
                return None
                
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email address."""
        db = self.get_firestore_client()
        if not db:
            logger.error("Firestore not available")
            return None
        
        try:
            users_ref = db.collection('users')
            users = users_ref.where('email', '==', email).limit(1).get()
            
            if users:
                user_data = users[0].to_dict()
                return {
                    'user_id': user_data['user_id'],
                    'email': user_data['email'],
                    'display_name': user_data['display_name']
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Get user by email failed: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by user ID."""
        db = self.get_firestore_client()
        if not db:
            logger.error("Firestore not available")
            return None
        
        try:
            user_doc = db.collection('users').document(user_id).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                return {
                    'user_id': user_data['user_id'],
                    'email': user_data['email'],
                    'display_name': user_data['display_name']
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Get user by ID failed: {str(e)}")
            return None

# Global Firebase instance
firebase_config = FirebaseConfig()
