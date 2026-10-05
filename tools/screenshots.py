#!/usr/bin/env python3
"""
tools/screenshots.py — Multi-Resolution Screenshot Utility for jimcollinsworth.github.io.

Captures any site page across 4 screen sizes and 2 orientations (8 viewports total):
  1. Phone:             390x844 (portrait) / 844x390 (landscape)
  2. Tablet:            820x1180 (portrait) / 1180x820 (landscape)
  3. Laptop:            768x1366 (portrait) / 1366x768 (landscape)
  4. Large Desktop/TV:  1080x1920 (portrait) / 1920x1080 (landscape)

Uses pure Python Playwright (no Node.js / npm).

Usage:
  # Capture home page (index.html) across all 8 viewports in light mode
  uv run python tools/screenshots.py

  # Capture a specific page
  uv run python tools/screenshots.py --page about.html
  uv run python tools/screenshots.py --page posts.html
  uv run python tools/screenshots.py --page posts/sleep-movement-evaluation-plan.html

  # Capture dark mode
  uv run python tools/screenshots.py --color-scheme dark

  # Capture both light and dark modes
  uv run python tools/screenshots.py --color-scheme both

  # Only viewport (above the fold) rather than full page
  uv run python tools/screenshots.py --viewport-only

  # Specific device or orientation
  uv run python tools/screenshots.py --device phone --orientation portrait
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Error: Playwright is not installed. Run 'uv add --dev playwright pytest-playwright' "
        "and 'uv run playwright install chromium'."
    )
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"

# Viewport Matrix: Name -> {portrait: (w, h), landscape: (w, h)}
VIEWPORT_MATRIX: Dict[str, Dict[str, Tuple[int, int]]] = {
    "phone": {
        "portrait": (390, 844),
        "landscape": (844, 390),
    },
    "tablet": {
        "portrait": (820, 1180),
        "landscape": (1180, 820),
    },
    "laptop": {
        "portrait": (768, 1366),
        "landscape": (1366, 768),
    },
    "desktop_tv": {
        "portrait": (1080, 1920),
        "landscape": (1920, 1080),
    },
}

DEVICE_LABELS = {
    "phone": "Phone (iPhone / Modern Mobile)",
    "tablet": "Tablet (iPad / Tablet)",
    "laptop": "Laptop (13-15\" Display)",
    "desktop_tv": "Large Desktop / TV (1080p)",
}


def resolve_page_target(page_arg: str) -> Tuple[str, str]:
    """
    Resolves the target page into a loadable URL (file:// or http://)
    and returns a clean slug for directory naming.
    """
    if page_arg.startswith(("http://", "https://")):
        slug = page_arg.split("/")[-1] or "home"
        slug = slug.replace(".html", "").replace("?", "_")
        return page_arg, slug

    # If local file, check output/ first, then repo root
    clean_arg = page_arg.lstrip("/\\")
    candidates = [
        OUTPUT_DIR / clean_arg,
        REPO_ROOT / clean_arg,
    ]

    target_path = None
    for cand in candidates:
        if cand.is_file():
            target_path = cand
            break

    if not target_path:
        # If output does not exist or page not found, check if pelican needs to run
        if not OUTPUT_DIR.exists():
            print(f"Warning: {OUTPUT_DIR} does not exist. Run 'uv run pelican content -s pelicanconf.py -o output' first.")
        # Fall back to root candidate if exists
        target_path = (OUTPUT_DIR / clean_arg).resolve()
        if not target_path.exists():
            root_fallback = (REPO_ROOT / clean_arg).resolve()
            if root_fallback.exists():
                target_path = root_fallback

    if not target_path.exists():
        print(f"Error: Target file could not be found at {target_path}")
        print(f"Available in output/: {[p.name for p in OUTPUT_DIR.glob('*.html') if p.is_file()]}")
        sys.exit(1)

    url = target_path.as_uri()
    slug = clean_arg.replace("/", "_").replace("\\", "_").replace(".html", "")
    if not slug or slug == ".":
        slug = "index"

    return url, slug


def generate_html_preview(target_dir: Path, page_name: str, images: List[Dict[str, str]]):
    """Generate a clean HTML preview page to inspect all captured screenshots."""
    html_lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8">',
        f"  <title>Responsive Screenshots — {page_name}</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f1117; color: #e1e4e8; margin: 0; padding: 24px; }",
        "    h1 { font-size: 1.6rem; margin-bottom: 4px; }",
        "    p.meta { color: #8b949e; margin-top: 0; margin-bottom: 24px; }",
        "    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; }",
        "    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; padding: 16px; }",
        "    .card-title { font-weight: 600; font-size: 1rem; margin-bottom: 6px; color: #58a6ff; }",
        "    .card-meta { font-size: 0.85rem; color: #8b949e; margin-bottom: 12px; }",
        "    .img-wrap { border: 1px solid #30363d; border-radius: 4px; overflow: hidden; background: #000; max-height: 480px; overflow-y: auto; }",
        "    .img-wrap img { width: 100%; display: block; height: auto; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h1>Responsive Screenshots: {page_name}</h1>",
        f"  <p class=\"meta\">Generated {len(images)} viewport previews across 4 screen sizes & 2 orientations.</p>",
        '  <div class="grid">',
    ]

    for item in images:
        html_lines.extend([
            '    <div class="card">',
            f'      <div class="card-title">{item["device_label"]} — {item["orientation"].title()}</div>',
            f'      <div class="card-meta">{item["dimensions"]} &bull; Theme: {item["theme"]} &bull; File: {item["filename"]}</div>',
            '      <div class="img-wrap">',
            f'        <a href="{item["filename"]}" target="_blank"><img src="{item["filename"]}" alt="{item["filename"]}"></a>',
            '      </div>',
            '    </div>',
        ])

    html_lines.extend([
        "  </div>",
        "</body>",
        "</html>",
    ])

    preview_file = target_dir / "preview.html"
    preview_file.write_text("\n".join(html_lines), encoding="utf-8")
    return preview_file


def capture_screenshots(
    page_target: str,
    output_dir: Path,
    devices: List[str],
    orientations: List[str],
    color_schemes: List[str],
    full_page: bool = True,
) -> List[Dict[str, str]]:
    """Capture screenshots using Playwright Chromium."""
    target_url, page_slug = resolve_page_target(page_target)
    page_outdir = output_dir / page_slug
    page_outdir.mkdir(parents=True, exist_ok=True)

    captured_items: List[Dict[str, str]] = []

    print(f"\n=======================================================")
    print(f" Capturing Screenshots: {page_target}")
    print(f" URL: {target_url}")
    print(f" Target Directory: {page_outdir}")
    print(f" Full Page Capture: {full_page}")
    print(f"=======================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for scheme in color_schemes:
            for dev_key in devices:
                for orient in orientations:
                    width, height = VIEWPORT_MATRIX[dev_key][orient]
                    dim_str = f"{width}x{height}"
                    filename = f"{page_slug}_{dev_key}_{orient}_{dim_str}_{scheme}.png"
                    dest_file = page_outdir / filename

                    # Create browser context with emulation
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        color_scheme=scheme,
                        device_scale_factor=1,
                    )
                    page = context.new_page()

                    try:
                        page.goto(target_url, wait_until="load")
                        # Allow any layout / styles to settle
                        page.wait_for_timeout(100)

                        page.screenshot(path=str(dest_file), full_page=full_page)
                        file_size_kb = dest_file.stat().st_size / 1024

                        label = DEVICE_LABELS.get(dev_key, dev_key.title())
                        print(
                            f"  [OK] {label:<32} {orient:<10} {dim_str:<11} "
                            f"({scheme:<5}) -> {filename} ({file_size_kb:.1f} KB)"
                        )

                        captured_items.append({
                            "device_key": dev_key,
                            "device_label": label,
                            "orientation": orient,
                            "dimensions": dim_str,
                            "theme": scheme,
                            "filename": filename,
                            "path": str(dest_file),
                        })

                    except Exception as err:
                        print(f"  [FAIL] {dev_key} {orient} {dim_str}: {err}")
                    finally:
                        context.close()

        browser.close()

    preview_path = generate_html_preview(page_outdir, page_slug, captured_items)
    print(f"\nCompleted! Captured {len(captured_items)} screenshots.")
    print(f"HTML Preview: {preview_path.as_uri()}\n")

    return captured_items


def main():
    parser = argparse.ArgumentParser(
        description="Capture multi-resolution screenshots across 4 device sizes & 2 orientations."
    )
    parser.add_argument(
        "--page",
        default="index.html",
        help="Page to capture (e.g. index.html, about.html, posts.html, or URL). Default: index.html",
    )
    parser.add_argument(
        "--outdir",
        default=str(REPO_ROOT / "screenshots"),
        help="Output directory for screenshots. Default: ./screenshots",
    )
    parser.add_argument(
        "--device",
        choices=["all", "phone", "tablet", "laptop", "desktop_tv"],
        default="all",
        help="Device to capture (phone, tablet, laptop, desktop_tv, or all). Default: all",
    )
    parser.add_argument(
        "--orientation",
        choices=["all", "portrait", "landscape"],
        default="all",
        help="Orientation to capture (portrait, landscape, or all). Default: all",
    )
    parser.add_argument(
        "--color-scheme",
        choices=["light", "dark", "both"],
        default="light",
        help="Color scheme / theme to emulate (light, dark, both). Default: light",
    )
    parser.add_argument(
        "--viewport-only",
        action="store_true",
        help="Capture only the visible viewport rather than the full scrolling page.",
    )

    args = parser.parse_args()

    # Determine devices
    if args.device == "all":
        devices = ["phone", "tablet", "laptop", "desktop_tv"]
    else:
        devices = [args.device]

    # Determine orientations
    if args.orientation == "all":
        orientations = ["portrait", "landscape"]
    else:
        orientations = [args.orientation]

    # Determine color schemes
    if args.color_scheme == "both":
        schemes = ["light", "dark"]
    else:
        schemes = [args.color_scheme]

    out_dir = Path(args.outdir).resolve()
    capture_screenshots(
        page_target=args.page,
        output_dir=out_dir,
        devices=devices,
        orientations=orientations,
        color_schemes=schemes,
        full_page=not args.viewport_only,
    )


if __name__ == "__main__":
    main()
