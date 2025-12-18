from fastapi import APIRouter, HTTPException
from app.db import db
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any
from bson import ObjectId

router = APIRouter()


# === Pydantic Models ===
class QuizSubmission(BaseModel):
    lesson_slug: str
    quiz_type: str  # multiple_choice, true_false, fill_in_blanks, match_following, short_answer
    answers: Dict[int, Any]  # {question_id: answer}
    user_email: str = None
    time_taken: float = None  # seconds


def serialize_doc(doc):
    """Convert MongoDB documents to JSON-serializable format"""
    if not doc:
        return None
    if isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    return doc


# === Quiz Retrieval ===

@router.get("/lesson/{lesson_slug}")
async def get_lesson_quizzes(lesson_slug: str):
    """
    Get all 5 quiz types for a lesson.
    Returns questions without correct answers (for security).
    """
    
    lesson = db['lessons'].find_one({'slug': lesson_slug})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    quiz_doc = db['quizzes'].find_one({'lesson_slug': lesson_slug})
    if not quiz_doc:
        raise HTTPException(status_code=404, detail="Quiz not found for this lesson")
    
    # Prepare response with quiz types
    quiz_types = {}
    for qtype_key, qtype_data in quiz_doc.get('quiz_types', {}).items():
        questions_clean = []
        for q in qtype_data.get('questions', []):
            # Remove answers for security during quiz taking
            q_clean = {
                'question_id': q.get('question_id'),
                'question': q.get('question'),
                'marks': q.get('marks', 1)
            }
            
            # Keep question-specific fields based on type
            if qtype_key == 'multiple_choice':
                q_clean['options'] = q.get('options', [])
            elif qtype_key == 'match_following':
                q_clean['pairs'] = q.get('pairs', [])
            
            questions_clean.append(q_clean)
        
        quiz_types[qtype_key] = {
            'type': qtype_data.get('type'),
            'total_questions': qtype_data.get('total_questions'),
            'questions': questions_clean
        }
    
    return {
        'lesson_slug': lesson_slug,
        'lesson_title': lesson.get('title'),
        'quiz_types': quiz_types
    }


@router.get("/quiz/{lesson_slug}/{quiz_type}")
async def get_quiz_by_type(lesson_slug: str, quiz_type: str):
    """Get a specific quiz type for a lesson."""
    
    quiz_doc = db['quizzes'].find_one({'lesson_slug': lesson_slug})
    if not quiz_doc:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz_type_data = quiz_doc.get('quiz_types', {}).get(quiz_type)
    if not quiz_type_data:
        raise HTTPException(status_code=404, detail=f"Quiz type '{quiz_type}' not found")
    
    # Remove answers for security
    questions_clean = []
    for q in quiz_type_data.get('questions', []):
        q_clean = {k: v for k, v in q.items() if k not in ['correct_answer', 'explanation']}
        questions_clean.append(q_clean)
    
    return {
        'lesson_slug': lesson_slug,
        'quiz_type': quiz_type,
        'type': quiz_type_data.get('type'),
        'total_questions': quiz_type_data.get('total_questions'),
        'questions': questions_clean
    }


# === Quiz Submission & Grading ===

