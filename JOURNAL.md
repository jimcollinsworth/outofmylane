# `JOURNAL.md` — Project History & Architectural Decision Records (ADRs)

Chronological record of milestones, architectural decisions, user steering, and technical refactorings for `outofmylane`.

---

## 2026-10-04 — Lakefront Theme Cleanup, Starter Templates & Lanes Pipeline Overhaul

> [!NOTE] User Instructions & Guidance:
> - *"need to clean up theme, AI put in too much actual content from the previous site, there should not be any more content in the site then is in the \content directory, right now i just have content\pages\about.md, but i see broken links for photos and others in the generated site. no categories, tags, links, archives, nothing should exist in the lakefront template or site. Should be Home About on menu. Home page should have short description/text/summary and then a list of all/any posts, of which there are currently none."*
> - *"style is a little off, attach a screen shot of previous site. fix up the lakeshore theme, fix styling and remove any and all content that isn't in the about page or home page now (you can fix up home.md now with summary and single list for small screen and double list for big screen)"*
> - *"give me simple templates to start with - too many in there now to start with, will circle back later for the complex ones like apps and gallery. For now lets start with page, post, idea, link, photo, chat."*
> - *"base.html shouldn't have all those page links in the footer, just about (and home). its a list generated from the pages. If needed the template should code for the empty edge cases."*
> - *"status should default to draft, not published"*
> - *"category will be used as my 'lanes' a key orientation of the site (and me), some starter ones would be 'ai', 'taichi', 'music', 'science', 'photography', 'art', 'crafts', 'diy'..."*
> - *"like the provenance concept - me, mine, ai, ours, theirs, lets simply make it a tag (with tag page override/enhance)"*
> - *"need a way to author prose and other content for specific tags/categories... from the /content/categories directory... (don't generate AI content for missing things, in fact add agent rules to always use obviously placeholder text instead of generating content, unless asked)."*
> - *"add custom 404 page - match theme"*
> - *"consider/how do we handle images, videos, midi and other files... In a media directory? next to the posts? what does pelican expect, what do we need"*

### Problem & Diagnosis
1. An earlier AI session had introduced hardcoded mock content directly into `themes/lakefront/templates/` (e.g., mock photo hero, mock "recent links" with fake AI books, dead links in the footer to ungenerated pages like `apps.html`, `photos.html`, `prompt-history.html`).
2. The UI styling diverged from the clean, open, typography-driven benchmark provided in the author's reference screenshot.
3. Category pages were unstyled and did not allow merging custom human-authored Markdown prose or introductory explanations.
4. Draft status was not defaulted, risking premature publication of working notes.
5. Media directory standards were undefined across Obsidian embeds and Pelican static copying.

### Root Cause & Technical Analysis
- Pelican's default behavior creates categories solely from article metadata tags without associating standalone Markdown documents or intro copy.
- The lakefront templates contained static HTML fixtures instead of relying solely on items present in `content/`.
- `pelicanconf.py` had `STATIC_PATHS` unspecified, preventing structured subfolders (`media/images`, `media/audio`, `media/video`) from being mirrored to `output/`.

