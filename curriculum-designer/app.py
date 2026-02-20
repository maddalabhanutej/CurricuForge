import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure page with custom theme
st.set_page_config(
    page_title="AI Curriculum Designer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Card styling */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card h3 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        font-weight: 600;
        animation: fadeIn 0.5s ease;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    .sidebar-content {
        color: white;
        padding: 1rem;
    }
    
    /* Animation for generated content */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .generated-content {
        animation: fadeIn 0.5s ease;
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-card {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
if 'model' not in st.session_state:
    st.session_state.model = None
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def initialize_gemini():
    """Initialize Gemini AI model"""
    try:
        if st.session_state.api_key:
            genai.configure(api_key=st.session_state.api_key)
            st.session_state.model = genai.GenerativeModel('gemini-pro')
            return True
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return False
    return False

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">🎓 Curriculum Designer</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key input with icon
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Google Gemini API key",
        placeholder="AIza..."
    )
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.session_state.model = None
    
    # Initialize button with animation
    if st.button("🚀 Initialize Gemini", type="primary", use_container_width=True):
        if initialize_gemini():
            st.markdown("""
            <div class="success-message">
                ✅ Gemini initialized successfully!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Failed to initialize Gemini")
    
    st.markdown("---")
    
    # Theme selector
    st.markdown("### 🎨 Customization")
    theme = st.selectbox("Theme", ["Light", "Dark", "System"], index=0)
    
    st.markdown("---")
    
    # App info with styled card
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #667eea; margin-bottom: 1rem;">📚 About</h3>
        <p style="color: #666;">This AI-powered curriculum designer helps educators create:</p>
        <ul style="color: #666; list-style-type: none; padding-left: 0;">
            <li style="margin: 0.5rem 0;">📝 <strong>Course outlines</strong></li>
            <li style="margin: 0.5rem 0;">📅 <strong>Lesson plans</strong></li>
            <li style="margin: 0.5rem 0;">📊 <strong>Assessments</strong></li>
            <li style="margin: 0.5rem 0;">🎯 <strong>Learning objectives</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎓 AI Curriculum Designer</h1>
    <p>Empowering educators with intelligent content creation</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.api_key:
    st.markdown("""
    <div class="info-box">
        <h3>👋 Welcome to AI Curriculum Designer!</h3>
        <p>Please enter your Gemini API key in the sidebar to get started.</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">Don't have an API key? 
        <a href="https://makersuite.google.com/app/apikey" target="_blank" style="color: white; text-decoration: underline;">
        Get one from Google AI Studio</a></p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Welcome message and metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📝</h3>
            <h3>Course Outlines</h3>
            <p>Create comprehensive structures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📅</h3>
            <h3>Lesson Plans</h3>
            <p>Design engaging lessons</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊</h3>
            <h3>Assessments</h3>
            <p>Generate quizzes & tests</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome section with animation
    st.markdown("""
    <div class="generated-content">
        <h2 style="color: #667eea; margin-bottom: 1rem;">✨ Welcome to the Future of Education</h2>
        <p style="color: #666; font-size: 1.1rem; line-height: 1.6;">
        Navigate through our intelligent tools to create professional educational content in minutes. 
        Each tool is powered by Google's Gemini AI to ensure high-quality, engaging, and effective learning materials.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <h3 style="color: #667eea;">📝 Course Outline</h3>
            <p style="color: #666;">Create structured course outlines with learning objectives and modules</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <h3 style="color: #667eea;">📅 Lesson Planner</h3>
            <p style="color: #666;">Design detailed lesson plans with timing and activities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <h3 style="color: #667eea;">📊 Assessment</h3>
            <p style="color: #666;">Generate quizzes, tests, and assignments with rubrics</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start guide with styled expander
    with st.expander("📖 Quick Start Guide", expanded=False):
        st.markdown("""
        <div style="padding: 1rem;">
            <h4 style="color: #667eea;">Follow these steps to create your first curriculum:</h4>
            <ol style="color: #666; font-size: 1.1rem; line-height: 2;">
                <li>🔑 <strong>Enter your API Key</strong> in the sidebar</li>
                <li>🚀 <strong>Initialize Gemini</strong> by clicking the button</li>
                <li>📋 <strong>Navigate</strong> to the desired tool using the sidebar menu</li>
                <li>✏️ <strong>Fill in the parameters</strong> for your curriculum element</li>
                <li>⚡ <strong>Generate</strong> and refine your content</li>
            </ol>
            
            <h4 style="color: #667eea; margin-top: 2rem;">💡 Pro Tips:</h4>
            <ul style="color: #666; font-size: 1.1rem; line-height: 2;">
                <li>🎯 Be specific about learning objectives for better results</li>
                <li>👥 Include target audience details to tailor the content</li>
                <li>⏱️ Specify duration and format requirements</li>
                <li>🔄 You can regenerate content with modified parameters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent generations gallery
    if st.session_state.generated_content:
        st.markdown("### 📋 Recent Creations")
        recent_items = list(st.session_state.generated_content.items())[-3:]
        
        cols = st.columns(len(recent_items))
        for idx, (key, value) in enumerate(recent_items):
            with cols[idx]:
                st.markdown(f"""
                <div class="custom-card">
                    <h4 style="color: #667eea; margin-bottom: 0.5rem;">📄 {key}</h4>
                    <p style="color: #666; font-size: 0.9rem;">🕒 {value['timestamp']}</p>
                    <p style="color: #666; font-size: 0.9rem;">📝 {value['prompt']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👁️ View", key=f"view_{idx}"):
                    st.session_state[f"view_{key}"] = value['content']

# Footer
st.markdown("""
<div class="footer">
    <p style="margin: 0; font-size: 1rem;">Powered by Google Gemini AI | Built with Streamlit</p>
    <p style="margin: 0.5rem 0 0; font-size: 0.9rem; opacity: 0.9;">© 2024 AI Curriculum Designer</p>
</div>
""", unsafe_allow_html=True)