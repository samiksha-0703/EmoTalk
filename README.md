# EmoTalk - AI-Based Mental Health Assistance

Speech Emotion Recognition (SER) web application for mental health tracking and insights.

## 🚀 Features

- **Real-time Emotion Recognition**: Analyze emotions from voice recordings using deep learning
- **Emotion History**: Track your emotional patterns over time
- **AI-Powered Insights**: Get personalized daily and weekly reports with Gemini AI
- **User-Friendly Interface**: Intuitive design for mental health use cases

## 📁 Project Structure

```
Emotalk/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration and model loader
│   │   ├── services/    # Business logic (prediction, database, AI)
│   │   └── main.py      # FastAPI application
│   └── models/          # Trained ML models
├── emotalk-frontend/     # React frontend
│   └── src/
│       ├── api/         # API client
│       ├── components/  # Reusable components
│       ├── pages/       # Page components
│       └── services/    # API services
└── ai_core/             # ML model training code
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **TensorFlow/Keras**: Deep learning model
- **Librosa**: Audio feature extraction
- **SQLite**: Emotion history database
- **Google Gemini API**: AI insights generation

### Frontend
- **React 19**: UI framework
- **Vite**: Build tool
- **React Media Recorder**: Audio recording
- **Axios**: HTTP client

## 📦 Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables. Create a local `.env` file inside `backend/` by
   copying the provided template, then add your own Gemini API key. This `.env`
   file is git-ignored and must never be committed.
```bash
cp .env.example .env   # On Windows: copy .env.example .env
```
Then edit `backend/.env` and set your key:
```
GEMINI_API_KEY=your_api_key_here
```
Get a key from https://aistudio.google.com/app/apikey

5. Run the server:
```bash
uvicorn app.main:app --reload
```

Backend will run on `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd emotalk-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set environment variables (create `.env` file):
```
VITE_API_URL=http://127.0.0.1:8000
```

4. Run development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🎯 API Endpoints

- `POST /api/v1/predict` - Predict emotion from audio
- `GET /api/v1/emotion-history` - Get emotion history
- `GET /api/v1/daily-report` - Get daily emotion report
- `GET /api/v1/weekly-report` - Get weekly emotion report
- `GET /health` - Health check


## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Real-time emotion tracking during recording
- [ ] Emotion journal with text notes
- [ ] Advanced analytics and visualizations
- [ ] Multi-language support
- [ ] User authentication and profiles

## 📄 License

This project is for educational purposes (Final Year Engineering Project).

## 👥 Team

Final Year Engineering Students

---

**Note**: This is a work in progress. Some features may be incomplete or under development.
