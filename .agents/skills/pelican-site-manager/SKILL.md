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
