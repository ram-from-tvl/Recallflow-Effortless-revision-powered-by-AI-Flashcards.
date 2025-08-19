# AI Flashcard Creator - Developer Guide

## Project Overview

The AI-Powered Flashcard Creator is a full-stack web application built with Flask that uses AI to generate educational flashcards. The application features user authentication, AI-powered content generation, and data persistence.

**Application URL**: http://localhost:5000

## Current Features

### Core Functionality
- Flask web application running on port 5000
- Responsive Bootstrap UI
- User authentication system
- AI-powered flashcard generation
- Interactive flashcard study interface
- User dashboard with statistics
- Search and filter functionality

### User Interface
- **Landing Page**: Professional homepage with feature highlights
- **Authentication**: Register/Login with email validation
- **Dashboard**: Overview of flashcard sets with statistics
- **Create Flashcards**: AI-powered generation interface
- **Study Interface**: Interactive flashcard viewer with flip animations
- **Collection Management**: View, search, and organize flashcard sets

### Design Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Modern, professional styling
- **Interactive Elements**: Hover effects, animations, smooth transitions
- **Accessibility**: Proper ARIA labels and keyboard navigation

### Technical Features
- **Flask Framework**: Robust Python web framework
- **Modular Architecture**: Clean separation of concerns
- **Error Handling**: Graceful degradation for missing services
- **Virtual Environment**: Isolated Python dependencies

## Architecture Overview

```
ai-flashcard-creator/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── templates/                # Jinja2 HTML templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Landing page
│   ├── dashboard.html       # User dashboard
│   ├── create_flashcards.html # Flashcard creation
│   ├── view_flashcards.html # Study interface
│   └── ...                  # Auth and error pages
├── static/                   # Static assets
│   ├── css/style.css        # Custom styles
│   └── js/main.js           # JavaScript functionality
└── utils/                    # Utility modules
    ├── firebase_config.py   # Firebase integration
    ├── groq_client.py       # AI API integration
    └── auth.py              # Authentication helpers
```

## Production Setup

### 1. Firebase Project Setup
1. Go to https://console.firebase.google.com
2. Create a new project
3. Enable Authentication (Email/Password)
4. Enable Firestore Database
5. Download service account key as `firebase_key.json`
6. Update `.env` with your project ID

### 2. Groq API Setup
1. Sign up at https://console.groq.com
2. Create an API key
3. Update `.env`: `GROQ_API_KEY=your_real_key_here`

### 3. Deployment Options

#### Google Cloud Run
```bash
gcloud run deploy ai-flashcard-creator \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

#### Railway
Connect your GitHub repository to Railway for automatic deployments.

#### Heroku
```bash
# Create Procfile: web: gunicorn app:app
heroku create your-app-name
git push heroku main
```

## Testing

### Basic Functionality Test
1. Visit http://localhost:5000
2. Register with email and password
3. Explore the dashboard
4. Create flashcards with any topic
5. Study the generated flashcards

### Features to Test
- User registration and login
- Flashcard creation
- Interactive flashcard study mode
- Search and filter flashcard sets
- Dashboard statistics
- Responsive design on mobile
- Navigation and user experience

## Troubleshooting

### Application Won't Start
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or myenv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Run with debugging
python app.py
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in app.py
app.run(port=5001)
```

### Import Errors
```bash
# Check virtual environment
which python
# Should show venv/bin/python

# Verify packages
pip list
```

## Project Benefits

### For Learning
- **Instant AI Generation**: Create flashcards on any topic
- **Interactive Study**: Engaging card flip interface
- **Progress Tracking**: Visual study progress
- **Topic Variety**: Works with any subject matter

### For Development
- **Modern Stack**: Python Flask + Firebase + AI
- **Professional UI**: Bootstrap 5 + custom styling
- **Scalable Architecture**: Modular, maintainable code
- **Production Ready**: Easy deployment options