@router.post("/submit")
async def submit_quiz(payload: QuizSubmission):
    """
    Submit quiz answers and get graded results.
    """
    
    # Validate lesson exists
    lesson = db['lessons'].find_one({'slug': payload.lesson_slug})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Get quiz
    quiz_doc = db['quizzes'].find_one({'lesson_slug': payload.lesson_slug})
    if not quiz_doc:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz_type_data = quiz_doc.get('quiz_types', {}).get(payload.quiz_type)
    if not quiz_type_data:
        raise HTTPException(status_code=404, detail=f"Quiz type '{payload.quiz_type}' not found")
    
    questions = quiz_type_data.get('questions', [])
    total_marks = sum(q.get('marks', 1) for q in questions)
    
    # Grade the quiz
    score = 0
    detailed_results = []
    
    for q in questions:
        q_id = q.get('question_id')
        user_answer = payload.answers.get(q_id)
        correct_answer = q.get('correct_answer')
        marks_awarded = 0
        is_correct = False
        
        if user_answer is None:
            detailed_results.append({
                'question_id': q_id,
                'user_answer': None,
                'is_correct': False,
                'marks_awarded': 0,
                'explanation': q.get('explanation', '')
            })
            continue
        
        # Grade based on quiz type
        if payload.quiz_type == 'multiple_choice':
            is_correct = user_answer == correct_answer
            marks_awarded = q.get('marks', 1) if is_correct else 0
            
        elif payload.quiz_type == 'true_false':
            # Handle string/boolean conversion
            if isinstance(user_answer, str):
                user_answer = user_answer.lower() in ['true', 'yes', '1']
            is_correct = user_answer == correct_answer
            marks_awarded = q.get('marks', 1) if is_correct else 0
            
        elif payload.quiz_type == 'fill_in_blanks':
            # Case-insensitive comparison
            is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
            marks_awarded = q.get('marks', 1) if is_correct else 0
            
        elif payload.quiz_type == 'match_following':
            # Compare pairs - user_answer should be a list of selected pairs
            user_pairs = user_answer if isinstance(user_answer, list) else []
            correct_pairs = correct_answer if isinstance(correct_answer, list) else [correct_answer]
            is_correct = set(tuple(sorted(p.items())) if isinstance(p, dict) else p for p in user_pairs) == \
                         set(tuple(sorted(p.items())) if isinstance(p, dict) else p for p in correct_pairs)
            marks_awarded = q.get('marks', 5) if is_correct else 0
            
        elif payload.quiz_type == 'short_answer':
            # Case-insensitive, partial matching accepted
            user_ans_lower = user_answer.lower().strip()
            correct_ans_lower = correct_answer.lower().strip() if isinstance(correct_answer, str) else str(correct_answer).lower().strip()
            is_correct = user_ans_lower == correct_ans_lower
            marks_awarded = q.get('marks', 2) if is_correct else 0
        
        score += marks_awarded
        detailed_results.append({
            'question_id': q_id,
            'user_answer': str(user_answer),
            'correct_answer': str(correct_answer),
            'is_correct': is_correct,
            'marks_awarded': marks_awarded,
            'explanation': q.get('explanation', '')
        })
    
    # Calculate percentage
    quiz_percentage = round((score / total_marks * 100), 2) if total_marks > 0 else 0

    # Record attempt to DB
    attempt_doc = {
        'lesson_slug': payload.lesson_slug,
        'quiz_type': payload.quiz_type,
        'score_earned': score,
        'total_marks': total_marks,
        'quiz_score': quiz_percentage,
        'detailed_results': detailed_results,
        'submitted_at': datetime.utcnow(),
        'time_taken': payload.time_taken,
        'user_email': payload.user_email or 'anonymous@local'
    }
    try:
        db['quiz_attempts'].insert_one(attempt_doc)
    except Exception:
        pass

    # Update user metrics via ML service if available
    try:
        from app.services.student_metrics import get_user_metrics
        user_email = payload.user_email or 'anonymous@local'
        metrics = get_user_metrics(user_email)
        # persist prediction into users collection
        db['users'].update_one(
            {'email': user_email},
            {'$set': {
                'level': metrics.get('predicted_level'),
                'recommendations': metrics.get('recommended_lessons'),
                'last_predicted_at': datetime.utcnow()
            }},
            upsert=True
        )
    except Exception:
        metrics = None

    return {
        'lesson_slug': payload.lesson_slug,
        'quiz_type': payload.quiz_type,
        'score_earned': score,
        'total_marks': total_marks,
        'percentage': quiz_percentage,
        'passed': quiz_percentage >= 70,  # 70% is passing score
        'detailed_results': detailed_results,
        'metrics': metrics
    }


@router.get("/answer-key/{lesson_slug}/{quiz_type}")
async def get_answer_key(lesson_slug: str, quiz_type: str):
    """Get the answer key for a quiz (teacher/admin only in production)."""
    
    quiz_doc = db['quizzes'].find_one({'lesson_slug': lesson_slug})
    if not quiz_doc:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz_type_data = quiz_doc.get('quiz_types', {}).get(quiz_type)
    if not quiz_type_data:
        raise HTTPException(status_code=404, detail=f"Quiz type not found")
    
    answer_key = []
    for q in quiz_type_data.get('questions', []):
        answer_key.append({
            'question_id': q.get('question_id'),
            'question': q.get('question'),
            'correct_answer': q.get('correct_answer'),
            'marks': q.get('marks'),
            'explanation': q.get('explanation')
        })
    
    return {
        'lesson_slug': lesson_slug,
        'quiz_type': quiz_type,
        'answer_key': answer_key
    }
