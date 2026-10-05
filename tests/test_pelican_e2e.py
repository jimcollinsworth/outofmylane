"""
test_pelican_e2e.py — Tier 2 End-to-End Build & Static Link Integrity Tests
Author: Jim Collinsworth & LLM-Gemini3.8
"""

from pathlib import Path
import re
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"


def test_core_pages_exist():
    """Verify essential pages are generated in output/."""
    assert (OUTPUT_DIR / "index.html").exists(), "index.html must exist"
    assert (OUTPUT_DIR / "about.html").exists(), "about.html must exist"
    assert (OUTPUT_DIR / "lanes.html").exists(), "lanes.html must exist"
    assert (OUTPUT_DIR / "tags.html").exists(), "tags.html must exist"
    assert (OUTPUT_DIR / "theme" / "css" / "style.css").exists(), "style.css must exist"


def test_no_unauthored_or_corrupt_pages():
    """Ensure all root HTML files correspond to source content or standard entry points, and no corrupt artifacts exist."""
    content_dir = REPO_ROOT / "content"
    pages_dir = content_dir / "pages"
    authored_pages = {f"{p.stem}.html" for p in pages_dir.glob("*.md")} if pages_dir.exists() else set()
    standard_entry_points = {"index.html", "lanes.html", "tags.html", "404.html"}
    expected_root_html = authored_pages | standard_entry_points

    # 1. Corrupt artifact check
    corrupt_filenames = ["false", "''", '""', "none", "null"]
    for corrupt in corrupt_filenames:
        assert not (OUTPUT_DIR / corrupt).exists(), f"Corrupt artifact '{corrupt}' found in output/"

    # 2. Check that root HTML pages only come from authored content or standard entry points
    root_html_files = {p.name for p in OUTPUT_DIR.glob("*.html")}
    unexpected_html = root_html_files - expected_root_html
    assert not unexpected_html, f"Unexpected unauthored HTML pages found in output/: {unexpected_html}"


def test_internal_links_resolve():
    """Crawl all relative internal href links in HTML files and verify targets exist."""
    href_pattern = re.compile(r"href=[\"']([^\"'#]+)(?:#[^\"']*)?[\"']", re.IGNORECASE)
    html_files = list(OUTPUT_DIR.glob("**/*.html"))

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        matches = href_pattern.findall(content)
        for link in matches:
            # Skip external links, mailto, and fragment-only links
            if link.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
                continue

            # Resolve relative link relative to the current file's parent directory
            target_path = (html_file.parent / link).resolve()

            # Ignore missing favicon if not provided yet
            if "favicon" in link:
                continue

            assert target_path.exists(), (
                f"Broken internal link '{link}' in {html_file.relative_to(REPO_ROOT)}: "
                f"Resolved target does not exist at {target_path}"
            )


def test_lanes_strictly_from_content():
    """Verify that output/lanes/ only contains lanes authored in content/lanes/."""
    lanes_output_dir = OUTPUT_DIR / "lanes"
    assert lanes_output_dir.exists(), "output/lanes/ directory must exist"
    lane_pages = list(lanes_output_dir.glob("*.html"))
    assert len(lane_pages) == 1, f"Expected exactly 1 lane page, found {len(lane_pages)}: {lane_pages}"
    assert (lanes_output_dir / "taichi.html").exists(), "taichi.html must exist in output/lanes/"

