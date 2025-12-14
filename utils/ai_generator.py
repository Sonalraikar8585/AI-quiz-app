import random

# Question templates and patterns for AI generation
QUESTION_TEMPLATES = {
    'definition': [
        "What is {keyword}?",
        "Define {keyword}.",
        "Which of the following best describes {keyword}?",
        "{keyword} is defined as:"
    ],
    'function': [
        "What is the primary function of {keyword}?",
        "Which function is performed by {keyword}?",
        "The main purpose of {keyword} is to:",
        "What does {keyword} do?"
    ],
    'comparison': [
        "What is the difference between {keyword1} and {keyword2}?",
        "Which statement correctly compares {keyword1} and {keyword2}?",
        "How does {keyword1} differ from {keyword2}?",
        "{keyword1} is different from {keyword2} in that:"
    ],
    'application': [
        "In which scenario would you use {keyword}?",
        "Which application best demonstrates {keyword}?",
        "An example of {keyword} in practice is:",
        "Where is {keyword} commonly applied?"
    ],
    'characteristic': [
        "Which characteristic is true for {keyword}?",
        "What property does {keyword} have?",
        "{keyword} is characterized by:",
        "A key feature of {keyword} is:"
    ]
}

# Sample knowledge base (can be expanded)
KNOWLEDGE_BASE = {
    'python': {
        'definitions': ['A high-level programming language', 'An interpreted language', 'A general-purpose language'],
        'characteristics': ['Dynamic typing', 'Object-oriented', 'Easy to learn', 'Extensive libraries'],
        'applications': ['Web development', 'Data science', 'Machine learning', 'Automation']
    },
    'database': {
        'definitions': ['A structured collection of data', 'An organized data storage system', 'A data management system'],
        'characteristics': ['ACID properties', 'Data integrity', 'Concurrent access', 'Query support'],
        'applications': ['Data storage', 'Transaction processing', 'Data analysis', 'Record keeping']
    },
    'algorithm': {
        'definitions': ['A step-by-step procedure', 'A problem-solving method', 'A computational process'],
        'characteristics': ['Well-defined steps', 'Finite execution', 'Input and output', 'Effectiveness'],
        'applications': ['Sorting data', 'Searching information', 'Optimization', 'Problem solving']
    },
    'html': {
        'definitions': ['HyperText Markup Language', 'A markup language for web pages', 'Standard web content structure'],
        'characteristics': ['Tag-based', 'Platform independent', 'Case insensitive', 'Structured format'],
        'applications': ['Creating web pages', 'Structuring content', 'Building websites', 'Web development']
    },
    'css': {
        'definitions': ['Cascading Style Sheets', 'A stylesheet language', 'Web design language'],
        'characteristics': ['Separation of content and design', 'Cascading rules', 'Selector-based', 'Responsive design'],
        'applications': ['Styling web pages', 'Layout design', 'Responsive websites', 'Visual presentation']
    }
}

def generate_mcq_questions(keywords, num_questions=5):
    """
    Generate MCQ questions based on keywords using rule-based AI logic
    
    Args:
        keywords: String of comma-separated keywords or chapter name
        num_questions: Number of questions to generate
    
    Returns:
        List of dictionaries containing question data
    """
    questions = []
    keyword_list = [k.strip().lower() for k in keywords.split(',')]
    
    # If keywords not in knowledge base, use generic generation
    if not any(kw in KNOWLEDGE_BASE for kw in keyword_list):
        keyword_list = ['python', 'database', 'algorithm', 'html', 'css']
    
    for i in range(num_questions):
        # Select random keyword from list
        keyword = random.choice([k for k in keyword_list if k in KNOWLEDGE_BASE] or list(KNOWLEDGE_BASE.keys()))
        
        # Select question type
        question_type = random.choice(list(QUESTION_TEMPLATES.keys()))
        
        # Generate question based on type
        question_data = None
        
        if question_type == 'definition':
            question_data = generate_definition_question(keyword)
        elif question_type == 'characteristic':
            question_data = generate_characteristic_question(keyword)
        elif question_type == 'application':
            question_data = generate_application_question(keyword)
        elif question_type == 'function':
            question_data = generate_function_question(keyword)
        else:
            question_data = generate_definition_question(keyword)
        
        if question_data:
            questions.append(question_data)
    
    return questions

def generate_definition_question(keyword):
    """Generate a definition-based question"""
    kb = KNOWLEDGE_BASE.get(keyword, KNOWLEDGE_BASE['python'])
    
    template = random.choice(QUESTION_TEMPLATES['definition'])
    question = template.format(keyword=keyword.capitalize())
    
    correct_answer = random.choice(kb['definitions'])
    
    # Generate distractors
    all_definitions = []
    for k, v in KNOWLEDGE_BASE.items():
        if k != keyword:
            all_definitions.extend(v['definitions'])
    
    distractors = random.sample(all_definitions, min(3, len(all_definitions)))
    
    # Create options
    options = [correct_answer] + distractors[:3]
    random.shuffle(options)
    
    correct_option = options.index(correct_answer) + 1
    
    return {
        'question': question,
        'options': options,
        'correct': correct_option
    }

def generate_characteristic_question(keyword):
    """Generate a characteristic-based question"""
    kb = KNOWLEDGE_BASE.get(keyword, KNOWLEDGE_BASE['python'])
    
    template = random.choice(QUESTION_TEMPLATES['characteristic'])
    question = template.format(keyword=keyword.capitalize())
    
    correct_answer = random.choice(kb['characteristics'])
    
    # Generate distractors
    all_characteristics = []
    for k, v in KNOWLEDGE_BASE.items():
        if k != keyword:
            all_characteristics.extend(v['characteristics'])
    
    distractors = random.sample(all_characteristics, min(3, len(all_characteristics)))
    
    # Create options
    options = [correct_answer] + distractors[:3]
    random.shuffle(options)
    
    correct_option = options.index(correct_answer) + 1
    
    return {
        'question': question,
        'options': options,
        'correct': correct_option
    }

def generate_application_question(keyword):
    """Generate an application-based question"""
    kb = KNOWLEDGE_BASE.get(keyword, KNOWLEDGE_BASE['python'])
    
    template = random.choice(QUESTION_TEMPLATES['application'])
    question = template.format(keyword=keyword.capitalize())
    
    correct_answer = random.choice(kb['applications'])
    
    # Generate distractors
    all_applications = []
    for k, v in KNOWLEDGE_BASE.items():
        if k != keyword:
            all_applications.extend(v['applications'])
    
    distractors = random.sample(all_applications, min(3, len(all_applications)))
    
    # Create options
    options = [correct_answer] + distractors[:3]
    random.shuffle(options)
    
    correct_option = options.index(correct_answer) + 1
    
    return {
        'question': question,
        'options': options,
        'correct': correct_option
    }

def generate_function_question(keyword):
    """Generate a function-based question"""
    kb = KNOWLEDGE_BASE.get(keyword, KNOWLEDGE_BASE['python'])
    
    template = random.choice(QUESTION_TEMPLATES['function'])
    question = template.format(keyword=keyword.capitalize())
    
    # Use application as function description
    correct_answer = random.choice(kb['applications'])
    
    # Generate distractors
    all_apps = []
    for k, v in KNOWLEDGE_BASE.items():
        if k != keyword:
            all_apps.extend(v['applications'])
    
    distractors = random.sample(all_apps, min(3, len(all_apps)))
    
    # Create options
    options = [correct_answer] + distractors[:3]
    random.shuffle(options)
    
    correct_option = options.index(correct_answer) + 1
    
    return {
        'question': question,
        'options': options,
        'correct': correct_option
    }