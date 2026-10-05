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

1. **pelican** python static site generator, old and unsupported but simple and easy to use and manipulate.
2. obsidian to directly edit the /content directory as the blog source, use obsidian mardown with linked media diretly in obsidian and as input to pelicn
2. **Automated Asset Optimization**: Build-time WebP/AVIF generation and image resizing via Pillow in `pelicanconf.py`.
3. **Automated Link Checker**: CI action to continuously audit external links in bookmarks and book notes.
