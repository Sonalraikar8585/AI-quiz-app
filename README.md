# AI Quiz Generator & Performance Analyzer

A comprehensive web application for generating AI-powered quizzes and analyzing student performance.

## Features

### Admin Features
- **User Management**: View and manage registered users
- **Subject Management**: Create, edit, and delete subjects
- **Chapter Management**: Organize chapters under subjects
- **Quiz Management**: Create quizzes with customizable settings
- **Question Management**: Add questions manually or generate using AI
- **AI Question Generator**: Automatically generate MCQ questions based on keywords
- **Analytics Dashboard**: View platform-wide statistics

### User Features
- **User Registration & Login**: Secure authentication system
- **Browse Subjects & Chapters**: Explore available learning materials
- **Take Quizzes**: Attempt quizzes with timer functionality
- **View Results**: Instant feedback with detailed scoring
- **Performance Analytics**: 
  - Overall accuracy tracking
  - Subject-wise performance
  - Chapter-wise strength/weakness analysis
  - Interactive charts and graphs
  - Recent attempts history

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite
- **Templating**: Jinja2
- **Charts**: Chart.js
- **Icons**: Font Awesome

## Project Structure

```
ai_quiz_app/
│
├── app.py                  # Main application file
├── models.py               # Database models
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── database.db            # SQLite database (auto-generated)
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── user_dashboard.html
│   ├── subjects.html
│   ├── add_subject.html
│   ├── edit_subject.html
│   ├── chapters.html
│   ├── add_chapter.html
│   ├── edit_chapter.html
│   ├── quizzes.html
│   ├── add_quiz.html
│   ├── edit_quiz.html
│   ├── questions.html
│   ├── add_question.html
│   ├── edit_question.html
│   ├── generate_ai_questions.html
│   ├── view_subject.html
│   ├── view_chapter.html
│   ├── take_quiz.html
│   ├── result.html
│   └── performance.html
│
├── utils/                 # Utility modules
│   ├── ai_generator.py    # AI question generation logic
│   └── charts.py          # Performance analytics functions
│
└── static/               # Static files (CSS, JS, images)
    ├── css/
    └── js/
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
# If you have git installed
git clone <repository-url>
cd ai_quiz_app

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

## Default Credentials

### Admin Account
- **Email**: admin@quiz.com
- **Password**: admin123

### User Account
- Register a new account through the registration page

## Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Create Subjects**: Navigate to Subjects → Add New Subject
3. **Create Chapters**: Navigate to Chapters → Add New Chapter
4. **Create Quizzes**: Navigate to Quizzes → Create New Quiz
5. **Add Questions**: 
   - Manually: Add questions one by one
   - AI Generation: Use the AI generator to create multiple questions automatically
6. **View Analytics**: Check the dashboard for platform statistics

### For Users

1. **Register** a new account
2. **Login** with your credentials
3. **Browse Subjects**: Select a subject from the dashboard
4. **Choose Chapter**: Select a chapter to view available quizzes
5. **Take Quiz**: Start a quiz and answer all questions
6. **Submit**: Submit your answers when done
7. **View Results**: Check your score and accuracy
8. **Analyze Performance**: Navigate to Performance to see detailed analytics

## AI Question Generation

The AI question generator uses rule-based logic to create MCQ questions. It includes:

- Pre-defined question templates
- Knowledge base for multiple topics (Python, Database, Algorithm, HTML, CSS)
- Multiple question types (Definition, Characteristics, Application, Function)
- Automatic distractor generation
- Configurable number of questions (1-20)

## Database Schema

### Tables
1. **users**: User information and credentials
2. **subjects**: Academic subjects
3. **chapters**: Sub-topics under subjects
4. **quizzes**: Quiz metadata
5. **questions**: MCQ questions with 4 options
6. **scores**: Quiz attempt records and scores

## Performance Analytics Features

- **Overall Accuracy**: Average performance across all quizzes
- **Accuracy Trend**: Line chart showing improvement over time
- **Subject Performance**: Bar chart comparing performance by subject
- **Strengths**: Top 3 chapters with highest accuracy
- **Weaknesses**: Chapters needing improvement
- **Recent Attempts**: History of last 10 quiz attempts

## Customization

### Adding More AI Knowledge
Edit `utils/ai_generator.py` and add new topics to the `KNOWLEDGE_BASE` dictionary:

```python
KNOWLEDGE_BASE = {
    'your_topic': {
        'definitions': [...],
        'characteristics': [...],
        'applications': [...]
    }
}
```

### Changing Theme Colors
Edit the CSS variables in `templates/base.html`:

```css
:root {
    --primary-color: #4361ee;
    --secondary-color: #3f37c9;
    /* Add more custom colors */
}
```

## Troubleshooting

### Database Not Found Error
The database is created automatically on first run. If you see errors, delete `database.db` and restart the application.

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change 5001 to any available port
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Project Evaluation Points

✅ Complete CRUD operations for all entities  
✅ Role-based access control (Admin/User)  
✅ AI-powered question generation  
✅ Performance analytics with charts  
✅ Responsive UI with Bootstrap  
✅ Form validation (Frontend & Backend)  
✅ Timer-based quiz functionality  
✅ RESTful API endpoints  
✅ Programmatic database creation  
✅ No external database required (SQLite)

## API Endpoints

### Public Endpoints
- `GET /`: Home page (redirects based on login status)
- `GET /login`: Login page
- `POST /login`: Process login
- `GET /register`: Registration page
- `POST /register`: Process registration

### Admin Endpoints
- `GET /admin/dashboard`: Admin dashboard
- `GET /admin/subjects`: Manage subjects
- `POST /admin/subject/add`: Add new subject
- `GET /admin/quiz/<id>/generate-ai`: AI question generation

### User Endpoints
- `GET /user/dashboard`: User dashboard
- `GET /user/quiz/<id>/start`: Start quiz
- `POST /user/quiz/<id>/submit`: Submit quiz
- `GET /user/performance`: Performance analytics

### API Endpoints (JSON)
- `GET /api/subjects`: Get all subjects
- `GET /api/user/<id>/performance`: Get user performance data

