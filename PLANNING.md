# `PLANNING.md` — Active Backlog & Sprint Milestones

Active backlog and task tracking for `outofmylane`.

---

## Active Sprint: Lakefront Theme Cleanup & Lanes Architecture (v0.8.03)

- [x] Branch setup: `feature/lakefront-theme-cleanup` and version bump to `0.8.03`
- [x] Media directory structure (`content/media/` consolidated)
- [x] Pelican configuration updates (`pelicanconf.py`):
  - [x] Default status to draft
  - [x] Static paths configured (`media`, `extra`)
  - [x] Clean navigation (`Home`, `About`)
  - [x] Category renamed to Lanes URL structure (`lanes/{slug}.html`, `lanes.html`)
  - [x] Relocate lane definition directory to `content/lanes/`
  - [x] Pelican signal hook for merging `content/lanes/<lane>.md` and `content/tags/<tag>.md`
  - [x] Remove artificial `STARTER_LANES` to emit only lanes present in `content/lanes/`
  - [x] Remove `home.md` intro hook; featured posts serve top-of-index display
  - [x] Featured items signal hook (`featured: true`, limit 3)
  - [x] Type metadata mapping dictionary
- [x] Lakefront theme cleanup and template consolidation:
  - [x] Purge obsolete templates (`about-this-site.html`, `apps.html`, `prompt-history.html`, `links.html`, `photos.html`, `ideas.html`)
  - [x] Rebuild `base.html` matching reference screenshot header and clean footer
  - [x] Rebuild `index.html` with featured showcase and responsive post stream (single on small screen, double on big screen)
  - [x] Rebuild `page.html`
  - [x] Rebuild `article.html`
  - [x] Create starter `idea.html`
  - [x] Create starter `link.html`
  - [x] Create starter `photo.html`
  - [x] Create starter `chat.html`
  - [x] Rebuild `category.html` (Lane detail)
  - [x] Rebuild `categories.html` (Lanes overview)
  - [x] Rebuild `category_icon.html` with SVG provenance and type badges
  - [x] Create custom `404.html`
- [x] Restyle `style.css` to match reference screenshot typography and layout
- [x] Sample content: `content/posts/photo-lakeshore.md` with featured status and sunrise photo
- [x] Governance and rule updates:
  - [x] Add mandatory obvious placeholder rule to `AGENTS.md` and `.agents/agent_rules.md`
  - [x] Update `README.md`
  - [x] Create `JOURNAL.md`
  - [x] Create `PLANNING.md`
  - [x] Create `ROADMAP.md`
  - [x] Create `TESTING.md`
- [x] Build execution and verification:
  - [x] Run Pelican static build with `uv run pelican content -s pelicanconf.py -o output -d`
  - [x] Validate 0 broken links and 0 ghost content (8 pytest tests passing)
  - [x] Responsive inspection across mobile and desktop viewports
  - [x] Capture visual evidence for user walkthrough

## Active Sprint: GitHub Pages Automated Deployment (v0.8.04)

- [x] Configure production `publishconf.py` (`SITEURL = "https://jimcollinsworth.github.io"`)
- [x] Create GitHub Actions automated deployment workflow (`.github/workflows/deploy.yml`)
- [x] Version bump to `0.8.04` across manifests and configs
- [x] Update governance docs (`PLANNING.md`, `JOURNAL.md`)
- [x] Push to `main` branch to trigger GitHub Pages build and deployment (merged in v0.8.05)

## Active Sprint: Project Pages & Main Deployment (v0.8.05)

- [x] Create standalone published page `content/pages/ai-metronome.md` sourced from `d:\projects\ai-metronome\README.md`
- [x] Create standalone published page `content/pages/sensor-net.md` sourced from `jimcollinsworth/sensor-net`
- [x] Update `themes/lakefront/templates/index.html` and `themes/lakefront/templates/category_icon.html` to list published standalone pages on the index stream
- [x] Update `tests/test_pelican_e2e.py` and `tests/test_playwright_responsive.py` for `ai-metronome.html` and `sensor-net.html`
- [x] Bump version to `0.8.05` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`
- [x] Run Pelican static build (`0.13s`), `pytest` (`29 passed`), and capture visual verification screenshots
- [x] Merge `feature/update-pelican-skills` to `main` and push to `origin/main`

## Active Sprint: Relocate Project Posts & WIP Template (v0.8.05.01)

- [x] Move `ai-metronome.md` and `sensor-net.md` from `content/pages/` to `content/posts/` with `template: wip`
- [x] Add `themes/lakefront/templates/wip.html` and `wip` clock SVG icon in `category_icon.html`
- [x] Restore `themes/lakefront/templates/index.html` stream to `stream_articles`
- [x] Update `tests/test_pelican_e2e.py` and `tests/test_playwright_responsive.py` for `/posts/ai-metronome.html` and `/posts/sensor-net.html`
- [x] Bump version to `0.8.05.01` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`
- [x] Run Pelican build (`0.07s`), `pytest` (`29 passed`), capture root-artifact screenshots and `walkthrough.md`, and commit on `feature/update-pelican-skills`

## Active Sprint: Root Domain Deployment (`jimcollinsworth.github.io`, v0.8.05.02)

- [x] Set `RELATIVE_URLS = True` in `publishconf.py` so links and CSS resolve on `jimcollinsworth.github.io` and `jimcollinsworth.com`
- [x] Bump version to `0.8.05.02` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`
- [ ] Rebuild Pelican, run `pytest`, merge `feature/update-pelican-skills` into `main`, archive legacy `jimcollinsworth.github.io` `main`, push `main` to both repos, and disable Project Pages on `outofmylane`

## Active Sprint: Root-Level Project Routing & Multi-Viewport Snapshots (v0.8.05.03 - v0.8.05.04)

- [x] Fast-forward local `main` to `origin/main` (`0938a2b`) and create branch `feature/project-root-urls`
- [x] Add `type: project`, `url: <slug>.html`, and `save_as: <slug>.html` to `content/posts/ai-metronome.md` and `content/posts/sensor-net.md`
- [x] Add `route_projects_to_root` (`signals.content_object_init`) in `pelicanconf.py` and create `themes/lakefront/templates/project.html`
- [x] Update `tests/test_pelican_e2e.py` and `tests/test_playwright_responsive.py` for root-level project paths
- [x] Build Pelican output (`0.14s`, 3 articles, 1 page), run `pytest` (`29 passed in 7.27s`), and capture viewport-only (`full_page=False`) browser-framed sheets (4-up PDF/HTML sheets + 3-variation × 2-page summary PNG)
- [x] Persist `/learn` rules and skill notes to `AGENTS.md`, `.agents/agent_rules.md`, `.agents/skills/pelican-site-manager/SKILL.md`, and `TESTING.md`
- [x] Bump version to `0.8.05.04` in `pyproject.toml`, `uv.lock`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`, merge `feature/project-root-urls` into `main`, and push `main` to `origin`

---

## Near-Term Backlog

- [ ] Authoring initial content notes for active Lanes: `taichi.md`, `ai.md`, `music.md`
- [ ] Minimal javascript - or toggle/debug - optional tracking and analytics
- [ ] Implement client-side audio player for MIDI/MP3 audio posts
- [ ] Add RSS / Atom feed generation for published posts once content volume grows
- [ ] Implement static search index (e.g. Pagefind or Stork zero-overhead search)
