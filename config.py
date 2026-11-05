import os
from pathlib import Path
from dotenv import load_dotenv
import imageio_ffmpeg

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Bridge Streamlit Cloud Secrets if running on share.streamlit.io
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for key in ["GEMINI_API_KEY", "PIXABAY_API_KEY", "PEXELS_API_KEY", "ELEVENLABS_API_KEY"]:
            if key in st.secrets and not os.getenv(key):
                os.environ[key] = str(st.secrets[key])
except Exception:
    pass

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "").strip()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB").split(",")[0].strip() # Adam (Deep, Authoritative)

# Voice configuration (Edge-TTS)
VOICE_NAME = os.getenv("VOICE_NAME", "en-US-ChristopherNeural").strip()
VOICE_RATE = "-4%"   # Slightly calmer pace for sleep/wellness content
VOICE_PITCH = "-2Hz" # Slightly deeper tone for calm relaxation

# Branding configuration
BRAND_TITLE = os.getenv("BRAND_TITLE", "SLEEP SCIENCE LAB").strip()
BRAND_HANDLE = os.getenv("BRAND_HANDLE", "@SLEEPHACKS").strip()

# Video specifications (Vertical 9:16)
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))

# Subtitle styling configuration
SUBTITLE_FONT = "Segoe UI"
SUBTITLE_FONT_SIZE = 19
SUBTITLE_PRIMARY_COLOR = "&H00FFFFFF"   # Crisp White text
SUBTITLE_HIGHLIGHT_COLOR = "&H0000FFFF" # Vivid Yellow highlight for key words
SUBTITLE_OUTLINE_COLOR = "&H00000000"   # Black outline
SUBTITLE_OUTLINE_WIDTH = 3
SUBTITLE_MARGIN_V = 220                 # Distance from bottom (safe area for TikTok/Reels)

# Directory paths
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
CLIPS_DIR = ASSETS_DIR / "clips"
AI_ART_DIR = ASSETS_DIR / "ai_art"
GRAPHICS_DIR = ASSETS_DIR / "graphics"
SFX_DIR = ASSETS_DIR / "sfx"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Ensure directories exist
for folder in [ASSETS_DIR, MUSIC_DIR, CLIPS_DIR, AI_ART_DIR, GRAPHICS_DIR, SFX_DIR, OUTPUT_DIR, TEMP_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

def get_daily_output_dir() -> Path:
    """Returns a date-based subfolder inside OUTPUT_DIR (e.g. output/2026-10-24/)."""
    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_dir = OUTPUT_DIR / today_str
    daily_dir.mkdir(parents=True, exist_ok=True)
    return daily_dir

# Locate FFmpeg binary automatically
try:
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception as e:
    FFMPEG_PATH = "ffmpeg"
