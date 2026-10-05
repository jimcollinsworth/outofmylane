"""
test_accessibility.py — Tier 1 Semantic HTML & Accessibility Compliance Tests
Author: Jim Collinsworth & LLM-Gemini3.8
"""

from pathlib import Path
import re
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"


@pytest.fixture(scope="session")
def html_files():
    """Retrieve all generated HTML files in output/ directory."""
    assert OUTPUT_DIR.exists(), "Output directory must exist. Run pelican build first."
    files = list(OUTPUT_DIR.glob("**/*.html"))
    assert len(files) > 0, "No HTML files found in output directory."
    return files


def test_zero_js_policy(html_files):
    """Assert zero unauthorized <script> tags exist in any generated HTML page."""
    script_pattern = re.compile(r"<script[\s>]", re.IGNORECASE)
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        assert not script_pattern.search(content), f"Found <script> tag in {html_file.name} violating zero-JS policy"


def test_html_lang_attribute(html_files):
    """Confirm <html lang="..."> attribute is present on all HTML pages."""
    lang_pattern = re.compile(r"<html\s+[^>]*lang=[\"'][^\"']+[\"']", re.IGNORECASE)
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        assert lang_pattern.search(content), f"Missing html lang attribute in {html_file.name}"


def test_skip_link_present(html_files):
    """Confirm skip-to-content link and target exist on all pages."""
    skip_pattern = re.compile(r"<a\s+href=[\"']#main-content[\"']\s+class=[\"']skip-link[\"']", re.IGNORECASE)
    target_pattern = re.compile(r"<main\s+id=[\"']main-content[\"']", re.IGNORECASE)
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        assert skip_pattern.search(content), f"Missing skip-link in {html_file.name}"
        assert target_pattern.search(content), f"Missing main#main-content in {html_file.name}"


def test_aria_landmarks(html_files):
    """Validate standard ARIA landmarks across all pages."""
    banner_pattern = re.compile(r"role=[\"']banner[\"']", re.IGNORECASE)
    contentinfo_pattern = re.compile(r"role=[\"']contentinfo[\"']", re.IGNORECASE)
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        assert banner_pattern.search(content), f"Missing role='banner' in {html_file.name}"
        assert contentinfo_pattern.search(content), f"Missing role='contentinfo' in {html_file.name}"
