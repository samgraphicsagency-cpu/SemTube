import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import re
import time

# ============================================
# 🔧 PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="SemTube - AI YouTube Empire",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 CUSTOM CSS - PROFESSIONAL DARK THEME
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FF0000 0%, #FF4444 25%, #FF6B6B 50%, #FF0000 75%, #CC0000 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 10px 0;
        animation: gradient-shift 3s ease infinite;
        letter-spacing: -1px;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .sub-header {
        text-align: center;
        font-size: 1.15rem;
        color: #888;
        margin-top: -10px;
        margin-bottom: 30px;
        font-weight: 400;
    }

    /* Brand Badge */
    .brand-badge {
        background: linear-gradient(135deg, #FF0000, #CC0000);
        color: white;
        padding: 5px 20px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        text-align: center;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
    }

    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 8px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .feature-card:hover {
        transform: translateY(-3px);
        border-color: #FF0000;
        box-shadow: 0 8px 30px rgba(255, 0, 0, 0.15);
    }

    .feature-card h4 {
        color: #FF6B6B;
        margin-bottom: 8px;
        font-weight: 700;
    }

    .feature-card p {
        color: #ccc;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 16px 40px !important;
        border: none !important;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(255, 0, 0, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(255, 0, 0, 0.5) !important;
    }

    /* Result Container */
    .result-box {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
        padding: 35px;
        border-radius: 20px;
        border: 1px solid rgba(255, 107, 107, 0.2);
        color: #e0e0e0;
        font-size: 1.05rem;
        line-height: 2;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        margin: 20px 0;
    }

    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #FF0000, #FF4444);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
    }

    .stat-card h2 {
        font-size: 2rem;
        margin: 0;
        font-weight: 800;
    }

    .stat-card p {
        margin: 5px 0 0;
        font-size: 0.85rem;
        opacity: 0.9;
    }

    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #111128 100%);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FF6B6B;
    }

    /* Tool Selector */
    .tool-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FF6B6B;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 107, 107, 0.2);
        margin-bottom: 15px;
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid rgba(255, 107, 107, 0.2) !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #FF0000 !important;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.1) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #FF6B6B !important;
    }

    /* Footer */
    .footer-section {
        text-align: center;
        padding: 40px 20px;
        margin-top: 50px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .footer-section h3 {
        color: #FF6B6B;
        font-weight: 700;
    }

    .footer-section p {
        color: #888;
        line-height: 1.8;
    }

    /* Pulse Animation for Generate Button */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }

    /* Success Message */
    .success-banner {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 15px 0;
    }

    /* Loading Spinner */
    .loading-text {
        text-align: center;
        font-size: 1.2rem;
        color: #FF6B6B;
        font-weight: 600;
    }

    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FF0000, transparent);
        margin: 30px 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# 📱 SIDEBAR - CONTROL PANEL
# ============================================
with st.sidebar:
    # SemTube Logo Area
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <div style='font-size: 3rem; margin-bottom: 5px;'>🎬</div>
        <div style='font-size: 1.8rem; font-weight: 900; 
                    background: linear-gradient(135deg, #FF0000, #FF6B6B);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;'>
            SemTube
        </div>
        <div style='font-size: 0.75rem; color: #888; letter-spacing: 3px; 
                    text-transform: uppercase; margin-top: 3px;'>
            AI YOUTUBE EMPIRE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # API Key Input
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "Gemini API Key:",
        type="password",
        help="🆓 Get your FREE API key from: aistudio.google.com",
        placeholder="Paste your API key here..."
    )

    # Connection Status
    if api_key:
        st.success("✅ API Key Connected")
    else:
        st.warning("⚠️ Enter API Key to start")

    st.markdown("---")

    # System Status Dashboard
    st.markdown("### 📊 System Status")

    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.metric("Tools", "10", "Active")
    with status_col2:
        st.metric("Cost", "$0", "Free")

    st.markdown("---")

    # Quick Start Guide
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    <div style='font-size: 0.85rem; line-height: 2; color: #ccc;'>
        <b>Step 1:</b> Get API Key from Google AI Studio<br>
        <b>Step 2:</b> Paste it above ☝️<br>
        <b>Step 3:</b> Choose your AI tool<br>
        <b>Step 4:</b> Enter topic & generate!<br>
        <b>Step 5:</b> Copy & use in YouTube
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Credits
    st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <p style='color: #666; font-size: 0.75rem;'>
            Powered by Google Gemini AI<br>
            Built with ❤️ by SemTube Team
        </p>
        <p style='color: #444; font-size: 0.7rem; margin-top: 5px;'>
            v2.0 • 2025 Edition
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 🏠 MAIN CONTENT AREA
# ============================================

