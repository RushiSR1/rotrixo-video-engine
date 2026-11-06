import os
import sys
import time
import re
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from src.script_agent import ScriptAgent
from src.voice_agent import VoiceAgent
from src.video_fetcher import VideoFetcher
from src.subtitle_engine import SubtitleEngine
from src.music_manager import MusicManager
from src.video_composer import VideoComposer
from src.trend_scout import ViralTrendScout
from src.graphics_engine import GraphicsEngine

BANNER = """
========================================================================
   🌙 BioSlumber VIRAL SHORTS & REELS AI AGENT (HIGH-GROWTH PIPELINE)
========================================================================
   Build-to-Grow Viral Engine:
   Full Video Deconstruction -> Hook Reverse Engineering -> 3D AI Video
========================================================================
"""

def generate_video(
    topic: str = "",
    context_hook: str = "",
    research_context: Optional[Dict[str, Any]] = None
) -> Optional[Path]:
    """Orchestrates the entire video generation lifecycle."""
    print("\n" + "="*65)
    target_name = research_context.get("title") if research_context else (topic or "Auto Viral Topic")
    print(f"[*] INITIATING AGENT PIPELINE FOR: '{target_name}'")

    if research_context:
        print("\n" + "-"*65)
        print("📊 DEEP VIRAL RESEARCH BREAKDOWN (REMAKING ORIGINAL VIDEO):")
        print("-"*65)
        print(f"🎬 Original Video   : {research_context.get('title')}")
        if research_context.get('channel'):
            print(f"📺 Channel & Views  : {research_context.get('channel')} ({research_context.get('formatted_views', '')})")
        if research_context.get('original_full_concept'):
            print(f"\n💡 Full Original Video Concept:\n   {research_context.get('original_full_concept')}")
        if research_context.get('viral_hook'):
            print(f"\n🪝 3-Second Viral Hook Component:\n   {research_context.get('viral_hook')}")
        if research_context.get('core_problem'):
            print(f"\n⚠️ Core Problem Addressed:\n   {research_context.get('core_problem')}")
        if research_context.get('scientific_mechanism'):
            print(f"\n🧬 Underlying Scientific Mechanism:\n   {research_context.get('scientific_mechanism')}")
        if research_context.get('actionable_hack'):
            print(f"\n🛠️ Actionable Hack / Solution:\n   {research_context.get('actionable_hack')}")
        if research_context.get('remake_strategy'):
            print(f"\n🚀 BioSlumber Remake Strategy:\n   {research_context.get('remake_strategy')}")
        print("-"*65)
    elif context_hook:
        print(f"[*] VIRAL HOOK ANGLE: {context_hook}")
    print("="*65)

    start_time = time.time()

    # 1. Generate Script (remaking the exact viral video)
    script_agent = ScriptAgent()
    script_input = research_context if research_context else (f"{topic}. Hook angle: {context_hook}" if context_hook else topic)
    script_data = script_agent.generate_script(script_input)
    title = script_data.get("title", "Sleep Secret")
    scenes = script_data.get("scenes", [])
    full_narration = script_agent.get_full_script_text(script_data)

    print(f"\n[SCRIPT] SCRIPT GENERATED: '{title}'")
    print(f"Scenes count: {len(scenes)}")
    for i, s in enumerate(scenes):
        card_info = f" [HUD: {s['graphic_card']['title']}]" if s.get("graphic_card") else ""
        print(f"   Scene {i+1}: [{s.get('visual_keyword')}]{card_info} -> {s.get('narration')[:60]}...")

    # 2. Generate Voiceover and Timestamp Boundaries
    voice_agent = VoiceAgent()
    voice_file = config.TEMP_DIR / f"voice_{int(time.time())}.mp3"
    cues = voice_agent.generate_speech(full_narration, voice_file)

    if not cues:
        print("[Error] Failed to generate voiceover cues.")
        return None

    # Measure exact audio file duration with composer to prevent video/audio desync
    composer = VideoComposer()
    actual_audio_dur = composer._get_audio_duration(voice_file)
    if cues and actual_audio_dur > cues[-1]["end"]:
        # Ensure final subtitles and visuals stretch smoothly until audio track concludes
        cues[-1]["end"] = max(cues[-1]["end"], actual_audio_dur)
    
    total_voice_duration = max(cues[-1]["end"] if cues else 0.0, actual_audio_dur)
    print(f"[VOICE] VOICEOVER COMPLETED: Duration = {total_voice_duration:.2f} seconds (Audio file: {actual_audio_dur:.2f}s)")

    # 3. Fetch Diverse, Topic-Specific B-Roll Clips for Each Scene (Zero Footage Repetition)
    video_fetcher = VideoFetcher()
    scene_clips = []
    
    num_scenes = len(scenes)
    duration_per_scene = total_voice_duration / num_scenes

    print(f"\n[B-ROLL] FETCHING TOPIC-SPECIFIC CLIPS ({num_scenes} scenes)...")
    for idx, scene in enumerate(scenes):
        keyword = scene.get("visual_keyword", "deep sleep cozy bedroom night")
        clip_path = video_fetcher.fetch_clip_for_scene(
            scene_index=idx,
            keyword=keyword,
            duration=duration_per_scene,
            narration=scene.get("narration", "")
        )
        scene_clips.append(clip_path)

    # 4. Generate Topic-Specific Floating Graphic HUD Cards
    graphics_engine = GraphicsEngine()
    hud_cards = graphics_engine.build_dynamic_cards_for_script(script_data, cues)

    # 5. Generate BIG BOLD COLOURFUL Subtitles (ASS)
    subtitle_engine = SubtitleEngine()
    subtitle_file = config.TEMP_DIR / f"subs_{int(time.time())}.ass"
    subtitle_engine.generate_ass_subtitles(cues, subtitle_file)

    # 6. Get Background Music
    music_mgr = MusicManager()
    bgm_file = music_mgr.get_background_music(target_duration=total_voice_duration)

    # 7. Compose Final Video in Date-Wise Output Directory
    daily_output_dir = config.get_daily_output_dir()
    safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title).strip('_')[:40]
    output_filename = daily_output_dir / f"{safe_title}_{int(time.time())}.mp4"

    composer = VideoComposer()
    final_video = composer.compose(
        scene_clips=scene_clips,
        voice_path=voice_file,
        bgm_path=bgm_file,
        subtitle_path=subtitle_file,
        output_path=output_filename,
        hud_cards=hud_cards
    )

    # 8. Save Upload Package (Metadata & Research Info alongside the video)
    upload_info_path = daily_output_dir / f"{safe_title}_info.txt"
    with open(upload_info_path, "w", encoding="utf-8") as f:
        f.write(f"TITLE: {title}\n")
        f.write(f"GENERATION DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("YOUTUBE / INSTAGRAM CAPTION:\n")
        f.write(f"Stop letting poor sleep drain your daily energy. Try this science-backed protocol tonight! Follow @bioslumber for daily sleep optimization.\n\n")
        f.write("HASHTAGS:\n")
        f.write("#sleep #sleepbetter #circadianrhythm #wellness #huberman #insomnia #healthtips #remcycle #shorts #reels\n\n")
        if research_context:
            f.write("ORIGINAL VIRAL RESEARCH:\n")
            f.write(f"- Source Video: {research_context.get('url', '')}\n")
            f.write(f"- Hook: {research_context.get('viral_hook', '')}\n")
            f.write(f"- Core Problem: {research_context.get('core_problem', '')}\n")
            f.write(f"- Mechanism: {research_context.get('scientific_mechanism', '')}\n")
            f.write(f"- Hack: {research_context.get('actionable_hack', '')}\n")

    elapsed = time.time() - start_time
    print("\n" + "="*65)
    print("✨ [SUCCESS] VIDEO SUCCESSFULLY GENERATED IN DATE-WISE FOLDER!")
    print("="*65)
    print(f"File Location : {final_video}")
    print(f"Date Folder   : {daily_output_dir.name}")
    print(f"Total Duration: {total_voice_duration:.1f} seconds")
    print(f"File Size     : {final_video.stat().st_size / (1024*1024):.2f} MB")
    print(f"Time Elapsed  : {elapsed:.1f} seconds")
    print(f"Upload Info   : {upload_info_path.name}")
    print("\n[METADATA] READY-TO-PASTE CAPTIONS & HASHTAGS:")
    print(f"Title: {title}")
    print("Caption: Stop letting poor sleep drain your daily focus. Follow for science-backed sleep hacks!")
    print("Hashtags: #sleep #sleepbetter #circadianrhythm #wellness #huberman #insomnia #healthtips #remcycle #shorts #reels")
    print("="*65 + "\n")

    return final_video

def main():
    print(BANNER)
    scout = ViralTrendScout()

    print("Select an option:")
    print("1. Scout Live Viral Trends (500k+ Views) & Full Video Deconstruction (Recommended)")
    print("2. Choose from Proven Viral Hits Database (500k to 48.5M Views)")
    print("3. Enter a Custom Sleep Topic")
    print("4. View Scouted Viral Trends & Source Video Links")
    print("5. 1-Click Fast Demo Video")
    print("6. Exit")

    choice = input("\nEnter choice (1-6) [default: 1]: ").strip() or "1"

    if choice == "1":
        query = input("\nEnter niche keyword to scout [default: 'sleep hacks shorts']: ").strip() or "sleep hacks shorts"
        print(f"\n[Scout] Hunting viral videos with minimum 500,000+ views for '{query}'...")
        scouted = scout.scout_viral_videos(query=query, min_views=500000, max_results=5)

        print("\n" + "="*65)
        print("🔥 TOP VIRAL SLEEP HITS DISCOVERED IN THE MARKET:")
        print("="*65)
        for idx, item in enumerate(scouted, 1):
            print(f"{idx}. [{item.get('formatted_views')}] {item.get('title')}")
            print(f"   Hook: {item.get('viral_hook')}")
            print(f"   URL : {item.get('url')}\n")

        pick = input(f"Select which viral hit to recreate [1-{len(scouted)}] (or 'A' for Auto #1) [default: A]: ").strip().upper() or "A"
        if pick == "A":
            selected = scouted[0]
        else:
            try:
                selected = scouted[int(pick) - 1]
            except Exception:
                selected = scouted[0]

        # Perform Deep Reverse-Engineering Research on the chosen viral video
        researched = scout.deep_research_viral_video(selected)
        generate_video(research_context=researched)

    elif choice == "2":
        saved = scout.load_saved_trends()
        print("\n" + "="*65)
        print("📚 PROVEN VIRAL SLEEP HITS DATABASE (FULL DECONSTRUCTIONS):")
        print("="*65)
        for idx, item in enumerate(saved, 1):
            print(f"{idx}. [{item.get('formatted_views')}] {item.get('title')}")
            if item.get("original_full_concept"):
                print(f"   Concept: {item.get('original_full_concept')[:90]}...")
            print(f"   Hook   : {item.get('viral_hook', '')}")
            print(f"   URL    : {item.get('url')}\n")

        pick = input(f"Select video to recreate [1-{len(saved)}] [default: 1]: ").strip() or "1"
        try:
            selected = saved[int(pick) - 1]
        except Exception:
            selected = saved[0]

        researched = scout.deep_research_viral_video(selected)
        generate_video(research_context=researched)

    elif choice == "3":
        topic = input("\nEnter your custom sleep topic: ").strip()
        generate_video(topic)

    elif choice == "4":
        saved = scout.load_saved_trends()
        print("\n" + "="*65)
        print(f"📁 SCOUTED VIRAL VIDEOS DATABASE ({len(saved)} Videos):")
        print("="*65)
        for idx, item in enumerate(saved, 1):
            print(f"{idx}. [{item.get('formatted_views')}] {item.get('title')}")
            print(f"   Channel: {item.get('channel')}")
            if item.get("original_full_concept"):
                print(f"   Concept: {item.get('original_full_concept')[:100]}...")
            print(f"   Hook   : {item.get('viral_hook')}")
            print(f"   Link   : {item.get('url')}\n")
        print(f"Database stored locally at: data/viral_trends.json\n")

    elif choice == "5":
        saved = scout.load_saved_trends()
        top_hit = saved[0]
        researched = scout.deep_research_viral_video(top_hit)
        generate_video(research_context=researched)

    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
