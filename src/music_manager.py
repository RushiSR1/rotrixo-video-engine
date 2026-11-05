import random
import subprocess
from pathlib import Path
from typing import Optional
import config

class MusicManager:
    def __init__(self):
        self.music_dir = config.MUSIC_DIR
        self.default_ambient_file = self.music_dir / "ambient_sleep_drone.mp3"

    def get_background_music(self, target_duration: float = 60.0) -> Path:
        """
        Returns a path to a background music file.
        If user put their own music files in assets/music/, picks one.
        Otherwise, synthesizes a soothing 432Hz ambient sleep frequency.
        """
        existing_tracks = list(self.music_dir.glob("*.mp3")) + list(self.music_dir.glob("*.wav"))
        
        # Exclude generated drone if user has custom music
        user_tracks = [t for t in existing_tracks if t.name != self.default_ambient_file.name]
        if user_tracks:
            selected = random.choice(user_tracks)
            print(f"[MusicManager] Using custom music track: {selected.name}")
            return selected

        # If ambient drone already generated and long enough, return it
        if self.default_ambient_file.exists() and self.default_ambient_file.stat().st_size > 10000:
            return self.default_ambient_file

        print("[MusicManager] Synthesizing soothing 432Hz ambient delta sleep frequency...")
        self._generate_ambient_sleep_music(self.default_ambient_file, duration=max(90.0, target_duration + 10))
        return self.default_ambient_file

    def _generate_ambient_sleep_music(self, output_path: Path, duration: float = 90.0):
        """
        Generates a therapeutic, warm ambient sound bed combining:
        - 136.1 Hz (Earth / Om frequency associated with deep calming relaxation)
        - 432 Hz healing harmonic overtone
        - Deep low-passed warm pink noise (like distant gentle ocean breeze)
        """
        cmd = [
            config.FFMPEG_PATH,
            "-y",
            "-f", "lavfi", "-i", "anoisesrc=c=pink:r=44100:a=0.02",
            "-f", "lavfi", "-i", "sine=f=136.1:r=44100",
            "-f", "lavfi", "-i", "sine=f=432.0:r=44100",
            "-filter_complex",
            (
                "[0:a]lowpass=f=220,volume=0.10[noise];"
                "[1:a]lowpass=f=200,volume=0.07[drone];"
                "[2:a]lowpass=f=450,volume=0.02[harmonic];"
                "[noise][drone][harmonic]amix=inputs=3:dropout_transition=0,"
                f"afade=t=in:ss=0:d=3,afade=t=out:st={duration - 4}:d=4[outa]"
            ),
            "-map", "[outa]",
            "-t", str(duration),
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            str(output_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"[MusicManager] Ambient sleep audio created: {output_path.name}")


if __name__ == "__main__":
    mgr = MusicManager()
    track = mgr.get_background_music(60.0)
    print("Background track:", track)
