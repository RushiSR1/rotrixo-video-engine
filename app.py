import os
import sys
import time
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Bridge Streamlit Cloud Secrets into environment variables if available
try:
    if hasattr(st, "secrets"):
        for key in ["GEMINI_API_KEY", "PIXABAY_API_KEY", "PEXELS_API_KEY", "ELEVENLABS_API_KEY", "BRAND_TITLE", "BRAND_HANDLE"]:
            if key in st.secrets and not os.getenv(key):
                os.environ[key] = str(st.secrets[key])
except Exception:
    pass

import config
from main import generate_video
from src.trend_scout import ViralTrendScout

# Streamlit Page Configuration
st.set_page_config(
    page_title="Rotrixo • Autonomous AI Video Engine",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Cyberpunk / Sleek B2B SaaS)
st.markdown("""
<style>
    .main {
        background-color: #05060A;
    }
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(16, 245, 160, 0.06) 0%, transparent 40%),
                    #05060A;
        color: #F8FAFC;
    }
    .metric-card {
        background: rgba(14, 18, 29, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .gradient-title {
        background: linear-gradient(135deg, #A855F7 0%, #10F5A0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🪐 Rotrixo Engine")
    st.markdown("**1-Click Autonomous Video Pipeline**")
    st.markdown("---")
    
    st.markdown("#### 🔑 API Status")
    has_gemini = bool(os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY)
    has_pixabay = bool(os.getenv("PIXABAY_API_KEY") or config.PIXABAY_API_KEY)
    
    st.write(f"• **Gemini API:** {'🟢 Connected' if has_gemini else '🟡 Free Tier / Fallback'}")
    st.write(f"• **Pixabay API:** {'🟢 Connected' if has_pixabay else '🟡 Fallback Mode'}")
    st.write(f"• **Edge-TTS Voice:** 🟢 Ready (en-US Neural)")
    
    st.markdown("---")
    st.markdown("#### ⚙️ Configuration")
    brand_title = st.text_input("Brand Title", value=config.BRAND_TITLE)
    brand_handle = st.text_input("Brand Handle", value=config.BRAND_HANDLE)
    
    st.markdown("---")
    st.caption("Powered by Rotrixo AI • 100% Client-Owned Engine")

# Main Header
st.markdown("<h1 class='gradient-title'>Deploy 1-Click Autonomous AI Video Engine</h1>", unsafe_allow_html=True)
st.caption("Benchmark viral hooks, synthesize psychological scripts, and compile 1080x1920 MP4 vertical videos in under 60 seconds.")

# Tab Selection
tab1, tab2, tab3 = st.tabs([
    "🔥 1-Click Viral Remake (Recommended)",
    "✍️ Custom Topic Generation",
    "🔍 Live Viral Trend Scout"
])

scout = ViralTrendScout()

# Tab 1: Proven Viral Hits Database
with tab1:
    st.subheader("📚 Proven Viral Hits Database (500k - 48M Views)")
    st.write("Select a proven viral video to deconstruct, reverse-engineer, and generate an original 9:16 vertical short.")
    
    saved_trends = scout.load_saved_trends()
    
    if saved_trends:
        trend_titles = [f"[{t.get('formatted_views', '500K+')}] {t.get('title', 'Viral Video')}" for t in saved_trends]
        selected_idx = st.selectbox("Choose a viral blueprint:", range(len(trend_titles)), format_func=lambda i: trend_titles[i])
        
        selected_trend = saved_trends[selected_idx]
        
        # Display Research Preview Card
        with st.container():
            st.markdown(f"""
            <div class='metric-card'>
                <strong>🎬 Title:</strong> {selected_trend.get('title')}<br>
                <strong>🪝 3-Second Hook:</strong> {selected_trend.get('viral_hook', 'N/A')}<br>
                <strong>💡 Core Concept:</strong> {selected_trend.get('original_full_concept', selected_trend.get('core_problem', 'N/A'))}<br>
                <strong>🔗 Reference Link:</strong> <a href="{selected_trend.get('url', '#')}" target="_blank" style="color: #10F5A0;">View Original Video</a>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🚀 Render 1-Click Viral Remake (<60s)", type="primary", use_container_width=True):
            with st.status("⚡ Running Autonomous Video Pipeline...", expanded=True) as status:
                st.write("🔬 Deconstructing viral hooks & scientific mechanisms...")
                researched = scout.deep_research_viral_video(selected_trend)
                
                st.write("✍️ Synthesizing high-retention script with Gemini 2.0...")
                time.sleep(0.5)
                
                st.write("🎙️ Generating Microsoft Neural Edge-TTS voiceover...")
                st.write("🎞️ Aligning vertical B-roll footage and kinetic subtitle cards...")
                
                output_video = generate_video(research_context=researched)
                
                status.update(label="✅ Video Successfully Rendered!", state="complete", expanded=False)

            if output_video and Path(output_video).exists():
                st.success("🎉 Video generation completed successfully!")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.subheader("📱 Video Preview")
                    st.video(str(output_video))
                    
                    with open(output_video, "rb") as f:
                        st.download_button(
                            label="⬇️ Download 1080x1920 MP4 Video",
                            data=f,
                            file_name=Path(output_video).name,
                            mime="video/mp4",
                            use_container_width=True
                        )
                
                with col2:
                    st.subheader("📋 Ready-To-Upload Package")
                    info_file = Path(output_video).with_name(Path(output_video).stem.rsplit('_', 1)[0] + "_info.txt")
                    metadata_text = ""
                    if info_file.exists():
                        metadata_text = info_file.read_text(encoding="utf-8")
                    else:
                        metadata_text = f"TITLE: {selected_trend.get('title')}\n\nCAPTION: Stop letting poor sleep drain your daily energy. Follow for daily science-backed protocols!\n\nHASHTAGS: #sleep #sleepbetter #circadianrhythm #wellness #huberman #insomnia #healthtips #shorts #reels"
                    
                    st.text_area("Captions & Hashtags (Copy & Paste):", value=metadata_text, height=360)

# Tab 2: Custom Topic
with tab2:
    st.subheader("✍️ Enter Your Custom Niche Topic")
    custom_topic = st.text_input(
        "Enter sleep / wellness topic:",
        placeholder="e.g. Magnesium Glycinate vs Melatonin for Deep REM Sleep"
    )
    
    if st.button("⚡ Generate Custom Video", type="primary", use_container_width=True):
        if not custom_topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.status("⚡ Generating Custom Video Workflow...", expanded=True) as status:
                st.write(f"🧠 Synthesizing custom script for: '{custom_topic}'...")
                output_video = generate_video(topic=custom_topic.strip())
                status.update(label="✅ Render Complete!", state="complete", expanded=False)
                
            if output_video and Path(output_video).exists():
                st.success("🎉 Custom short generated successfully!")
                st.video(str(output_video))
                with open(output_video, "rb") as f:
                    st.download_button(
                        label="⬇️ Download MP4",
                        data=f,
                        file_name=Path(output_video).name,
                        mime="video/mp4"
                    )

# Tab 3: Live Scout
with tab3:
    st.subheader("🔍 Scout Live Trending Videos on YouTube Shorts")
    scout_query = st.text_input("Niche Search Keyword:", value="sleep hacks shorts")
    min_views = st.number_input("Minimum Views Threshold:", min_value=100000, max_value=50000000, value=500000, step=100000)
    
    if st.button("🔎 Scout Trending Videos"):
        with st.spinner("Scouting high-retention shorts across YouTube..."):
            live_scouted = scout.scout_viral_videos(query=scout_query, min_views=min_views, max_results=4)
            if live_scouted:
                st.session_state["live_scouted"] = live_scouted
                st.success(f"Discovered {len(live_scouted)} viral shorts!")
            else:
                st.info("No new live videos found matching criteria. Fallback to saved database.")

    if "live_scouted" in st.session_state and st.session_state["live_scouted"]:
        scouted_list = st.session_state["live_scouted"]
        for idx, item in enumerate(scouted_list):
            st.markdown(f"""
            <div class='metric-card'>
                <h4>{idx+1}. [{item.get('formatted_views')}] {item.get('title')}</h4>
                <p><strong>Channel:</strong> {item.get('channel')} | <strong>Hook:</strong> {item.get('viral_hook')}</p>
                <a href='{item.get('url')}' target='_blank' style='color:#10F5A0;'>Watch Source Video</a>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Recreate Video #{idx+1}", key=f"rec_{idx}"):
                with st.spinner("Researching & Rendering..."):
                    researched = scout.deep_research_viral_video(item)
                    out = generate_video(research_context=researched)
                    if out and Path(out).exists():
                        st.video(str(out))

