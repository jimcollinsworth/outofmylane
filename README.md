# Out of My Lane (`outofmylane`)

> Personal static site and knowledge garden for Jim Collinsworth, exploring software, data science, tai chi, classical guitar, piano, woodworking, and AI.

---

## 1. Architecture & Design Approach

* **Engine**: [Pelican](https://getpelican.com/) static site generator powered by Python 3.12+ and managed with `uv`.
* **Theme**: Custom `themes/lakefront/` theme inspired by Bear Blog (pinewind) and Mark Boulton (anewcanon).
* **Zero Client-Side JavaScript**: Zero `<script>` tags on published content. Interactivity (light/dark mode toggle, high-contrast mode, font size adjustment, responsive navigation) is achieved entirely through standard semantic HTML5 and CSS specifications (`:has()`, media queries).
* **Responsive Layout**: Designed for mobile portrait/landscape (>= 390px), tablets, standard desktop, and high-resolution displays. On large screens, the home post stream splits into a dual-column list; on mobile, it flows in a single stacked column.
* **WCAG AAA Accessibility**: High contrast, fluid typography, visible focus indicators, skip-to-content links, and minimum 44px touch targets.

---

## 2. Content Taxonomy & "Lanes" Architecture

In `outofmylane`, topics are organized by **Lanes** rather than generic categories.
 
### A. Lanes (`category`)
Pelican's native `category` field functions as the primary "Lane".
* **Authored in `/content/lanes/`**: Each Lane is defined by a Markdown file in `content/lanes/<lane>.md` (e.g., `content/lanes/taichi.md`). The YAML frontmatter (`title`, `slug`, `summary`) and Markdown body in this file are merged into the Lane detail page (`lanes/<slug>.html`) and the Lane index (`lanes.html`).
* **Strict Provenance**: Only lanes authored in `content/lanes/` are emitted in the compiled site. Articles specify their lane via `category: <slug>`. If an article does not assign a lane, it is published without category grouping.
* **Placeholder Rule**: If structural scaffolding is needed, obvious placeholder indicators (e.g. `[Lane notes in progress]`) are used rather than simulated AI copy.

### B. Tags & Provenance
* **Provenance Tags**: Reflect authorship origin: `me`, `mine`, `ai`, `ours`, `theirs`, or dual `ai+mine`.
* **Topic Tags**: Fine-grained taxonomy (e.g., `taichi-108`, `chicago`, `python`).
* **Tag Prose Merging via `/content/tags/`**: Subfolders and files in `content/tags/<tag>.md` can supply custom editorial prose for specific tags.

### C. Article Template Types
Articles specify their template in frontmatter:
| Template | Code Badge | Icon | Intended Content |
| :--- | :--- | :--- | :--- |
| `post` | `POST` | Feather | Standard essay, project update, or narrative |
| `idea` | `IDEA` | Sparkle | Seedling concept, prompt, or unpolished thought |
| `link` | `LINK` | Chain | Curated external reference or book review |
| `photo` | `PHOTO` | Camera | Individual photograph with caption and telemetry |
| `chat` | `CHAT` | Message | Conversational dialogue or AI session transcript |
| `project` | `APP` | Box | Software tool, interactive model, or dataset |
| `til` | `TIL` | Bulb | "Today I Learned" concise technical note |
| `read` | `READ` | Book | Book review or reading notes |
| `view` | `VIEW` | Film | Film, video, or lecture summary |
| `spec` | `SPEC` | Document | Architecture or engineering specification |
| `wip` | `WIP` | Clock | Work in progress |

### D. Supported Frontmatter Metadata
```yaml
---
title: Chicago Lakefront Sky Study
slug: chicago-lakefront-sky-study
date: 2026-10-04
modified: 2026-10-04
category: taichi                    # Lane slug (must match content/lanes/<slug>.md)
tags: mine, chicago, lakefront      # Provenance and topic tags
author: Jim Collinsworth            # Author (e.g. Jim Collinsworth or LLM-Gemini3.8)
status: published                   # Defaults to 'draft' if omitted
template: photo                     # post, idea, link, photo, chat, etc.
summary: Early morning light study over Lake Michigan.
featured: true                      # Highlight in Lane streams
external_url: https://example.com   # Target URL for link templates
original_author: Jane Doe           # Attribution for curated links
isbn: 978-0123456789                # For book reviews (read/link)
menu: false                         # Exclude from main nav bar
menu_order: 10                      # Sort position in navigation
menu_title: Short Title             # Nav link label override
---
```

---

## 3. Media Handling & Obsidian Bridge

Static media is organized under `content/media/` and `content/attachments/`:
```text
content/
├── media/
│   ├── images/       # Photos, screenshots, diagrams
│   ├── audio/        # MP3 audio recordings, MIDI files
│   ├── video/        # Short web-optimized MP4/WebM clips (< 500 KB)
│   └── docs/         # Schematics, PDFs, reference documents
├── attachments/      # Direct drop target for Obsidian standard embeds
├── pages/            # Static pages (about.md, home.md)
├── categories/       # Category / Lane prose files (taichi.md, ai.md)
└── posts/            # Human-authored Markdown articles
```
* **Obsidian Markdown Links**: Standard embeds like `![Sky](media/images/sky.jpg)` resolve identically in Obsidian and Pelican's compiled HTML output.
* **Large Asset Governance**: Files committed to Git must stay under 500 KB. High-resolution raw media, albums, and video streams resolve to external hosting (Google Photos, YouTube, Vimeo, S3/Cloudflare R2).

---

## 4. DevOps, Setup & Build Commands

### Environment Setup
Python dependencies are managed via `uv`:
```cmd
:: Activate virtual environment
.venv\Scripts\activate

:: Install / sync dependencies
uv sync
```

### Static Site Build
```cmd
:: Build site locally with delete-output (-d) flag
uv run pelican content -s pelicanconf.py -o output -d

:: Serve site locally with auto-reload
uv run pelican --listen -r
```

### Testing & Verification
Test suites are located in `tests/` and execute with `pytest`:
```cmd
:: Run full verification suite
cmd /c "uv run pytest -v"

:: Target smoke check
cmd /c "uv run pytest tests/test_accessibility.py -v"
```

---

## 5. Agent Guidelines & Operational Rules

1. **Mandatory Obvious Placeholder Rule**: Missing content or structural scaffolding must strictly use obvious placeholder text (e.g. `[Placeholder summary]`). Agents must **never** fabricate AI copy.
2. **AI Attribution Standard**: Any code, templates, or documentation co-authored by AI models must explicitly cite the model identifier (e.g., `LLM-Gemini3.8`) per Rule 12 in `AGENTS.md`.
3. **Small-Team Git Branching**: `main` is production-only. All active work occurs on feature branches (`feature/*`) and is never pushed without explicit user instruction.
4. **Mandatory Governance Documents**: `README.md`, `PLANNING.md`, `ROADMAP.md`, `JOURNAL.md`, `AGENTS.md`, and `TESTING.md`.
