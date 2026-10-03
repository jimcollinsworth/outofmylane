---
name: pelican-obsidian-bridge
description: >-
  Configure and maintain the Markdown bridge between an Obsidian vault and the Pelican static site generator for outofmylane. Use when handling Obsidian YAML frontmatter, wikilinks, image embeds, callouts, and vault folder mappings.
---

# Pelican-Obsidian Bridge (out of my lane)

This skill manages the content flow from Jim's **Obsidian vault** into the **Pelican static site pipeline** for `outofmylane`.

---

## 1. Source Content Guidelines

- **Clean Markdown in `content/`**: Source notes dropped into `content/posts/` and `content/pages/` are written directly by Jim.
- **YAML Frontmatter Standard**:
  ```yaml
  ---
  title: Page Title
  slug: page-slug
  date: 2026-10-03
  summary: Brief summary of page content
  author: Jim Collinsworth
  template: page
  ---
  ```

---

## 2. Attachment & Image Resolution

- Place image assets in `content/images/` or `content/attachments/`.
- Images are referenced in standard Markdown: `![Description](attachments/image.jpg)`.
