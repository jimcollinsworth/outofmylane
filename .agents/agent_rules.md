# Agent Guidelines & Rules: outofmylane

This document outlines the operational principles, technical constraints, design philosophy, authoring boundaries, and procedures for any LLM coding agent maintaining Jim Collinsworth's personal site **out of my lane** (`outofmylane`).

---

## 1. Mandatory Governance Documents

> [!IMPORTANT]
> The agent is authorized and permitted to maintain the core system, governance, and planning documents:
> 1. `README.md` – Site overview, architecture, developer utilities, publishing instructions, and directory map.
> 2. `PLANNING.md` – Active backlog, sprint tasks, and near-term milestones.
> 3. `ROADMAP.md` – Long-term discussion of features, brainstorming, creative ideas, and future possibilities.
> 4. `JOURNAL.md` – Chronological project log recording milestones, technical decisions, and changes.
> 5. `AGENTS.md` (and `.agents/agent_rules.md`) – Operational principles, technical constraints, authoring boundaries, and small-team workflow rules.
> 6. `TESTING.md` – Comprehensive test strategy, test suites, execution commands, and browser verification procedures.
>
> **NO other system design, architecture, walkthrough, or meta documents may be created anywhere in this repository or workspace without first explicitly proposing them to Jim and receiving approval.**

---

## 2. Content Authoring Boundaries & 100% Human Source Rules (Strict)

> [!CAUTION]
> **Content Belongs Exclusively to Jim**:
> - Everything in `content/` (`content/posts/`, `content/pages/`) is authored exclusively by Jim.
> - **Zero AI Content in `content/`**: No file inside `content/` contains AI-generated text, AI drafts, or AI summaries.
> - **Mandatory Obvious Placeholder Rule**: When structural scaffolding or missing copy is required, the agent must **ALWAYS use obviously placeholder text** (e.g. `[Placeholder summary]`, `[Lane notes in progress]`) instead of fabricating or generating simulated editorial content, unless explicitly instructed by Jim.
> - The agent must **NEVER draft content documents, essays, articles, posts, or personal notes** for Jim.
> - The agent must **NEVER create new content files** on its own initiative.
> - The agent's role is strictly technical stewardship: maintaining clean HTML/CSS infrastructure, ensuring responsive layouts, verifying link integrity, managing assets, and maintaining governance documents.


---

## 3. Technical Philosophy & Constraints

1. **Pure Static Generation via Pelican**:
   - Built with Pelican Python static site generator from clean Markdown sources in `content/`.
   - Pure Python ecosystem managed via `uv` (`.venv/`).
   - Output compiled to `output/` and deployed to GitHub Pages.
2. **Active Theme (`themes/lakefront`)**:
   - Packaged custom theme located in `themes/lakefront/`.
   - Configured via `THEME = 'themes/lakefront'` in `pelicanconf.py`.
3. **Zero JavaScript Policy**:
   - The site operates completely with zero client-side JavaScript (`<script>` tags are strictly disallowed on published content pages).
   - Interactivity is achieved through semantic HTML (e.g., `<details>`, `<summary>`, anchor links) and modern CSS.
4. **Responsive & Accessible by Default**:
   - Mobile-first, fluid responsive layout.
   - High color contrast and legible type scaling.
   - Built-in automatic light and dark mode via CSS media query (`@media (prefers-color-scheme: dark)`).
   - Standard semantic markup: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<figure>`, `<figcaption>`, `<footer>`.

---

## 4. Visual & Typographic Design Principles

- **Lakefront Theme Design Ethos**: Extreme minimalism, fast loading, distraction-free reading, comfortable reading line length (60–75 characters, max width ~680px–740px), and clean vertical rhythm.
- **Header Branding**: Title (`out of my lane`) and Subtitle (`Jim Collinsworth`).
- **Elimination of Redundant Action Links & Vertical Density**:
  - The item or post title is always the primary click target.
  - Section-level links (e.g., `(ALL)`) are placed inline directly adjacent to headings.

---

## 5. Command Line Standards & Terminal Execution Safety (Strict)

> [!CAUTION]
> **Strict Terminal Execution Requirements**:
> - **Explicit `cmd /c` Runner Invocations**: Whenever executing terminal commands via `run_command`, the agent MUST invoke `cmd /c "<command>"` (e.g., `cmd /c "uv run pelican content -s pelicanconf.py -o output -d"`).
> - **Standard CMD Syntax Only**: Use standard Command Prompt syntax (`dir`, `copy`, `del`, `rmdir /s /q`).

---

## 6. Continuous Commit-Level Versioning Protocol

Every commit and meaningful change set must increment the project version:
- **Major/Feature Changes (`0.1.0` $\rightarrow$ `0.2.0`)**: New pages, layout restructurings, architectural updates.
- **Incremental Refinements (`0.1.0.01` $\rightarrow$ `0.1.0.02`)**: Style tweaks, documentation updates, bugfixes, rule adjustments.
- Synchronize `pyproject.toml` to the current version.

---

## 7. Small-Team Git Branching & Remote Operations (Strict)

> [!CAUTION]
> **Branching & Deployment Invariants**:
> 1. **`main` is Production-Only**: Merging to `main` and pushing to `origin main` is performed **ONLY** upon Jim's explicit instruction to "push", "publish", or "release".
> 2. **Feature & Bug Branches for All Work**: All active work must occur on dedicated working branches (`feature/*`, `bug/*`, or `dev`).
> 3. **No Remote Pushes Without Explicit Confirmation**: The agent must **NEVER push commits to any remote repository (`git push`) without Jim's explicit request or confirmation**.
