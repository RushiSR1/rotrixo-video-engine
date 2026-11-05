from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import config

class GraphicsEngine:
    def __init__(self):
        self.width = config.VIDEO_WIDTH
        self.height = config.VIDEO_HEIGHT
        self.graphics_dir = config.ASSETS_DIR / "graphics"
        self.temp_dir = config.TEMP_DIR
        self.graphics_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Load system fonts (Segoe UI or Arial)
        self.font_bold = self._load_font("segoui.ttf", 46, fallback="arial.ttf")
        self.font_title = self._load_font("segoeuib.ttf", 34, fallback="arialbd.ttf")
        self.font_small = self._load_font("segoeui.ttf", 26, fallback="arial.ttf")
        self.font_badge = self._load_font("segoeuib.ttf", 22, fallback="arialbd.ttf")

    def _load_font(self, font_name: str, size: int, fallback: str = "arial.ttf"):
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            try:
                return ImageFont.truetype(fallback, size)
            except Exception:
                return ImageFont.load_default()

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
        """Splits text into multiple lines that fit within max_width."""
        words = text.split()
        if not words:
            return []
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_w = bbox[2] - bbox[0]
            if line_w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def generate_brand_header(self, brand_title: str = "SLEEP SCIENCE LAB", brand_handle: str = "@SLEEPHACKS") -> Path:
        """
        Creates a sleek top frosted-glass brand banner (1080x1920 transparent PNG).
        Positioned at Y=120-210 (above video content, safe from top notch).
        """
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        pill_w = 640
        pill_h = 76
        pill_x = (self.width - pill_w) // 2
        pill_y = 130

        # Translucent dark background with neon cyan accent border
        draw.rounded_rectangle(
            [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
            radius=38,
            fill=(10, 15, 26, 215),
            outline=(0, 240, 255, 180),
            width=2
        )

        draw.text((pill_x + 30, pill_y + 20), "⚡", font=self.font_badge, fill=(0, 240, 255, 255))
        draw.text((pill_x + 70, pill_y + 22), brand_title, font=self.font_badge, fill=(255, 255, 255, 240))
        draw.text((pill_x + 360, pill_y + 22), "•", font=self.font_badge, fill=(100, 120, 150, 255))
        draw.text((pill_x + 390, pill_y + 22), brand_handle, font=self.font_badge, fill=(0, 240, 255, 230))

        out_path = self.graphics_dir / "brand_header.png"
        img.save(out_path, "PNG")
        return out_path

    def generate_hud_card(
        self,
        name: str,
        tag: str,
        title: str,
        subtitle: str,
        accent_color: Tuple[int, int, int] = (0, 220, 255), # RGB
        icon: str = "⚡",
        card_y: int = 400
    ) -> Path:
        """
        Creates a custom topic-specific floating scientific HUD overlay card.
        Positioned in upper-middle area so it never collides with subtitles at bottom.
        """
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        card_w = 900
        card_h = 230
        card_x = (self.width - card_w) // 2

        # Glassmorphic dark card backing
        draw.rounded_rectangle(
            [(card_x, card_y), (card_x + card_w, card_y + card_h)],
            radius=24,
            fill=(8, 12, 22, 235),
            outline=(*accent_color, 210),
            width=3
        )

        # Top-left badge tag
        tag_text = f"{icon}  {tag.upper()}"
        tag_bbox = draw.textbbox((0, 0), tag_text, font=self.font_badge)
        tag_w = max(220, (tag_bbox[2] - tag_bbox[0]) + 30)
        tag_h = 38
        draw.rounded_rectangle(
            [(card_x + 24, card_y + 20), (card_x + 24 + tag_w, card_y + 20 + tag_h)],
            radius=10,
            fill=(*accent_color, 50),
            outline=(*accent_color, 190),
            width=1
        )
        draw.text((card_x + 36, card_y + 24), tag_text, font=self.font_badge, fill=(*accent_color, 255))

        # Big bold title with word-wrap
        title_lines = self._wrap_text(title.upper(), self.font_title, card_w - 60, draw)
        text_y = card_y + 72
        for line in title_lines[:2]: # Max 2 lines for title
            draw.text((card_x + 30, text_y), line, font=self.font_title, fill=(255, 255, 255, 255))
            text_y += 40

        # Subtitle with word-wrap
        sub_lines = self._wrap_text(subtitle, self.font_small, card_w - 60, draw)
        for line in sub_lines[:2]: # Max 2 lines for subtitle
            draw.text((card_x + 32, text_y + 8), line, font=self.font_small, fill=(180, 205, 230, 230))
            text_y += 32

        # Futuristic tech corner accent lines
        draw.line([(card_x + card_w - 45, card_y + 24), (card_x + card_w - 20, card_y + 24)], fill=(*accent_color, 220), width=2)
        draw.line([(card_x + card_w - 20, card_y + 24), (card_x + card_w - 20, card_y + 49)], fill=(*accent_color, 220), width=2)
        draw.line([(card_x + card_w - 20, card_y + card_h - 24), (card_x + card_w - 45, card_y + card_h - 24)], fill=(*accent_color, 160), width=2)

        out_path = self.temp_dir / f"card_{name}_{int(abs(hash(name+title))%100000)}.png"
        img.save(out_path, "PNG")
        return out_path

    def build_dynamic_cards_for_script(
        self,
        script_data: Dict[str, Any],
        cues: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Dynamically analyzes script scenes and creates 2-3 topic-specific HUD cards
        timed accurately to cue start/end timestamps.
        """
        cards_list: List[Dict[str, Any]] = []
        scenes = script_data.get("scenes", [])
        if not scenes or not cues:
            return cards_list

        total_duration = cues[-1]["end"]
        duration_per_scene = total_duration / len(scenes)

        # Color schemes mapping
        color_map = {
            "red": (255, 75, 75),       # Danger/Problem
            "amber": (255, 185, 30),    # Warning/Formula
            "cyan": (0, 230, 255),      # Biological mechanism/Science
            "green": (50, 240, 140),    # Solution/Hack/Takeaway
            "purple": (185, 100, 255)   # Protocol/Secret
        }

        # Check if scenes have explicit graphic_card definitions from ScriptAgent
        explicit_found = False
        for i, scene in enumerate(scenes):
            gc = scene.get("graphic_card")
            if gc and isinstance(gc, dict) and gc.get("title"):
                explicit_found = True
                accent = color_map.get(gc.get("color", "cyan").lower(), (0, 230, 255))
                card_path = self.generate_hud_card(
                    name=f"scene_{i}",
                    tag=gc.get("tag", "SCIENCE ALERT"),
                    title=gc.get("title", ""),
                    subtitle=gc.get("subtitle", ""),
                    accent_color=accent,
                    icon=gc.get("icon", "⚡")
                )
                start_t = max(0.5, i * duration_per_scene + 0.3)
                end_t = min(total_duration - 0.5, start_t + min(4.5, duration_per_scene - 0.4))
                cards_list.append({
                    "image_path": card_path,
                    "start_time": start_t,
                    "end_time": end_t
                })

        # If no explicit cards were provided by AI, auto-generate 2-3 high-impact cards from scene text
        if not explicit_found and len(scenes) >= 3:
            # Card 1: Problem / Discovery card (at scene 1, roughly second 3-7)
            s1 = scenes[1] if len(scenes) > 1 else scenes[0]
            card1 = self.generate_hud_card(
                name="topic_alert",
                tag="BIOLOGY SCAN",
                title=script_data.get("title", "SLEEP MECHANISM")[:45],
                subtitle=s1.get("narration", "")[:85],
                accent_color=color_map["red"],
                icon="⚠️"
            )
            cards_list.append({
                "image_path": card1,
                "start_time": 3.0,
                "end_time": min(7.5, total_duration - 2.0)
            })

            # Card 2: Solution / Protocol card (at scene 3 or 4)
            sol_index = min(len(scenes) - 2, 3)
            if sol_index > 1 and len(scenes) > sol_index:
                s_sol = scenes[sol_index]
                card2 = self.generate_hud_card(
                    name="topic_solution",
                    tag="PROVEN PROTOCOL",
                    title="THE SCIENCE-BACKED HACK",
                    subtitle=s_sol.get("narration", "")[:85],
                    accent_color=color_map["cyan"],
                    icon="🧬"
                )
                start_2 = sol_index * duration_per_scene
                cards_list.append({
                    "image_path": card2,
                    "start_time": start_2,
                    "end_time": min(start_2 + 4.5, total_duration - 1.0)
                })

        print(f"[GraphicsEngine] Built {len(cards_list)} custom topic-specific HUD cards for this video.")
        return cards_list


if __name__ == "__main__":
    ge = GraphicsEngine()
    test_card = ge.generate_hud_card(
        name="test",
        tag="SCIENCE PROTOCOL",
        title="THE NAVY SEAL 2-MINUTE TECHNIQUE",
        subtitle="Step 1: Release tension from facial muscles, jaw, and tongue",
        accent_color=(0, 230, 255),
        icon="⚡"
    )
    print("Test card generated:", test_card)
