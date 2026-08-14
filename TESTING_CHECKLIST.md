# EmoTalk Testing Checklist

## 🎯 Testing Overview

This checklist helps verify that all functionality works correctly after recent enhancements.

**Testing Approach**: Manual testing with focus on functionality, stability, and demo-readiness.

---

## 📋 Pre-Testing Setup

### Backend Setup
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Model files exist (`models/emotion_model.h5`, `models/label_encoder.pkl`)
- [ ] Database file exists or will be created (`emotion_history.db`)
- [ ] Environment variables set (optional: `GEMINI_API_KEY`)
- [ ] Backend server starts without errors
- [ ] Health check endpoint works: `GET http://127.0.0.1:8000/health`

### Frontend Setup
- [ ] Dependencies installed (`npm install`)
- [ ] Environment variables set (optional: `VITE_API_URL`)
- [ ] Frontend server starts without errors
- [ ] Browser console shows no critical errors

---

## 🔧 Backend Testing

### 1. Server Startup & Health
- [ ] **Test**: Start backend server
  - **Command**: `uvicorn app.main:app --reload`
  - **Expected**: Server starts, model loads successfully
  - **Check**: Console shows "✅ Model loaded successfully"
  - **Check**: No error messages

- [ ] **Test**: Health check endpoint
  - **URL**: `http://127.0.0.1:8000/health`
  - **Expected**: `{"status": "healthy", "model_loaded": true, "version": "1.0.0"}`
  - **Check**: `model_loaded` is `true`

- [ ] **Test**: API documentation
  - **URL**: `http://127.0.0.1:8000/docs` (Swagger UI)
  - **Expected**: API documentation page loads
  - **Check**: All endpoints visible

### 2. Model Loading
- [ ] **Test**: Model loads on startup
  - **Check**: Console shows model input shape
  - **Check**: Console shows label classes
  - **Expected**: No errors during model loading

- [ ] **Test**: Model file missing scenario
  - **Action**: Temporarily rename `emotion_model.h5`
  - **Expected**: Server starts but logs error
  - **Expected**: Health check shows `model_loaded: false`
  - **Action**: Restore model file

### 3. Audio Prediction Endpoint

#### Basic Functionality
- [ ] **Test**: Upload valid audio file (WAV)
  - **Endpoint**: `POST /api/v1/predict`
  - **Tool**: Postman or curl
  - **Expected**: Returns `{"emotion": "...", "confidence": 0.xxx}`
  - **Check**: Response has valid emotion label
  - **Check**: Confidence is between 0 and 1

- [ ] **Test**: Upload valid audio file (WebM)
  - **Expected**: Same as above
  - **Note**: WebM is common from browser recordings

- [ ] **Test**: Upload valid audio file (MP3)
  - **Expected**: Same as above

#### Error Handling
- [ ] **Test**: Upload file without content-type
  - **Expected**: Should still work (we allow this)

- [ ] **Test**: Upload invalid file type (e.g., image)
  - **Expected**: `400 Bad Request` with error message
  - **Check**: Error message is user-friendly

- [ ] **Test**: Upload file too large (>10MB)
  - **Expected**: `400 Bad Request` with size limit message

- [ ] **Test**: Upload empty file
  - **Expected**: Error from librosa or model

- [ ] **Test**: Upload corrupted audio file
  - **Expected**: Error handling, no server crash

#### Database Integration
- [ ] **Test**: Prediction saves to database
  - **Action**: Make a prediction
  - **Check**: Database has new entry
  - **Check**: Entry has correct emotion, confidence, timestamp

### 4. Emotion History Endpoint
- [ ] **Test**: Get emotion history
  - **Endpoint**: `GET /api/v1/emotion-history`
  - **Expected**: Returns array of emotion records
  - **Check**: Records ordered by date (newest first)
  - **Check**: Each record has `date`, `emotion`, `confidence`

- [ ] **Test**: History with no records
  - **Action**: Clear database or use fresh database
  - **Expected**: Returns empty array or `{"data": [], "count": 0}`

### 5. Daily Report Endpoint
- [ ] **Test**: Get daily report with data
  - **Endpoint**: `GET /api/v1/daily-report`
  - **Prerequisite**: At least one emotion recorded today
  - **Expected**: Returns report with `dominantEmotion`, `insight`, `suggestion`
  - **Check**: Insight is not empty
  - **Check**: Suggestion is not empty

- [ ] **Test**: Get daily report with no data
  - **Action**: Use date with no records
  - **Expected**: Returns `{"error": true, "details": "..."}`

- [ ] **Test**: Daily report with Gemini API
  - **Prerequisite**: `GEMINI_API_KEY` set
  - **Expected**: AI-generated insights
  - **Check**: Insights are relevant and empathetic

- [ ] **Test**: Daily report without Gemini API
  - **Action**: Remove `GEMINI_API_KEY`
  - **Expected**: Fallback insights (still works)

