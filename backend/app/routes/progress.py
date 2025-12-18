# # # from fastapi import APIRouter, Depends
# # # from app.routes.auth import get_current_user
# # # from app.db import db
# # # from bson import ObjectId

# # # router = APIRouter()

# # # def serialize_doc(doc: dict) -> dict:
# # #     """
# # #     Convert MongoDB document (including ObjectId) to JSON-serializable dict.
# # #     Handles nested dicts/lists.
# # #     """
# # #     if not doc:
# # #         return {}
    
# # #     def convert(obj):
# # #         if isinstance(obj, ObjectId):
# # #             return str(obj)
# # #         elif isinstance(obj, dict):
# # #             return {k: convert(v) for k, v in obj.items()}
# # #         elif isinstance(obj, list):
# # #             return [convert(i) for i in obj]
# # #         else:
# # #             return obj

# # #     return convert(doc)

# # # @router.get('/')
# # # async def get_progress(user=Depends(get_current_user)):
# # #     email = user['email']
# # #     results = list(db['exercise_results'].find({'user_email': email}))
    
# # #     # Serialize documents to remove ObjectId issues
# # #     results = [serialize_doc(r) for r in results]

# # #     total = len(results)
# # #     avg_score = sum(r.get('evaluation', {}).get('score', 0) for r in results)/total if total > 0 else None

# # #     return {
# # #         'count': total,
# # #         'avg_score': avg_score,
# # #         'recent': results[-10:]
# # #     }


# # # @router.post('/favorite')
# # # async def set_favorite(payload: dict, user=Depends(get_current_user)):
# # #     """Toggle favorite flag for a saved exercise result.
# # #     Expects JSON: {"result_id": "<id>", "favorite": true}
# # #     """
# # #     result_id = payload.get('result_id')
# # #     fav = bool(payload.get('favorite', True))
# # #     if not result_id:
# # #         return {'ok': False, 'error': 'result_id required'}

# # #     db['exercise_results'].update_one({'_id': ObjectId(result_id), 'user_email': user['email']}, {'$set': {'favorite': fav}})
# # #     return {'ok': True}


# # # @router.get('/export')
# # # async def export_progress(format: str = 'json', user=Depends(get_current_user)):
# # #     """Export user's progress as JSON or CSV. Query param: ?format=csv"""
# # #     email = user['email']
# # #     results = list(db['exercise_results'].find({'user_email': email}))
# # #     # Serialize
# # #     results = [serialize_doc(r) for r in results]

# # #     if format == 'csv':
# # #         # Build CSV manually
# # #         import io, csv
# # #         output = io.StringIO()
# # #         fieldnames = ['_id', 'lesson_id', 'user_input', 'score', 'submitted_at', 'favorite']
# # #         w = csv.DictWriter(output, fieldnames=fieldnames)
# # #         w.writeheader()
# # #         for r in results:
# # #             row = {
# # #                 '_id': r.get('_id'),
# # #                 'lesson_id': r.get('lesson_id'),
# # #                 'user_input': r.get('user_input'),
# # #                 'score': r.get('evaluation', {}).get('score'),
# # #                 'submitted_at': r.get('submitted_at'),
# # #                 'favorite': r.get('favorite', False)
# # #             }
# # #             w.writerow(row)
# # #         return output.getvalue()

# # #     return {'results': results}


# # from fastapi import APIRouter, Depends
# # from app.routes.auth import get_current_user
# # from app.db import db
# # from bson import ObjectId
# # from app.services.ai_service import predict_learning_path

# # router = APIRouter()

# # def serialize_doc(doc: dict) -> dict:
# #     """Convert MongoDB document (including ObjectId) to JSON-serializable dict."""
# #     if not doc:
# #         return {}
    
# #     def convert(obj):
# #         if isinstance(obj, ObjectId):
# #             return str(obj)
# #         elif isinstance(obj, dict):
# #             return {k: convert(v) for k, v in obj.items()}
# #         elif isinstance(obj, list):
# #             return [convert(i) for i in obj]
# #         else:
# #             return obj
# #     return convert(doc)

# # @router.get('/')
# # async def get_progress(user=Depends(get_current_user)):
# #     email = user['email']
# #     results = list(db['exercise_results'].find({'user_email': email}))
# #     results = [serialize_doc(r) for r in results]

# #     total = len(results)
# #     avg_score = sum(r.get('evaluation', {}).get('score', 0) for r in results)/total if total > 0 else None

# #     # Personalized learning path
# #     learning_path = predict_learning_path(results, user.get('level', 'beginner'))

# #     return {
# #         'count': total,
# #         'avg_score': avg_score,
# #         'recent': results[-10:],
# #         'personalized_path': learning_path
# #     }

# # @router.post('/favorite')
# # async def set_favorite(payload: dict, user=Depends(get_current_user)):
# #     """Toggle favorite flag for a saved exercise result."""
# #     from bson import ObjectId
# #     result_id = payload.get('result_id')
# #     fav = bool(payload.get('favorite', True))
# #     if not result_id:
# #         return {'ok': False, 'error': 'result_id required'}
# #     db['exercise_results'].update_one(
# #         {'_id': ObjectId(result_id), 'user_email': user['email']},
# #         {'$set': {'favorite': fav}}
# #     )
# #     return {'ok': True}

# # @router.get('/export')
# # async def export_progress(format: str = 'json', user=Depends(get_current_user)):
# #     """Export user's progress as JSON or CSV."""
# #     results = list(db['exercise_results'].find({'user_email': user['email']}))
# #     results = [serialize_doc(r) for r in results]