### Solution & Standard Procedure
1. **Branch & Version**: Created working branch `feature/lakefront-theme-cleanup` and bumped version to `0.8.02` in `pyproject.toml`.
2. **Ghost Content Purge**: Removed all hardcoded mock content, unused templates (`about-this-site.html`, `apps.html`, `prompt-history.html`), and purged broken links from `base.html`.
3. **Starter Templates**: Consolidated templates to `page.html`, `article.html`, `idea.html`, `link.html`, `photo.html`, `chat.html`, and `404.html`.
4. **Header & Footer Restructure**: Realigned `base.html` to mirror the reference screenshot: prominent author name on left, horizontal nav below it, site moniker on the right in muted gray, separated by a crisp 1px rule. Footer strictly limited to Home and About plus accessibility toggles.
5. **Responsive Home Stream**: Configured `index.html` to pull intro text from `content/pages/home.md` and display a clean post list that adapts to a single column on mobile and a two-column grid on desktop/TV displays, with clean empty-state handling for 0 posts.
6. **Lanes & Tags Prose-Merge Hook**: Implemented a Pelican signal handler (`merge_lane_and_tag_metadata`) in `pelicanconf.py` that merges frontmatter and Markdown body from `content/categories/<lane>.md` and `content/tags/<tag>.md` into Pelican `Category` and `Tag` objects (`category.name`, `category.title`, `category.summary`, `category.intro_html`).
7. **Draft by Default**: Configured `DEFAULT_METADATA = {'status': 'draft'}` in `pelicanconf.py`.
8. **Media Directory Architecture**: Structured `content/media/` (`images/`, `audio/`, `video/`, `docs/`) with `STATIC_PATHS = ["media", "extra"]`. Deleted redundant `content/attachments/` directory to maintain a single canonical media source.
9. **Mandatory Placeholder Rule**: Codified the rule into `AGENTS.md` and `.agents/agent_rules.md` requiring obvious placeholder text (e.g. `[Placeholder summary]`) for missing content, strictly prohibiting fabricated AI prose.
10. **Featured Content Pipeline**: Implemented `collect_featured_items` signal in `pelicanconf.py` scanning pages, articles, categories, and tags for `featured: true` or numeric order, capped at 3 items. Populated user's sample post `content/posts/photo-lakeshore.md` pointing to `content/media/images/sky-clouds.jpg`.
11. **Governance Documentation**: Updated `README.md`, `PLANNING.md`, `ROADMAP.md`, and this journal.

---

## 2026-10-05 — Pure Content-Driven Lanes, Directory Relocation & Featured Showcase Primacy

> [!NOTE] User Instructions & Guidance:
> - *"i removed the home.md we don't need that to feed the index page, instead the featured posts do the same purpose, let me display arbitrary content at the top of the index page. better and more consistent than home.md->index"*
> - *"where did all the category pages come from, we only have taichi in content, so there should only be a taichi category in output."*
> - *"just lanes, not pursuit lanes"*
> - *"we can use /content/lanes, instead of content/categories"*

### Problem & Diagnosis
1. An artificial list of starter lanes (`STARTER_LANES`) in `pelicanconf.py` injected 8 categories into `generator.categories` during the build, producing unauthored category output files (`lanes/ai.html`, `lanes/art.html`, etc.) when only `taichi.md` existed in content.
2. The category prose folder was named `/content/categories` rather than the canonical `/content/lanes`.
3. The Lanes index template (`categories.html`) contained the label "Pursuit Lanes" and an unrequested editorial paragraph.
4. The Home page template (`index.html`) contained an intro prose block and fallback copy rather than letting featured posts sit directly at the top.

### Root Cause & Technical Analysis
- `pelicanconf.py` populated starter categories programmatically to demonstrate taxonomies, violating the principle of generating only what exists in `content/`.
- In Pelican's `URLWrapper` / `Category`, assigning `cat.name` directly resets `_slug` to regenerate from the name via `slugify()` unless `cat.slug = slug` is invoked explicitly through the property setter, causing `valid_lanes` filtering mismatches.

### Solution & Standard Procedure
1. **Remove Starter Categories**: Deleted `STARTER_LANES` from `pelicanconf.py`.
2. **Relocate to `/content/lanes/`**: Pointed the lane metadata merge hook to `content/lanes/`.
3. **Strict Lane Output Enforcement**: Configured `merge_lane_and_tag_metadata` to prune `generator.categories` to only categories authored in `content/lanes/*.md`. For unassigned articles, cleared `art.category = None` to prevent broken links.
4. **Remove `home.md` Pipeline**: Deleted `extract_home_page_intro` from `pelicanconf.py` and removed the `<div class="page-intro">` block from `themes/lakefront/templates/index.html`. Featured posts now render immediately at the top of the Home page.
5. **Rename "Pursuit Lanes" to "Lanes"**: Updated `categories.html` header to `Lanes` and removed the fabricated explanatory paragraph.
6. **Automated Verification**: Added `test_lanes_strictly_from_content` to `tests/test_pelican_e2e.py` verifying that `output/lanes/` contains exactly 1 lane (`taichi.html`). All 8 tests pass in 0.22s.
7. **Version Bump**: Incremented version to `0.8.03` in `pyproject.toml` and `pelicanconf.py`.

