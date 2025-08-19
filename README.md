<<<<<<< HEAD
# AI-Powered Flashcard Creator

A full-stack Python web application that uses AI to generate educational flashcards. Built with Flask, Firebase, and the Groq API.

## Features

- **User Authentication**: Secure sign-up and sign-in using Firebase Authentication
- **AI-Powered Flashcard Generation**: Generate flashcards on any topic using Groq's high-speed LLM inference
- **Data Persistence**: Save and retrieve flashcards using Firebase Firestore
- **Clean Web Interface**: Simple, responsive web interface built with Flask and Bootstrap

## Technology Stack

- **Frontend**: Python Flask with Jinja2 templates and Bootstrap CSS
- **Backend**: Python Flask with Firebase Admin SDK
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **AI Integration**: Groq API for LLM inference
- **Deployment**: Cloud-ready (Google Cloud Run, Railway, etc.)

## Project Structure

```
ai-flashcard-creator/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── firebase_key.json      # Firebase service account key (not included)
├── .env                   # Environment variables (not included)
├── .gitignore            # Git ignore file
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_flashcards.html
│   └── view_flashcards.html
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── utils/                # Utility modules
    ├── firebase_config.py
    ├── groq_client.py
    └── auth.py
```

## Prerequisites

1. Python 3.8+
2. Firebase project with Authentication and Firestore enabled
3. Groq API key
4. Firebase service account key

## Setup Instructions

1. **Clone and navigate to the project**:
   ```bash
   cd ai-flashcard-creator
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Firebase**:
   - Create a Firebase project at https://console.firebase.google.com
   - Enable Authentication (Email/Password)
   - Enable Firestore Database
   - Generate a service account key and save as `firebase_key.json`

5. **Get Groq API key**:
   - Sign up at https://console.groq.com
   - Get your API key

5. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Groq API key and Firebase configuration:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   FIREBASE_PROJECT_ID=your_firebase_project_id
   DEBUG=True
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Open your browser** and navigate to `http://localhost:5000`

## Usage

1. **Register/Login**: Create an account or sign in
2. **Create Flashcards**: Enter a topic and let AI generate flashcards
3. **View Flashcards**: Browse your saved flashcard sets
4. **Study**: Review your flashcards for learning

## Environment Variables

Create a `.env` file with the following variables:

```
GROQ_API_KEY=your_groq_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FIREBASE_PROJECT_ID=your_firebase_project_id
DEBUG=True
```

## Security Best Practices

- Never commit `firebase_key.json` or `.env` files to version control
- Use environment variables for sensitive configuration
- Implement proper session management
- Validate all user inputs
- Use HTTPS in production

## Deployment

This application can be deployed to various platforms:

- **Google Cloud Run**: Recommended for Firebase integration
- **Railway**: Simple deployment with automatic builds
- **Heroku**: Classic PaaS deployment
- **DigitalOcean App Platform**: Modern app deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
=======
# Recallflow-Effortless-revision-powered-by-AI-Flashcards.
AI-powered flashcard generator with Flask, Firebase, and Groq API. Intelligent study tool with automated content creation.
>>>>>>> 5ef9d5b18cbf06a42f496411bee3dd310113e18d
