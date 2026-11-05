"""
Rotrixo Brand Assets Generator
Generates:
- assets/img/logo.svg
- assets/img/logo-icon.svg
- assets/img/logo-light.svg
- assets/img/favicon.svg
- favicon.ico
- favicon-32.png
- favicon-192.png
- favicon-512.png
- apple-touch-icon.png
- assets/img/logo-icon-512.png
- assets/img/og-image.png
- assets/img/profile.jpg (optimized from Website/my image 2003.jpeg)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs("assets/img", exist_ok=True)

# 1. Generate SVG Files

# Logo Icon SVG
logo_icon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" fill="none">
  <defs>
    <linearGradient id="rx-grad" x1="12" y1="16" x2="116" y2="112" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#A855F7" />
      <stop offset="45%" stop-color="#8B5CF6" />
      <stop offset="100%" stop-color="#10F5A0" />
    </linearGradient>
    <linearGradient id="rx-orbit" x1="10" y1="64" x2="118" y2="64" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#A855F7" stop-opacity="0.8" />
      <stop offset="70%" stop-color="#10F5A0" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#10F5A0" />
    </linearGradient>
    <radialGradient id="rx-glow" cx="64" cy="64" r="64" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.35" />
      <stop offset="60%" stop-color="#10F5A0" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#05060A" stop-opacity="0" />
    </radialGradient>
    <filter id="rx-blur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Ambient Glow -->
  <circle cx="64" cy="64" r="54" fill="url(#rx-glow)" />

  <!-- Outer Orbital Ring with Trailing Dashes -->
  <circle cx="64" cy="64" r="52" stroke="url(#rx-orbit)" stroke-width="3" stroke-linecap="round" stroke-dasharray="190 70" transform="rotate(-35 64 64)" opacity="0.85" />
  
  <!-- Counter-Orbit Accent Arc -->
  <path d="M 32 104 A 52 52 0 0 1 18 52" stroke="#10F5A0" stroke-width="2.5" stroke-linecap="round" opacity="0.6" />

  <!-- Orbiting Node / Spark -->
  <circle cx="106" cy="38" r="4.5" fill="#10F5A0" filter="url(#rx-blur)" />
  <circle cx="106" cy="38" r="2.5" fill="#FFFFFF" />

  <!-- Central Monogram R Structure -->
  <!-- Vertical Pillar -->
  <rect x="36" y="32" width="12" height="64" rx="6" fill="url(#rx-grad)" />

  <!-- Upper Loop -->
  <path d="M 42 32 H 68 C 84 32 94 42 94 54 C 94 66 84 76 68 76 H 48" 
        stroke="url(#rx-grad)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none" />

  <!-- Dynamic Diagonal Kick Leg with Arrow/Acceleration Flare -->
  <path d="M 64 74 L 86 96" 
        stroke="url(#rx-grad)" stroke-width="12" stroke-linecap="round" fill="none" />

  <!-- Center Energy Core -->
  <circle cx="62" cy="54" r="4" fill="#10F5A0" />
</svg>'''

with open("assets/img/logo-icon.svg", "w", encoding="utf-8") as f:
    f.write(logo_icon_svg)

# Favicon SVG (clean, high-visibility version)
favicon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="fav-grad" x1="6" y1="8" x2="58" y2="56" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#A855F7" />
      <stop offset="100%" stop-color="#10F5A0" />
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="#05060A" />
  <circle cx="32" cy="32" r="26" stroke="url(#fav-grad)" stroke-width="2.5" stroke-dasharray="110 30" transform="rotate(-30 32 32)" />
  <circle cx="51" cy="18" r="2.5" fill="#10F5A0" />
  <!-- Monogram R -->
  <rect x="20" y="18" width="7" height="28" rx="3.5" fill="url(#fav-grad)" />
  <path d="M 23 18 H 36 C 44 18 49 23 49 29 C 49 35 44 40 36 40 H 26" stroke="url(#fav-grad)" stroke-width="6.5" stroke-linecap="round" fill="none" />
  <path d="M 34 38 L 45 46" stroke="url(#fav-grad)" stroke-width="6.5" stroke-linecap="round" fill="none" />
  <circle cx="33" cy="29" r="2" fill="#10F5A0" />
</svg>'''

with open("assets/img/favicon.svg", "w", encoding="utf-8") as f:
    f.write(favicon_svg)

# Logo Horizontal (Dark Mode - for navbar & dark backgrounds)
logo_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 64" fill="none">
  <defs>
    <linearGradient id="lh-grad" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#A855F7" />
      <stop offset="50%" stop-color="#8B5CF6" />
      <stop offset="100%" stop-color="#10F5A0" />
    </linearGradient>
    <linearGradient id="text-x-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10F5A0" />
      <stop offset="100%" stop-color="#34D399" />
    </linearGradient>
    <filter id="lh-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Group: Icon (size 52x52 at x=6, y=6) -->
  <g transform="translate(6, 6)">
    <circle cx="26" cy="26" r="24" stroke="url(#lh-grad)" stroke-width="2" stroke-linecap="round" stroke-dasharray="90 30" transform="rotate(-35 26 26)" opacity="0.9" />
    <circle cx="45" cy="14" r="2.5" fill="#10F5A0" filter="url(#lh-glow)" />
    <!-- Pillar -->
    <rect x="14" y="13" width="5.5" height="26" rx="2.75" fill="url(#lh-grad)" />
    <!-- Loop -->
    <path d="M 17 13 H 28 C 35 13 39 17.5 39 22.5 C 39 27.5 35 32 28 32 H 19" stroke="url(#lh-grad)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
    <!-- Kick -->
    <path d="M 26 31 L 36 39" stroke="url(#lh-grad)" stroke-width="5" stroke-linecap="round" fill="none" />
    <circle cx="25.5" cy="22.5" r="1.8" fill="#10F5A0" />
  </g>

  <!-- Wordmark "Rotrixo" -->
  <g transform="translate(74, 43)">
    <!-- R -->
    <text x="0" y="0" font-family="'Space Grotesk', 'Inter', -apple-system, sans-serif" font-size="31" font-weight="800" fill="#FFFFFF" letter-spacing="-0.5">Rotri</text>
    <!-- x (accented in neon emerald) -->
    <text x="77" y="0" font-family="'Space Grotesk', 'Inter', -apple-system, sans-serif" font-size="31" font-weight="800" fill="url(#text-x-grad)" letter-spacing="-0.5">x</text>
    <!-- o -->
    <text x="94" y="0" font-family="'Space Grotesk', 'Inter', -apple-system, sans-serif" font-size="31" font-weight="800" fill="#FFFFFF" letter-spacing="-0.5">o</text>
    
    <!-- Mini Sub-tag / Node Accent -->
    <circle cx="119" cy="-18" r="3" fill="#10F5A0" opacity="0.9" />
    <circle cx="119" cy="-18" r="1.5" fill="#FFFFFF" />
  </g>
</svg>'''

with open("assets/img/logo.svg", "w", encoding="utf-8") as f:
    f.write(logo_svg)

# Logo Horizontal (Light Mode - for light backgrounds)
logo_light_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 64" fill="none">
  <defs>
    <linearGradient id="ll-grad" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7C3AED" />
      <stop offset="60%" stop-color="#6D28D9" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
  </defs>

  <g transform="translate(6, 6)">
    <circle cx="26" cy="26" r="24" stroke="url(#ll-grad)" stroke-width="2" stroke-linecap="round" stroke-dasharray="90 30" transform="rotate(-35 26 26)" />
    <circle cx="45" cy="14" r="2.5" fill="#059669" />
    <rect x="14" y="13" width="5.5" height="26" rx="2.75" fill="url(#ll-grad)" />
    <path d="M 17 13 H 28 C 35 13 39 17.5 39 22.5 C 39 27.5 35 32 28 32 H 19" stroke="url(#ll-grad)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
    <path d="M 26 31 L 36 39" stroke="url(#ll-grad)" stroke-width="5" stroke-linecap="round" fill="none" />
    <circle cx="25.5" cy="22.5" r="1.8" fill="#059669" />
  </g>

  <g transform="translate(74, 43)">
    <text x="0" y="0" font-family="'Space Grotesk', 'Inter', -apple-system, sans-serif" font-size="31" font-weight="800" fill="#0B0D14" letter-spacing="-0.5">Rotri</text>
    <text x="77" y="0" font-family="'Space Grotesk', 'Inter', -apple-system, sans-serif" font-size="31" font-weight="800" fill="#059669" letter-spacing="-0.5">x</text>
    <text x="94" y="0" font-family="'Space Grotesk', 'Inter', -apple-system, sans-serif" font-size="31" font-weight="800" fill="#0B0D14" letter-spacing="-0.5">o</text>
    <circle cx="119" cy="-18" r="3" fill="#059669" />
  </g>
</svg>'''

with open("assets/img/logo-light.svg", "w", encoding="utf-8") as f:
    f.write(logo_light_svg)

print("SVG files generated successfully.")

# 2. Process Profile Picture
profile_source = os.path.join("Website", "my image 2003.jpeg")
if os.path.exists(profile_source):
    with Image.open(profile_source) as img:
        img_rgb = img.convert("RGB")
        # Save high quality web-optimized profile image
        img_rgb.save("assets/img/profile.jpg", "JPEG", quality=92, optimize=True)
        img_rgb.resize((400, 400), Image.Resampling.LANCZOS).save("assets/img/profile-400.jpg", "JPEG", quality=90, optimize=True)
        print("Profile image processed and saved to assets/img/profile.jpg")
else:
    print("Warning: Profile image source not found at Website/my image 2003.jpeg")

# 3. High-Fidelity Icon Drawer using PIL
def render_icon(size=512, background="#05060A", rounded=False):
    # Render at 2x for supersampled anti-aliasing
    scale = 2
    render_size = size * scale
    img = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if background:
        if rounded:
            r = int(render_size * 0.22)
            draw.rounded_rectangle([0, 0, render_size, render_size], radius=r, fill=background)
        else:
            draw.rectangle([0, 0, render_size, render_size], fill=background)

    cx, cy = render_size // 2, render_size // 2
    
    # Outer orbital glow
    glow_radius = int(render_size * 0.42)
    # Draw soft glow circles
    for r_offset in range(12, 0, -2):
        alpha = int(12 - r_offset) * 4
        draw.ellipse([cx - glow_radius - r_offset*3, cy - glow_radius - r_offset*3,
                      cx + glow_radius + r_offset*3, cy + glow_radius + r_offset*3],
                     outline=(139, 92, 246, alpha), width=3)

    # Orbital ring (arc)
    orbit_r = int(render_size * 0.40)
    orbit_bbox = [cx - orbit_r, cy - orbit_r, cx + orbit_r, cy + orbit_r]
    draw.arc(orbit_bbox, start=-210, end=40, fill=(16, 245, 160, 230), width=int(14 * scale))
    draw.arc(orbit_bbox, start=60, end=110, fill=(168, 85, 247, 200), width=int(12 * scale))

    # Orbiting satellite spark
    spark_angle = math.radians(-30)
    sx = cx + int(orbit_r * math.cos(spark_angle))
    sy = cy + int(orbit_r * math.sin(spark_angle))
    draw.ellipse([sx - 16*scale, sy - 16*scale, sx + 16*scale, sy + 16*scale], fill=(16, 245, 160, 80))
    draw.ellipse([sx - 8*scale, sy - 8*scale, sx + 8*scale, sy + 8*scale], fill=(16, 245, 160, 255))
    draw.ellipse([sx - 4*scale, sy - 4*scale, sx + 4*scale, sy + 4*scale], fill=(255, 255, 255, 255))

    # Monogram R geometry
    # Colors: Purple to Emerald
    pillar_w = int(24 * scale)
    pillar_h = int(128 * scale)
    px = cx - int(48 * scale)
    py = cy - int(60 * scale)

    # Pillar
    draw.rounded_rectangle([px, py, px + pillar_w, py + pillar_h], radius=pillar_w//2, fill=(168, 85, 247, 255))

    # Upper Loop (outer circle & inner cut)
    loop_cx = px + int(36 * scale)
    loop_cy = py + int(36 * scale)
    loop_r = int(46 * scale)
    loop_stroke = int(24 * scale)
    loop_bbox = [loop_cx - loop_r, loop_cy - loop_r, loop_cx + loop_r, loop_cy + loop_r]
    draw.arc(loop_bbox, start=-90, end=90, fill=(139, 92, 246, 255), width=loop_stroke)
    draw.rectangle([px + pillar_w//2, py, loop_cx, py + loop_stroke], fill=(168, 85, 247, 255))
    draw.rectangle([px + pillar_w//2, py + loop_stroke*2 + int(4*scale), loop_cx, py + loop_stroke*3], fill=(139, 92, 246, 255))

    # Dynamic Diagonal Kick Leg
    leg_start_x = loop_cx - int(4 * scale)
    leg_start_y = py + int(60 * scale)
    leg_end_x = px + pillar_w + int(68 * scale)
    leg_end_y = py + pillar_h
    draw.line([leg_start_x, leg_start_y, leg_end_x, leg_end_y], fill=(16, 245, 160, 255), width=int(22 * scale))

    # Small center neon core
    draw.ellipse([loop_cx - 8*scale, loop_cy - 8*scale, loop_cx + 8*scale, loop_cy + 8*scale], fill=(16, 245, 160, 255))

    # Downsample with Lanczos for smooth subpixel anti-aliasing
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

# Generate Icons
icon_512 = render_icon(512, background="#05060A", rounded=False)
icon_512.save("favicon-512.png", "PNG")
icon_512.save("assets/img/logo-icon-512.png", "PNG")

icon_192 = render_icon(192, background="#05060A", rounded=False)
icon_192.save("favicon-192.png", "PNG")

icon_180 = render_icon(180, background="#05060A", rounded=True)
icon_180.save("apple-touch-icon.png", "PNG")

icon_32 = render_icon(32, background="#05060A", rounded=True)
icon_32.save("favicon-32.png", "PNG")

# Generate Multi-size favicon.ico
ico_16 = render_icon(16, background="#05060A", rounded=True)
ico_32 = render_icon(32, background="#05060A", rounded=True)
ico_48 = render_icon(48, background="#05060A", rounded=True)
ico_16.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

print("Favicons and app icons generated.")

# 4. Generate OpenGraph Image (1200x630)
def generate_og_image():
    W, H = 1200, 630
    og = Image.new("RGBA", (W, H), (5, 6, 10, 255)) # #05060A
    draw = ImageDraw.Draw(og)

    # Cyberpunk background grid
    grid_color = (255, 255, 255, 8)
    for x in range(0, W, 40):
        draw.line([x, 0, x, H], fill=grid_color, width=1)
    for y in range(0, H, 40):
        draw.line([0, y, W, y], fill=grid_color, width=1)

    # Ambient radial gradients (purple on top-left, emerald on bottom-right)
    # Simulate purple glow
    for r in range(350, 0, -20):
        alpha = int((350 - r) * 0.14)
        draw.ellipse([100 - r, 80 - r, 100 + r, 80 + r], fill=(139, 92, 246, alpha))

    # Simulate emerald glow
    for r in range(400, 0, -25):
        alpha = int((400 - r) * 0.12)
        draw.ellipse([1050 - r, 450 - r, 1050 + r, 450 + r], fill=(16, 245, 160, alpha))

    # Add Card Container
    card_margin = 40
    draw.rounded_rectangle([card_margin, card_margin, W - card_margin, H - card_margin],
                           radius=24, outline=(255, 255, 255, 25), width=2,
                           fill=(11, 13, 20, 210))

    # Embed Icon in OG image
    brand_icon = render_icon(140, background=None, rounded=False)
    og.paste(brand_icon, (90, 80), brand_icon)

    # Text & Typography
    # Try system fonts or default
    font_bold_title = None
    font_medium = None
    font_sub = None
    font_badge = None

    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font_bold_title = ImageFont.truetype(fp, 52)
                font_brand = ImageFont.truetype(fp, 64)
                font_medium = ImageFont.truetype(fp, 26)
                font_sub = ImageFont.truetype(fp, 20)
                font_badge = ImageFont.truetype(fp, 18)
                break
            except Exception:
                pass

    if not font_bold_title:
        font_brand = ImageFont.load_default()
        font_bold_title = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Brand Title "Rotrixo"
    draw.text((250, 115), "Rotrixo", font=font_brand, fill=(255, 255, 255, 255))
    draw.text((495, 120), "•", font=font_medium, fill=(16, 245, 160, 255))
    draw.text((520, 126), "AI Automation Engine", font=font_medium, fill=(168, 85, 247, 255))

    # Tagline
    draw.text((90, 260), "Deploy 1-Click Autonomous AI Video Engines", font=font_bold_title, fill=(255, 255, 255, 255))
    draw.text((90, 325), "For Your Content Agency", font=font_bold_title, fill=(16, 245, 160, 255))

    # Description
    desc_line = "Custom Python, Gemini & ElevenLabs pipelines generating high-retention shorts in <60s."
    draw.text((90, 405), desc_line, font=font_medium, fill=(203, 213, 225, 240))

    # Bottom Pill Badges
    badges = ["⚡ <60s Generation", "🔒 100% Client-Owned Code", "💸 $0 Recurring Platform Fees", "🚀 Private Streamlit UI"]
    bx = 90
    by = 490
    for badge in badges:
        # Measure
        bbox = draw.textbbox((0, 0), badge, font=font_badge)
        bw = bbox[2] - bbox[0] + 32
        bh = 44
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=22, fill=(139, 92, 246, 35), outline=(139, 92, 246, 80), width=1)
        draw.text((bx + 16, by + 11), badge, font=font_badge, fill=(255, 255, 255, 240))
        bx += bw + 18

    # Bottom Right Domain watermark
    draw.text((980, 502), "rotrixo.com", font=font_sub, fill=(16, 245, 160, 220))

    og_rgb = og.convert("RGB")
    og_rgb.save("assets/img/og-image.png", "PNG", quality=95)
    print("OpenGraph image generated at assets/img/og-image.png")

generate_og_image()
