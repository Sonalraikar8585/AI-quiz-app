from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import after app creation
from models import db, User, Subject, Chapter, Quiz, Question, Score
from utils.ai_generator import generate_mcq_questions
from utils.charts import generate_performance_data

# Initialize database
db.init_app(app)

# Create tables and admin user
with app.app_context():
    db.create_all()
    # Create admin if not exists
    admin = User.query.filter_by(username='admin@quiz.com').first()
    if not admin:
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin@quiz.com',
            password=generate_password_hash('admin123'),
            full_name='Quiz Master',
            qualification='Administrator',
            date_of_birth=datetime(1990, 1, 1).date(),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@quiz.com / admin123")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Access denied. Admin only.', 'danger')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        from werkzeug.security import check_password_hash
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            if user.is_admin:
                flash('Welcome Admin!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash(f'Welcome {user.full_name}!', 'success')
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob = request.form.get('date_of_birth')
        
        if User.query.filter_by(username=username).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        from werkzeug.security import generate_password_hash
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            full_name=full_name,
            qualification=qualification,
            date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date(),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

# Admin Routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    users = User.query.filter_by(is_admin=False).all()
    subjects = Subject.query.all()
    quizzes = Quiz.query.all()
    total_attempts = Score.query.count()
    
    return render_template('admin_dashboard.html', 
                         users=users, 
                         subjects=subjects,
                         quizzes=quizzes,
                         total_attempts=total_attempts)

# Subject Management
@app.route('/admin/subjects')
@admin_required
def manage_subjects():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

@app.route('/admin/subject/add', methods=['GET', 'POST'])
@admin_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully', 'success')
        return redirect(url_for('manage_subjects'))
    
    return render_template('add_subject.html')

@app.route('/admin/subject/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    
    if request.method == 'POST':
        subject.name = request.form.get('name')
        subject.description = request.form.get('description')
        db.session.commit()
        
        flash('Subject updated successfully', 'success')
        return redirect(url_for('manage_subjects'))
    
    return render_template('edit_subject.html', subject=subject)

@app.route('/admin/subject/delete/<int:id>')
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    
    flash('Subject deleted successfully', 'success')
    return redirect(url_for('manage_subjects'))

# Chapter Management
@app.route('/admin/chapters')
@admin_required
def manage_chapters():
    chapters = Chapter.query.all()
    return render_template('chapters.html', chapters=chapters)

@app.route('/admin/chapter/add', methods=['GET', 'POST'])
@admin_required
def add_chapter():
    subjects = Subject.query.all()
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        name = request.form.get('name')
        description = request.form.get('description')
        
        chapter = Chapter(subject_id=subject_id, name=name, description=description)
        db.session.add(chapter)
        db.session.commit()
        
        flash('Chapter added successfully', 'success')
        return redirect(url_for('manage_chapters'))
    
    return render_template('add_chapter.html', subjects=subjects)

@app.route('/admin/chapter/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    subjects = Subject.query.all()
    
    if request.method == 'POST':
        chapter.subject_id = request.form.get('subject_id')
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        db.session.commit()
        
        flash('Chapter updated successfully', 'success')
        return redirect(url_for('manage_chapters'))
    
    return render_template('edit_chapter.html', chapter=chapter, subjects=subjects)

@app.route('/admin/chapter/delete/<int:id>')
@admin_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter)
    db.session.commit()
    
    flash('Chapter deleted successfully', 'success')
    return redirect(url_for('manage_chapters'))

# Quiz Management
@app.route('/admin/quizzes')
@admin_required
def manage_quizzes():
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)

@app.route('/admin/quiz/add', methods=['GET', 'POST'])
@admin_required
def add_quiz():
    chapters = Chapter.query.all()
    
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id')
        date_of_quiz = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        
        quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d').date(),
            time_duration=time_duration,
            remarks=remarks
        )
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz created successfully', 'success')
        return redirect(url_for('manage_questions', quiz_id=quiz.id))
    
    return render_template('add_quiz.html', chapters=chapters)

