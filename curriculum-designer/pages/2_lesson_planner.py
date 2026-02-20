import streamlit as st
from utils.gemini_helper import generate_content, format_lesson_plan
from utils.prompts import LESSON_PLAN_PROMPTS

st.set_page_config(page_title="Lesson Planner", page_icon="📅")

# Custom CSS for this page
st.markdown("""
<style>
    .lesson-header {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(132, 250, 176, 0.3);
    }
    
    .timeline-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .timeline-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .activity-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #84fab0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="lesson-header">
    <h1>📅 AI Lesson Planner</h1>
    <p>Design engaging, interactive lessons that captivate your students</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get('model'):
    st.warning("⚠️ Please initialize Gemini AI in the main page first.")
    st.stop()

# Main form
with st.form("lesson_plan_form"):
    st.markdown("### 📝 Lesson Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Lesson Title*", placeholder="e.g., Introduction to Photosynthesis")
        course = st.text_input("Course Name*", placeholder="e.g., Biology 101")
        duration = st.slider("Lesson Duration (minutes)*", min_value=15, max_value=180, value=60, step=15)
        
    with col2:
        class_size = st.number_input("Class Size*", min_value=1, value=25)
        objectives = st.text_area(
            "Learning Objectives*",
            placeholder="What should students know or be able to do by the end of this lesson?",
            height=100
        )
    
    st.markdown("### 📚 Resources & Prerequisites")
    materials = st.text_input(
        "Materials Needed",
        placeholder="e.g., Textbook, worksheets, projector, lab equipment"
    )
    
    prerequisites = st.text_input(
        "Prior Knowledge Required",
        placeholder="What should students already know?"
    )
    
    # Teaching style selection with visual indicators
    st.markdown("### 🎯 Teaching Approach")
    teaching_style = st.selectbox(
        "Select teaching style",
        options=list(LESSON_PLAN_PROMPTS.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Engagement features
    st.markdown("### ✨ Engagement Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        group_work = st.checkbox("👥 Group Activities")
        technology = st.checkbox("💻 Technology Integration")
    
    with col2:
        hands_on = st.checkbox("✋ Hands-on Exercises")
        discussion = st.checkbox("💬 Class Discussion")
    
    with col3:
        assessment = st.checkbox("📊 Formative Assessment")
        differentiation = st.checkbox("🎯 Differentiation")
    
    submitted = st.form_submit_button("🚀 Generate Lesson Plan", type="primary", use_container_width=True)

if submitted:
    if not all([title, course, duration, objectives]):
        st.error("❌ Please fill in all required fields (*)")
    else:
        lesson_data = {
            'title': title,
            'course': course,
            'duration': duration,
            'class_size': class_size,
            'objectives': objectives,
            'materials': materials,
            'prerequisites': prerequisites
        }
        
        base_prompt = format_lesson_plan(lesson_data)
        style_prompt = LESSON_PLAN_PROMPTS[teaching_style]
        
        # Add engagement features to prompt
        engagement_features = []
        if group_work: engagement_features.append("group activities")
        if technology: engagement_features.append("technology integration")
        if hands_on: engagement_features.append("hands-on exercises")
        if discussion: engagement_features.append("class discussions")
        if assessment: engagement_features.append("formative assessments")
        if differentiation: engagement_features.append("differentiation strategies")
        
        if engagement_features:
            style_prompt += f"\n\nInclude these engagement features: {', '.join(engagement_features)}"
        
        full_prompt = f"{base_prompt}\n\n{style_prompt}"
        
        with st.spinner("🎨 Crafting your engaging lesson plan..."):
            lesson_plan = generate_content(full_prompt)
        
        if lesson_plan:
            st.success("✅ Lesson plan generated successfully!")
            
            # Interactive timeline visualization
            st.markdown("### ⏱️ Lesson Timeline")
            
            cols = st.columns(4)
            timeline_segments = [
                ("🎯 Opening", "5-10 min", "Hook & Objectives"),
                ("📚 Instruction", "15-20 min", "Content Delivery"),
                ("✋ Practice", "15-20 min", "Guided & Independent"),
                ("🎉 Closing", "5-10 min", "Review & Assessment")
            ]
            
            for col, (title, duration, desc) in zip(cols, timeline_segments):
                with col:
                    st.markdown(f"""
                    <div class="timeline-step">
                        <h4>{title}</h4>
                        <p style="font-size: 1.2rem; margin: 0.5rem 0;">{duration}</p>
                        <p style="font-size: 0.9rem; opacity: 0.9;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display lesson plan
            st.markdown("### 📝 Detailed Lesson Plan")
            st.markdown(f"""
            <div class="outline-container">
                <h2 style="color: #84fab0;">{title}</h2>
                <p><strong>Course:</strong> {course} | <strong>Duration:</strong> {duration} minutes</p>
                <p><strong>Class Size:</strong> {class_size} students</p>
                <hr>
                {lesson_plan}
            </div>
            """, unsafe_allow_html=True)
            
            # Download options
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Lesson Plan",
                    data=lesson_plan,
                    file_name=f"{title.lower().replace(' ', '_')}_lesson_plan.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.success("Copied to clipboard!")

# Sidebar with differentiation strategies
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
                padding: 1rem; border-radius: 10px; color: #2c3e50;">
        <h3>🎯 Differentiation Strategies</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📚 For Different Learners"):
        st.markdown("""
        - **Visual learners**: Diagrams, charts, videos
        - **Auditory learners**: Discussions, recordings
        - **Kinesthetic learners**: Hands-on activities
        - **Reading/Writing**: Text-based materials
        """)
    
    with st.expander("⚡ For Quick Learners"):
        st.markdown("""
        - Extension activities
        - Independent research
        - Peer tutoring opportunities
        - Advanced problems
        """)
    
    with st.expander("🆘 For Struggling Learners"):
        st.markdown("""
        - Scaffolded instructions
        - Additional practice
        - One-on-one support
        - Modified assignments
        """)