---

## 2026-10-05 — GitHub Pages Automated Deployment Pipeline (v0.8.04)

> [!NOTE] User Instructions & Guidance:
> - *"Lets push it all now to my github io site"*
> - Deployment preference: Set up GitHub Actions workflow to automatically build and deploy the site to GitHub Pages on push to `main`. Target URL: `https://jimcollinsworth.github.io`.

### Problem & Diagnosis
- The repository lacked an automated CI/CD deployment pipeline to build Pelican and publish artifacts to GitHub Pages upon pushing to `main`.
- `publishconf.py` had an empty `SITEURL` setting.

### Root Cause & Technical Analysis
- Without `.github/workflows/deploy.yml` configuring GitHub Pages deployment via `actions/deploy-pages@v4`, pushes to `main` do not automatically publish live static HTML to GitHub Pages.

### Solution & Standard Procedure
1. **GitHub Pages Actions Workflow**: Created `.github/workflows/deploy.yml` with `actions/checkout@v4`, `astral-sh/setup-uv@v5`, `uv run pelican content -s publishconf.py -o output -d`, `actions/upload-pages-artifact@v3`, and `actions/deploy-pages@v4`.
2. **Production Site URL Configuration**: Set `SITEURL = "https://jimcollinsworth.github.io"` and `RELATIVE_URLS = False` in `publishconf.py`.
3. **Version Synchronization**: Incremented project version to `0.8.04` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`.

---

## 2026-11-17 — Add AI Metronome and Sensor Net Pages & Deploy to Main (v0.8.05)

> [!NOTE] User Instructions & Guidance:
> - *"Add pages for ai-metronome.md and sensor-net.mk, merge deploy"*
> - *"SensorNet and AI Metronome are in the projects directory and GitHub repos"*
> - *"What's the problem? What do we know now? Can we continue and deploy?"*

### Problem & Diagnosis
1. `content/pages/` contained only `about.md`; neither `ai-metronome.md` nor `sensor-net.md` existed in the repository.
2. `themes/lakefront/templates/index.html` iterated only over `articles`, so published standalone pages in `content/pages/` other than `about.md` were not listed on the home page.
3. `themes/lakefront/templates/category_icon.html` accessed `article.tags` unconditionally inside `article_icons()`, which fails on Pelican `Page` objects that lack a `tags` attribute unless guarded.
4. `sensor-net` had no local folder in `d:\projects`, requiring inspection of the GitHub repository `jimcollinsworth/sensor-net`.

### Root Cause & Technical Analysis
- Pelican stores `content/pages/*.md` items in `pages` rather than `articles` and omits the `tags` attribute from `Page` instances by default.
- The `feature/update-pelican-skills` branch had not yet been merged into `main` to trigger `.github/workflows/deploy.yml`.

### Solution & Standard Procedure
1. **Added Project Pages**: Created `content/pages/ai-metronome.md` (from `d:\projects\ai-metronome\README.md`) and `content/pages/sensor-net.md` (from `jimcollinsworth/sensor-net`) with `status: published` and `type: project` (authored by `Jim Collinsworth, LLM-Argon`).
2. **Updated Lakefront Templates**: Added a `tags` guard to `article_icons()` in `themes/lakefront/templates/category_icon.html` and appended non-`about`/`home`/non-featured `pages` to `stream_items` in `themes/lakefront/templates/index.html`.
3. **Updated Tests & Version**: Added `ai-metronome.html` and `sensor-net.html` checks to `tests/test_pelican_e2e.py` and `tests/test_playwright_responsive.py`, and incremented the version to `0.8.05` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`.
4. **Build, Verify, Merge & Push**: Built output with Pelican, executed `uv run pytest -v`, captured screenshots, merged `feature/update-pelican-skills` into `main`, and pushed `main` to `origin`.

---

## 2026-11-17 — Relocate Project Posts to `content/posts/` with `wip` Template & Fix Screenshot Previews (v0.8.05.01)

> [!NOTE] User Instructions & Guidance:
> - *"Move the 2 new pages into posts, mark as wip template, fix visual verification,  no previews"*

### Problem & Diagnosis
1. `ai-metronome.md` and `sensor-net.md` were placed in `content/pages/` (`/<slug>.html`) instead of `content/posts/` (`/posts/<slug>.html`).
2. Lakefront lacked a `wip.html` template and `wip` clock icon inside `category_icon.html` for articles specifying `template: wip`.
3. Visual verification images in the v0.8.05 response used nested subdirectories and Windows backslashes (`C:\...`), causing preview embeds not to render in the chat UI.

### Root Cause & Technical Analysis
- Pelican routes files under `content/posts/` to `posts/{slug}.html` and selects the template matching frontmatter `template: wip` (`themes/lakefront/templates/wip.html`).
- Markdown image rendering requires forward-slash paths pointing to files located directly in the artifact directory (`<appDataDir>/brain/<conversation-id>/`).

### Solution & Standard Procedure
1. **Moved Content to Posts**: Removed `content/pages/ai-metronome.md` and `content/pages/sensor-net.md`, created `content/posts/ai-metronome.md` and `content/posts/sensor-net.md` with `template: wip`, `status: published`, and removed duplicate body H1 titles.
2. **Added `wip` Template & Icon**: Created `themes/lakefront/templates/wip.html`, added the `wip` clock SVG icon and `article_icons()` guard in `themes/lakefront/templates/category_icon.html`, and restored `stream_articles` iteration in `themes/lakefront/templates/index.html`.
3. **Updated Tests & Version**: Updated `tests/test_pelican_e2e.py` and `tests/test_playwright_responsive.py` to check `posts/ai-metronome.html` and `posts/sensor-net.html`, and incremented version to `0.8.05.01`.
4. **Fixed Visual Verification**: Rebuilt output, executed `pytest`, copied `.png` screenshots into the root artifact directory, created `walkthrough.md`, and committed changes locally on `feature/update-pelican-skills`.

---

## 2026-11-17 — Deploy `outofmylane` to Root Repository `jimcollinsworth.github.io` (v0.8.05.02)

> [!NOTE] User Instructions & Guidance:
> - *"Why is thd new site deployed to jimcollinsworth.github.io/outofmylane,  but there is old content at root"*
> - *"New site should be at root"*

### Problem & Diagnosis
1. GitHub Pages serves the root site (`https://jimcollinsworth.github.io/` / `https://jimcollinsworth.com/`) from `jimcollinsworth/jimcollinsworth.github.io`, while `jimcollinsworth/outofmylane` deploys as a Project Site at `/outofmylane/`.
2. `publishconf.py` set `RELATIVE_URLS = False` with `SITEURL = "https://jimcollinsworth.github.io"`, while `jimcollinsworth.github.io` has custom domain `jimcollinsworth.com` configured (`cname: "jimcollinsworth.com"`).

### Root Cause & Technical Analysis
- `origin` in `d:\projects\outofmylane` pointed only to `jimcollinsworth/outofmylane.git`.
- Pushing `main` to `jimcollinsworth/outofmylane` triggered GitHub Pages at `/outofmylane/` without updating `jimcollinsworth/jimcollinsworth.github.io`.

### Solution & Standard Procedure
1. **Relative Production URLs**: Set `RELATIVE_URLS = True` in `publishconf.py` and bumped version to `0.8.05.02` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`.
2. **Legacy Root Archive**: Added `root-pages` remote (`jimcollinsworth/jimcollinsworth.github.io.git`), fetched `root-pages/main`, and pushed its previous commit state to `archive/legacy-site-2026-10`.
3. **Dual-Remote Root Deployment**: Merged `feature/update-pelican-skills` into `main`, pushed `main` to both `jimcollinsworth/outofmylane` and `jimcollinsworth/jimcollinsworth.github.io`, and disabled Project Site Pages on `jimcollinsworth/outofmylane`.

---

## 2026-11-18 — Root-Level Routing for Project Posts & Multi-Viewport Snapshot Verification (v0.8.05.03)

> [!NOTE] User Instructions & Guidance:
> - *"update our project repo, this is my new personal blog."*
> - *"update the sensor-net and ai-metronome posts so they appear at the root, i assume we can override with meta data? all projects will at root level and these are projects, not posts, not pages i guess. do the updates, also need to see a snapshot series of the site (phone, tablet, desktop.., portrait/landscape)."*

### Problem & Diagnosis
1. The local working copy was behind `origin/main` at commit `f0a6073`, while `origin/main` had advanced to `0938a2b` (`v0.8.05.02`) containing `content/posts/ai-metronome.md`, `content/posts/sensor-net.md`, `themes/lakefront/templates/wip.html`, `tests/test_playwright_responsive.py`, and `tools/screenshots.py`.
2. `pelicanconf.py` routed all `content/posts/*.md` articles to `posts/{slug}.html` via `ARTICLE_URL` and `ARTICLE_SAVE_AS`, so `ai-metronome` and `sensor-net` were emitted under `output/posts/` instead of the root directory.
3. Neither project metadata (`url`, `save_as`, `type: project`) nor a signal hook existed to route `project` entries from `content/posts/` to root `{slug}.html`, and `themes/lakefront/templates/project.html` did not exist.
4. `tests/test_pelican_e2e.py` and `tests/test_playwright_responsive.py` asserted `posts/ai-metronome.html` and `posts/sensor-net.html` and `test_no_unauthored_or_corrupt_pages()` only checked `content/pages/*.md` for root HTML files.

### Root Cause & Technical Analysis
- Pelican applies `ARTICLE_URL = 'posts/{slug}.html'` and `ARTICLE_SAVE_AS = 'posts/{slug}.html'` globally to files in `ARTICLE_PATHS = ['posts']` unless overridden per article via `url` and `save_as` frontmatter keys or `override_url` / `override_save_as` during `signals.content_object_init`.
- Setting `type: project` without a `project.html` template risks `TemplateNotFound` if an author sets `template: project` directly instead of `template: wip`.

### Solution & Standard Procedure
1. **Sync & Branch**: Fast-forwarded `main` from `f0a6073` to `0938a2b` via `git pull --ff-only origin main` and created working branch `feature/project-root-urls`.
2. **Project Frontmatter Overrides**: Added `type: project`, `url: <slug>.html`, and `save_as: <slug>.html` (keeping `template: wip` and `status: published`) to `content/posts/ai-metronome.md` and `content/posts/sensor-net.md`.
3. **Automatic Root Project Routing & Template**: Added `route_projects_to_root` connected to `signals.content_object_init` in `pelicanconf.py` to default `override_url` and `override_save_as` to `{slug}.html` for any `Article` with `type: project` or `template: project`. Created `themes/lakefront/templates/project.html` (attributed to `Jim Collinsworth & LLM-Gemini3.8, LLM-Argon`).
4. **Tests & Documentation**: Updated `tests/test_pelican_e2e.py` (root file assertions, negative `output/posts/` checks, and `content/posts/*.md` stem inclusion in `test_no_unauthored_or_corrupt_pages`) and `tests/test_playwright_responsive.py`. Documented `type`, `url`, and `save_as` in `README.md` and incremented version to `0.8.05.03` in `pyproject.toml`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`.
5. **Build & Verification**: Built static output via `uv run pelican content -s pelicanconf.py -o output -d` (`0.19s`, 3 articles, 1 page), verified all `29` tests pass via `uv run pytest -v` (`8.98s`), and captured 24 screenshots via `tools/screenshots.py` across 8 viewports (`phone`, `tablet`, `laptop`, `desktop_tv` in `portrait` and `landscape`) for `index.html`, `ai-metronome.html`, and `sensor-net.html`.

---

## 2026-11-18 — `/learn` Visual Verification Standard, Docs Update & Release to `main` (v0.8.05.04)

> [!NOTE] User Instructions & Guidance:
> - *"wow, those were not screenshots you just rendered all the content, dumb. i need to see scrreen shots of each example page running in a browser/playwrite in various orientations and then combined onto a document maybe 4 per page."*
> - *"ok, just 3 variations on the screen sizes/orientations, and then 2 different pages. i assume ai-metronome and sensor-net are at root now. /learn update lessons, journal, other docs, merge to main, push to origin. done for the day on this"*

### Problem & Diagnosis
1. `tools/screenshots.py` defaulted to `full_page=True`, which expanded screenshots vertically to full document scroll height, removing portrait vs. landscape viewport proportions.
2. Embedding 24 unframed full-scroll PNGs vertically in Markdown caused the UI to render them as raw repeated page text instead of browser viewport previews.
3. Inside flexbox browser window frames (`inline-flex` column), an unconstrained `.browser-chrome` header stretched narrow portrait `<img>` elements horizontally until `.browser-chrome` used `width: 0; min-width: 100%` and `img` used `object-fit: contain`.
4. Running `uv run` without `--frozen` on `uv 0.6.10` downgraded `uv.lock` from `revision = 3` to `revision = 1` across package entries.

### Root Cause & Technical Analysis
- Viewport verification requires `full_page=False` with proportional scaling (`object-fit: contain`) inside a constrained browser chrome header (`width: 0; min-width: 100%`) grouped onto composite multi-up contact sheets rather than full-scroll dumps.
- Keeping `uv.lock` aligned requires bumping only the `outofmylane` package version entry and passing `--frozen` to `uv run`.

### Solution & Standard Procedure
1. **Viewport Contact Sheets**: Captured `full_page=False` browser-framed viewport screenshots for `index.html`, `ai-metronome.html`, `sensor-net.html`, and `about.html` across 8 viewports combined 4 per page into `responsive_snapshots_4up.pdf` / `.html` and 3 variations (`390x844`, `1180x820`, `1920x1080`) × 2 pages (`index.html`, `ai-metronome.html`) into `sheet_3x2_summary.png`.
2. **Persisted Rules & Skills (`/learn`)**:
   - Updated `AGENTS.md` (Section 11) and `.agents/agent_rules.md` (Section 8) to require `full_page=False` browser-framed composite contact sheets across 3 viewport variations × 2 pages.
   - Updated `.agents/skills/pelican-site-manager/SKILL.md` (Section 5 item 9 for root-level project routing from `content/posts/`, Section 6 item 4 for viewport-only composite checks).
   - Updated `TESTING.md` (Section 6) with gotchas for `full_page=True` distortion, `content/posts/*.md` root allowlist checks, and `uv.lock` `--frozen` usage.
3. **Version, Build, Merge & Push**: Incremented version to `0.8.05.04` in `pyproject.toml`, `uv.lock`, `pelicanconf.py`, `PLANNING.md`, and `JOURNAL.md`; verified `pelican` build and `29` passing `pytest` checks; committed on `feature/project-root-urls`; merged `--no-ff` into `main`; and pushed `main` to `origin`.