@app.route('/admin/quiz/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    chapters = Chapter.query.all()
    
    if request.method == 'POST':
        quiz.chapter_id = request.form.get('chapter_id')
        quiz.date_of_quiz = datetime.strptime(request.form.get('date_of_quiz'), '%Y-%m-%d').date()
        quiz.time_duration = request.form.get('time_duration')
        quiz.remarks = request.form.get('remarks')
        db.session.commit()
        
        flash('Quiz updated successfully', 'success')
        return redirect(url_for('manage_quizzes'))
    
    return render_template('edit_quiz.html', quiz=quiz, chapters=chapters)

@app.route('/admin/quiz/delete/<int:id>')
@admin_required
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    
    flash('Quiz deleted successfully', 'success')
    return redirect(url_for('manage_quizzes'))

# Question Management
@app.route('/admin/quiz/<int:quiz_id>/questions')
@admin_required
def manage_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('questions.html', quiz=quiz, questions=questions)

@app.route('/admin/quiz/<int:quiz_id>/question/add', methods=['GET', 'POST'])
@admin_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        question = Question(
            quiz_id=quiz_id,
            question_statement=request.form.get('question_statement'),
            option1=request.form.get('option1'),
            option2=request.form.get('option2'),
            option3=request.form.get('option3'),
            option4=request.form.get('option4'),
            correct_option=int(request.form.get('correct_option'))
        )
        db.session.add(question)
        db.session.commit()
        
        flash('Question added successfully', 'success')
        return redirect(url_for('manage_questions', quiz_id=quiz_id))
    
    return render_template('add_question.html', quiz=quiz)

@app.route('/admin/question/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    
    if request.method == 'POST':
        question.question_statement = request.form.get('question_statement')
        question.option1 = request.form.get('option1')
        question.option2 = request.form.get('option2')
        question.option3 = request.form.get('option3')
        question.option4 = request.form.get('option4')
        question.correct_option = int(request.form.get('correct_option'))
        db.session.commit()
        
        flash('Question updated successfully', 'success')
        return redirect(url_for('manage_questions', quiz_id=question.quiz_id))
    
    return render_template('edit_question.html', question=question)

@app.route('/admin/question/delete/<int:id>')
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    
    flash('Question deleted successfully', 'success')
    return redirect(url_for('manage_questions', quiz_id=quiz_id))

# AI Question Generation
@app.route('/admin/quiz/<int:quiz_id>/generate-ai', methods=['GET', 'POST'])
@admin_required
def generate_ai_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        num_questions = int(request.form.get('num_questions', 5))
        keywords = request.form.get('keywords', quiz.chapter.name)
        
        questions = generate_mcq_questions(keywords, num_questions)
        
        for q in questions:
            question = Question(
                quiz_id=quiz_id,
                question_statement=q['question'],
                option1=q['options'][0],
                option2=q['options'][1],
                option3=q['options'][2],
                option4=q['options'][3],
                correct_option=q['correct']
            )
            db.session.add(question)
        
        db.session.commit()
        flash(f'{num_questions} AI-generated questions added successfully', 'success')
        return redirect(url_for('manage_questions', quiz_id=quiz_id))
    
    return render_template('generate_ai_questions.html', quiz=quiz)

# User Routes
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    user = User.query.get(session['user_id'])
    subjects = Subject.query.all()
    recent_scores = Score.query.filter_by(user_id=user.id).order_by(Score.timestamp_of_attempt.desc()).limit(5).all()
    
    return render_template('user_dashboard.html', 
                         user=user, 
                         subjects=subjects,
                         recent_scores=recent_scores)

@app.route('/user/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('view_subject.html', subject=subject, chapters=chapters)

@app.route('/user/chapter/<int:chapter_id>')
@login_required
def view_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('view_chapter.html', chapter=chapter, quizzes=quizzes)

@app.route('/user/quiz/<int:quiz_id>/start')
@login_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if not questions:
        flash('This quiz has no questions yet', 'warning')
        return redirect(url_for('view_chapter', chapter_id=quiz.chapter_id))
    
    return render_template('take_quiz.html', quiz=quiz, questions=questions)

@app.route('/user/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    total_questions = len(questions)
    correct_answers = 0
    
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and int(user_answer) == question.correct_option:
            correct_answers += 1
    
    total_score = correct_answers
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    score = Score(
        quiz_id=quiz_id,
        user_id=session['user_id'],
        timestamp_of_attempt=datetime.now(),
        total_score=total_score,
        accuracy_percentage=accuracy
    )
    db.session.add(score)
    db.session.commit()
    
    flash(f'Quiz submitted! Score: {total_score}/{total_questions} ({accuracy:.2f}%)', 'success')
    return redirect(url_for('view_result', score_id=score.id))

@app.route('/user/result/<int:score_id>')
@login_required
def view_result(score_id):
    score = Score.query.get_or_404(score_id)
    
    if score.user_id != session['user_id']:
        flash('Access denied', 'danger')
        return redirect(url_for('user_dashboard'))
    
    return render_template('result.html', score=score)

@app.route('/user/performance')
@login_required
def performance_analysis():
    user_id = session['user_id']
    scores = Score.query.filter_by(user_id=user_id).all()
    
    performance_data = generate_performance_data(user_id)
    
    return render_template('performance.html', 
                         scores=scores,
                         performance_data=performance_data)

# API Routes
@app.route('/api/subjects', methods=['GET'])
def api_subjects():
    subjects = Subject.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description
    } for s in subjects])

@app.route('/api/user/<int:user_id>/performance', methods=['GET'])
@login_required
def api_user_performance(user_id):
    if session['user_id'] != user_id and not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    performance_data = generate_performance_data(user_id)
    return jsonify(performance_data)

if __name__ == '__main__':
    app.run(debug=True)