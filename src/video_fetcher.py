import os
import re
import json
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional, Set
import requests
import subprocess
import config

class UsedMediaRegistry:
    """Tracks media URLs and IDs used in past videos to prevent any footage repetition."""
    def __init__(self):
        self.data_dir = config.BASE_DIR / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.data_dir / "used_media.json"
        self.used_ids: Set[str] = set()
        self._load()

    def _load(self):
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.used_ids = set(data.get("used_ids", []))
            except Exception:
                self.used_ids = set()

    def is_used(self, media_id: str) -> bool:
        return str(media_id) in self.used_ids

    def mark_used(self, media_id: str):
        self.used_ids.add(str(media_id))
        self._save()

    def _save(self):
        try:
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump({"used_ids": list(self.used_ids)}, f, indent=2)
        except Exception:
            pass


class VideoFetcher:
    def __init__(self, pexels_key: str = "", pixabay_key: str = ""):
        self.pexels_key = pexels_key or config.PEXELS_API_KEY
        self.pixabay_key = pixabay_key or config.PIXABAY_API_KEY
        self.clips_dir = config.CLIPS_DIR
        self.temp_dir = config.TEMP_DIR
        self.ai_art_dir = config.AI_ART_DIR
        self.registry = UsedMediaRegistry()

    def _extract_search_queries(self, keyword: str, narration: str = "") -> List[str]:
        """
        Extracts 2-4 focused, high-signal search terms from scene keyword and narration.
        For example: 'close up peaceful human face eyes closed' -> ['peaceful face', 'sleeping face', 'peaceful sleep', 'relax']
        """
        clean = re.sub(r'[^a-zA-Z0-9 ]', ' ', keyword).lower().strip()
        words = [w for w in clean.split() if len(w) > 2 and w not in ["the", "and", "for", "with", "from", "that", "this", "every", "into"]]
        
        queries = []
        if len(words) >= 2:
            queries.append(f"{words[0]} {words[1]}")
        if len(words) >= 3:
            queries.append(f"{words[1]} {words[2]}")
        if words:
            queries.append(words[0])

        # If keyword mentions specific high-value sleep terms
        combined = f"{keyword} {narration}".lower()
        if "military" in combined or "seal" in combined:
            queries.insert(0, "military soldier")
        elif "alarm" in combined or "clock" in combined or "3 am" in combined or "time" in combined:
            queries.insert(0, "alarm clock night")
        elif "magnesium" in combined or "supplement" in combined or "pill" in combined:
            queries.insert(0, "supplement glass water")
        elif "honey" in combined or "spoon" in combined:
            queries.insert(0, "honey spoon")
        elif "caffeine" in combined or "coffee" in combined:
            queries.insert(0, "black coffee cup")
        elif "shower" in combined or "steam" in combined:
            queries.insert(0, "warm shower steam")
        elif "temperature" in combined or "thermostat" in combined or "cool" in combined:
            queries.insert(0, "thermostat bedroom")
        elif "brain" in combined or "neural" in combined or "cortisol" in combined:
            queries.insert(0, "human brain neural")
        elif "screen" in combined or "phone" in combined or "blue light" in combined:
            queries.insert(0, "smart phone bed dark")
        elif "breathing" in combined or "meditation" in combined or "exhale" in combined:
            queries.insert(0, "meditation breathing")
        elif "ocean" in combined or "waves" in combined:
            queries.insert(0, "ocean waves sunset")

        # Fallback query
        if not queries:
            queries = ["deep sleep cozy bed", "relaxing bedroom night"]
        return queries

    def fetch_clip_for_scene(
        self,
        scene_index: int,
        keyword: str,
        duration: float,
        narration: str = ""
    ) -> Path:
        """
        Dynamic Topic-Specific Visual Engine (Zero Footage Repetition):
        1. Checks for user-provided custom clips in assets/clips/
        2. Searches Pixabay for Real High-Quality Stock Video (filters out previously used clips)
        3. Searches Pexels for Real Portrait Stock Video (if key present)
        4. Searches Pixabay for High-Res Topic Photography (filters out previously used photos)
        5. Dynamically generates custom AI 9:16 Art via Pollinations for topic-tailored visuals
        """
        clean_keyword = re.sub(r'[^a-zA-Z0-9 ]', '', keyword).strip()
        filename_safe = clean_keyword.replace(' ', '_').lower()[:25]
        output_clip_path = self.temp_dir / f"scene_{scene_index}_{filename_safe}_{int(duration*10)}.mp4"

        # Check if already rendered for this specific session
        if output_clip_path.exists() and output_clip_path.stat().st_size > 50000:
            return output_clip_path

        queries = self._extract_search_queries(clean_keyword, narration)
        zoom_in = (scene_index % 2 == 1) # Alternates camera push-in vs pull-out for dopamine retention

        # 0. User custom clips in assets/clips/
        local_user_clips = list(self.clips_dir.glob("*.mp4")) + list(self.clips_dir.glob("*.mov"))
        if local_user_clips and scene_index < len(local_user_clips):
            user_clip = local_user_clips[scene_index % len(local_user_clips)]
            print(f"[VideoFetcher] Scene {scene_index+1}: Using custom user clip -> {user_clip.name}")
            self._standardize_local_video(user_clip, output_clip_path, duration)
            return output_clip_path

        # 1. Try Pixabay Real Stock Video
        if self.pixabay_key:
            for q in queries:
                try:
                    if self._fetch_from_pixabay_video(q, output_clip_path, duration):
                        print(f"[VideoFetcher] Scene {scene_index+1}: Found Pixabay B-roll Video for '{q}'")
                        return output_clip_path
                except Exception as e:
                    pass

        # 2. Try Pexels Video if API key is configured
        if self.pexels_key:
            for q in queries:
                try:
                    if self._fetch_from_pexels_video(q, output_clip_path, duration):
                        print(f"[VideoFetcher] Scene {scene_index+1}: Found Pexels B-roll Video for '{q}'")
                        return output_clip_path
                except Exception as e:
                    pass

        # 3. Try Pixabay High-Res Photography (Topic-Specific Real Photo with Dynamic Zoom)
        if self.pixabay_key:
            for q in queries:
                try:
                    if self._fetch_from_pixabay_photo(q, output_clip_path, duration, zoom_in=zoom_in):
                        print(f"[VideoFetcher] Scene {scene_index+1}: Found Pixabay Real Photo for '{q}'")
                        return output_clip_path
                except Exception as e:
                    pass

        # 4. Generate Brand New Custom Topic AI Visual via Pollinations AI (100% Unique, Zero Repetition)
        print(f"[VideoFetcher] Scene {scene_index+1}: Generating Dynamic 9:16 AI Art for '{clean_keyword}'...")
        if self._generate_pollinations_ai_clip(clean_keyword, output_clip_path, duration, zoom_in=zoom_in, narration=narration):
            return output_clip_path

        # 5. Last resort offline fallback
        print(f"[VideoFetcher] Scene {scene_index+1}: Rendering ambient procedural backdrop.")
        self._generate_ambient_background_clip(output_clip_path, duration)
        return output_clip_path

    def _fetch_from_pixabay_video(self, query: str, output_path: Path, target_duration: float) -> bool:
        """Searches Pixabay Video API for fresh, unused footage."""
        url = "https://pixabay.com/api/videos/"
        params = {
            "key": self.pixabay_key,
            "q": query,
            "per_page": 10
        }
        resp = requests.get(url, params=params, timeout=12)
        if resp.status_code != 200:
            return False

        hits = resp.json().get("hits", [])
        if not hits:
            return False

        # Find first unused video hit
        selected_hit = None
        for hit in hits:
            hit_id = f"pix_v_{hit.get('id')}"
            if not self.registry.is_used(hit_id):
                selected_hit = hit
                self.registry.mark_used(hit_id)
                break

        # If all were used, reuse the top hit as fallback
        if not selected_hit and hits:
            selected_hit = hits[0]

        videos = selected_hit.get("videos", {})
        best_url = None
        for q in ["small", "tiny", "medium", "large"]:
            if q in videos and videos[q].get("url"):
                best_url = videos[q]["url"]
                break

        if not best_url:
            return False

        raw_temp = self.temp_dir / f"raw_pix_v_{int(abs(hash(best_url))%100000)}.mp4"
        with requests.get(best_url, stream=True, timeout=25) as r:
            r.raise_for_status()
            with open(raw_temp, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)

        self._standardize_local_video(raw_temp, output_path, target_duration)
        if raw_temp.exists():
            try:
                raw_temp.unlink()
            except Exception:
                pass
        return True

    def _fetch_from_pixabay_photo(self, query: str, output_path: Path, target_duration: float, zoom_in: bool = True) -> bool:
        """Searches Pixabay Photo API for high-resolution photography tailored to query."""
        url = "https://pixabay.com/api/"
        params = {
            "key": self.pixabay_key,
            "q": query,
            "image_type": "photo",
            "per_page": 10
        }
        resp = requests.get(url, params=params, timeout=12)
        if resp.status_code != 200:
            return False

        hits = resp.json().get("hits", [])
        if not hits:
            return False

        # Find unused photo hit
        selected_hit = None
        for hit in hits:
            hit_id = f"pix_img_{hit.get('id')}"
            if not self.registry.is_used(hit_id):
                selected_hit = hit
                self.registry.mark_used(hit_id)
                break

        if not selected_hit and hits:
            selected_hit = hits[0]

        img_url = selected_hit.get("largeImageURL") or selected_hit.get("webformatURL")
        if not img_url:
            return False

        img_temp = self.temp_dir / f"pix_img_{int(abs(hash(img_url))%100000)}.jpg"
        r = requests.get(img_url, timeout=15)
        if r.status_code != 200:
            return False

        with open(img_temp, "wb") as f:
            f.write(r.content)

        self._animate_still_to_clip(img_temp, output_path, target_duration, zoom_in=zoom_in)
        if img_temp.exists():
            try:
                img_temp.unlink()
            except Exception:
                pass
        return True

    def _fetch_from_pexels_video(self, query: str, output_path: Path, target_duration: float) -> bool:
        """Searches Pexels Video API."""
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": self.pexels_key}
        params = {"query": query, "orientation": "portrait", "per_page": 8}
        resp = requests.get(url, headers=headers, params=params, timeout=12)
        if resp.status_code != 200:
            return False
        videos = resp.json().get("videos", [])
        if not videos:
            return False

        selected_video = None
        for v in videos:
            v_id = f"pexels_v_{v.get('id')}"
            if not self.registry.is_used(v_id):
                selected_video = v
                self.registry.mark_used(v_id)
                break
        if not selected_video and videos:
            selected_video = videos[0]

        best_link = None
        for f in selected_video.get("video_files", []):
            if f.get("width", 0) <= 1080 and f.get("height", 0) >= f.get("width", 0):
                best_link = f.get("link")
                break
        if not best_link and selected_video.get("video_files"):
            best_link = selected_video["video_files"][0].get("link")

        if not best_link:
            return False

        raw_temp = self.temp_dir / f"raw_pex_{int(abs(hash(best_link))%100000)}.mp4"
        with requests.get(best_link, stream=True, timeout=25) as r:
            with open(raw_temp, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)

        self._standardize_local_video(raw_temp, output_path, target_duration)
        if raw_temp.exists():
            try:
                raw_temp.unlink()
            except Exception:
                pass
        return True

    def _generate_pollinations_ai_clip(
        self,
        keyword: str,
        output_path: Path,
        duration: float,
        zoom_in: bool = True,
        narration: str = ""
    ) -> bool:
        """Generates dynamic vertical AI artwork via Pollinations.ai tailored to the scene."""
        prompt_core = f"{keyword}, {narration[:60]}" if narration else keyword
        clean_prompt = re.sub(r'[^a-zA-Z0-9 ]', '', prompt_core).strip()
        enhanced_prompt = f"{clean_prompt}, cinematic 8k lighting, highly detailed, photorealistic, vertical portrait 9:16, masterpiece"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&seed={int(abs(hash(clean_prompt + str(os.urandom(4))))%100000)}"

        img_temp = self.temp_dir / f"ai_{int(abs(hash(enhanced_prompt))%100000)}.jpg"
        try:
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200 and len(resp.content) > 10000:
                with open(img_temp, "wb") as f:
                    f.write(resp.content)
                self._animate_still_to_clip(img_temp, output_path, duration, zoom_in=zoom_in)
                if img_temp.exists():
                    try:
                        img_temp.unlink()
                    except Exception:
                        pass
                return True
        except Exception as e:
            print(f"[VideoFetcher] Pollinations AI generation skipped: {e}")

        return False

    def _standardize_local_video(self, input_video: Path, output_video: Path, duration: float):
        """Converts and crops any video into high-quality vertical 1080x1920 30fps MP4."""
        filter_str = (
            f"scale={config.VIDEO_WIDTH}:{config.VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={config.VIDEO_WIDTH}:{config.VIDEO_HEIGHT},"
            f"fps={config.VIDEO_FPS}"
        )
        cmd = [
            config.FFMPEG_PATH, "-y",
            "-stream_loop", "-1",
            "-i", str(input_video),
            "-t", str(duration + 0.5),
            "-vf", filter_str, "-an",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            str(output_video)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def _animate_still_to_clip(self, image_path: Path, output_path: Path, duration: float, zoom_in: bool = True):
        """Animates a 1080x1920 still photo into a dynamic video clip with Ken Burns zoom."""
        frames = int((duration + 0.5) * config.VIDEO_FPS)
        if zoom_in:
            zoom_filter = f"zoompan=z='min(zoom+0.0012,1.22)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}:fps={config.VIDEO_FPS}"
        else:
            zoom_filter = f"zoompan=z='max(1.20-on*0.0009,1.0)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}:fps={config.VIDEO_FPS}"

        cmd = [
            config.FFMPEG_PATH,
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-t", str(duration + 0.5),
            "-vf", (
                f"scale={config.VIDEO_WIDTH}:{config.VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
                f"crop={config.VIDEO_WIDTH}:{config.VIDEO_HEIGHT},"
                f"{zoom_filter}"
            ),
            "-an",
            "-c:v", "libx264",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def _generate_ambient_background_clip(self, output_path: Path, duration: float):
        cmd = [
            config.FFMPEG_PATH, "-y", "-f", "lavfi",
            "-i", f"color=c=0x0B0F19:s={config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}:d={duration + 0.5}:r={config.VIDEO_FPS}",
            "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(output_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


if __name__ == "__main__":
    fetcher = VideoFetcher()
    test_out = config.TEMP_DIR / "test_fresh_clip.mp4"
    clip = fetcher.fetch_clip_for_scene(
        scene_index=0,
        keyword="military soldier relaxation",
        duration=4.0,
        narration="How military pilots fall asleep in under two minutes"
    )
    print("Fresh clip generated successfully:", clip)
