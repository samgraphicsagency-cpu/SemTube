import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import re

# Page Configuration
st.set_page_config(
    page_title="🚀 My AI Tube Empire", 
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF0000, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF0000, #FF6B6B);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px 30px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - API Key Management
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=100)
    st.title("⚙️ Control Panel")
    
    api_key = st.text_input(
        "🔑 Enter Gemini API Key:", 
        type="password",
        help="Get free API from: aistudio.google.com"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard")
    st.success("✅ System Online")
    st.info("💡 10 AI Tools Active")
    
    st.markdown("---")
    st.markdown("### 📚 Quick Guide")
    st.write("1️⃣ Get API Key from Google AI Studio")
    st.write("2️⃣ Paste it above")
    st.write("3️⃣ Select tool & generate!")
    st.write("4️⃣ Copy & use in YouTube")
    
    st.markdown("---")
    st.caption("Made with ❤️ by You")

# Main Header
st.markdown('<h1 class="main-header">🚀 MY AI TUBE EMPIRE</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Your Complete YouTube Automation System - 100% Free Forever</p>", unsafe_allow_html=True)

# Feature Selection
st.markdown("## 🎯 Choose Your AI Tool:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📝 Content Creation")
    tools_content = [
        "🔥 Viral Video Ideas Generator",
        "📜 Full Video Script Writer",
        "🎯 Thumbnail Text Suggestions",
        "💬 Comment Reply Generator"
    ]
    selected_tool = st.radio("", tools_content, key="content")

with col2:
    st.markdown("### 🔍 SEO & Optimization")
    tools_seo = [
        "🏷️ Title Generator (10 Variants)",
        "📝 SEO Description Writer",
        "🔖 Trending Tags Finder",
        "📊 Keyword Research Tool"
    ]
    if st.checkbox("Use SEO Tools"):
        selected_tool = st.radio("", tools_seo, key="seo")

with col3:
    st.markdown("### 🎬 Advanced Tools")
    tools_advanced = [
        "📹 YouTube Video Summarizer",
        "🎤 Hook Generator (First 5 Sec)"
    ]
    if st.checkbox("Use Advanced Tools"):
        selected_tool = st.radio("", tools_advanced, key="advanced")

# Input Section
st.markdown("---")
st.markdown("## ✍️ Your Input:")

# Different inputs based on tool
if selected_tool == "📹 YouTube Video Summarizer":
    user_input = st.text_input(
        "Enter YouTube Video URL:",
        placeholder="https://www.youtube.com/watch?v=xxxxx"
    )
else:
    user_input = st.text_input(
        "Enter Your Topic/Niche/Keyword:",
        placeholder="e.g., How to make money with AI in 2025"
    )

# Additional Options
with st.expander("⚙️ Advanced Options (Optional)"):
    tone = st.selectbox("Select Tone:", ["Professional", "Casual", "Funny", "Educational", "Motivational"])
    language = st.selectbox("Language:", ["English", "Hinglish", "Bengali"])
    length = st.slider("Content Length:", 50, 500, 200)

# Generate Button
st.markdown("---")
generate_col1, generate_col2, generate_col3 = st.columns([1,2,1])

with generate_col2:
    generate_btn = st.button("🚀 GENERATE WITH AI", use_container_width=True)

# AI Generation Logic
if generate_btn:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar!")
        st.stop()
    
    if not user_input:
        st.warning("⚠️ Please enter a topic or URL!")
        st.stop()
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt Engineering based on selected tool
        
        if selected_tool == "🔥 Viral Video Ideas Generator":
            prompt = f"""Act as a YouTube strategist with 10 years experience. 
            Generate 10 highly viral and unique video ideas about '{user_input}' in {language} language with {tone} tone.
            
            For each idea provide:
            1. Catchy Title
            2. Brief Description (2 lines)
            3. Why it will go viral (1 line)
            
            Format as numbered list."""
        
        elif selected_tool == "📜 Full Video Script Writer":
            prompt = f"""Write a complete, engaging YouTube video script about '{user_input}' in {language} language with {tone} tone.
            
            Structure:
            1. **HOOK (0-5 sec)**: Attention-grabbing opening
            2. **INTRO (5-30 sec)**: Problem statement
            3. **MAIN CONTENT**: {length} words with clear points
            4. **CALL TO ACTION**: Subscribe/Like reminder
            5. **OUTRO**: Closing statement
            
            Make it conversational and engaging!"""
        
        elif selected_tool == "🏷️ Title Generator (10 Variants)":
            prompt = f"""Act as YouTube SEO expert. Generate 10 high-CTR, click-worthy titles about '{user_input}'.
            
            Requirements:
            - Under 60 characters
            - Include power words (Free, Secret, Proven, etc.)
            - Use numbers where possible
            - Create curiosity gap
            - {tone} tone in {language}
            
            Format: Just list titles numbered 1-10."""
        
        elif selected_tool == "📝 SEO Description Writer":
            prompt = f"""Write a YouTube video description optimized for SEO about '{user_input}'.
            
            Include:
            1. **First Paragraph (150 chars)**: Hook with keyword
            2. **Second Paragraph**: Detailed explanation with keywords
            3. **Third Paragraph**: Call to action
            4. **Timestamps** (if applicable)
            5. **Social Links Section** (placeholder)
            6. **Hashtags** (5 relevant ones)
            
            Language: {language}, Tone: {tone}"""
        
        elif selected_tool == "🔖 Trending Tags Finder":
            prompt = f"""Act as YouTube algorithm expert. Generate 30 highly searched, trending tags for '{user_input}'.
            
            Include:
            - 10 broad tags
            - 10 medium-specific tags  
            - 10 long-tail keyword tags
            
            Format: Comma-separated list"""
        
        elif selected_tool == "📊 Keyword Research Tool":
            prompt = f"""Perform YouTube keyword research for '{user_input}'.
            
            Provide:
            1. **5 High Volume Keywords** (most searched)
            2. **5 Low Competition Keywords** (easier to rank)
            3. **5 Long-tail Keywords** (specific phrases)
            4. **Search Intent** for each category
            
            Format as organized lists."""
        
        elif selected_tool == "🎤 Hook Generator (First 5 Sec)":
            prompt = f"""Generate 10 powerful hooks (first 5 seconds) for a video about '{user_input}'.
            
            Each hook should:
            - Be 1-2 sentences max
            - Create curiosity/shock/value
            - Make viewer want to keep watching
            - Use {tone} tone in {language}
            
            Format: Numbered list 1-10."""
        
        elif selected_tool == "🎯 Thumbnail Text Suggestions":
            prompt = f"""Generate 10 thumbnail text options for '{user_input}'.
            
            Requirements:
            - Maximum 4 words each
            - Big, bold, readable
            - Create curiosity
            - Use power words
            - {tone} tone
            
            Format: Just list the text options."""
        
        elif selected_tool == "💬 Comment Reply Generator":
            prompt = f"""Generate 10 engaging comment reply templates for a YouTube video about '{user_input}'.
            
            Include replies for:
            - Positive comments (3)
            - Questions (3)
            - Criticism (2)
            - Generic engagement (2)
            
            Make them {tone} and in {language}."""
        
        elif selected_tool == "📹 YouTube Video Summarizer":
            # Extract video ID
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', user_input)
            if not video_id_match:
                st.error("Invalid YouTube URL!")
                st.stop()
            
            video_id = video_id_match.group(1)
            
            # Get transcript
            with st.spinner("📥 Downloading transcript..."):
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    full_text = " ".join([t['text'] for t in transcript])
                    
                    # Get video title
                    yt = YouTube(user_input)
                    video_title = yt.title
                    
                    st.info(f"📹 Video: {video_title}")
                    
                except:
                    st.error("❌ Transcript not available for this video!")
                    st.stop()
            
            prompt = f"""Summarize this YouTube video transcript in {language} language:
            
            VIDEO TITLE: {video_title}
            
            TRANSCRIPT:
            {full_text[:4000]}  # Limiting to avoid token limit
            
            Provide:
            1. **Quick Summary** (3 lines)
            2. **Key Points** (5-7 bullet points)
            3. **Main Takeaway** (1 sentence)
            4. **Who should watch** (1 line)"""
        
        # Generate with AI
        with st.spinner("🧠 AI is working its magic... Please wait..."):
            response = model.generate_content(prompt)
        
        # Display Results
        st.markdown("---")
        st.success("✅ Content Generated Successfully!")
        
        # Results in a nice box
        st.markdown("### 📋 Your Generated Content:")
        
        result_container = st.container()
        with result_container:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 30px; 
                        border-radius: 15px; 
                        color: white;
                        font-size: 1.1rem;
                        line-height: 1.8;'>
                {response.text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
        
        # Copy Button
        st.markdown("---")
        st.code(response.text, language="text")
        st.caption("☝️ Click the copy icon in top-right corner to copy")
        
        # Download Option
        st.download_button(
            label="📥 Download as Text File",
            data=response.text,
            file_name=f"{selected_tool.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("💡 Try checking your API key or internet connection")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <h3>🌟 Features You Just Unlocked:</h3>
    <p>✅ Unlimited AI Generations | ✅ 10 Professional Tools | ✅ 100% Free Forever</p>
    <p>✅ No Login Required | ✅ Privacy First | ✅ Lightning Fast</p>
    <br>
    <p style='font-size: 0.9rem;'>Made with ❤️ and 🤖 AI | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)