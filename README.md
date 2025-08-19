# Recallflow - AI-Powered Flashcard Creator

A web application that leverages artificial intelligence to generate educational flashcards automatically. Built with Flask, Firebase, and Groq API for intelligent study material creation.

## Demo Video

<div align="center">
  <video width="80%" controls autoplay muted>
    <source src="https://github.com/ram-from-tvl/Recallflow-Effortless-revision-powered-by-AI-Flashcards./raw/main/demo_video.mp4" type="video/mp4">
    <p>Your browser does not support HTML5 video. <a href="https://github.com/ram-from-tvl/Recallflow-Effortless-revision-powered-by-AI-Flashcards./raw/main/demo_video.mp4">Click here to download the video</a>.</p>
  </video>
</div>

## Features

- **AI-Powered Content Generation**: Automatically create comprehensive flashcards on any topic using advanced language models
- **Secure User Authentication**: Register and login with Firebase Authentication
- **Cloud Data Persistence**: Store and retrieve flashcards using Firebase Firestore
- **Interactive Study Interface**: Engaging flashcard experience with smooth flip animations
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Smart Organization**: Search, filter, and organize flashcard collections
- **Real-time Updates**: Instant synchronization across devices

## Technology Stack

- **Backend**: Python Flask framework with modular architecture
- **Frontend**: Bootstrap 5 with custom CSS and JavaScript
- **Database**: Firebase Firestore for scalable NoSQL storage
- **Authentication**: Firebase Authentication with email/password
- **AI Integration**: Groq API for high-speed language model inference
- **Deployment**: Cloud-ready with environment-based configuration

## Project Structure

```
recallflow/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # User authentication
│   ├── register.html     # User registration
│   ├── dashboard.html    # User dashboard
│   ├── create_flashcards.html # Flashcard creation
│   └── view_flashcards.html   # Study interface
├── static/               # Static assets
│   ├── css/style.css     # Custom styles
│   └── js/main.js        # JavaScript functionality
└── utils/                # Utility modules
    ├── firebase_config.py # Firebase integration
    ├── groq_client.py     # AI API client
    └── auth.py            # Authentication helpers
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
