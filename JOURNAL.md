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

