# Quick Test Guide for EmoTalk

## 🚀 Quick Start Testing

### 1. Backend Quick Check (30 seconds)

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start server
uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Initializing database...
INFO:     ✅ Database initialized
INFO:     Loading emotion recognition model...
INFO:     ✅ Model loaded successfully
INFO:     ✅ EmoTalk API started successfully
INFO:     Application startup complete.
```

**If you see errors:**
- ❌ Model file not found → Check `backend/models/emotion_model.h5` exists
- ❌ Import errors → Run `pip install -r requirements.txt`
- ❌ Port already in use → Change port or kill existing process

### 2. Test Health Endpoint

Open browser or use curl:
```bash
curl http://127.0.0.1:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### 3. Test Debug Endpoint (New!)

```bash
curl http://127.0.0.1:8000/debug/status
```

**Expected:** Detailed system status including:
- Model loading status
- File paths
- Database status
- Recent predictions

### 4. Frontend Quick Check (30 seconds)

```bash
cd emotalk-frontend

# Install if needed
npm install

# Start dev server
npm run dev
```

**Expected:**
- Server starts on `http://localhost:5173`
- No errors in terminal
- Browser opens automatically

### 5. Test Recording (1 minute)

1. **Open** `http://localhost:5173`
2. **Click** microphone button
3. **Speak** for 3-5 seconds (say something happy/sad/neutral)
4. **Click** microphone again to stop
5. **Click** "Analyze Emotion" button
6. **Wait** 2-5 seconds
7. **See** emotion result with emoji and confidence

**Expected:**
- ✅ Recording starts (button turns red, pulsing)
- ✅ Duration timer appears
- ✅ Waveform animation shows
- ✅ Audio player appears after stopping
- ✅ Loading spinner during analysis
- ✅ Emotion result appears with confidence bar

**If it fails:**
- Check browser console (F12) for errors
- Check backend is running
- Check microphone permissions

---

## 🧪 Manual Test Cases

### Test Case 1: Happy Emotion
1. Record: "I'm feeling great today! Everything is wonderful!"
2. Expected: Emotion = "happy", Confidence > 0.5

### Test Case 2: Sad Emotion
1. Record: "I'm feeling down and sad today..."
2. Expected: Emotion = "sad", Confidence > 0.5

### Test Case 3: Neutral Emotion
1. Record: "Today is a normal day, nothing special."
2. Expected: Emotion = "neutral" or "calm"

### Test Case 4: Multiple Recordings
1. Record 3 different emotions
2. Navigate to History page
3. Expected: All 3 records appear in history

### Test Case 5: Daily Report
1. Make at least 2 predictions today
2. Navigate to Report page
3. Expected: Daily report shows dominant emotion and insights

---

## 🐛 Common Issues & Quick Fixes

### Issue: "Backend not connected"
**Fix:**
- Check backend is running (`curl http://127.0.0.1:8000/health`)
- Check frontend API URL in `src/config/api.js`
- Check CORS settings in backend

### Issue: "Model not loaded"
**Fix:**
- Check `backend/models/emotion_model.h5` exists
- Check `backend/models/label_encoder.pkl` exists
- Check backend logs for error messages

### Issue: "CORS error" in browser
**Fix:**
- Add frontend URL to `CORS_ORIGINS` in `backend/app/core/config.py`
- Restart backend

### Issue: "404 Not Found" on API calls
**Fix:**
- Check API prefix: frontend should use `/api/v1/predict`
- Verify `API_BASE_URL` in frontend config includes prefix

### Issue: Recording doesn't work
**Fix:**
- Check browser microphone permissions
- Try different browser (Chrome recommended)
- Check browser console for errors

### Issue: Prediction takes too long
**Fix:**
- Normal: 2-5 seconds is expected
- If >10 seconds: Check backend logs, may be model loading issue
- Check file size (should be <10MB)

---

## 📊 Verification Checklist

Before demo/presentation:

- [ ] Backend starts without errors
- [ ] Health endpoint returns `model_loaded: true`
- [ ] Frontend loads without console errors
- [ ] Can record audio (microphone works)
- [ ] Can analyze emotion (prediction works)
- [ ] Result displays correctly
- [ ] History page shows records
- [ ] Report page shows insights
- [ ] No critical errors in console

---

## 🔍 Debugging Tips

### Backend Logs
Watch backend terminal for:
- ✅ `✅ Prediction: happy (85.3% confidence)` = Success
- ❌ `Error processing audio` = Problem with audio file
- ❌ `Model not loaded` = Model file issue

### Frontend Console
Open browser DevTools (F12) → Console tab:
- ✅ No red errors = Good
- ⚠️ Yellow warnings = Usually OK
- ❌ Red errors = Check API connection

### Network Tab
Open browser DevTools (F12) → Network tab:
- Check API calls to `/api/v1/predict`
- Status should be `200 OK`
- If `404`: Check API prefix
- If `500`: Check backend logs

---

## 🎯 Demo Flow (5 minutes)

1. **Start Backend** (30s)
   ```bash
   cd backend && uvicorn app.main:app --reload
   ```

2. **Start Frontend** (30s)
   ```bash
   cd emotalk-frontend && npm run dev
   ```

3. **Show Features** (4 minutes)
   - Record happy emotion → Show result
   - Record sad emotion → Show result
   - Show history page
   - Show daily report
   - Show weekly report

4. **Handle Questions**
   - Use debug endpoint to show system status
   - Show backend logs if needed
   - Show API documentation at `/docs`

---

## 📝 Test Results Template

```
Date: ___________
Backend Status: [ ] OK [ ] Issues
Frontend Status: [ ] OK [ ] Issues
Recording: [ ] Works [ ] Issues
Prediction: [ ] Works [ ] Issues
History: [ ] Works [ ] Issues
Reports: [ ] Works [ ] Issues

Issues Found:
1. ___________
2. ___________

Ready for Demo: [ ] Yes [ ] No
```

---

**Quick Test Time: ~5 minutes**
**Full Test Time: ~30 minutes (see TESTING_CHECKLIST.md)**

