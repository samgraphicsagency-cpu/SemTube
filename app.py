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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

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

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #111128 100%);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FF6B6B;
    }

    .tool-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FF6B6B;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 107, 107, 0.2);
        margin-bottom: 15px;
    }

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

    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #FF6B6B !important;
    }

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

    .loading-text {
        text-align: center;
        font-size: 1.2rem;
        color: #FF6B6B;
        font-weight: 600;
    }

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

    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "Gemini API Key:",
        type="password",
        help="🆓 Get your FREE API key from: aistudio.google.com",
        placeholder="Paste your API key here..."
    )

    if api_key:
        st.success("✅ API Key Connected")
    else:
        st.warning("⚠️ Enter API Key to start")

    st.markdown("---")

    st.markdown("### 📊 System Status")

    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.metric("Tools", "10", "Active")
    with status_col2:
        st.metric("Cost", "$0", "Free")

    st.markdown("---")

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

st.markdown("<div style='text-align: center; margin-bottom: 5px;'><span class='brand-badge'>🎬 SEMTUBE AI</span></div>", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">SemTube</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Complete AI-Powered YouTube Automation System — 10 Pro Tools, 100% Free Forever</p>', unsafe_allow_html=True)

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
        # Configure Gemini AI
        genai.configure(api_key=api_key)
        
        # ✅ FIXED: Use correct model name with fallback
        model = None
        model_options = [
            "gemini-1.5-flash",
            "gemini-1.5-pro", 
            "gemini-pro",
            "gemini-1.0-pro"
        ]
        
        for model_name in model_options:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple request
                test_response = model.generate_content("Hi")
                if test_response:
                    break
            except:
                continue
        
        if model is None:
            st.error("❌ Could not connect to Gemini AI. Please check your API key.")
            st.stop()

        # ============================================
        # 📋 PROMPT ENGINEERING FOR EACH TOOL
        # ============================================

        prompt = ""

        if selected_tool == "🔥 Viral Video Ideas Generator":
            prompt = f"""You are a top YouTube strategist with 10+ years of experience.

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

Format each idea clearly with numbers 1-10."""

        elif selected_tool == "📜 Full Video Script Writer":
            prompt = f"""You are a professional YouTube scriptwriter.

Write a complete YouTube video script about: '{user_input}'

Target Audience: {target_audience}
Tone: {tone}  
Language: {language}
Length: {length} words

STRUCTURE:
🎣 **HOOK (0-5 seconds)**: Attention-grabbing opening
📢 **INTRO (5-30 seconds)**: Introduce topic, state problem, build credibility
📚 **MAIN CONTENT**: 3-5 clear sections with examples
🔔 **CALL TO ACTION**: Subscribe, like, comment prompts
👋 **OUTRO**: Summary and closing

Use [B-ROLL], [SHOW ON SCREEN], [PAUSE] markers."""

        elif selected_tool == "🏷️ Title Generator (10 Variants)":
            prompt = f"""You are a YouTube SEO expert.

Generate 10 high-CTR YouTube video titles about: '{user_input}'

Language: {language}
Tone: {tone}

Requirements:
✅ Under 60 characters
✅ Include power words
✅ Use numbers where possible
✅ Create curiosity gap

Categories:
1-2: Number-based
3-4: How-to
5-6: Curiosity/Mystery
7-8: Urgency
9-10: Bold/Controversial

For each: Rate CTR potential ⭐⭐⭐⭐⭐"""

        elif selected_tool == "📝 SEO Description Writer":
            prompt = f"""You are a YouTube SEO specialist.

Write an SEO-optimized description for: '{user_input}'

Language: {language}
Tone: {tone}

Include:
📌 First 2 lines with keyword (appears in search)
📝 Detailed overview paragraph
⏱️ Timestamps section
🔗 Resources/Links placeholders
📱 Social media placeholders
🏷️ 5 relevant hashtags"""

        elif selected_tool == "🔖 Trending Tags Finder":
            prompt = f"""You are a YouTube algorithm expert.

Generate 30 tags for a video about: '{user_input}'

Categories:
🔵 BROAD TAGS (10): High volume, 1-2 words
🟡 MEDIUM-SPECIFIC (10): Moderate volume, 2-4 words
🟢 LONG-TAIL (10): Low competition, 4-7 words

Rules: Under 30 chars each, no duplicates

Also provide:
📊 Tag Strategy Tip
⚠️ 3 Tags to AVOID"""

        elif selected_tool == "📊 Keyword Research Tool":
            prompt = f"""You are a YouTube keyword research expert.

Research keywords for: '{user_input}'

Language: {language}
Target Audience: {target_audience}

Provide:
📈 5 HIGH VOLUME keywords with sample titles
📉 5 LOW COMPETITION keywords with sample titles
🎯 5 LONG-TAIL keywords with search intent
🔥 3 TRENDING keywords
💡 2 CONTENT GAP keywords

📋 Strategy recommendation paragraph"""

        elif selected_tool == "🎤 Hook Generator (First 5 Sec)":
            prompt = f"""You are a YouTube retention expert.

Generate 10 powerful hooks (first 5 seconds) for: '{user_input}'

Tone: {tone}
Language: {language}

Categories:
🤯 SHOCK HOOKS (2)
❓ QUESTION HOOKS (2)
💰 VALUE HOOKS (2)
📖 STORY HOOKS (2)
⚡ BOLD CLAIM HOOKS (2)

For each:
🎭 Delivery Tip
📊 Retention Impact ⭐⭐⭐⭐⭐"""

        elif selected_tool == "🎯 Thumbnail Text Suggestions":
            prompt = f"""You are a thumbnail design expert.

Generate 10 thumbnail text options for: '{user_input}'

Tone: {tone}

Requirements:
- Maximum 3-4 WORDS
- Must be readable on phone
- Create curiosity/emotion

Categories:
😱 SHOCK/EMOTION (3)
🔢 NUMBER-BASED (3)
❓ CURIOSITY (2)
🏆 VALUE/BENEFIT (2)

For each suggest:
🎨 Color
📍 Position
✨ Style"""

        elif selected_tool == "💬 Comment Reply Generator":
            prompt = f"""You are a YouTube community manager.

Generate comment reply templates for: '{user_input}'

Tone: {tone}
Language: {language}

Categories:
😊 POSITIVE COMMENTS (4 replies)
❓ QUESTION COMMENTS (4 replies)
😤 CRITICAL COMMENTS (3 replies)
🔥 ENGAGEMENT COMMENTS (3 replies)

📌 Also write 1 perfect PINNED COMMENT"""

        elif selected_tool == "📹 YouTube Video Summarizer":
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', user_input)

            if not video_id_match:
                st.error("❌ Invalid YouTube URL!")
                st.stop()

            video_id = video_id_match.group(1)

            with st.spinner("📥 Downloading transcript..."):
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    full_text = " ".join([t['text'] for t in transcript_list])

                    try:
                        yt = YouTube(user_input)
                        video_title = yt.title
                        video_author = yt.author
                    except:
                        video_title = "Unknown"
                        video_author = "Unknown"

                    st.info(f"📹 Video: {video_title} | 👤 Channel: {video_author}")

                except Exception as e:
                    st.error(f"❌ Could not get transcript: {str(e)}")
                    st.stop()

            prompt = f"""Summarize this YouTube video:

VIDEO: {video_title}
CHANNEL: {video_author}
Language: {language}

TRANSCRIPT:
{full_text[:5000]}

Provide:
📋 QUICK SUMMARY (3-4 sentences)
🔑 KEY POINTS (5-7 bullet points)
💡 MAIN INSIGHT
👥 WHO SHOULD WATCH
✅ ACTION ITEMS (3-5)
⭐ QUALITY RATING (1-5 stars)"""

        # Generate with AI
        progress_placeholder = st.empty()
        progress_bar = st.progress(0)

        messages = [
            "🧠 Initializing SemTube AI...",
            "🔍 Analyzing request...",
            "📊 Processing with Gemini...",
            "✍️ Generating content...",
            "✨ Polishing output...",
            "🎯 Almost done..."
        ]

        for i, msg in enumerate(messages):
            progress_placeholder.markdown(f'<p class="loading-text">{msg}</p>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) * 16)
            time.sleep(0.4)

        response = model.generate_content(prompt)

        progress_bar.progress(100)
        progress_placeholder.empty()
        progress_bar.empty()

        # Display Results
        st.markdown("""
        <div class="success-banner">
            ✅ Content Generated Successfully!
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='text-align: center; margin: 10px 0;'>
            <span style='background: rgba(255,0,0,0.1); color: #FF6B6B; padding: 5px 15px; 
                        border-radius: 20px; font-size: 0.9rem; font-weight: 600;'>
                {selected_tool}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 Your Generated Content:")

        formatted_text = response.text.replace('\n', '<br>')

        st.markdown(f"""
        <div class="result-box">
            {formatted_text}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📥 Export Options:")

        export_col1, export_col2 = st.columns(2)

        with export_col1:
            st.text_area(
                "📋 Copy-Paste Version:",
                response.text,
                height=300
            )

        with export_col2:
            st.download_button(
                label="📥 Download as .TXT",
                data=response.text,
                file_name=f"SemTube_Output.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.download_button(
                label="📄 Download as .MD",
                data=f"# SemTube AI Output\n\n{response.text}",
                file_name=f"SemTube_Output.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.info("🔄 Want different results? Change options and click Generate again!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        
        if "404" in str(e) or "not found" in str(e).lower():
            st.warning("🔧 Model issue detected. Please try again.")
        elif "quota" in str(e).lower() or "limit" in str(e).lower():
            st.warning("⏳ Rate limit reached. Wait 1 minute and try again.")
        else:
            st.info("💡 Check your API key and try again.")


# ============================================
# 📊 WORKFLOW GUIDE
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

with st.expander("📋 Complete YouTube Workflow Guide", expanded=False):
    st.markdown("""
    ### 🎬 SemTube Complete Video Production Workflow

    | Step | Tool | Output |
    |------|------|--------|
    | 1️⃣ | Viral Video Ideas | 10 trending ideas |
    | 2️⃣ | Keyword Research | Best keywords |
    | 3️⃣ | Full Script Writer | Complete script |
    | 4️⃣ | Hook Generator | Perfect opening |
    | 5️⃣ | *Record Video* | Your content |
    | 6️⃣ | Thumbnail Text | Bold text options |
    | 7️⃣ | Title Generator | 10 title options |
    | 8️⃣ | SEO Description | Optimized description |
    | 9️⃣ | Trending Tags | 30 tags |
    | 🔟 | Comment Replies | Engagement templates |
    """)


# ============================================
# 🦶 FOOTER
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-section">
    <div style='font-size: 2rem; margin-bottom: 10px;'>🎬</div>
    <h3>SemTube — AI YouTube Empire</h3>
    <p>
        ✅ 10 Pro Tools | ✅ Unlimited Use | ✅ 100% Free Forever
    </p>
    <p style='font-size: 0.85rem; color: #555;'>
        Powered by Google Gemini AI • Made with ❤️ by SemTube Team
    </p>
    <p style='font-size: 0.75rem; color: #444;'>
        © 2025 SemTube v2.0
    </p>
</div>
""", unsafe_allow_html=True)
