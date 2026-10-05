# Testing Documentation & Verification Guide: outofmylane

This document defines the testing strategy, test suites, execution commands, browser verification procedures, and operational standards for the static site build.

---

## 1. Testing Architecture & Verification Pyramid

Testing for this static site operates across three distinct tiers:

```
           ▲
          / \
         /   \     Tier 3: Browser Engine & Responsive Verification
        / Tier\    (Playwright Chromium: computed styles, scroll overflow,
       /   3   \   zero console errors, layout mode switching)
      /---------\
     /  Tier 2   \  Tier 2: End-to-End Build & Static Integrity
    /             \ (Pelican CLI output, link crawling, asset resolution,
   /---------------\ route separation, template rendering)
  /     Tier 1      \ Tier 1: Semantic HTML & Accessibility Compliance
 /                   \ (WCAG 2.1/2.2 AA/AAA, aria landmarks, skip links, alt tags,
/_____________________\ touch targets, zero-JS policy verification)
```

---

## 2. Environment & Test Tooling Setup

### Toolchain Versions & Requirements
* **Environment & Package Manager**: `uv` (`.venv/`)
* **Python Runtime**: Python 3.12+
* **Static Site Generator**: `pelican` (v4.12+) with `markdown`, `pyyaml`, `jinja2`, `pillow`
* **Test Framework**: `pytest` (v9.1+)
* **Browser Automation**: `playwright` (v1.63+ / `pytest-playwright`) with Chromium engine
* **CLI Runner Standard**: Windows Command Prompt (`cmd.exe`) via `cmd /c "<command>"`.

### Dependencies (`pyproject.toml`)
```toml
[dependency-groups]
dev = [
    "playwright>=1.63.0",
    "pytest>=9.1.1",
    "pytest-playwright>=0.9.0",
]
```

### Headless Browser Installation
```cmd
cmd /c "uv run playwright install chromium"
```

---

## 3. Session Build Fixture

The Pelican compilation runs once per test session via a session-scoped autouse fixture in the test suites:

```python
import subprocess
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"

@pytest.fixture(scope="session", autouse=True)
def build_site():
    """Execute Pelican build once for the test session."""
    cmd = [
        sys.executable,
        "-m",
        "pelican",
        "content",
        "-s",
        "pelicanconf.py",
        "-o",
        "output",
        "-d",
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"Pelican build failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    assert OUTPUT_DIR.exists(), "Output directory was not created."
```

---

## 4. Test Suites

### Tier 1: Semantic HTML & Accessibility (`tests/test_accessibility.py`)
Performs static parsing on all HTML files in `output/` using regular expressions and string matching:
* **Zero-JS Policy**: Asserts no unauthorized `<script>` tags exist in editorial content.
* **HTML Lang Attribute**: Confirms `<html lang="...">` exists on all pages.
* **Skip Link**: Confirms `<a href="#main-content" class="skip-link">` and `<main id="main-content" tabindex="-1">`.
* **Landmarks**: Validates `role="banner"`, `role="contentinfo"`, and unique `aria-label` attributes on navigation regions.
* **Aria Current**: Validates active page navigation items have `aria-current="page"`.
* **Image Alt Attributes**: Confirms all `<img>` tags possess non-empty `alt` attributes.
* **CSS Accessibility Rules**: Validates `:focus-visible`, `prefers-contrast`, `prefers-reduced-motion`, and `forced-colors` in stylesheet.
* **Touch Target Dimensions**: Checks interactive navigation elements maintain minimum heights (>= 38px / 44px).

### Tier 2: Pelican End-to-End & Integrity (`tests/test_pelican_e2e.py`)
Validates static build generation, content parsing, and integrity:
* **Core Page Existence**: Checks required HTML routes and static assets.
* **Link & Asset Crawler**: Crawls all internal `href` and image `src` paths across generated HTML to verify zero dead links or missing image assets.
* **Source Boundary Validation**: Verifies source Markdown files in `content/` contain zero forbidden source-level badges (`[Mine]`, `[AI]`).

### Tier 3: Browser Engine & Responsive Verification (`tests/test_playwright_responsive.py`)
Launches headless Chromium using Playwright to inspect real browser layout and behavior:
* **Console Error Auditing**: Navigates to all core pages and confirms zero unhandled exceptions or console errors across responsive viewports:
  * `phone_portrait` (390 x 844)
  * `desktop_landscape` (1920 x 1080)
* **Horizontal Scrollbar Overflow**: Asserts `document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2`.
* **Computed Styles & Layout**: Verifies header heights, font sizes, margins, and visibility across breakpoints using `window.getComputedStyle()` and `getBoundingClientRect()`.

---

## 5. Execution Commands

All commands must be executed using Windows Command Prompt (`cmd.exe`).

### Full Test Suite
```cmd
cmd /c "uv run pytest -v"
```

### Targeted Single-File Executions
```cmd
cmd /c "uv run pytest tests/test_accessibility.py -v"
cmd /c "uv run pytest tests/test_pelican_e2e.py -v"
cmd /c "uv run pytest tests/test_playwright_responsive.py -v"
```

### Targeted Smoke Checks (Single Test)
```cmd
cmd /c "uv run pytest tests/test_accessibility.py -k test_html_lang_attribute"
```

### Test Collection Only
```cmd
cmd /c "uv run pytest --collect-only"
```

---

## 6. Operational Gotchas & Lessons Learned

| Issue | Technical Root Cause | Resolution |
| :--- | :--- | :--- |
| **`CRITICAL ValueError: You need to specify a path containing the content`** | Pelican expects the source directory at `content/` as set in `pelicanconf.py`. | Keep `content/` as the primary Git directory. If an Obsidian vault uses an alternate name, create an NTFS directory junction (`mklink /J <vault-name> content`). |
| **Playwright `file:///` Path Resolution** | Windows backslashes (`\`) break URL parsing in Playwright `page.goto()`. | Always format paths with `.resolve().as_posix()` and prefix `file:///`: `f"file:///{path.resolve().as_posix()}"`. |
| **CRLF vs LF False-Positive Diffs** | Windows Git checkouts convert LF to CRLF (`core.autocrlf=true`), causing byte comparison failures against Git HEAD blobs. | Normalize newlines (`.replace(b"\r\n", b"\n")`) before programmatic diffs. |
| **Command Prompt Chaining** | PowerShell fails when executing standard CMD command chaining syntax. | Invoke through `cmd /c "<command>"`. Avoid nested double quotes. |
| **Unnecessary Full Test Runs** | Running entire test suites on minor metadata edits wastes execution time. | Run single-test smoke executions for routine sanity checks. |
