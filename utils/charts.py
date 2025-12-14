from models import Score, Quiz, Chapter, Subject
from sqlalchemy import func
from collections import defaultdict

def generate_performance_data(user_id):
    """
    Generate comprehensive performance analytics data for a user
    
    Args:
        user_id: ID of the user
    
    Returns:
        Dictionary containing various performance metrics
    """
    scores = Score.query.filter_by(user_id=user_id).all()
    
    if not scores:
        return {
            'overall_accuracy': 0,
            'total_quizzes': 0,
            'total_score': 0,
            'accuracy_trend': [],
            'subject_performance': [],
            'chapter_performance': [],
            'recent_attempts': []
        }
    
    # Calculate overall metrics
    total_quizzes = len(scores)
    total_accuracy = sum(s.accuracy_percentage for s in scores)
    overall_accuracy = total_accuracy / total_quizzes if total_quizzes > 0 else 0
    total_score = sum(s.total_score for s in scores)
    
    # Accuracy trend over time
    accuracy_trend = []
    for score in sorted(scores, key=lambda x: x.timestamp_of_attempt):
        accuracy_trend.append({
            'date': score.timestamp_of_attempt.strftime('%Y-%m-%d'),
            'accuracy': round(score.accuracy_percentage, 2),
            'score': score.total_score
        })
    
    # Subject-wise performance
    subject_scores = defaultdict(lambda: {'total_accuracy': 0, 'count': 0, 'total_score': 0})
    
    for score in scores:
        subject = score.quiz.chapter.subject
        subject_scores[subject.name]['total_accuracy'] += score.accuracy_percentage
        subject_scores[subject.name]['count'] += 1
        subject_scores[subject.name]['total_score'] += score.total_score
    
    subject_performance = []
    for subject_name, data in subject_scores.items():
        avg_accuracy = data['total_accuracy'] / data['count'] if data['count'] > 0 else 0
        subject_performance.append({
            'subject': subject_name,
            'average_accuracy': round(avg_accuracy, 2),
            'total_score': data['total_score'],
            'attempts': data['count']
        })
    
    # Sort by accuracy
    subject_performance.sort(key=lambda x: x['average_accuracy'], reverse=True)
    
    # Chapter-wise performance
    chapter_scores = defaultdict(lambda: {'total_accuracy': 0, 'count': 0, 'total_score': 0})
    
    for score in scores:
        chapter = score.quiz.chapter
        chapter_scores[chapter.name]['total_accuracy'] += score.accuracy_percentage
        chapter_scores[chapter.name]['count'] += 1
        chapter_scores[chapter.name]['total_score'] += score.total_score
    
    chapter_performance = []
    for chapter_name, data in chapter_scores.items():
        avg_accuracy = data['total_accuracy'] / data['count'] if data['count'] > 0 else 0
        chapter_performance.append({
            'chapter': chapter_name,
            'average_accuracy': round(avg_accuracy, 2),
            'total_score': data['total_score'],
            'attempts': data['count']
        })
    
    # Sort by accuracy
    chapter_performance.sort(key=lambda x: x['average_accuracy'], reverse=True)
    
    # Identify strengths and weaknesses
    strengths = [ch for ch in chapter_performance if ch['average_accuracy'] >= 75][:3]
    weaknesses = [ch for ch in chapter_performance if ch['average_accuracy'] < 60][:3]
    
    # Recent attempts (last 10)
    recent_attempts = []
    for score in sorted(scores, key=lambda x: x.timestamp_of_attempt, reverse=True)[:10]:
        recent_attempts.append({
            'quiz_id': score.quiz_id,
            'subject': score.quiz.chapter.subject.name,
            'chapter': score.quiz.chapter.name,
            'date': score.timestamp_of_attempt.strftime('%Y-%m-%d %H:%M'),
            'score': score.total_score,
            'accuracy': round(score.accuracy_percentage, 2)
        })
    
    return {
        'overall_accuracy': round(overall_accuracy, 2),
        'total_quizzes': total_quizzes,
        'total_score': total_score,
        'accuracy_trend': accuracy_trend,
        'subject_performance': subject_performance,
        'chapter_performance': chapter_performance,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'recent_attempts': recent_attempts
    }

def get_admin_analytics():
    """
    Generate analytics for admin dashboard
    
    Returns:
        Dictionary containing platform-wide statistics
    """
    from models import User, Subject, Chapter, Quiz, Question, Score
    
    total_users = User.query.filter_by(is_admin=False).count()
    total_subjects = Subject.query.count()
    total_chapters = Chapter.query.count()
    total_quizzes = Quiz.query.count()
    total_questions = Question.query.count()
    total_attempts = Score.query.count()
    
    # Average platform accuracy
    avg_accuracy = Score.query.with_entities(
        func.avg(Score.accuracy_percentage)
    ).scalar() or 0
    
    # Most popular subjects (by quiz attempts)
    popular_subjects = []
    subjects = Subject.query.all()
    
    for subject in subjects:
        attempts = 0
        for chapter in subject.chapters:
            for quiz in chapter.quizzes:
                attempts += len(quiz.scores)
        
        if attempts > 0:
            popular_subjects.append({
                'name': subject.name,
                'attempts': attempts
            })
    
    popular_subjects.sort(key=lambda x: x['attempts'], reverse=True)
    
    # Recent activity
    recent_scores = Score.query.order_by(Score.timestamp_of_attempt.desc()).limit(10).all()
    recent_activity = []
    
    for score in recent_scores:
        recent_activity.append({
            'user': score.user.full_name,
            'quiz': f"{score.quiz.chapter.subject.name} - {score.quiz.chapter.name}",
            'score': score.total_score,
            'accuracy': round(score.accuracy_percentage, 2),
            'date': score.timestamp_of_attempt.strftime('%Y-%m-%d %H:%M')
        })
    
    return {
        'total_users': total_users,
        'total_subjects': total_subjects,
        'total_chapters': total_chapters,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'average_accuracy': round(avg_accuracy, 2),
        'popular_subjects': popular_subjects[:5],
        'recent_activity': recent_activity
    }