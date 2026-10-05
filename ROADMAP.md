# `ROADMAP.md` — Long-Term Vision & Feature Backlog

Strategic proposals, future template explorations, and architectural ideas for `outofmylane`.

---

## 1. Vision & Core Philosophy

`outofmylane` is an intellectual workshop and personal garden representing 50+ years of curiosity across technology, art, music, somatics, and AI. The platform prioritizes:
1. **Longevity & Independence**: Pure static files, standard Markdown, zero proprietary lock-in.
2. **Performance & Sustainability**: Zero unnecessary client-side JavaScript, minimal network payloads, fast load times.
3. **Transparent Provenance**: Clear attribution for thoughts, experiments, human craftsmanship, and AI collaboration.

---

## 2. Future Template Proposals

### A. Dedicated Gallery Template (`gallery.html`)
* **Concept**: Interactive photo mosaic / study viewer for photography, woodworking projects, and tai chi postures.
* **Requirements**: Keyboard navigation (arrow keys), EXIF metadata display (focal length, aperture, film simulation), and direct links to full-resolution Google Photos / cloud storage.
* **Deferred from v0.8.02**: Intentionally postponed until single-photo post workflow and asset storage conventions mature.

### B. Interactive Application Showcase (`apps.html` / `project.html`)
* **Concept**: Showcase standalone data pipelines, interactive widgets, and generative models (e.g. Hugging Face Spaces embeds, Pixeltable demonstrations).
* **Requirements**: Responsive sandbox container, lazy loading, fallback previews, data schema inspectors.
* **Deferred from v0.8.02**: Kept separate from core publishing flow to maintain the zero-JS constraint for editorial content.

---

## 3. Platform & Pipeline Enhancements

1. **Pelican Engine**: Mature Python static site generator (`pelican`), clean and extensible via custom readers (`pelicanconf.py`).
2. **Obsidian Content Pipeline**: Direct editing in `/content/` vault, resolving wikilinks and image attachments seamlessly into compiled static HTML.
3. **Automated Asset Optimization**: Build-time WebP/AVIF generation and image resizing via Pillow in `pelicanconf.py`.
4. **Automated Link Checker**: CI action to continuously audit external links in bookmarks and book notes.

---

## 4. Architectural Exploration Proposals

### A. Zero-JS Email & Form Commenting Pipeline
* **Concept**: Allow reader feedback and inline post comments without introducing client-side JavaScript or third-party tracking scripts.
* **Architecture**:
  1. **HTML5 Form**: Standard `<form method="POST" action="https://script.google.com/macros/s/.../exec">` embedded at the bottom of posts and contact pages.
  2. **Google Apps Script & Sheets**: Form submits directly to a Google Apps Script webhook that appends responses to a private Google Sheet.
  3. **LLM Spam & Content Filter**: A build-time Python script (`tools/sync_comments.py`) fetches new rows from Google Sheets, runs spam validation, and formats approved reader comments into static HTML callouts during static site generation.

### B. Website Usage Tracking Analysis (Zero JavaScript)
* **Requirement**: Track visitor traffic, popular pages, and referrer trends without adding client-side JavaScript tags (Google Analytics disallowed under Zero-JS policy).
* **Option 1: GitHub Pages + GitHub Traffic API (Default for GitHub Hosting)**
  - **Mechanism**: GitHub repository Traffic Insights (`Insights` $\rightarrow$ `Traffic`) and REST API (`/repos/{owner}/{repo}/traffic/views`).
  - **Pros**: 100% Zero-JS out of the box, zero client payload, zero tracking cookies, privacy-respecting.
  - **Cons**: Retains granular daily data for 14 days only. Requires a periodic Python task (`tools/fetch_github_traffic.py`) to archive daily metrics into `content/data/traffic.json` for long-term trends.
* **Option 2: GoDaddy Web Hosting + Server Access Logs (Default for GoDaddy Hosting)**
  - **Mechanism**: Native Apache/Nginx HTTP access server logs analyzed via cPanel tools (AWStats, Webalizer) or raw log inspection.
  - **Pros**: 100% Zero-JS (server-side HTTP request logging), captures full request paths, referrers, bandwidth, and HTTP status codes indefinitely without client overhead.
  - **Cons**: Requires self-hosted GoDaddy server instance; log analysis requires cPanel access or log fetching script.
* **Recommendation**:
  - If hosted on **GitHub Pages**: Use GitHub Traffic API + periodic Python archiver script.
  - If hosted on **GoDaddy**: Use native server access logs (AWStats) for permanent HTTP request analytics.