# Top Brand Badge
st.markdown("<div style='text-align: center; margin-bottom: 5px;'><span class='brand-badge'>🎬 SEMTUBE AI</span></div>", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">SemTube</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Complete AI-Powered YouTube Automation System — 10 Pro Tools, 100% Free Forever</p>', unsafe_allow_html=True)

# Stats Row
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown("""
    <div class="stat-card">
        <h2>10</h2>
        <p>AI Tools</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
    <div class="stat-card">
        <h2>∞</h2>
        <p>Generations</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
    <div class="stat-card">
        <h2>$0</h2>
        <p>Forever Free</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown("""
    <div class="stat-card">
        <h2>3</h2>
        <p>Languages</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ============================================
# 🎯 TOOL SELECTION AREA
# ============================================

st.markdown("## 🎯 Select Your AI Tool")

# Tool Categories in Tabs
tab1, tab2, tab3 = st.tabs(["📝 Content Creation", "🔍 SEO & Optimization", "🎬 Advanced Tools"])

with tab1:
    st.markdown('<p class="tool-header">📝 Content Creation Tools</p>', unsafe_allow_html=True)

    content_col1, content_col2 = st.columns(2)

    with content_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🔥 Viral Video Ideas</h4>
            <p>Get 10 unique, trending video ideas with viral potential analysis for your niche.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>📜 Full Video Script</h4>
            <p>Complete script with Hook, Intro, Main Content, CTA & Outro — ready to record.</p>
        </div>
        """, unsafe_allow_html=True)

    with content_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Thumbnail Text</h4>
            <p>Bold, attention-grabbing text suggestions for your video thumbnails.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>💬 Comment Replies</h4>
            <p>Smart reply templates for positive, negative, and question comments.</p>
        </div>
        """, unsafe_allow_html=True)

    selected_content_tool = st.selectbox(
        "Choose Content Tool:",
        [
            "🔥 Viral Video Ideas Generator",
            "📜 Full Video Script Writer",
            "🎯 Thumbnail Text Suggestions",
            "💬 Comment Reply Generator"
        ],
        key="content_select"
    )

with tab2:
    st.markdown('<p class="tool-header">🔍 SEO & Optimization Tools</p>', unsafe_allow_html=True)

    seo_col1, seo_col2 = st.columns(2)

    with seo_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🏷️ Title Generator</h4>
            <p>10 high-CTR, click-worthy title variations with power words & curiosity gaps.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>📝 SEO Description</h4>
            <p>Fully optimized video description with keywords, timestamps & hashtags.</p>
        </div>
        """, unsafe_allow_html=True)

    with seo_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔖 Trending Tags</h4>
            <p>30 researched tags — broad, medium-specific & long-tail for maximum reach.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h4>📊 Keyword Research</h4>
            <p>High volume, low competition & long-tail keywords with search intent analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    selected_seo_tool = st.selectbox(
        "Choose SEO Tool:",
        [
            "🏷️ Title Generator (10 Variants)",
            "📝 SEO Description Writer",
            "🔖 Trending Tags Finder",
            "📊 Keyword Research Tool"
        ],
        key="seo_select"
    )

with tab3:
    st.markdown('<p class="tool-header">🎬 Advanced AI Tools</p>', unsafe_allow_html=True)

    adv_col1, adv_col2 = st.columns(2)

    with adv_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📹 Video Summarizer</h4>
            <p>Paste any YouTube URL and get a complete summary with key takeaways.</p>
        </div>
        """, unsafe_allow_html=True)

    with adv_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎤 Hook Generator</h4>
            <p>10 powerful first-5-second hooks that stop the scroll and grab attention.</p>
        </div>
        """, unsafe_allow_html=True)

    selected_adv_tool = st.selectbox(
        "Choose Advanced Tool:",
        [
            "📹 YouTube Video Summarizer",
            "🎤 Hook Generator (First 5 Sec)"
        ],
        key="adv_select"
    )

# Determine which tool is actually selected based on last interaction
# Use session state to track active tab
if 'active_tool' not in st.session_state:
    st.session_state.active_tool = "🔥 Viral Video Ideas Generator"

# Tool selector unified
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("## 🛠️ Active Tool Selection")

all_tools = [
    "🔥 Viral Video Ideas Generator",
    "📜 Full Video Script Writer",
    "🎯 Thumbnail Text Suggestions",
    "💬 Comment Reply Generator",
    "🏷️ Title Generator (10 Variants)",
    "📝 SEO Description Writer",
    "🔖 Trending Tags Finder",
    "📊 Keyword Research Tool",
    "📹 YouTube Video Summarizer",
    "🎤 Hook Generator (First 5 Sec)"
]

selected_tool = st.selectbox(
    "🎯 Select the tool you want to use:",
    all_tools,
    key="main_tool_select",
    help="Choose one of the 10 AI tools to generate content"
)


# ============================================
# ✍️ INPUT SECTION
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("## ✍️ Your Input")

# Different input based on selected tool
if selected_tool == "📹 YouTube Video Summarizer":
    user_input = st.text_input(
        "🔗 Enter YouTube Video URL:",
        placeholder="https://www.youtube.com/watch?v=xxxxx",
        help="Paste the full YouTube video URL. Video must have subtitles/captions enabled."
    )
else:
    user_input = st.text_area(
        "📝 Enter Your Topic / Niche / Keyword:",
        placeholder="e.g., How to make money with AI in 2025, Best productivity apps for students, etc.",
        help="Be specific for better results! The more detail you give, the better AI output you get.",
        height=100
    )

# Advanced Options
with st.expander("⚙️ Advanced Options (Customize Your Output)", expanded=False):
    opt_col1, opt_col2, opt_col3 = st.columns(3)

    with opt_col1:
        tone = st.selectbox(
            "🎭 Content Tone:",
            ["Professional", "Casual & Friendly", "Funny & Entertaining", "Educational", "Motivational", "Dramatic"],
            help="Choose the mood/style of your content"
        )

    with opt_col2:
        language = st.selectbox(
            "🌍 Language:",
            ["English", "Bengali (বাংলা)", "Hinglish", "Hindi", "Mix (English + Bengali)"],
            help="Select output language"
        )

    with opt_col3:
        target_audience = st.selectbox(
            "👥 Target Audience:",
            ["General", "Students", "Professionals", "Beginners", "Tech Enthusiasts", "Business Owners"],
            help="Who is your video for?"
        )

    length = st.slider(
        "📏 Content Length (approx. words):",
        min_value=100,
        max_value=1000,
        value=300,
        step=50,
        help="Adjust the length of generated content"
    )


# ============================================
# 🚀 GENERATE BUTTON
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])

with gen_col2:
    generate_btn = st.button(
        "🚀 GENERATE WITH SEMTUBE AI",
        use_container_width=True,
        type="primary"
    )


# ============================================
# 🧠 AI GENERATION LOGIC
# ============================================

if generate_btn:
    # Validation
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar first!")
        st.markdown("""
        <div style='background: #1a1a2e; padding: 20px; border-radius: 12px; border-left: 4px solid #FF0000; margin: 10px 0;'>
            <h4 style='color: #FF6B6B;'>🔑 How to get your FREE API Key:</h4>
            <ol style='color: #ccc; line-height: 2;'>
                <li>Go to <a href='https://aistudio.google.com' target='_blank' style='color: #FF6B6B;'>aistudio.google.com</a></li>
                <li>Sign in with your Google account</li>
                <li>Click "Get API Key" → "Create API Key"</li>
                <li>Copy the key and paste in sidebar</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    if not user_input:
        st.warning("⚠️ Please enter a topic or YouTube URL!")
        st.stop()

    try:
        # Configure Gemini AI with fallback models
        genai.configure(api_key=api_key)
        
        # Try to use the latest available model
        model_names = [
            'gemini-2.0-flash-exp',      # Latest experimental
            'gemini-1.5-pro-latest',     # Latest stable pro
            'gemini-1.5-flash-latest',   # Latest stable flash
            'gemini-1.5-pro',            # Standard pro
            'gemini-pro'                 # Fallback
        ]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                st.info(f"✅ Using model: {model_name}")
                break
            except Exception as model_error:
                continue
        
        if model is None:
            st.error("❌ Could not initialize any Gemini model. Please check your API key.")
            st.stop()

        # ============================================
        # 📋 PROMPT ENGINEERING FOR EACH TOOL
        # ============================================

        if selected_tool == "🔥 Viral Video Ideas Generator":
            prompt = f"""You are a top YouTube strategist with 10+ years of experience growing channels from 0 to millions.

Generate 10 highly viral and unique YouTube video ideas about: '{user_input}'

Target Audience: {target_audience}
Tone: {tone}
Language: {language}

For EACH idea, provide:
📌 **Video Title**: (Catchy, click-worthy, under 60 chars)
📝 **Brief Description**: (2-3 lines explaining the concept)
🎯 **Why It Will Go Viral**: (1 line - psychological trigger)
📊 **Estimated Difficulty**: (Easy / Medium / Hard to produce)
💰 **Monetization Potential**: (Low / Medium / High)

Format each idea clearly with numbers 1-10.
Make each idea UNIQUE - no repetition!
Focus on ideas that can realistically go viral in 2025."""

        elif selected_tool == "📜 Full Video Script Writer":
            prompt = f"""You are a professional YouTube scriptwriter who has written scripts for channels with millions of subscribers.

Write a complete, highly engaging YouTube video script about: '{user_input}'

Target Audience: {target_audience}
Tone: {tone}  
Language: {language}
Approximate Length: {length} words

SCRIPT STRUCTURE:

🎣 **HOOK (0-5 seconds)**:
Write an attention-grabbing opening that makes viewers STOP scrolling. Use curiosity, shock value, or a bold claim.

📢 **INTRO (5-30 seconds)**:
- Introduce the topic
- State the problem/opportunity
- Tell viewers what they'll learn
- Build credibility

📚 **MAIN CONTENT (Body)**:
- Break into 3-5 clear sections/points
- Use storytelling and examples
- Include transitions between points
- Add "Pattern Interrupts" every 60-90 seconds (to maintain retention)
- Include viewer engagement prompts ("Comment below if...")

🔔 **CALL TO ACTION (Before Outro)**:
- Ask to subscribe with specific reason
- Like reminder
- Comment prompt with specific question
- Share request

👋 **OUTRO (Last 15-20 seconds)**:
- Summarize key takeaway
- Tease next video
- End with memorable closing line

FORMATTING RULES:
- Use [B-ROLL] markers for visual suggestions
- Use [SHOW ON SCREEN] for text/graphic suggestions
- Use [PAUSE] for dramatic effect
- Write in conversational, spoken language
- Add emotion cues [ENTHUSIASTIC], [SERIOUS], [WHISPER] etc.

Make it feel natural, NOT robotic!"""

        elif selected_tool == "🏷️ Title Generator (10 Variants)":
            prompt = f"""You are a YouTube SEO expert who specializes in creating high-CTR titles that rank #1 in search.

Generate 10 unique, high-performing YouTube video titles about: '{user_input}'

Language: {language}
Tone: {tone}

REQUIREMENTS FOR EACH TITLE:
✅ Under 60 characters (STRICT)
✅ Include at least ONE power word (Free, Secret, Proven, Ultimate, Insane, etc.)
✅ Use numbers where possible
✅ Create a curiosity gap
✅ Must make someone NEED to click

TITLE CATEGORIES (create variety):
1-2: Number-based titles ("7 Ways...", "Top 5...")
3-4: How-to titles ("How to..." "How I...")
5-6: Curiosity/Mystery titles ("The Secret...", "Nobody Tells You...")
7-8: Urgency titles ("Stop Doing This!", "Before It's Too Late...")
9-10: Bold/Controversial titles ("I Was Wrong About...", "The Truth About...")

For each title also provide:
📊 **Estimated CTR Potential**: ⭐⭐⭐⭐⭐ (rate 1-5)
🎯 **Best For**: (Search / Browse / Both)

Format as numbered list 1-10."""

        elif selected_tool == "📝 SEO Description Writer":
            prompt = f"""You are a YouTube SEO specialist who has helped 500+ channels rank on page 1.

Write a fully SEO-optimized YouTube video description about: '{user_input}'

Language: {language}
Tone: {tone}

DESCRIPTION STRUCTURE:

📌 **FIRST 2 LINES (Above the fold - MOST IMPORTANT):**
- Hook with main keyword naturally included
- This appears in search results, make it compelling!
- Under 150 characters

📝 **PARAGRAPH 2 (Detailed Overview):**
- 3-4 sentences explaining what the video covers
- Include 3-5 relevant keywords naturally
- Add value proposition

⏱️ **TIMESTAMPS:**
0:00 - Introduction
[Generate 5-8 realistic timestamps based on topic]

🔗 **RESOURCES & LINKS:**
📌 [Resource 1 mentioned in video]
📌 [Resource 2 mentioned in video]
📌 Free Download: [Placeholder]

📱 **SOCIAL MEDIA:**
📸 Instagram: @[your-handle]
🐦 Twitter: @[your-handle]
💼 LinkedIn: [your-profile]
🌐 Website: [your-website]

📧 **BUSINESS INQUIRIES:**
Email: [your-email]

🏷️ **TAGS IN DESCRIPTION:**
#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5

⚖️ **DISCLAIMER (if applicable):**
[Standard disclaimer text]

RULES:
- Use main keyword in first sentence
- Include 5-8 secondary keywords throughout
- Total length: 200-300 words
- Make it scannable with line breaks
- Include call-to-action to subscribe"""

        elif selected_tool == "🔖 Trending Tags Finder":
            prompt = f"""You are a YouTube algorithm expert who understands how tags affect video discovery and ranking.

Generate 30 highly effective, searchable tags for a YouTube video about: '{user_input}'

ORGANIZE INTO 3 CATEGORIES:

🔵 **BROAD TAGS (10 tags):**
- High search volume
- General terms related to the topic
- 1-2 word tags
- These help YouTube understand your content category

🟡 **MEDIUM-SPECIFIC TAGS (10 tags):**
- Moderate search volume  
- More specific to the exact topic
- 2-4 word phrases
- These help rank for specific searches

🟢 **LONG-TAIL TAGS (10 tags):**
- Lower competition
- Very specific phrases
- 4-7 word phrases
- These help you rank faster as a small channel

RULES:
- Each tag under 30 characters
- No duplicate concepts
- Mix singular and plural forms
- Include common misspellings if relevant
- Include trending variations

Also provide:
📊 **Tag Strategy Tip**: One paragraph about how to best use these tags
⚠️ **Tags to AVOID**: 3 tags that might seem relevant but would hurt performance"""

        elif selected_tool == "📊 Keyword Research Tool":
            prompt = f"""You are a YouTube keyword research expert with deep knowledge of search algorithms and trends.

Perform comprehensive YouTube keyword research for: '{user_input}'

Language: {language}
Target Audience: {target_audience}

PROVIDE:

📈 **1. HIGH VOLUME KEYWORDS (5 keywords):**
For each keyword:
- Keyword phrase
- Estimated Monthly Searches: High/Very High
- Competition Level: High
- Best content type: (Tutorial/Review/List/Vlog)
- Sample title using this keyword

📉 **2. LOW COMPETITION KEYWORDS (5 keywords):**
For each keyword:
- Keyword phrase
- Estimated Monthly Searches: Medium
- Competition Level: Low
- Why it's easy to rank for
- Sample title using this keyword

🎯 **3. LONG-TAIL KEYWORDS (5 keywords):**
For each keyword:
- Keyword phrase (4-7 words)
- Search Intent: (Informational/Commercial/Navigational)
- Competition Level: Very Low
- Best for: (New channels/Established channels)
- Sample title using this keyword

🔥 **4. TRENDING KEYWORDS (3 keywords):**
- Currently trending related terms
- Why they're trending
- Time sensitivity (Act now / Evergreen)

💡 **5. CONTENT GAP KEYWORDS (2 keywords):**
- Terms people search but few videos cover
- Opportunity analysis

📋 **STRATEGY RECOMMENDATION:**
One paragraph about which keywords to target first and why."""

        elif selected_tool == "🎤 Hook Generator (First 5 Sec)":
            prompt = f"""You are a YouTube retention expert who specializes in the critical first 5 seconds of a video.

Generate 10 POWERFUL hooks for a video about: '{user_input}'

Tone: {tone}
Language: {language}
Target Audience: {target_audience}

REQUIREMENTS FOR EACH HOOK:
- Maximum 2 sentences (must be deliverable in 5 seconds)
- Must create immediate curiosity, shock, or perceived value
- Must make the viewer psychologically UNABLE to scroll away
- Must connect to the actual video content (no clickbait)

HOOK CATEGORIES:

🤯 **SHOCK HOOKS (2):**
Start with a surprising fact or statement

❓ **QUESTION HOOKS (2):**
Ask a question the viewer desperately wants answered

💰 **VALUE HOOKS (2):**
Promise specific, tangible value immediately

📖 **STORY HOOKS (2):**
Start with a mini-story or personal experience

⚡ **BOLD CLAIM HOOKS (2):**
Make a confident, specific claim

For each hook also provide:
🎭 **Delivery Tip**: How to say it (tone, speed, expression)
📊 **Retention Impact**: ⭐⭐⭐⭐⭐ (rate 1-5)

Make each hook UNIQUE and IMPOSSIBLE to resist!"""

        elif selected_tool == "🎯 Thumbnail Text Suggestions":
            prompt = f"""You are a thumbnail design expert who has created thumbnails for videos with 10M+ views.

Generate 10 thumbnail text options for a video about: '{user_input}'

Tone: {tone}

STRICT REQUIREMENTS:
- Maximum 3-4 WORDS per text (thumbnails need BIG readable text)
- Must be readable on a phone screen
- Must create curiosity or emotion
- Must complement (not repeat) the video title

TEXT CATEGORIES:

😱 **SHOCK/EMOTION (3 options):**
- Text that triggers emotional response
- Example style: "IT'S OVER" / "I QUIT" / "NOT AGAIN"

🔢 **NUMBER-BASED (3 options):**
- Include specific numbers for credibility
- Example style: "$10K/MONTH" / "IN 7 DAYS" / "100% FREE"

❓ **CURIOSITY (2 options):**
- Make viewer need to know more
- Example style: "DON'T DO THIS" / "FINALLY..." / "THE TRUTH"

🏆 **VALUE/BENEFIT (2 options):**
- Promise clear benefit
- Example style: "GAME CHANGER" / "EASY METHOD" / "IT WORKS"

For each text also suggest:
🎨 **Color**: Best text color for this specific text
📍 **Position**: Where to place on thumbnail (top-left, center, bottom-right, etc.)
✨ **Style**: Font style suggestion (Bold, Outline, 3D, etc.)
🖼️ **Background Suggestion**: What should be in the thumbnail image behind the text"""

        elif selected_tool == "💬 Comment Reply Generator":
            prompt = f"""You are a YouTube community manager expert who knows how to boost engagement through strategic comment replies.

Generate smart comment reply templates for a video about: '{user_input}'

Tone: {tone}
Language: {language}

CREATE REPLIES FOR THESE CATEGORIES:

😊 **POSITIVE/PRAISE COMMENTS (4 replies):**
Example comments: "Great video!", "This was so helpful!", "Best channel ever!"
- Reply should: Thank them, encourage more engagement, ask a follow-up question

❓ **QUESTION COMMENTS (4 replies):**
Example comments: "How does this work?", "Can you explain more?", "What tool did you use?"
- Reply should: Answer helpfully, add value, encourage them to watch another video

😤 **CRITICAL/NEGATIVE COMMENTS (3 replies):**
Example comments: "This doesn't work", "You're wrong about this", "Waste of time"
- Reply should: Stay professional, address the concern, turn negativity into engagement

🔥 **ENGAGEMENT BOOSTING COMMENTS (3 replies):**
Example comments: "First!", "Who's watching in 2025?", Generic emoji comments
- Reply should: Create conversation, ask questions, boost algorithm signals

📌 **PINNED COMMENT SUGGESTION (1):**
Write the perfect pinned comment for this video that:
- Summarizes key value
- Asks an engaging question
- Encourages likes/subscriptions
- Under 3 lines

For each reply:
✅ Make it feel PERSONAL (not copy-paste)
✅ Include emoji naturally
✅ Keep under 2-3 sentences
✅ End with engagement trigger (question/CTA)"""

        elif selected_tool == "📹 YouTube Video Summarizer":
            # Extract video ID from URL
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', user_input)

            if not video_id_match:
                st.error("❌ Invalid YouTube URL! Please use format: https://www.youtube.com/watch?v=xxxxx")
                st.stop()

            video_id = video_id_match.group(1)

            # Get transcript
            with st.spinner("📥 Downloading video transcript..."):
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    full_text = " ".join([t['text'] for t in transcript_list])

                    # Try to get video title
                    try:
                        yt = YouTube(user_input)
                        video_title = yt.title
                        video_author = yt.author
                        video_length = yt.length
                        st.info(f"📹 **Video:** {video_title}\n\n👤 **Channel:** {video_author} | ⏱️ **Duration:** {video_length // 60} min {video_length % 60} sec")
                    except:
                        video_title = "Unknown Title"
                        video_author = "Unknown"
                        st.info(f"📹 Transcript downloaded successfully!")

                except Exception as transcript_error:
                    st.error(f"❌ Could not get transcript: {str(transcript_error)}")
                    st.info("💡 This video might not have subtitles/captions enabled. Try a different video.")
                    st.stop()

            prompt = f"""You are an expert content analyst. Summarize this YouTube video transcript comprehensively.

VIDEO TITLE: {video_title}
CHANNEL: {video_author}

Language for summary: {language}

TRANSCRIPT:
{full_text[:5000]}

PROVIDE:

📋 **QUICK SUMMARY (TL;DR):**
3-4 sentences capturing the entire video essence

🔑 **KEY POINTS (Main Takeaways):**
- List 5-7 most important points
- Each point in 1-2 sentences
- Include specific details/numbers mentioned

💡 **MAIN INSIGHT:**
The single most valuable takeaway from this video (1-2 sentences)

📊 **CONTENT BREAKDOWN:**
- Topic Category: [category]
- Content Type: [tutorial/review/opinion/news/etc.]
- Depth Level: [beginner/intermediate/advanced]

👥 **WHO SHOULD WATCH:**
1-2 sentences about who would benefit most from this video

✅ **ACTION ITEMS:**
3-5 specific things the viewer can do after watching

🔗 **RELATED TOPICS:**
5 related topics/videos the viewer might want to explore next

⭐ **CONTENT QUALITY ASSESSMENT:**
- Information Value: ⭐⭐⭐⭐⭐ (rate 1-5)
- Practical Usefulness: ⭐⭐⭐⭐⭐ (rate 1-5)
- Uniqueness: ⭐⭐⭐⭐⭐ (rate 1-5)"""

        # ============================================
        # 🚀 GENERATE CONTENT WITH AI
        # ============================================

        # Progress Animation
        progress_placeholder = st.empty()
        progress_bar = st.progress(0)

        progress_messages = [
            "🧠 Initializing SemTube AI Engine...",
            "🔍 Analyzing your request...",
            "📊 Processing with Gemini AI...",
            "✍️ Generating premium content...",
            "✨ Polishing the output...",
            "🎯 Almost there..."
        ]

        for i, msg in enumerate(progress_messages):
            progress_placeholder.markdown(f'<p class="loading-text">{msg}</p>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) * 16)
            time.sleep(0.5)

        # Generate with Gemini
        response = model.generate_content(prompt)

        progress_bar.progress(100)
        progress_placeholder.empty()
        progress_bar.empty()

        # ============================================
        # 📋 DISPLAY RESULTS
        # ============================================

        # Success Banner
        st.markdown("""
        <div class="success-banner">
            ✅ Content Generated Successfully by SemTube AI!
        </div>
        """, unsafe_allow_html=True)

        # Tool Used Badge
        st.markdown(f"""
        <div style='text-align: center; margin: 10px 0;'>
            <span style='background: rgba(255,0,0,0.1); color: #FF6B6B; padding: 5px 15px; 
                        border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                {selected_tool}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Main Result
        st.markdown("### 📋 Your Generated Content:")

        # Format the response text for HTML display
        formatted_text = response.text.replace('\n', '<br>')

        st.markdown(f"""
        <div class="result-box">
            {formatted_text}
        </div>
        """, unsafe_allow_html=True)

        # Action Buttons Row
        st.markdown("### 📥 Export Options:")

        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            # Copy-friendly text box
            st.text_area(
                "📋 Copy-Paste Friendly Version:",
                response.text,
                height=300,
                help="Click inside, Ctrl+A to select all, Ctrl+C to copy"
            )

        with export_col2:
            # Download as TXT
            st.download_button(
                label="📥 Download as .TXT",
                data=response.text,
                file_name=f"SemTube_{selected_tool.replace(' ', '_').replace('/', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            # Download as Markdown
            st.download_button(
                label="📄 Download as .MD",
                data=f"# SemTube AI Generated Content\n## Tool: {selected_tool}\n\n---\n\n{response.text}",
                file_name=f"SemTube_{selected_tool.replace(' ', '_').replace('/', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with export_col3:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; 
                        border: 1px solid rgba(255,255,255,0.1); height: 100%;'>
                <h4 style='color: #FF6B6B; margin-bottom: 10px;'>💡 Pro Tips:</h4>
                <p style='color: #ccc; font-size: 0.85rem; line-height: 1.8;'>
                    • Always customize AI content with your personal touch<br>
                    • Test different tones for best results<br>
                    • Combine multiple tools for a complete workflow<br>
                    • Re-generate for different variations
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Regenerate suggestion
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.info("🔄 **Want different results?** Change the tone, language, or rephrase your topic and click Generate again!")

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

        # Detailed error handling
        error_msg = str(e).lower()

        if "404" in error_msg or "not found" in error_msg or "model" in error_msg:
            st.markdown("""
            <div style='background: #1a1a2e; padding: 20px; border-radius: 12px; border-left: 4px solid #FF0000; margin: 10px 0;'>
                <h4 style='color: #FF6B6B;'>🤖 Model Not Available:</h4>
                <ul style='color: #ccc; line-height: 2;'>
                    <li>The Gemini model version may have changed</li>
                    <li>Try updating to the latest model name</li>
                    <li>Check <a href='https://ai.google.dev/models/gemini' target='_blank' style='color: #FF6B6B;'>Google AI Models</a> for available versions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        elif "api" in error_msg or "key" in error_msg or "invalid" in error_msg:
            st.markdown("""
            <div style='background: #1a1a2e; padding: 20px; border-radius: 12px; border-left: 4px solid #FF0000; margin: 10px 0;'>
                <h4 style='color: #FF6B6B;'>🔑 API Key Issue:</h4>
                <ul style='color: #ccc; line-height: 2;'>
                    <li>Make sure your API key is correct (no extra spaces)</li>
                    <li>Try generating a new key from <a href='https://aistudio.google.com' target='_blank' style='color: #FF6B6B;'>aistudio.google.com</a></li>
                    <li>Ensure you haven't exceeded the free quota</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        elif "quota" in error_msg or "limit" in error_msg or "rate" in error_msg:
            st.markdown("""
            <div style='background: #1a1a2e; padding: 20px; border-radius: 12px; border-left: 4px solid #FFB800; margin: 10px 0;'>
                <h4 style='color: #FFB800;'>⏳ Rate Limit Reached:</h4>
                <ul style='color: #ccc; line-height: 2;'>
                    <li>You've made too many requests in a short time</li>
                    <li>Wait 1-2 minutes and try again</li>
                    <li>The free tier allows ~60 requests per minute</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        elif "network" in error_msg or "connection" in error_msg:
            st.markdown("""
            <div style='background: #1a1a2e; padding: 20px; border-radius: 12px; border-left: 4px solid #4A90D9; margin: 10px 0;'>
                <h4 style='color: #4A90D9;'>🌐 Connection Issue:</h4>
                <ul style='color: #ccc; line-height: 2;'>
                    <li>Check your internet connection</li>
                    <li>Try refreshing the page</li>
                    <li>If using VPN, try disabling it</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("💡 Try refreshing the page and attempting again. If the issue persists, check your API key and internet connection.")