### 6. Weekly Report Endpoint
- [ ] **Test**: Get weekly report with data
  - **Endpoint**: `GET /api/v1/weekly-report`
  - **Prerequisite**: At least one emotion recorded this week
  - **Expected**: Returns report with trends, distribution, insights
  - **Check**: `weeklyTrend` has 7 days
  - **Check**: `distribution` shows emotion counts

- [ ] **Test**: Get weekly report with no data
  - **Expected**: Returns error message

---

## 🎨 Frontend Testing

### 1. Application Load
- [ ] **Test**: Frontend loads without errors
  - **Check**: Browser console has no errors
  - **Check**: All pages accessible

- [ ] **Test**: API connection
  - **Action**: Open browser DevTools → Network tab
  - **Check**: API calls go to correct URL
  - **Check**: CORS headers present (if needed)

### 2. Home Page - Recording

#### Recording Functionality
- [ ] **Test**: Start recording
  - **Action**: Click microphone button
  - **Expected**: Button shows recording state (red, pulsing)
  - **Expected**: Duration timer starts
  - **Expected**: Waveform animation appears
  - **Check**: Browser asks for microphone permission (first time)

- [ ] **Test**: Stop recording
  - **Action**: Click microphone again while recording
  - **Expected**: Recording stops
  - **Expected**: Audio player appears
  - **Expected**: "Analyze Emotion" button appears

- [ ] **Test**: Recording duration
  - **Action**: Record for 10+ seconds
  - **Expected**: Duration shows correctly (e.g., "0:10")
  - **Expected**: Timer continues during recording

#### Audio Playback
- [ ] **Test**: Play recorded audio
  - **Action**: Use audio player controls
  - **Expected**: Audio plays correctly
  - **Expected**: Can pause, seek, adjust volume

#### Emotion Analysis
- [ ] **Test**: Analyze emotion
  - **Action**: Click "Analyze Emotion" button
  - **Expected**: Loading spinner appears
  - **Expected**: "Analyzing your emotions..." message
  - **Expected**: Button disabled during analysis
  - **Expected**: Result appears after 2-5 seconds

- [ ] **Test**: Emotion result display
  - **Expected**: Large emoji for emotion
  - **Expected**: Emotion name (capitalized)
  - **Expected**: Confidence percentage
  - **Expected**: Confidence bar visualization
  - **Expected**: Color matches emotion

- [ ] **Test**: Record again after result
  - **Action**: Click microphone after getting result
  - **Expected**: Previous result clears
  - **Expected**: New recording starts

#### Error Handling
- [ ] **Test**: Backend not running
  - **Action**: Stop backend, try to analyze
  - **Expected**: Error message appears
  - **Expected**: Error message is user-friendly
  - **Expected**: Can dismiss error

- [ ] **Test**: Network error
  - **Action**: Disconnect internet, try to analyze
  - **Expected**: Error message about connection

- [ ] **Test**: Invalid audio
  - **Action**: Try to analyze very short/empty recording
  - **Expected**: Error message (if backend rejects)

### 3. Navigation & Other Pages
- [ ] **Test**: Navigation bar
  - **Check**: All navigation links work
  - **Check**: Active page highlighted

- [ ] **Test**: History page
  - **Action**: Navigate to History
  - **Expected**: Shows emotion history
  - **Check**: Records displayed correctly
  - **Check**: Dates formatted properly

- [ ] **Test**: Calendar page
  - **Action**: Navigate to Calendar
  - **Expected**: Calendar view loads
  - **Check**: Days with emotions highlighted

- [ ] **Test**: Report page
  - **Action**: Navigate to Report
  - **Expected**: Daily report loads
  - **Check**: Insights displayed
  - **Check**: Can view weekly report

- [ ] **Test**: Resources page
  - **Action**: Navigate to Resources
  - **Expected**: Resources page loads

### 4. Responsive Design
- [ ] **Test**: Mobile view (Chrome DevTools)
  - **Action**: Toggle device toolbar, select mobile device
  - **Check**: Layout adapts correctly
  - **Check**: Buttons are tappable size
  - **Check**: Text is readable

- [ ] **Test**: Tablet view
  - **Check**: Layout works on tablet sizes

---

## 🧠 ML Model Testing

### 1. Model Accuracy (Basic)
- [ ] **Test**: Happy emotion
  - **Action**: Record yourself saying something happy/cheerful
  - **Expected**: Model predicts "happy" with reasonable confidence (>0.5)

- [ ] **Test**: Sad emotion
  - **Action**: Record something sad/melancholic
  - **Expected**: Model predicts "sad" with reasonable confidence

- [ ] **Test**: Neutral emotion
  - **Action**: Record in neutral tone
  - **Expected**: Model predicts "neutral" or similar

- [ ] **Test**: Angry emotion
  - **Action**: Record something angry/frustrated
  - **Expected**: Model predicts "angry" with reasonable confidence

### 2. Edge Cases
- [ ] **Test**: Very short audio (<1 second)
  - **Expected**: Model still processes (may pad)

- [ ] **Test**: Very long audio (>10 seconds)
  - **Expected**: Model processes first 3 seconds

