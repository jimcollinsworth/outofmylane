# Pelican Testing Reference Guide (outofmylane)

A technical reference guide detailing the testing architecture, browser verification strategies, accessibility enforcement, and execution standards for Pelican static site generation.

---

## 1. Overview & Verification Strategy

Pelican static site generation is validated through three distinct testing layers:
1. **Tier 1: Semantic HTML & Accessibility Compliance (`tests/test_accessibility.py`)**: Static analysis validating WCAG 2.1/2.2 standards, landmark roles, skip links, image alt attributes, touch targets, and the zero-client-side JavaScript policy.
2. **Tier 2: End-to-End Build & Static Integrity (`tests/test_pelican_e2e.py`)**: Static build validation confirming file generation, link and asset integrity crawling, route isolation, title deduplication, and Markdown source boundaries.
3. **Tier 3: Headless Browser Engine & Responsive Verification (`tests/test_playwright_responsive.py`)**: Chromium browser verification using Playwright, inspecting computed CSS styles, layout bounding boxes, horizontal scroll overflow, and interactive controls.

For comprehensive test suite details, see [TESTING.md](../TESTING.md).

---

## 2. Environment & CLI Execution

### Dependencies
* `uv` package manager with Python 3.12+
* `pytest` (>= 9.1)
* `pytest-playwright` and `playwright` with Chromium installed
* `pelican` (4.12+)

### Headless Browser Setup
```cmd
cmd /c "uv run playwright install chromium"
```

### Running Tests
Execute all commands via Windows Command Prompt (`cmd.exe`):

* **Single Smoke Check**:
  ```cmd
  cmd /c "uv run pytest tests/test_accessibility.py -k test_html_lang_attribute"
  ```
* **Full Test Suite**:
  ```cmd
  cmd /c "uv run pytest -v"
  ```

---

## 3. Playwright Browser Verification Best Practices

### A. Local File URL Navigation
Navigate local files using the `file:///` scheme and forward slashes:
```python
target_file = OUTPUT_DIR / "index.html"
page.goto(f"file:///{target_file.resolve().as_posix()}")
```
*Note*: `response.status` returns `0` (or `200`) for `file://` protocols. Both are valid.

### B. Viewport & Layout Overflow Testing
Test at specific responsive breakpoints:
* Mobile Portrait: 390 x 844
* Mobile Landscape: 844 x 390
* Laptop / Desktop: 1366 x 768 / 1920 x 1080

Assert that no element forces horizontal page overflow:
```python
scroll_width = page.evaluate("() => document.documentElement.scrollWidth")
client_width = page.evaluate("() => document.documentElement.clientWidth")
assert scroll_width <= client_width + 2
```

### C. Computed Styles & Interactivity Validation
Assert against computed styles via `window.getComputedStyle()` or element attributes (e.g. `hasAttribute('open')`) rather than assuming CSS rules applied cleanly.

---

## 4. Key Gotchas & Troubleshooting

1. **Source Directory Mismatch (`PATH = 'content'`)**:
   Pelican requires the `content` folder to exist in the repository root. If Obsidian uses a different folder name, create an NTFS junction (`mklink /J <vault-name> content`) rather than moving or renaming the folder.
2. **Windows Backslash Escapes**:
   Always normalize paths to POSIX slashes (`.as_posix()`) when passing URIs to browser automation.
3. **CRLF vs LF Comparisons**:
   When comparing disk files to Git tree objects, strip `\r` carriage returns to prevent false differences.
