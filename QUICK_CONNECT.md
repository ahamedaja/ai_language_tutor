# Quick Connect Guide

## ⚡ Get Started in 3 Steps

### Step 1: Ensure MongoDB is Running
```bash
mongosh
# If connection successful, MongoDB is running
# Type: exit to close
```

### Step 2: Clear Database & Seed Fresh Data
```bash
# Terminal 1
cd d:\ai-language-tutor\backend\scripts
python seed_data.py
```

Output should show:
```
[*] Starting Database Seeding...
[+] Connected to MongoDB: english_tutor
[+] Inserted 10 lessons
[+] Inserted 10 quiz sets
[+] Seeding completed successfully!
```

### Step 3: Start Backend & Frontend

**Terminal 1 - Backend**:
```bash
cd d:\ai-language-tutor\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Look for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2 - Frontend**:
```bash
cd d:\ai-language-tutor\frontend
npm run dev
```

Look for:
```
VITE v5.4.21  ready in ...
➜  Local:   http://localhost:5173/ (or 5174)
```

### Step 4: Open Browser

Navigate to: **http://localhost:5173**

---

## What You'll See

### Landing Page
- "Language Tutor" title
- Login/Register options

### Dashboard (After Login)
- 10 lesson cards showing:
  - Lesson title
  - Difficulty level (Beginner/Intermediate/Advanced)
  - Estimated time
  - Progress indicator

### Click on Any Lesson to:
1. **View Content** - Read full lesson with examples
2. **Take Quiz** - 5 different quiz types:
   - Multiple Choice (10 Q)
   - True/False (10 Q)
   - Fill in the Blanks (10 Q)
   - Match the Following (10 Q)
   - Short Answer (10 Q)
3. **See Results** - Score, percentage, pass/fail

---

## Connected Features

✅ **Lessons List** - All 10 lessons loaded from backend  
✅ **Lesson Details** - Full content with examples  
✅ **Quiz System** - All 5 quiz types working  
✅ **Auto Grading** - Instant score calculation  
✅ **Progress Tracking** - Score history per lesson  
✅ **Responsive Design** - Works on different screen sizes  

---

## API Endpoints Working

```
✓ GET /api/lessons/
✓ GET /api/lessons/{slug}
✓ GET /api/quiz/lesson/{lesson_slug}
✓ GET /api/quiz/quiz/{lesson_slug}/{quiz_type}
✓ POST /api/quiz/submit
✓ GET /api/quiz/answer-key/{lesson_slug}/{quiz_type}
```

---

## Lesson Slugs Available

1. `basics-of-english-grammar`
2. `parts-of-speech`
3. `tenses`
4. `subject-verb-agreement`
5. `active-passive-voice`
6. `direct-indirect-speech`
7. `sentence-structure`
8. `common-grammar-mistakes`
9. `paragraph-writing`
10. `practical-english-daily-use`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5173 in use | Frontend auto-switches to 5174, 5175, etc. |
| "Cannot connect to backend" | Check if `http://localhost:8000/api/lessons/` works |
| Lessons not showing | Reseed database: `python seed_data.py` |
| Quiz won't load | Clear browser cache and refresh |
| "MongoDB connection error" | Ensure mongod is running |

---

## File Structure

```
d:\ai-language-tutor\
├── backend/
│   ├── app/
│   │   ├── main.py (FastAPI app)
│   │   ├── routes/
│   │   │   ├── lessons.py
│   │   │   ├── quiz.py
│   │   │   └── ...
│   │   └── db.py (MongoDB)
│   ├── scripts/
│   │   ├── seed_data.py (Run this!)
│   │   ├── lessons_and_quizzes.json
│   │   └── quizzes_part*.json
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   ├── components/
│   │   │   ├── QuizInterface.jsx
│   │   │   ├── LessonDetail.jsx
│   │   │   └── ...
│   │   └── utils/
│   │       └── api.js
│   └── package.json
│
└── docs/
    └── (Documentation files)
```

---

## Test the Integration

### Test 1: Check Backend is Running
```bash
powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/lessons/" -UseBasicParsing
```

Should return JSON array of lessons.

### Test 2: Check Frontend Loads
Navigate to: `http://localhost:5173`

Should see the Language Tutor dashboard.

### Test 3: Try a Lesson
1. Click "View Lesson" on any lesson card
2. Scroll through the content
3. Click "Start Quiz"

### Test 4: Submit Quiz
1. Answer some questions
2. Click "Submit Quiz"
3. See your score and feedback

---

## Database Structure

### Lessons Collection
```json
{
  "_id": ObjectId,
  "title": "Basics of English Grammar",
  "slug": "basics-of-english-grammar",
  "description": "...",
  "difficulty": "Beginner",
  "estimated_time": 45,
  "notes": "Long detailed lesson content...",
  "examples": [
    {
      "example": "The cat is on the mat.",
      "explanation": "..."
    }
  ]
}
```

### Quizzes Collection
```json
{
  "_id": ObjectId,
  "lesson_slug": "basics-of-english-grammar",
  "quiz_types": {
    "multiple_choice": {
      "questions": [
        {
          "question_id": 1,
          "question": "What is grammar?",
          "options": [...],
          "correct_answer": "...",
          "explanation": "...",
          "marks": 1
        }
      ]
    },
    "true_false": {...},
    "fill_in_blanks": {...},
    "match_following": {...},
    "short_answer": {...}
  }
}
```

---

## Performance Tips

1. **Browser**: Use Chrome, Firefox, or Edge for best performance
2. **RAM**: Need ~500MB free for both backend and frontend
3. **Network**: Local machine performance is fast (~<50ms API calls)
4. **Database**: MongoDB queries are indexed for speed

---

## Next Time You Start

```bash
# Terminal 1: Seed (only if database is empty)
cd backend\scripts && python seed_data.py

# Terminal 2: Backend
cd backend && python -m uvicorn app.main:app --reload

# Terminal 3: Frontend
cd frontend && npm run dev

# Browser: Open http://localhost:5173
```

---

**All Systems Ready!** 🚀  
Start from **Step 1** above to get up and running.
