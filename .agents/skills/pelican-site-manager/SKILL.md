---
name: pelican-site-manager
description: >-
  Manage, configure, build, and maintain a static site using the Pelican Python
  static site generator. Use when setting up or modifying pelicanconf.py,
  building HTML from content/, configuring themes, testing builds, or publishing to GitHub Pages.
---

# Pelican Site Manager

This skill guides the setup, configuration, local testing, and maintenance of static websites powered by **Pelican**, the mature Python-based static site generator.

---

## 1. Architecture & Directory Layout

A standard, clean Pelican layout for this repository:

```text
├── content/                    # Source Markdown files (Obsidian vault drop)
│   ├── posts/                  # Blog posts and deep dives
│   ├── pages/                  # Static pages (about, reads, gallery)
│   ├── lanes/                  # Category / Lane Markdown definitions and intro copy
│   └── media/                  # Images, audio, video (media/images/)
├── themes/                     # Theme directory
│   └── lakefront/              # Active Lakefront theme templates & CSS
│       ├── templates/          # Jinja2 templates (base.html, index.html, page.html)
│       └── static/css/         # Stylesheets (theme/css/style.css)
├── pelicanconf.py              # Local development configuration
├── publishconf.py              # Production / GitHub Pages configuration
└── output/                     # Generated static HTML
```

---

## 2. Core Pelican Configuration (`pelicanconf.py`)

When configuring Pelican, always adhere to the site's **Zero-JS policy** and **pure HTML5/CSS design system**:

```python
AUTHOR = 'Jim Collinsworth'
SITENAME = 'Out of My Lane'
SITESUBTITLE = 'Jim Collinsworth'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

# URL structure
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
CATEGORY_URL = 'lanes/{slug}.html'
CATEGORY_SAVE_AS = 'lanes/{slug}.html'
CATEGORIES_URL = 'lanes.html'
CATEGORIES_SAVE_AS = 'lanes.html'

# Content paths
ARTICLE_PATHS = ['posts']
PAGE_PATHS = ['pages']
STATIC_PATHS = ['media', 'extra']

# Default all articles and pages to draft status
DEFAULT_METADATA = {
    'status': 'draft',
}

# Navigation Menu Configuration — strictly Home and About
MENUITEMS = (
    ('Home', '/index.html', 'index.html'),
    ('About', '/about.html', 'about'),
)

# Custom Theme
THEME = 'themes/lakefront'

# Feeds disabled for development
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False
RELATIVE_URLS = True
```

---

## 3. Standard CLI Commands (Reproducible)

Per the project's **Command Line Standards**, always use clean, standard commands that can be run directly in the terminal via `uv`:

### Install Dependencies
```bash
uv sync
```

### Build the Site (Development)
```bash
uv run pelican content -s pelicanconf.py -o output -d
```

### Local Live Preview
Start Pelican's built-in local web server with auto-regeneration:
```bash
uv run pelican --listen
```
Open `http://localhost:8000` in the browser.

### Production Build
```bash
uv run pelican content -s publishconf.py -o output -d
```

---

## 4. Strict Content Boundary & Placeholder Rule

> [!CAUTION]
> **Zero Unauthorized Content Generation & Mandatory Placeholder Rule**:
> - **100% Human Content in `content/`**: Everything in `content/` is authored exclusively by Jim. The agent must NEVER draft brand-new articles, opinionated business copy, or fabricate editorial content.
> - **Mandatory Obvious Placeholder Rule**: When structural scaffolding or missing copy is required, the agent must **ALWAYS use obviously placeholder text** (e.g., `[Placeholder summary]`, `[No posts published yet.]`, `[Lane notes in progress]`) instead of fabricating or generating simulated editorial content.

### Scaffolding Template
```markdown
---
title: [Post Title]
date: 2026-10-05
category: taichi
tags: mine, practice
slug: post-slug
summary: "[Placeholder summary]"
status: draft
template: post
---

[Post content in progress]
```

---

## 5. Discovered Pelican Patterns, Tips & Tricks

1. **Pelican Category Internals & Content-Driven Taxonomy**:
   - Assigning `cat.name = title` causes Pelican's `URLWrapper` internal setter to overwrite `_slug` via `slugify()`. In signal handlers (`article_generator_finalized`), `cat.slug = slug` must be explicitly assigned alongside `cat.name = title`.
   - To prevent ghost categories from being emitted, prune `generator.categories` against authored Markdown files in `content/lanes/*.md`, and clear orphaned article pointers (`article.category = None`) for any category lacking an authored file to prevent 404 links.

2. **Post-Driven Featured Showcase vs Dedicated Home Intro Scaffolding**:
   - Universal `featured: true` (or numeric priority) metadata on posts/articles allows arbitrary content to headline the home index without requiring an artificial `home.md` hook.
   - The Jinja template cleanly separates `featured_items` (top showcase grid) from `stream_articles` (chronological list) using `articles|rejectattr('slug', 'in', featured_slugs)`.

3. **Pure CSS Zero-JS Accessibility Controls**:
   - High-contrast mode, dark/light theme, and text size scaling toggles can be implemented with zero client-side JavaScript by placing hidden checkbox inputs (`#theme-toggle`, `#contrast-toggle`, `#text-size-toggle`) at the top of `base.html` and styling with CSS sibling selectors (`#contrast-toggle:checked ~ .site-container`).

4. **Strict Media Path Architecture**:
   - Consolidate all images, audio, video, and documents under `content/media/` (`media/images/`, `media/audio/`, `media/video/`) with `STATIC_PATHS = ["media", "extra"]`. This guarantees clean mirroring to `output/media/` and predictable Markdown image pathing (`media/images/photo.jpg`).

5. **Resilient Jinja2 Logic for Empty Article Lists**:
   - Always guard article indexing in templates with `{% if standard_articles %}` or `{% if stream_articles %}` to prevent `UndefinedError` on newly initialized sites or sites with 0 articles.

6. **Automated Intra-Site Link & Wikilink Resolution**:
   - Inheriting from `pelican.readers.MarkdownReader` allows automatic translation of Obsidian `[[wikilinks]]` and relative `.md` links into Pelican `{filename}` references (`{filename}/pages/about.md` or `{filename}/posts/...`), preventing broken links on static output pages.

7. **Pure CSS Zero-JS Sticky Slide-Cover**:
   - Stack pinned background header (`position: sticky; top: 0; z-index: 1`) behind scrolling body container (`position: relative; z-index: 2; background-color: var(--bg)`). Use `@media (max-height: 500px) and (orientation: landscape)` to automatically hide the sticky header on small landscape smartphones.

8. **Theme Reusability & Modular Pathing**:
   - Configure modular theme paths via `THEME = 'themes/lakefront'` for instant deployment across multiple sites.

---

## 6. Verification Checklist

After executing a static build:
1. **Targeted Smoke Run**: `uv run pytest tests/test_accessibility.py -k test_html_lang_attribute`
2. **Zero-JS Check**: Verify no unauthorized `<script>` tags were introduced into editorial content.
3. **Link & Asset Integrity**: Ensure relative internal links and referenced images resolve cleanly.
4. **Browser & Responsive Check**: Inspect computed styles, layout margins, and responsive viewports across mobile and desktop.
