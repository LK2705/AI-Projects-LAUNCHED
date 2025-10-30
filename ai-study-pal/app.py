from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Simple study plans database
study_plans = {
    'math': [
        "Review basic formulas and concepts",
        "Practice with sample problems", 
        "Work on word problems",
        "Take a practice test"
    ],
    'science': [
        "Read the chapter summary",
        "Review key terms and definitions",
        "Conduct a simple experiment",
        "Create concept maps"
    ],
    'history': [
        "Create a timeline of events",
        "Study key figures and their roles",
        "Review cause and effect relationships",
        "Write a short summary"
    ]
}

# Quiz questions database
quiz_questions = {
    'math': {
        'easy': [
            {"question": "What is 5 + 7?", "options": ["11", "12", "13", "14"], "answer": "12"},
            {"question": "What is 9 × 6?", "options": ["54", "56", "58", "60"], "answer": "54"}
        ],
        'medium': [
            {"question": "Solve for x: 2x + 5 = 15", "options": ["5", "10", "7.5", "8"], "answer": "5"},
            {"question": "What is the area of a circle with radius 3?", "options": ["9π", "6π", "3π", "12π"], "answer": "9π"}
        ]
    },
    'science': {
        'easy': [
            {"question": "What planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
            {"question": "What is H2O?", "options": ["Oxygen", "Hydrogen", "Water", "Carbon dioxide"], "answer": "Water"}
        ],
        'medium': [
            {"question": "What is the chemical symbol for gold?", "options": ["Go", "Gd", "Au", "Ag"], "answer": "Au"},
            {"question": "What gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "answer": "Carbon dioxide"}
        ]
    }
}

# Motivational messages
motivational_quotes = [
    "Great job on your studies! Keep up the good work!",
    "You're making excellent progress!",
    "Every minute you study brings you closer to your goals!",
    "Your hard work is paying off!",
    "Stay curious and keep learning!"
]

# Study tips
study_tips = [
    "Break your study time into 25-minute chunks with 5-minute breaks",
    "Review your notes within 24 hours of learning new material",
    "Teach what you've learned to someone else",
    "Create flashcards for key concepts",
    "Find a quiet, dedicated study space"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    try:
        data = request.json
        subject = data.get('subject', '').lower()
        hours = float(data.get('hours', 1))
        
        # Generate study plan
        if subject in study_plans:
            base_plan = study_plans[subject]
        else:
            base_plan = [
                "Review key concepts",
                "Practice with examples", 
                "Test your understanding",
                "Review and summarize"
            ]
        
        # Distribute time across activities
        time_per_activity = (hours * 60) / len(base_plan)  # Convert to minutes
        detailed_plan = []
        
        for i, activity in enumerate(base_plan):
            detailed_plan.append({
                'time': f"{int(time_per_activity)} mins",
                'activity': activity
            })
        
        # Generate quiz
        quiz = []
        if subject in quiz_questions:
            difficulty = 'easy' if hours <= 2 else 'medium'
            quiz = random.sample(quiz_questions[subject][difficulty], 
                                min(3, len(quiz_questions[subject][difficulty])))
        
        # Generate summary (simplified)
        summary = f"Your {hours}-hour study plan for {subject.capitalize()} focuses on key concepts and practice exercises."
        
        # Get random motivational message and tips
        motivation = random.choice(motivational_quotes)
        tips = random.sample(study_tips, 2)
        
        response = {
            'success': True,
            'plan': detailed_plan,
            'quiz': quiz,
            'summary': summary,
            'motivation': motivation,
            'tips': tips,
            'subject': subject.capitalize(),
            'total_hours': hours
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download_schedule', methods=['POST'])
def download_schedule():
    data = request.json
    plan = data.get('plan', [])
    subject = data.get('subject', 'Study')
    
    # Create CSV content
    csv_content = "Time,Activity\n"
    for item in plan:
        csv_content += f"{item['time']},{item['activity']}\n"
    
    return jsonify({
        'csv_content': csv_content,
        'filename': f"{subject}_Study_Plan.csv"
    })

if __name__ == '__main__':
    app.run(debug=True)