from functools import wraps
from flask import session, request, redirect, url_for, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_required(f):
    """
    Decorator to require authentication for routes.
    Redirects to login page if user is not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current user information from session."""
    if 'user_id' in session:
        return {
            'user_id': session['user_id'],
            'email': session.get('email'),
            'display_name': session.get('display_name')
        }
    return None

def create_user_session(email, user_id, display_name=None):
    """Create a user session with user information."""
    session['user_id'] = user_id
    session['email'] = email
    session['display_name'] = display_name or email.split('@')[0]
    session.permanent = True
    logger.info(f"User session created for: {email}")

def clear_user_session():
    """Clear user session data."""
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('display_name', None)
    logger.info("User session cleared")

def validate_email(email):
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Basic password validation."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"
