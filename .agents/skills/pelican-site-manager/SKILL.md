---
name: pelican-site-manager
description: >-
  Manage, configure, build, and maintain a static site for outofmylane using the Pelican Python
  static site generator. Use when setting up or modifying pelicanconf.py,
  building HTML from content/, configuring the Lakefront theme, testing builds, or publishing.
---

# Pelican Site Manager (out of my lane)

This skill guides the setup, configuration, local testing, and maintenance of static websites powered by **Pelican** for **`outofmylane`**.

---

## 1. Architecture & Directory Layout

Standard layout for this repository:

```text
├── content/                    # Source Markdown files
│   ├── posts/                  # Blog posts and deep dives
│   └── pages/                  # Static pages (about.md, etc.)
├── themes/                     # Packaged theme directory
│   └── lakefront/              # Active Lakefront theme templates & CSS
│       ├── templates/          # Jinja2 templates (base.html, index.html, page.html)
│       └── static/css/         # Central visual stylesheet (style.css)
├── pelicanconf.py              # Local development configuration (THEME = 'themes/lakefront')
├── publishconf.py              # Production configuration
└── output/                     # Generated static HTML
```

---

## 2. Pelican CLI Build Commands

Always execute build commands using `uv` inside `d:\projects\outofmylane`:

### Local Build
```bash
cmd /c "uv run pelican content -s pelicanconf.py -o output -d"
```

### Production Build
```bash
cmd /c "uv run pelican content -s publishconf.py -o output -d"
```

---

## 3. Discovered Pelican Patterns, Tips & Tricks

1. **Resilient Jinja2 Logic for Empty Article Lists**:
   - Always guard article indexing in templates with `{% if standard_articles %}` to prevent `UndefinedError: list object has no element 0` on newly initialized sites or sites with 0 articles:
     ```jinja2
     {% set standard_articles = articles|rejectattr('type', 'equalto', 'IDEA')|list %}
     {% set featured_matches = standard_articles|selectattr('featured', 'defined')|selectattr('featured')|list %}
     {% if featured_matches %}
       {% set featured = featured_matches[0] %}
     {% elif standard_articles %}
       {% set featured = standard_articles[0] %}
     {% else %}
       {% set featured = none %}
     {% endif %}
     {% set stream_articles = standard_articles|rejectattr('slug', 'equalto', featured.slug)|list if featured else [] %}
     ```

2. **Automated Intra-Site Link & Wikilink Resolution (`pelicanconf.py`)**:
   - Inheriting from `pelican.readers.MarkdownReader` allows automatic translation of Obsidian `[[wikilinks]]` and relative `.md` links into Pelican `{filename}` references (`{filename}/pages/about.md` or `{filename}/posts/...`), preventing broken links on static output pages.

3. **Pure CSS Zero-JS Sticky Slide-Cover**:
   - Stack pinned background header (`position: sticky; top: 0; z-index: 1`) behind scrolling body container (`position: relative; z-index: 2; background-color: var(--bg); box-shadow: ...`). Use `@media (max-height: 500px) and (orientation: landscape)` to automatically hide the sticky header on small landscape smartphones.

4. **Dynamic Image Src Resolution & HTML5 Figure Wrapping**:
   - Standardize `![alt](attachments/photo.jpg)` into semantic `<figure><img ...><figcaption>alt</figcaption></figure>`. Automatically adjust `src` depth (`../attachments/photo.jpg` for nested post pages vs `attachments/photo.jpg` for top-level pages).

5. **Responsive Mobile Table Scroll Containers**:
   - AST post-processing of `<table>` elements into `<div class="table-container" style="overflow-x: auto;">` prevents narrow mobile viewports from breaking layout alignment.

6. **Theme Reusability & Modular Pathing**:
   - Configure modular theme paths via `THEME = 'themes/lakefront'` for instant deployment across multiple sites.
