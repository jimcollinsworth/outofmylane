"""
LLM_generate_obsidian_templates.py — CLI utility to generate standard Obsidian frontmatter templates.

Prefix: LLM (Automated Harness and Prompt-Driven Utility).
Usage:
    python tools/LLM_generate_obsidian_templates.py --help
    python tools/LLM_generate_obsidian_templates.py --model LLM-Gemini3.8 --output-dir content/templates
"""

from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATES: dict[str, str] = {
    "01-blog-post.md": """---
title: "Post Title Here"
date: 2026-09-15
# modified: 2026-09-15        # (Optional) Last modified date
category: Mine                # Category options: Mine (human work), Me (autobiographical), Ours (collaboration), Theirs (curated/external)
tags: [essay, technology]     # Flexible subject tags (comma-separated list)
slug: post-title-here          # URL slug (defaults to title if omitted)
# summary: "Short teaser for post lists"  # (Optional) Derived automatically from body text if omitted
# status: draft               # (Optional) Options: published (default), draft, hidden
author: Jim Collinsworth
---

# Lead Section Heading

Lead introductory paragraph establishing the core topic, context, and thesis. Written in clean, 100% human prose.

## Subheading

Body paragraph discussing details, observations, or analysis.

> [!note]
> Important takeaway or context callout.

### Code / Technical Example

```python
def example_function():
    return "Clean Python code snippet"
```

Summary or concluding thoughts.
""",
    "02-til-note.md": """---
title: "TIL: Short Technical Insight"
date: 2026-09-15
category: Mine                # Categories: Mine (human work), Me, Ours, Theirs
tags: [til, python, cli]      # Subject tags
slug: til-short-technical-insight
summary: "Quick technical insight or command-line fix."
author: Jim Collinsworth
---

Quick introduction explaining the exact technical problem or unexpected behavior encountered.

```bash
# Solution command or CLI one-liner
uv run pytest -v tests/test_pelican_e2e.py
```

Why this fix works and key takeaways for future reference.
""",
    "03-project-build.md": """---
title: "Project: Engineering / Fabrication Build Name"
date: 2026-09-15
category: Mine                # Categories: Mine (making/software), Ours (collaboration)
tags: [project, hardware, fabrication, software]
slug: project-build-name
summary: "Active engineering or physical build project overview and log."
author: Jim Collinsworth
---

## Project Overview

High-level summary of the build goal, target specifications, and design choices.

### Key Specifications
- **Dimensions / Measure**: Target scale or form factor
- **Core Stack / Components**: Materials or microcontrollers used
- **Status**: Active / Milestone 1

## Milestone Breakdown

1. **Phase 1: Architecture & Design** &mdash; Initial schematics and component selection.
2. **Phase 2: Fabrication & Assembly** &mdash; Physical build process.
3. **Phase 3: Testing & Calibration** &mdash; Verification and tuning.

## Build Notes & Log

> [!tip]
> Measurement and assembly note callout.

![Project prototype photo](attachments/project-build-photo.jpg)
*Figure 1: Initial bench prototype layout.*
""",
    "04-standalone-page.md": """---
title: "Standalone Page Title"
slug: custom-page-slug         # URL path will be /custom-page-slug.html
template: page                 # Default page template (or custom template name)
category: Mine
menu: true                     # Set to true to include in top navigation menu
menu_order: 10                 # Optional menu sorting order
summary: "Page description for search indexing."
author: Jim Collinsworth
---

# Page Title

Lead introductory paragraph establishing the purpose of this standalone site page.

## Section Header

Core narrative content formatted with semantic headings, structured lists, and figures.

- **Key Point 1**: Description.
- **Key Point 2**: Description.
""",
    "05-custom-topic-page.md": """---
title: "Topic Title (e.g. Tai Chi, Music, Science)"
slug: topic-name               # Target URL: /topic-name.html
template: page                 # Custom template or standard page layout
category: Mine
menu: true                     # Appears in top site menu if enabled
menu_order: 15
summary: "Curated collection and notes on Topic Name."
author: Jim Collinsworth
---

# Topic Title

Introductory overview explaining this curated subject area and personal synthesis.

## Curated Deep Dives & Related Posts

- [Primary Essay Title](posts/primary-essay-slug.html) &mdash; Brief note on this post.
- [Technical Note Title](posts/technical-note-slug.html) &mdash; Key takeaways.

## Key Principles & Framework

> [!important]
> Core guiding principle or foundational concept.
""",
    "06-photo-essay.md": """---
title: "Photo Essay Title"
date: 2026-09-15
category: Mine                # Categories: Mine (photos by Jim), Me (autobiographical)
tags: [photos, photography, lakefront, chicago]
slug: photo-essay-title
summary: "Photographic essay covering Chicago sky, Lake Michigan, or craft."
author: Jim Collinsworth
---

Brief introductory note setting the location, lighting conditions, or context for the photographic collection.

![Chicago sky and lakefront composition](attachments/lakefront-sunset.jpg)
*Figure 1: Sunset over Lake Michigan, Chicago.*

![Architectural line detail](attachments/architecture-lines.jpg)
*Figure 2: Perspective and light on stone and glass.*

Concluding reflection on the study.
""",
    "07-book-synthesis.md": """---
title: "Shelf: Book Title by Author Name"
date: 2026-09-15
category: Mine                # Category: Mine (reflections), Theirs (external book/link highlight)
type: read                    # Distinguishes this as a read item
item_kind: book               # Item kind: book, article, paper, url
read_author: "Author Name"    # Primary author of the book or work
isbn13: "978-0123456789"      # Standard 13-digit International Standard Book Number
isbn10: "0123456789"          # Standard 10-digit ISBN (optional)
asin: "B000000000"            # Amazon Standard Identification Number (optional)
doi: "10.1000/182"            # Digital Object Identifier for academic papers (optional)
external_url: "https://example.com/book-or-article" # Direct URL reference (optional)
tags: [shelf, reads, books, synthesis]
slug: shelf-book-title
summary: "Curated synthesis, key ideas, and reflections on Book Title by Author Name."
author: Jim Collinsworth
---

## Book Overview & Core Thesis

- **Title**: Book Title
- **Author**: Author Name
- **Publication Year**: 2024
- **ISBN-13**: 978-0123456789

High-level summary of the book's central argument and significance.

## Key Takeaways & Core Concepts

1. **First Major Idea**: Explanation and practical application.
2. **Second Major Idea**: Synthesis of arguments.

> [!quote]
> "Representative excerpt or memorable quote from the text." &mdash; Author Name (p. 42)

## Personal Reflection & Application

How these concepts relate to active projects and creative work.
""",
    "08-idea-seedling.md": """---
title: "Idea: Seedling Title"
date: 2026-09-15
category: Mine                # Categories: Mine, Ours
tags: [idea, seedling, concept, future]
slug: idea-seedling-title
status: published              # Set to 'draft' or 'hidden' if strictly private
summary: "Unexecuted hypothesis or architectural prompt for future exploration."
author: Jim Collinsworth
---

## Hypothesis & Core Concept

Brief description of an unexecuted idea, feature concept, or research hypothesis.

## Potential Value & Applications

- **Why it matters**: Solves X problem or opens Y creative path.
- **Target stack / implementation**: Potential Python or hardware approach.

## Open Questions & Risks

- [ ] Is X constraint feasible under zero-JS limits?
- [ ] What is the simplest minimal viable prototype?
""",
    "09-autobiographical-note.md": """---
title: "Personal Reflection / Update"
date: 2026-09-15
category: Me                  # Category: 'Me' (autobiographical notes, health/activity, biodata)
tags: [personal, journal, reflection]
slug: personal-reflection-update
summary: "Autobiographical notes and reflections by Jim."
author: Jim Collinsworth
---

Personal reflection, activity note, or autobiographical observation.

### Activity & Health Tracking
- **Rest & Recovery**: Sleep score / sleep metrics
- **Physical Activity**: Walking, Tai Chi, movement tracking
- **Observations**: Daily rhythm and energy notes

> [!note]
> Reflection on habit consistency and focus.
""",
    "10-curated-reference.md": """---
title: "Reference: Curated Title / Highlight"
date: 2026-09-15
category: Theirs              # Category: 'Theirs' (external works, curated references, quotes)
tags: [reference, link, curated, quote]
slug: reference-curated-title
summary: "Curated external article, quote, or reference highlight."
author: Jim Collinsworth
---

## Source & Context

- **Source Title**: [External Article Title](https://example.com/article)
- **Author / Source**: Author / Publication Name
- **Curated Date**: 2026-09-15

## Key Excerpt & Quote

> "Exact external quote or excerpt highlighting the core insight."

## Personal Commentary & Relevance

Why this reference is noteworthy and how it connects to ongoing topics.
""",
}


def build_templates(output_dir: Path, model_tag: str) -> list[Path]:
    """Generate all 10 standard frontmatter templates in output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for filename, content in TEMPLATES.items():
        target_path = output_dir / filename
        target_path.write_text(content.strip() + "\n", encoding="utf-8")
        created.append(target_path)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LLM Harness CLI: Generate 10 standard Obsidian frontmatter templates for Pelican site authoring."
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("content/templates"),
        help="Destination directory for Obsidian templates (default: content/templates)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="LLM-Gemini3.8",
        help="Model attribution tag for logging and metadata (default: LLM-Gemini3.8)",
    )

    args = parser.parse_args()

    print(f"[{args.model}] Generating 10 Obsidian frontmatter templates into: {args.output_dir}")
    created = build_templates(args.output_dir, args.model)
    for p in created:
        print(f"  + Created template: {p}")
    print(f"[{args.model}] Success: {len(created)} templates created.")


if __name__ == "__main__":
    main()
