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
- [ ] Push to `main` branch to trigger GitHub Pages build and deployment

---

## Near-Term Backlog

- [ ] Authoring initial content notes for active Lanes: `taichi.md`, `ai.md`, `music.md`
- [ ] Minimal javascript - or toggle/debug - optional tracking and analytics
- [ ] Chinese support (post variants / cross-platform links for TikTok/RedNote)
- [ ] Implement client-side audio player for MIDI/MP3 audio posts
- [ ] Add RSS / Atom feed generation for published posts once content volume grows
- [ ] Implement static search index (e.g. Pagefind or Stork zero-overhead search)
