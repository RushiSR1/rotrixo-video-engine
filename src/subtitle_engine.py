from pathlib import Path
from typing import List, Dict, Any
import re
import config

class SubtitleEngine:
    def __init__(self):
        # Big bold punchy font
        self.font = "Arial"
        self.font_size = 82
        
        # Colour Palette (ASS format: &HAABBGGRR&)
        self.color_white = "&H00FFFFFF&"
        self.color_yellow = "&H0000FFFF&" # Electric Neon Yellow
        self.color_green = "&H0033FF33&"  # Vibrant Emerald Green
        self.color_cyan = "&H00FFFF00&"   # Electric Cyan
        self.color_red = "&H002222FF&"    # Radiant Red / Orange
        self.outline_color = "&H00000000&"# Thick Black Outline
        self.margin_v = 520               # Sweet spot (center-lower third, safe from UI)

    def _seconds_to_ass_time(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        centiseconds = int((secs - int(secs)) * 100)
        return f"{hours}:{minutes:02d}:{int(secs):02d}.{centiseconds:02d}"

    def _get_word_color(self, clean_word: str) -> str:
        """Determines vibrant highlight color based on emotional / semantic weight."""
        red_words = {"cortisol", "stress", "danger", "warning", "adrenaline", "fight-or-flight", "stop", "ruin", "ruins", "worst", "mistake", "failing"}
        yellow_words = {"3:00", "3", "am", "4:00", "4", "glycogen", "glucose", "sugar", "liver", "brain", "seconds", "minutes", "hours", "night", "waking", "wide", "awake"}
        green_words = {"honey", "almond", "butter", "deep", "sleep", "fix", "hack", "protocol", "relax", "natural", "method", "save", "follow", "magnesium", "solution"}
        cyan_words = {"circadian", "rhythm", "hormone", "blood", "levels", "military", "pilots", "body", "science", "secret"}

        if clean_word in red_words:
            return self.color_red
        if clean_word in yellow_words:
            return self.color_yellow
        if clean_word in green_words:
            return self.color_green
        if clean_word in cyan_words:
            return self.color_cyan
        return self.color_white

    def generate_ass_subtitles(self, cues: List[Dict[str, Any]], output_path: Path) -> Path:
        """
        Generates BIG, BOLD, COLOURFUL animated viral subtitles (Hormozi / Reels style).
        Uses rapid 1-3 word bursts with dynamic neon colored keyword highlights.
        """
        ass_header = f"""[Script Info]
Title: BioSlumber Viral Bold Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: {config.VIDEO_WIDTH}
PlayResY: {config.VIDEO_HEIGHT}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BigBold,{self.font},{self.font_size},{self.color_white},&H000000FF,{self.outline_color},&HA0000000,-1,0,0,0,100,100,2,0,1,8,4,2,40,40,{self.margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        dialogue_lines: List[str] = []

        for cue in cues:
            sentence = cue.get("text", "").strip()
            if not sentence:
                continue

            words = sentence.split()
            if not words:
                continue

            start_time = cue["start"]
            end_time = cue["end"]
            total_duration = max(0.4, end_time - start_time)

            # Rapid 2-3 word chunks (fast dopamine pacing)
            chunk_size = 2 if len(words) <= 5 else 3
            chunks = []
            for i in range(0, len(words), chunk_size):
                chunks.append(words[i:i + chunk_size])

            duration_per_chunk = total_duration / len(chunks)

            for idx, chunk in enumerate(chunks):
                chunk_start = start_time + (idx * duration_per_chunk)
                chunk_end = chunk_start + duration_per_chunk

                # Style each word in chunk
                styled_parts = []
                for w in chunk:
                    clean_w = re.sub(r'[^a-zA-Z0-9:]', '', w).lower()
                    color = self._get_word_color(clean_w)
                    if color != self.color_white:
                        styled_parts.append(f"{{\\c{color}}}{w.upper()}{{\\c{self.color_white}}}")
                    else:
                        styled_parts.append(w.upper())

                text_content = " ".join(styled_parts)
                start_ass = self._seconds_to_ass_time(chunk_start)
                end_ass = self._seconds_to_ass_time(chunk_end)

                line = f"Dialogue: 0,{start_ass},{end_ass},BigBold,,0,0,0,,{text_content}"
                dialogue_lines.append(line)

        full_ass = ass_header + "\n".join(dialogue_lines) + "\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_ass)

        print(f"[SubtitleEngine] Generated Big Bold Colourful captions at: {output_path.name}")
        return output_path


if __name__ == "__main__":
    engine = SubtitleEngine()
    test_cues = [
        {"start": 0.0, "end": 2.5, "text": "If you wake up at 3:00 AM every night"},
        {"start": 2.5, "end": 4.8, "text": "your cortisol hormone is spiking dangerously"}
    ]
    out = config.TEMP_DIR / "test_bold_sub.ass"
    engine.generate_ass_subtitles(test_cues, out)
    print("Subtitles generated successfully!")