# #     if format == 'csv':
# #         import io, csv
# #         output = io.StringIO()
# #         fieldnames = ['_id', 'lesson_id', 'user_input', 'score', 'submitted_at', 'favorite']
# #         writer = csv.DictWriter(output, fieldnames=fieldnames)
# #         writer.writeheader()
# #         for r in results:
# #             row = {
# #                 '_id': r.get('_id'),
# #                 'lesson_id': r.get('lesson_id'),
# #                 'user_input': r.get('user_input'),
# #                 'score': r.get('evaluation', {}).get('score'),
# #                 'submitted_at': r.get('submitted_at'),
# #                 'favorite': r.get('favorite', False)
# #             }
# #             writer.writerow(row)
# #         return output.getvalue()

# #     return {'results': results}


# from fastapi import APIRouter, Depends
# from app.routes.auth import get_current_user
# from app.db import db
# from bson import ObjectId
# from app.services.ai_service import predict_learning_path

# router = APIRouter()

# def serialize_doc(doc: dict) -> dict:
#     if not doc:
#         return {}
    
#     def convert(obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         elif isinstance(obj, dict):
#             return {k: convert(v) for k, v in obj.items()}
#         elif isinstance(obj, list):
#             return [convert(i) for i in obj]
#         else:
#             return obj
#     return convert(doc)

# @router.get('/')
# async def get_progress(user=Depends(get_current_user)):
#     email = user['email']
#     results = list(db['exercise_results'].find({'user_email': email}))
#     results = [serialize_doc(r) for r in results]

#     total = len(results)
#     avg_score = sum(r.get('evaluation', {}).get('score', 0) for r in results)/total if total > 0 else None

#     learning_path = predict_learning_path(results, user.get('level', 'beginner'))

#     return {
#         'count': total,
#         'avg_score': avg_score,
#         'recent': results[-10:],
#         'personalized_path': learning_path
#     }



from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
from app.db import db
from bson import ObjectId
from app.services.student_metrics import get_user_metrics
import io
import csv

router = APIRouter()

def serialize_doc(doc: dict) -> dict:
    if not doc:
        return {}
    
    def convert(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        else:
            return obj
    return convert(doc)

@router.get('/')
async def get_progress(user=Depends(get_current_user)):
    """
    Get user's progress including metrics and ML model predictions.
    """
    email = user['email']
    
    # Get student metrics and ML prediction
    user_metrics_data = get_user_metrics(email)
    
    # Get recent quiz attempts (last 20)
    recent_attempts = list(db['quiz_attempts'].find({'user_email': email}).sort('submitted_at', -1).limit(20))
    recent_attempts = [serialize_doc(a) for a in recent_attempts]
    
    # Calculate overall statistics
    all_attempts = list(db['quiz_attempts'].find({'user_email': email}))
    
    lessons_stats = {}
    for attempt in all_attempts:
        lesson = attempt['lesson_slug']
        if lesson not in lessons_stats:
            lessons_stats[lesson] = {
                'lesson_slug': lesson,
                'attempts': 0,
                'total_score': 0,
                'best_score': 0
            }
        
        lessons_stats[lesson]['attempts'] += 1
        lessons_stats[lesson]['total_score'] += attempt.get('quiz_score', 0)
        lessons_stats[lesson]['best_score'] = max(
            lessons_stats[lesson]['best_score'],
            attempt.get('quiz_score', 0)
        )
    
    # Calculate averages
    for stats in lessons_stats.values():
        if stats['attempts'] > 0:
            stats['average_score'] = round(stats['total_score'] / stats['attempts'], 2)
    
    return {
        'count': len(all_attempts),
        'metrics': user_metrics_data['metrics'],
        'predicted_level': user_metrics_data['predicted_level'],
        'confidence': user_metrics_data['confidence'],
        'difficulty_adjustment': user_metrics_data['difficulty_adjustment'],
        'recommended_lessons': user_metrics_data['recommended_lessons'],
        'lessons_stats': list(lessons_stats.values()),
        'recent_attempts': recent_attempts
    }


@router.get('/export')
async def export_progress(format: str = 'json', user=Depends(get_current_user)):
    """
    Export user's progress as JSON or CSV.
    Query param: ?format=csv or ?format=json
    """
    email = user['email']
    
    # Get all attempts
    all_attempts = list(db['quiz_attempts'].find({'user_email': email}))
    all_attempts = [serialize_doc(a) for a in all_attempts]
    
    if format.lower() == 'csv':
        # Create CSV output
        output = io.StringIO()
        fieldnames = [
            'lesson_slug',
            'quiz_type',
            'quiz_score',
            'score_earned',
            'total_marks',
            'submitted_at'
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for attempt in all_attempts:
            row = {
                'lesson_slug': attempt.get('lesson_slug', ''),
                'quiz_type': attempt.get('quiz_type', ''),
                'quiz_score': attempt.get('quiz_score', 0),
                'score_earned': attempt.get('score_earned', 0),
                'total_marks': attempt.get('total_marks', 0),
                'submitted_at': attempt.get('submitted_at', '')
            }
            writer.writerow(row)
        
        return {
            'format': 'csv',
            'filename': f"progress_{email.replace('@', '_')}.csv",
            'data': output.getvalue()
        }
    
    else:
        # Return JSON
        return {
            'format': 'json',
            'email': email,
            'total_attempts': len(all_attempts),
            'attempts': all_attempts
        }