- [ ] **Test**: Background noise
  - **Action**: Record with background noise
  - **Expected**: Model still works (may be less accurate)

- [ ] **Test**: Low volume audio
  - **Expected**: Model processes (may normalize)

### 3. Confidence Scores
- [ ] **Test**: High confidence predictions
  - **Action**: Record clear, strong emotion
  - **Expected**: Confidence > 0.7

- [ ] **Test**: Low confidence predictions
  - **Action**: Record ambiguous/mixed emotion
  - **Expected**: Confidence may be lower (<0.6)
  - **Note**: This is normal for ambiguous cases

---

## 🔄 End-to-End Flow Testing

### Complete User Journey
1. [ ] **Start**: Open application
   - Frontend loads
   - No errors in console

2. [ ] **Record**: Click microphone
   - Recording starts
   - Duration timer works
   - Can see waveform

3. [ ] **Stop**: Click microphone again
   - Recording stops
   - Audio player appears

4. [ ] **Analyze**: Click "Analyze Emotion"
   - Loading state appears
   - Result displays after processing
   - Result saved to database

5. [ ] **View History**: Navigate to History page
   - New record appears in history
   - Record has correct data

6. [ ] **View Report**: Navigate to Report page
   - Daily report includes new emotion
   - Insights are generated

7. [ ] **Repeat**: Record multiple emotions
   - Each prediction works
   - History updates correctly
   - Reports reflect trends

### Error Recovery
- [ ] **Test**: Backend restart during use
  - **Action**: Restart backend while frontend is open
  - **Action**: Try to analyze
  - **Expected**: Error message, can retry after backend restarts

- [ ] **Test**: Network interruption
  - **Action**: Disconnect network, try to analyze
  - **Expected**: Error message
  - **Action**: Reconnect network
  - **Expected**: Can retry successfully

---

## 🐛 Potential Failure Points (After Recent Changes)

### Backend
1. **Model Loading**
   - ❗ **Issue**: Model path incorrect
   - ✅ **Check**: Verify `MODEL_PATH` in config.py
   - ✅ **Fix**: Ensure model files in `backend/models/`

2. **API Prefix**
   - ❗ **Issue**: Frontend calls `/predict` but backend expects `/api/v1/predict`
   - ✅ **Check**: Verify frontend uses `API_ENDPOINTS` from config
   - ✅ **Fix**: Update frontend API calls if needed

3. **CORS**
   - ❗ **Issue**: CORS errors in browser
   - ✅ **Check**: Verify frontend URL in `CORS_ORIGINS`
   - ✅ **Fix**: Add frontend URL to config

4. **File Upload**
   - ❗ **Issue**: File type validation too strict
   - ✅ **Check**: Verify `ALLOWED_AUDIO_TYPES` includes WebM
   - ✅ **Fix**: Add missing types if needed

5. **Database Path**
   - ❗ **Issue**: Database not created
   - ✅ **Check**: Verify `DB_PATH` in config
   - ✅ **Fix**: Ensure write permissions

### Frontend
1. **API URL**
   - ❗ **Issue**: API calls fail
   - ✅ **Check**: Verify `VITE_API_URL` or default in config
   - ✅ **Fix**: Set correct backend URL

2. **API Prefix**
   - ❗ **Issue**: 404 errors on API calls
   - ✅ **Check**: Verify frontend uses `/api/v1` prefix
   - ✅ **Fix**: Update API client base URL

3. **Error Handling**
   - ❗ **Issue**: Errors not displayed to user
   - ✅ **Check**: Verify error state in components
   - ✅ **Fix**: Add error boundaries if needed

---

## ✅ Demo Readiness Checklist

### Before Demo
- [ ] All critical tests pass
- [ ] No console errors
- [ ] Sample data in database (for demo)
- [ ] Backend running and stable
- [ ] Frontend responsive and polished
- [ ] Error messages are user-friendly
- [ ] Loading states work correctly
- [ ] Audio recording works on demo device
- [ ] Microphone permissions granted

### Demo Flow
1. [ ] Show home page with recording
2. [ ] Record a sample emotion
3. [ ] Show prediction result
4. [ ] Show history page
5. [ ] Show daily report
6. [ ] Show weekly report
7. [ ] Handle any errors gracefully

---

## 📊 Test Results Template

```
Date: ___________
Tester: ___________

Backend Tests: ___/___
Frontend Tests: ___/___
E2E Tests: ___/___
ML Model Tests: ___/___

Critical Issues: ___
Minor Issues: ___

Status: [ ] Ready for Demo [ ] Needs Fixes
```

---

## 🚀 Quick Test Script

Run these commands to quickly verify setup:

```bash
# Backend
cd backend
python -c "from app.core.model_loader import model_loader; model_loader.load_model()"
uvicorn app.main:app --reload &
curl http://127.0.0.1:8000/health

# Frontend
cd emotalk-frontend
npm run dev
# Open http://localhost:5173
```

---

**Note**: This checklist focuses on functionality and stability. For production, add automated tests, performance testing, and security testing.

