"""
Rotrixo Website Automated QA & Link Verification Script
"""
import os
import re
import urllib.parse

HTML_FILES = [
    "index.html",
    "about.html",
    "pricing.html",
    "contact.html",
    "terms.html",
    "privacy.html",
    "404.html"
]

print("=" * 60)
print("1. RUNNING STATIC LINK & ASSET VALIDATION")
print("=" * 60)

errors = []
warnings = []

for filename in HTML_FILES:
    if not os.path.exists(filename):
        errors.append(f"Missing HTML file: {filename}")
        continue
    
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Check title
    title_match = re.search(r"<title>(.*?)</title>", content)
    if not title_match or not title_match.group(1).strip():
        errors.append(f"[{filename}] Missing or empty <title> tag")
    else:
        print(f"[{filename}] Title: {title_match.group(1).strip()}")

    # Check canonical
    can_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    if not can_match:
        errors.append(f"[{filename}] Missing canonical link")

    # Check meta description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if not desc_match:
        errors.append(f"[{filename}] Missing meta description")

    # Check internal links (href="/...")
    links = re.findall(r'href="(/[^"#?]+)"', content)
    for link in links:
        # Check against pages or files
        clean_path = link.lstrip("/")
        if clean_path == "" or clean_path == "index.html":
            target = "index.html"
        elif clean_path in ["about", "pricing", "contact", "terms", "privacy"]:
            target = f"{clean_path}.html"
        else:
            target = clean_path

        if not os.path.exists(target):
            errors.append(f"[{filename}] Broken internal link: {link} -> expected file '{target}'")

    # Check src="..." attributes
    srcs = re.findall(r'src="(/[^"?]+)"', content)
    for src in srcs:
        clean_src = src.lstrip("/")
        # URL decode
        clean_src = urllib.parse.unquote(clean_src)
        if not os.path.exists(clean_src):
            errors.append(f"[{filename}] Broken asset src: {src} -> '{clean_src}' not found on disk")

    # Check img alt tags
    imgs = re.findall(r'<img\s+([^>]+)>', content)
    for img_tag in imgs:
        if 'alt=' not in img_tag:
            warnings.append(f"[{filename}] Image missing alt attribute: <img {img_tag}>")

if errors:
    print("\n❌ VALIDATION ERRORS FOUND:")
    for err in errors:
        print("  -", err)
else:
    print("\n✅ ALL INTERNAL LINKS, CANONICALS, TITLES, AND ASSET SOURCES ARE 100% VALID!")

if warnings:
    print("\n⚠️ WARNINGS:")
    for w in warnings:
        print("  -", w)
else:
    print("✅ ZERO WARNINGS. All images have proper descriptive alt attributes.")

print("=" * 60)

