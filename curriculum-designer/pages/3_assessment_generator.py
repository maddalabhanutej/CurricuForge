import streamlit as st
from utils.gemini_helper import generate_content, format_assessment
from utils.prompts import ASSESSMENT_PROMPTS

st.set_page_config(page_title="Assessment Generator", page_icon="📊")

# Custom CSS for this page
st.markdown("""
<style>
    .assessment-header {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(255, 154, 158, 0.3);
    }
    
    .question-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #ff9a9e;
        transition: transform 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateX(10px);
    }
    
    .difficulty-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .easy { background: #d4edda; color: #155724; }
    .medium { background: #fff3cd; color: #856404; }
    .hard { background: #f8d7da; color: #721c24; }
    
    .rubric-table {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .rubric-table th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        text-align: left;
    }
    
    .rubric-table td {
        padding: 1rem;
        border-bottom: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="assessment-header">
    <h1>📊 Assessment Generator</h1>
    <p>Create comprehensive assessments with automatic answer keys and rubrics</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get('model'):
    st.warning("⚠️ Please initialize Gemini AI in the main page first.")
    st.stop()

# Main form
with st.form("assessment_form"):
    st.markdown("### 📝 Assessment Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        assessment_type = st.selectbox(
            "Assessment Type*",
            ["Quiz", "Test", "Exam", "Assignment", "Project", "Worksheet"],
            format_func=lambda x: f"📌 {x}"
        )
        topic = st.text_input("Topic/Subject*", placeholder="e.g., Quadratic Equations")
        grade_level = st.text_input("Grade Level*", placeholder="e.g., 10th Grade, College")
        
    with col2:
        num_questions = st.number_input("Number of Questions*", min_value=1, max_value=50, value=10)
        difficulty = st.select_slider(
            "Difficulty Level*",
            options=["Very Easy", "Easy", "Medium", "Hard", "Very Hard"],
            value="Medium"
        )
    
    objectives = st.text_area(
        "Learning Objectives Tested*",
        placeholder="What specific knowledge or skills should this assessment measure?",
        height=100
    )
    
    requirements = st.text_area(
        "Additional Requirements",
        placeholder="e.g., Include real-world problems, require written explanations, etc.",
        height=80
    )
    
    # Assessment purpose
    st.markdown("### 🎯 Assessment Purpose")
    assessment_style = st.radio(
        "Select the main purpose",
        options=list(ASSESSMENT_PROMPTS.keys()),
        format_func=lambda x: x.title(),
        horizontal=True
    )
    
    # Question types with visual icons
    st.markdown("### 📋 Question Types")
    q_col1, q_col2, q_col3 = st.columns(3)
    
    with q_col1:
        multiple_choice = st.checkbox("🔘 Multiple Choice", value=True)
        true_false = st.checkbox("✅ True/False")
        
    with q_col2:
        short_answer = st.checkbox("📝 Short Answer", value=True)
        essay = st.checkbox("📄 Essay")
        
    with q_col3:
        matching = st.checkbox("🔗 Matching")
        fill_blank = st.checkbox("✏️ Fill in the Blank", value=True)
    
    submitted = st.form_submit_button("🚀 Generate Assessment", type="primary", use_container_width=True)

if submitted:
    if not all([topic, grade_level, objectives]):
        st.error("❌ Please fill in all required fields (*)")
    else:
        # Compile question types
        question_types = []
        if multiple_choice: question_types.append("multiple choice")
        if true_false: question_types.append("true/false")
        if short_answer: question_types.append("short answer")
        if essay: question_types.append("essay")
        if matching: question_types.append("matching")
        if fill_blank: question_types.append("fill in the blank")
        
        assessment_data = {
            'type': assessment_type,
            'topic': topic,
            'grade_level': grade_level,
            'num_questions': num_questions,
            'difficulty': difficulty,
            'objectives': objectives,
            'requirements': f"{requirements}\nQuestion types to include: {', '.join(question_types)}"
        }
        
        base_prompt = format_assessment(assessment_data)
        style_prompt = ASSESSMENT_PROMPTS[assessment_style]
        full_prompt = f"{base_prompt}\n\n{style_prompt}"
        
        with st.spinner("📝 Generating your assessment..."):
            assessment = generate_content(full_prompt)
        
        if assessment:
            st.success("✅ Assessment generated successfully!")
            
            # Display assessment in styled tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Assessment", "🔑 Answer Key", "📊 Rubric", "📈 Analysis"])
            
            with tab1:
                st.markdown(f"""
                <div class="outline-container">
                    <h2 style="color: #ff9a9e;">{topic} - {assessment_type}</h2>
                    <p><strong>Grade Level:</strong> {grade_level} | <strong>Difficulty:</strong> 
                        <span class="difficulty-badge {'easy' if difficulty in ['Very Easy', 'Easy'] else 'medium' if difficulty == 'Medium' else 'hard'}">
                            {difficulty}
                        </span>
                    </p>
                    <hr>
                    {assessment}
                </div>
                """, unsafe_allow_html=True)
            
            with tab2:
                st.info("🔑 Generating answer key...")
                answer_key_prompt = f"Create a detailed answer key for this {assessment_type}:\n\n{assessment}"
                answer_key = generate_content(answer_key_prompt)
                if answer_key:
                    st.markdown(f"""
                    <div class="outline-container">
                        <h3 style="color: #ff9a9e;">Answer Key</h3>
                        {answer_key}
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab3:
                st.info("📊 Generating scoring rubric...")
                rubric_prompt = f"Create a detailed scoring rubric for this {assessment_type}:\n\n{assessment}"
                rubric = generate_content(rubric_prompt)
                if rubric:
                    st.markdown(f"""
                    <div class="rubric-table">
                        <h3 style="padding: 1rem; color: #ff9a9e;">Scoring Rubric</h3>
                        {rubric}
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab4:
                st.markdown("### 📈 Assessment Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Difficulty Distribution")
                    difficulty_data = {
                        "Easy": 30,
                        "Medium": 50,
                        "Hard": 20
                    }
                    
                    for level, percentage in difficulty_data.items():
                        st.markdown(f"**{level}**")
                        st.progress(percentage / 100)
                        st.caption(f"{percentage}% of questions")
                
                with col2:
                    st.markdown("#### Question Type Distribution")
                    for q_type in question_types:
                        st.markdown(f"• {q_type.title()}")
            
            # Download options
            st.markdown("### 💾 Download Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📥 Download Assessment",
                    data=assessment,
                    file_name=f"{topic.lower().replace(' ', '_')}_assessment.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                st.button("📄 Export as PDF", use_container_width=True)
            
            with col3:
                st.button("📋 Copy All", use_container_width=True)

# Question bank feature in sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                padding: 1rem; border-radius: 10px; color: #2c3e50;">
        <h3>📚 Question Bank</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if 'question_bank' not in st.session_state:
        st.session_state.question_bank = []
    
    # Quick question generator
    with st.expander("➕ Add Custom Question", expanded=False):
        q_topic = st.text_input("Topic", key="q_topic", placeholder="e.g., Algebra")
        q_type = st.selectbox("Type", ["Multiple Choice", "Short Answer", "Essay", "Problem Solving"])
        q_difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
        
        if st.button("Generate Question", use_container_width=True):
            if q_topic:
                with st.spinner("Generating..."):
                    q_prompt = f"Generate one {q_difficulty} {q_type} question about {q_topic} for {grade_level if 'grade_level' in locals() else 'appropriate'} level"
                    question = generate_content(q_prompt)
                    if question:
                        st.session_state.question_bank.append({
                            'question': question,
                            'topic': q_topic,
                            'type': q_type,
                            'difficulty': q_difficulty
                        })
                        st.success("✅ Question added!")
    
    # Display question bank
    if st.session_state.question_bank:
        st.markdown("### 📌 Saved Questions")
        for i, q in enumerate(st.session_state.question_bank[-3:]):
            with st.container():
                st.markdown(f"""
                <div class="question-card">
                    <span class="difficulty-badge {q['difficulty'].lower()}">{q['difficulty']}</span>
                    <span style="color: #666;">{q['type']}</span>
                    <p style="margin-top: 0.5rem;"><strong>{q['topic']}</strong></p>
                    <p style="font-size: 0.9rem; color: #666;">{q['question'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)