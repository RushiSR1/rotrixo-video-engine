# 🚀 Rotrixo Netlify Deployment & Domain Setup Guide

This guide walks you through deploying **Rotrixo** (https://rotrixo.com) to Netlify as a high-performance static site, connecting your custom domain, and submitting your site to Google Search Console for rapid discovery and site name indexing.

---

## 📁 1. Architecture Overview

The Rotrixo website is a pure static, multi-page website built with HTML5, Tailwind CSS, and vanilla JavaScript. There is **zero build step** required—Netlify serves the root folder directly.

- **Root directory**: `.`
- **Pages**:
  - `/index.html` → Home Command Center
  - `/about.html` → About Rushikesh Rautrao & Engineering Philosophy
  - `/pricing.html` → Agency Beta Launch Deal ($199) & Stepper
  - `/contact.html` → Direct Inquiries & Netlify Form
  - `/terms.html` → Terms & Conditions
  - `/privacy.html` → Privacy Policy & Credential Isolation Guarantee
  - `/404.html` → Cyberpunk Custom 404 Page
- **Configuration**:
  - `netlify.toml`: Handles clean URLs (`/about` instead of `/about.html`), www to non-www 301 redirects, security headers, and asset caching.
  - `site.webmanifest`, `robots.txt`, `sitemap.xml`: SEO, crawling, and mobile PWA metadata.
  - `/assets/js/config.js`: Central configuration file for links, URLs, and emails.

---

## ⚡ 2. Deploying to Netlify

You can deploy using either **Option A (Git Repository - Recommended)** or **Option B (Drag and Drop)**:

### Option A: Via GitHub (Continuous Deployment)
1. Initialize git and push this repository to your GitHub account:
   ```bash
   git add .
   git commit -m "feat: complete Rotrixo agency multi-page website"
   git push origin main
   ```
2. Log in to [Netlify](https://app.netlify.com/).
3. Click **Add new site** → **Import an existing project** → **GitHub**.
4. Select your repository.
5. In **Build settings**:
   - **Base directory**: Leave blank (or `.`)
   - **Build command**: Leave blank (no build step needed!)
   - **Publish directory**: `.` (root directory)
6. Click **Deploy site**. Your site will be live on a `*.netlify.app` subdomain in under 10 seconds!

### Option B: Drag and Drop (Instant)
1. Log in to [Netlify](https://app.netlify.com/).
2. Go to the **Sites** tab.
3. Scroll down to the bottom where it says *"Want to deploy a new site without connecting to Git? Drag and drop your site output folder here"*.
4. Drag and drop the website folder into the drop zone.
5. The site is instantly live!

---

## 🌐 3. Connecting Your Custom Domain (`rotrixo.com`)

1. In your Netlify Site dashboard, go to **Site configuration** → **Domain management**.
2. Click **Add a domain** (or **Add custom domain**) and enter `rotrixo.com`.
3. Set `rotrixo.com` as the **Primary domain** (this ensures all `www.rotrixo.com` traffic redirects automatically to `https://rotrixo.com`).
4. Choose one of the two DNS setup methods at your domain registrar (e.g. Namecheap, GoDaddy, Cloudflare, Google Domains):

### Method 1: Netlify DNS (Easiest)
1. Netlify will provide 4 nameservers (e.g., `dns1.p01.nsone.net`, `dns2.p01.nsone.net`, etc.).
2. In your domain registrar's control panel, change your domain's Name Servers to **Custom DNS** and paste Netlify's 4 nameservers.
3. Netlify will automatically manage all DNS records, HTTPS certificates, and subdomains.

### Method 2: Standard DNS Records (If keeping existing registrar DNS)
In your domain registrar's DNS management panel, add these two records:
| Record Type | Host / Name | Target / Value | TTL |
| :--- | :--- | :--- | :--- |
| **A Record** | `@` (or blank) | `75.2.60.5` | Automatic / 300s |
| **CNAME** | `www` | `<your-site-name>.netlify.app` | Automatic / 300s |

### SSL / HTTPS Certificate
Once DNS propagates (usually 5 to 30 minutes), scroll down to **HTTPS** in Netlify Domain management and click **Verify DNS configuration** → **Provision Certificate**. Netlify will automatically issue a free, auto-renewing Let's Encrypt SSL certificate.

---

## 📩 4. Netlify Forms Verification

The Contact page (`/contact.html`) contains a native Netlify Form:
- Form name: `contact`
- Honeypot spam filtering: `bot-field` enabled
- AJAX submission handler configured in `/assets/js/main.js` with direct fallback.

### Notification Setup:
1. In Netlify, go to **Site configuration** → **Forms** → **Form notifications**.
2. Click **Add notification** → **Email notification**.
3. Set your notification recipient to `hello@rotrixo.com` (or your preferred inbox).
4. You will now receive an instant email alert whenever an agency submits workflow specifications!

---

## 🔍 5. Google Search Console & Discovery Checklist

To ensure Google quickly indexes your brand name **"Rotrixo"**, displays your logo in search snippets, and indexes all pages:

1. **Verify Domain in Google Search Console**:
   - Go to [Google Search Console](https://search.google.com/search-console).
   - Choose **Domain** property and enter `rotrixo.com`.
   - Add the TXT verification record provided by Google to your DNS records.
2. **Submit Sitemap**:
   - Under the **Indexing** sidebar in Search Console, click **Sitemaps**.
   - In "Add a new sitemap", type `sitemap.xml` (full URL: `https://rotrixo.com/sitemap.xml`).
   - Click **Submit**. Google will crawl all 6 primary pages (`/`, `/about`, `/pricing`, `/contact`, `/terms`, `/privacy`).
3. **Site Name & Logo Verification**:
   - Rotrixo includes Google-recommended JSON-LD structured data on the homepage (`index.html`):
     - `WebSite` schema with `name: "Rotrixo"` and `alternateName: ["Rotrixo AI", "rotrixo.com"]`.
     - `Organization` schema linking to `https://rotrixo.com/assets/img/logo-icon-512.png` (512x512 high-resolution logo).
   - Use the [Google Rich Results Test](https://search.google.com/test/rich-results) on `https://rotrixo.com/` to verify that both schemas pass with zero warnings.
4. **URL Inspection & Priority Indexing**:
   - In Search Console, paste `https://rotrixo.com/` into the top search bar and click **Request Indexing**. Repeat for `https://rotrixo.com/about` and `https://rotrixo.com/pricing`.

---

## ⚙️ 6. Quick Placeholder Customization Checklist

Before public launch, open `/assets/js/config.js` and customize these variables:

| Variable | Current Placeholder | Description |
| :--- | :--- | :--- |
| `STREAMLIT_DEMO_URL` | `'https://rotrixo-video-engine-xjgwr2mdyyvcroahgmmcoi.streamlit.app/'` | The live URL of your deployed Streamlit video generator demo app. |
| `UPWORK_URL` | `'https://www.upwork.com/YOUR-PROFILE-OR-CONTRACT-LINK'` | Your Upwork Direct Contract or Profile checkout link. |
| `EMAIL` | `'hello@rotrixo.com'` | Your business contact email. |
| `SITE_URL` | `'https://rotrixo.com'` | Canonical production domain. |
| `SOCIAL` | Twitter, LinkedIn, GitHub URLs | Your social profiles (optional). |

All links on buttons and footers update automatically across all pages when you edit `config.js`!

