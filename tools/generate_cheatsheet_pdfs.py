"""
tools/generate_cheatsheet_pdfs.py — Generate high-resolution PDF cheat sheets
from HTML and Mermaid sources using Playwright.
"""

from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs" / "cheatsheets"


def render_pdf(html_file: Path, pdf_file: Path) -> None:
    print(f"[*] Rendering {html_file.name} -> {pdf_file.name}...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to local file URI
        file_url = html_file.resolve().as_uri()
        page.goto(file_url, wait_until="networkidle")
        
        # Wait for all Mermaid diagrams to render
        mermaid_count = page.locator(".mermaid").count()
        print(f"    Found {mermaid_count} Mermaid diagram containers.")
        
        # Give a buffer for rendering
        page.wait_for_timeout(2000)
        
        # Validate that every diagram rendered an SVG without syntax errors
        diagrams = page.locator(".mermaid").all()
        for idx, diag in enumerate(diagrams, 1):
            svg_count = diag.locator("svg").count()
            inner_text = diag.inner_text()
            if "Syntax error" in inner_text or svg_count == 0:
                browser.close()
                raise RuntimeError(
                    f"Mermaid rendering failure in diagram #{idx} of {html_file.name}: {inner_text[:120]}"
                )
        print(f"    All {mermaid_count} diagrams rendered cleanly (0 syntax errors).")
        
        # Generate Letter-format PDF with exact background colors and margins
        page.pdf(
            path=str(pdf_file),
            format="Letter",
            print_background=True,
            margin={
                "top": "10mm",
                "bottom": "10mm",
                "left": "10mm",
                "right": "10mm",
            },
        )
        browser.close()
    print(f"[+] Successfully created {pdf_file.name} ({pdf_file.stat().st_size:,} bytes)")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    sheets = [
        ("architecture_flow.html", "architecture_flow.pdf"),
        ("content_authoring.html", "content_authoring.pdf"),
    ]
    
    for html_name, pdf_name in sheets:
        html_path = DOCS_DIR / html_name
        pdf_path = DOCS_DIR / pdf_name
        if not html_path.exists():
            print(f"[!] Error: {html_path} does not exist.")
            sys.exit(1)
        render_pdf(html_path, pdf_path)

    print("\n[+] All cheat sheet PDFs generated successfully in docs/cheatsheets/.")


if __name__ == "__main__":
    main()
