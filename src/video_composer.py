import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import config

class VideoComposer:
    def __init__(self):
        self.ffmpeg_path = config.FFMPEG_PATH
        self.temp_dir = config.TEMP_DIR
        self.sfx_dir = config.SFX_DIR

    def _get_audio_duration(self, audio_path: Path) -> float:
        """Determines audio duration using ffmpeg."""
        cmd = [self.ffmpeg_path, "-i", str(audio_path)]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        for line in res.stderr.split("\n"):
            if "Duration:" in line:
                try:
                    parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                    hours = float(parts[0])
                    minutes = float(parts[1])
                    seconds = float(parts[2])
                    return hours * 3600 + minutes * 60 + seconds
                except Exception:
                    pass
        return 42.0

    def compose(
        self,
        scene_clips: List[Path],
        voice_path: Path,
        bgm_path: Path,
        subtitle_path: Path,
        output_path: Path,
        hud_cards: Optional[List[Dict[str, Any]]] = None
    ) -> Path:
        """
        Assembles full-screen hybrid visuals with topic-specific HUD cards,
        BIG BOLD COLOURFUL subtitles, smooth top retention progress line,
        voiceover, and ambient audio mix.
        """
        print(f"[VideoComposer] Rendering clean cinematic short: {output_path.name}")
        voice_duration = self._get_audio_duration(voice_path)
        target_video_duration = voice_duration + 0.5

        # 1. Concat Demuxer with loop safety
        total_clips_dur = 0.0
        for clip in scene_clips:
            try:
                total_clips_dur += self._get_audio_duration(clip)
            except Exception:
                pass

        concat_txt = self.temp_dir / f"concat_{int(abs(hash(str(output_path)))%100000)}.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for clip in scene_clips:
                safe_clip_path = str(clip.resolve()).replace("\\", "/")
                f.write(f"file '{safe_clip_path}'\n")
            # If total footage is less than target video duration, duplicate clips so video never runs out
            if 0 < total_clips_dur < target_video_duration:
                repeats = int(target_video_duration // total_clips_dur) + 1
                for _ in range(repeats):
                    for clip in scene_clips:
                        safe_clip_path = str(clip.resolve()).replace("\\", "/")
                        f.write(f"file '{safe_clip_path}'\n")

        # 2. Subtitle Filter Path (escape backslashes and colons for ffmpeg)
        escaped_sub_path = str(subtitle_path.resolve()).replace("\\", "/").replace(":", r"\:")

        # 3. Audio & SFX Setup
        sfx_bass = self.sfx_dir / "bass_impact.mp3"
        has_bass = sfx_bass.exists()

        cmd_inputs = [
            self.ffmpeg_path, "-y",
            "-stream_loop", "-1",
            "-f", "concat", "-safe", "0", "-i", str(concat_txt), # [0] Video (seamless loop safety)
            "-i", str(voice_path),                                # [1] Voice
            "-i", str(bgm_path),                                  # [2] BGM
        ]

        input_counter = 3
        bass_idx = None
        if has_bass:
            cmd_inputs.extend(["-i", str(sfx_bass)])
            bass_idx = input_counter
            input_counter += 1

        v_chain = "0:v"
        filter_parts = []

        # Overlay topic-specific graphic cards if provided
        if hud_cards:
            for c_idx, card in enumerate(hud_cards):
                c_path = card.get("image_path")
                st = card.get("start_time", 0.0)
                et = card.get("end_time", st + 4.0)
                if c_path and Path(c_path).exists():
                    cmd_inputs.extend(["-i", str(c_path)])
                    next_v = f"v_card{c_idx}"
                    filter_parts.append(
                        f"[{v_chain}][{input_counter}:v]overlay=0:0:enable='between(t,{st:.2f},{et:.2f})'[{next_v}]"
                    )
                    v_chain = next_v
                    input_counter += 1

        # Subtitles and top progress bar
        filter_parts.append(f"[{v_chain}]subtitles='{escaped_sub_path}'[v_sub]")
        filter_parts.append(
            f"[v_sub]drawbox=x=0:y=0:w='iw*(t/{target_video_duration:.2f})':h=10:color=0x00F0FF@0.95:t=fill[outv]"
        )

        # Audio mix
        if bass_idx is not None:
            filter_parts.append("[1:a]volume=1.0[voice]")
            filter_parts.append("[2:a]volume=0.10[bgm]")
            filter_parts.append(f"[{bass_idx}:a]volume=0.85[sfx_bass]")
            filter_parts.append("[voice][bgm][sfx_bass]amix=inputs=3:duration=first:dropout_transition=2[outa]")
        else:
            filter_parts.append("[1:a]volume=1.0[voice]")
            filter_parts.append("[2:a]volume=0.10[bgm]")
            filter_parts.append("[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]")

        filter_complex = ";".join(filter_parts)

        cmd = cmd_inputs + [
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "[outa]",
            "-t", str(target_video_duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "19",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_path)
        ]

        print("[VideoComposer] Executing clean rendering pipeline with topic graphics and captions...")
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            print(f"[VideoComposer] Primary render note: {proc.stderr[-300:]}")
            # Streamlined fallback without HUD card overlays if primary had filter mismatch
            alt_filter = (
                f"[0:v]subtitles='{escaped_sub_path}'[outv];"
                f"[1:a]volume=1.0[voice];[2:a]volume=0.10[bgm];"
                f"[voice][bgm]amix=inputs=2:duration=first[outa]"
            )
            alt_cmd = [
                self.ffmpeg_path, "-y",
                "-stream_loop", "-1",
                "-f", "concat", "-safe", "0", "-i", str(concat_txt),
                "-i", str(voice_path), "-i", str(bgm_path),
                "-filter_complex", alt_filter,
                "-map", "[outv]", "-map", "[outa]",
                "-t", str(target_video_duration),
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
                str(output_path)
            ]
            subprocess.run(alt_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        if concat_txt.exists():
            try:
                concat_txt.unlink()
            except Exception:
                pass

        print(f"[VideoComposer] Video successfully created! Size: {output_path.stat().st_size / (1024*1024):.2f} MB")
        return output_path


if __name__ == "__main__":
    composer = VideoComposer()
    print("VideoComposer initialized successfully.")
