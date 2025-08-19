from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta, timezone
import logging
import traceback

# Import custom modules
from config import Config
from utils.firebase_config import firebase_config
from utils.groq_client import groq_client
from utils.auth import login_required, get_current_user, create_user_session, clear_user_session, validate_email, validate_password

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
    # Set session permanent lifetime
    app.permanent_session_lifetime = timedelta(days=7)
    
    # Validate configuration on startup
    try:
        Config.validate_config()
        logger.info("Configuration validated successfully")
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"Configuration error: {str(e)}")
        logger.error("Please check your .env file and firebase_key.json")
        # Don't exit, just log the error for development
    
    # Routes
    @app.route('/')
    def index():
        """Home page - redirect to dashboard if logged in, otherwise show landing page."""
        user = get_current_user()
        if user:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration."""
        if request.method == 'POST':
            try:
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                display_name = request.form.get('display_name', '').strip()
                
                # Basic validation
                if not email or not password:
                    flash('Email and password are required', 'error')
                    return render_template('register.html')
                
                if not validate_email(email):
                    flash('Please enter a valid email address', 'error')
                    return render_template('register.html')
                
                is_valid, message = validate_password(password)
                if not is_valid:
                    flash(message, 'error')
                    return render_template('register.html')
                
                # Create user
                user_record = firebase_config.create_user(
                    email=email,
                    password=password,
                    display_name=display_name or email.split('@')[0]
                )
                
                if user_record:
                    # Create session
                    create_user_session(email, user_record['user_id'], user_record['display_name'])
                    flash('Registration successful! Welcome to FlashGenius!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Registration failed. Email might already be in use. Please try again with a different email.', 'error')
                    
            except Exception as e:
                app.logger.error(f"Registration error: {str(e)}")
                flash('An error occurred during registration. Please try again.', 'error')
        
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login."""
        if request.method == 'POST':
            try:
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                
                if not email or not password:
                    flash('Email and password are required', 'error')
                    return render_template('login.html')
                
                # Authenticate user
                user_record = firebase_config.authenticate_user(email, password)
                
                if user_record:
                    # Create session
                    create_user_session(email, user_record['user_id'], user_record['display_name'])
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password. Please check your credentials and try again.', 'error')
                    
            except Exception as e:
                app.logger.error(f"Login error: {str(e)}")
                flash('An error occurred during login. Please try again.', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout."""
        clear_user_session()
        flash('You have been logged out successfully', 'success')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard."""
        user = get_current_user()
        
        try:
            # Get user's flashcard sets
            db = firebase_config.get_firestore_client()
            flashcard_sets = []
            
            if db:
                sets_ref = db.collection('users').document(user['user_id']).collection('flashcard_sets')
                docs = sets_ref.order_by('created_at', direction='DESCENDING').get()
                
                for doc in docs:
                    data = doc.to_dict()
                    data['id'] = doc.id
                    flashcard_sets.append(data)
                    
        except Exception as e:
            app.logger.error(f"Error fetching dashboard data: {str(e)}")
            flashcard_sets = []
            flash('Unable to load your flashcard sets. Please try again.', 'error')
        
        return render_template('dashboard.html', user=user, flashcard_sets=flashcard_sets)
    
    @app.route('/create', methods=['GET', 'POST'])
    @login_required
    def create_flashcards():
        """Create new flashcards using AI."""
        if request.method == 'POST':
            try:
                topic = request.form.get('topic', '').strip()
                
                if not topic:
                    flash('Please enter a topic for your flashcards', 'error')
                    return render_template('create_flashcards.html')
                
                if len(topic) > Config.MAX_TOPIC_LENGTH:
                    flash(f'Topic must be less than {Config.MAX_TOPIC_LENGTH} characters', 'error')
                    return render_template('create_flashcards.html')
                
                # Generate flashcards using Groq
                flashcards = groq_client.generate_flashcards(topic, Config.FLASHCARDS_PER_SET)
                
                if not flashcards:
                    flash('Failed to generate flashcards. Please try again.', 'error')
                    app.logger.error(f"Groq API returned no flashcards for topic: {topic}")
                    return render_template('create_flashcards.html')
                
                # Save to Firestore
                user = get_current_user()
                db = firebase_config.get_firestore_client()
                if not db:
                    flash('Firestore is not available. Please check your Firebase setup.', 'error')
                    app.logger.error("Firestore client not available.")
                    return render_template('create_flashcards.html')
                
                # Save flashcard set to Firestore
                flashcard_set_data = {
                    'topic': topic,
                    'flashcards': flashcards,
                    'created_at': datetime.now(timezone.utc),
                    'card_count': len(flashcards)
                }
                
                try:
                    doc_ref = db.collection('users').document(user['user_id']).collection('flashcard_sets').add(flashcard_set_data)
                    flash(f'Successfully created {len(flashcards)} flashcards for "{topic}"!', 'success')
                    return redirect(url_for('view_flashcards', set_id=doc_ref[1].id))
                    
                except Exception as firestore_error:
                    flash('Failed to save flashcards to Firestore.', 'error')
                    app.logger.error(f"Firestore error: {firestore_error}")
                    return render_template('create_flashcards.html')
                    
            except Exception as e:
                app.logger.error(f"Error creating flashcards: {str(e)}")
                import traceback
                app.logger.error(traceback.format_exc())
                flash('Failed to create flashcards. Please try again later.', 'error')
        
        return render_template('create_flashcards.html')
    
    @app.route('/flashcards')
    @login_required
    def all_flashcards():
        """View all user's flashcard sets."""
        user = get_current_user()
        
        try:
            db = firebase_config.get_firestore_client()
            flashcard_sets = []
            
            if db:
                sets_ref = db.collection('users').document(user['user_id']).collection('flashcard_sets')
                docs = sets_ref.order_by('created_at', direction='DESCENDING').get()
                
                for doc in docs:
                    data = doc.to_dict()
                    data['id'] = doc.id
                    flashcard_sets.append(data)
                    
        except Exception as e:
            app.logger.error(f"Error fetching flashcard sets: {str(e)}")
            flashcard_sets = []
            flash('Unable to load flashcard sets. Please try again.', 'error')
        
        return render_template('all_flashcards.html', flashcard_sets=flashcard_sets)
    
    @app.route('/flashcards/<set_id>')
    @login_required
    def view_flashcards(set_id):
        """View a specific flashcard set."""
        user = get_current_user()
        
        try:
            db = firebase_config.get_firestore_client()
            if not db:
                flash('Unable to connect to database', 'error')
                return redirect(url_for('dashboard'))
            
            # Get the specific flashcard set
            doc_ref = db.collection('users').document(user['user_id']).collection('flashcard_sets').document(set_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                flash('Flashcard set not found', 'error')
                return redirect(url_for('dashboard'))
            
            flashcard_set = doc.to_dict()
            flashcard_set['id'] = doc.id
            
            return render_template('view_flashcards.html', flashcard_set=flashcard_set)
            
        except Exception as e:
            app.logger.error(f"Error fetching flashcard set {set_id}: {str(e)}")
            flash('Unable to load flashcard set. Please try again.', 'error')
            return redirect(url_for('dashboard'))
    
    @app.route('/flashcards/<set_id>/delete', methods=['POST'])
    @login_required
    def delete_flashcard_set(set_id):
        """Delete a flashcard set."""
        user = get_current_user()
        
        try:
            db = firebase_config.get_firestore_client()
            if not db:
                flash('Unable to connect to database', 'error')
                return redirect(url_for('dashboard'))
            
            # Delete the flashcard set
            doc_ref = db.collection('users').document(user['user_id']).collection('flashcard_sets').document(set_id)
            doc_ref.delete()
            
            flash('Flashcard set deleted successfully', 'success')
            
        except Exception as e:
            app.logger.error(f"Error deleting flashcard set {set_id}: {str(e)}")
            flash('Unable to delete flashcard set. Please try again.', 'error')
        
        return redirect(url_for('dashboard'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error="Page not found", code=404), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error="Internal server error", code=500), 500
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
