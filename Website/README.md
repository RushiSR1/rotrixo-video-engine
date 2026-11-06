# 🪐 Rotrixo (https://rotrixo.com) - Production Website

Production-ready, pure static multi-page agency website for **Rotrixo**, an AI Automation agency founded by **Rushikesh Rautrao**.

Designed for seamless deployment to **Netlify** by dragging and dropping this `Website` folder or linking the repository.

---

## 📁 Website Folder Structure

```
Website/
├── index.html              # Home Command Center (Hero, Terminal Simulator, Features, FAQ)
├── about.html              # About Rushikesh Rautrao (Bio, Philosophy, Tech Stack, Stats)
├── pricing.html            # Agency Beta Launch Deal ($199) & 4-Step Onboarding Stepper
├── contact.html            # Direct Inquiries & Netlify AJAX Form
├── terms.html              # Terms & Conditions (IP transfer, escrow, warranty)
├── privacy.html            # Privacy Policy (Zero API Key Interception guarantee)
├── 404.html                # Custom Cyberpunk 404 Error Page
├── netlify.toml            # Clean URL rewrites, SSL redirects, security & cache headers
├── robots.txt              # Search engine crawler permissions & sitemap link
├── sitemap.xml             # XML sitemap with all crawlable routes
├── site.webmanifest        # PWA & mobile icon metadata
├── favicon.ico             # Multi-size legacy favicon (16, 32, 48)
├── favicon-32.png          # Standard browser tab icon
├── favicon-192.png         # Android / Chrome home screen icon
├── favicon-512.png         # High-resolution splash icon
├── apple-touch-icon.png    # iOS home screen icon (180x180)
├── DEPLOY.md               # Complete Netlify deployment & rotrixo.com DNS guide
├── my image 2003.jpeg      # Original profile image
├── components/
│   ├── header.html         # Modular navigation header
│   └── footer.html         # Modular footer & quick links
└── assets/
    ├── css/
    │   └── theme.css       # Design system (Dark cyberpunk, glows, animations)
    ├── js/
    │   ├── config.js       # Central configuration for links & placeholders
    │   └── main.js         # Navigation, terminal simulator, FAQ, Netlify form handler
    └── img/
        ├── logo.svg        # Horizontal brand logo (dark theme)
        ├── logo-icon.svg   # Standalone orbital monogram "R" icon
        ├── logo-light.svg  # Light theme brand logo
        ├── favicon.svg     # Modern vector favicon
        ├── logo-icon-512.png # Square 512x512 logo for Google Schema
        ├── og-image.png    # 1200x630 OpenGraph social share card
        ├── profile.jpg     # Web-optimized profile portrait (800x800)
        └── profile-400.jpg # Web-optimized profile portrait (400x400)
```

---

## 🔑 Placeholders To Replace Before Launch

Edit [`assets/js/config.js`](file:///assets/js/config.js) to update links across all pages automatically:

| Key | Current Value | Action Required |
| :--- | :--- | :--- |
| `STREAMLIT_DEMO_URL` | `'https://rotrixo-video-engine-v21py.streamlit.app/'` | Replace with your actual live Streamlit demo URL. |
| `UPWORK_URL` | `'https://www.upwork.com/YOUR-PROFILE-OR-CONTRACT-LINK'` | Replace with your Upwork Profile or Direct Contract link. |
| `EMAIL` | `'hello@rotrixo.com'` | Replace with your preferred contact email if different. |
| `SITE_URL` | `'https://rotrixo.com'` | Canonical domain name. |
| `SOCIAL` | Twitter, LinkedIn, GitHub URLs | Update with your social handles. |

---

## 🚀 How to Deploy on Netlify

### Option 1: Drag-and-Drop (Instant)
1. Log in to [Netlify](https://app.netlify.com/).
2. Drag and drop this `Website` folder directly into the Netlify deploy dropzone.

### Option 2: Git Repository
1. In your Netlify site settings:
   - **Publish directory**: `Website` (or `.` if deploying only this subfolder).
   - **Build command**: *None* (pure static site, zero build step needed).

*See [`DEPLOY.md`](file:///DEPLOY.md) for custom domain (`rotrixo.com`) DNS configuration and Google Search Console sitemap submission instructions.*

