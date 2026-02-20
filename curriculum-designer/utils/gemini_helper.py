import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

def generate_content(prompt, max_retries=3):
    """Generate content using Gemini AI with retry logic"""
    
    if not st.session_state.model:
        st.error("Gemini model not initialized. Please check your API key.")
        return None
    
    for attempt in range(max_retries):
        try:
            with st.spinner(f"Generating content... (Attempt {attempt + 1}/{max_retries})"):
                response = st.session_state.model.generate_content(prompt)
                
                if response and response.text:
                    # Save to session state
                    content_id = f"Content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    st.session_state.generated_content[content_id] = {
                        'content': response.text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt
                    }
                    return response.text
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                st.error(f"Failed to generate content after {max_retries} attempts: {str(e)}")
                return None
    
    return None

def format_course_outline(course_data):
    """Format course outline data for prompt"""
    return f"""
    Create a comprehensive course outline with the following specifications:
    
    Course Title: {course_data['title']}
    Subject Area: {course_data['subject']}
    Target Audience: {course_data['audience']}
    Duration: {course_data['duration']} {course_data['duration_unit']}
    Level: {course_data['level']}
    
    Additional Requirements:
    - {course_data.get('additional_reqs', 'None specified')}
    
    Please include:
    1. Course description and learning objectives
    2. Prerequisites
    3. Module/Week-by-week breakdown
    4. Key topics for each module
    5. Learning activities and resources
    6. Assessment methods
    """

def format_lesson_plan(lesson_data):
    """Format lesson plan data for prompt"""
    return f"""
    Create a detailed lesson plan with the following specifications:
    
    Lesson Title: {lesson_data['title']}
    Course: {lesson_data['course']}
    Duration: {lesson_data['duration']} minutes
    Class Size: {lesson_data['class_size']} students
    
    Learning Objectives:
    {lesson_data['objectives']}
    
    Materials Needed:
    {lesson_data.get('materials', 'Standard classroom materials')}
    
    Prior Knowledge Required:
    {lesson_data.get('prerequisites', 'None specified')}
    
    Please structure the lesson plan with:
    1. Opening/Hook activity (5-10 minutes)
    2. Direct instruction/Content delivery (15-20 minutes)
    3. Guided practice activities (15-20 minutes)
    4. Independent practice (10-15 minutes)
    5. Closing/Assessment (5-10 minutes)
    6. Differentiation strategies for diverse learners
    7. Extension activities for early finishers
    """

def format_assessment(assessment_data):
    """Format assessment data for prompt"""
    return f"""
    Create a comprehensive assessment with the following specifications:
    
    Assessment Type: {assessment_data['type']}
    Subject/Topic: {assessment_data['topic']}
    Grade Level: {assessment_data['grade_level']}
    Number of Questions: {assessment_data['num_questions']}
    Difficulty Level: {assessment_data['difficulty']}
    
    Learning Objectives Tested:
    {assessment_data['objectives']}
    
    Additional Requirements:
    - {assessment_data.get('requirements', 'Standard assessment format')}
    
    Please include:
    1. Clear instructions for students
    2. Mix of question types (multiple choice, short answer, etc.)
    3. Point values for each question
    4. Answer key with explanations
    5. Scoring rubric where applicable
    6. Estimated completion time
    """