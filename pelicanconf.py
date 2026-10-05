"""
pelicanconf.py — Pelican Static Site Generator Configuration
for out of my lane (outofmylane)
Author: Jim Collinsworth & LLM-Gemini3.8
Version: 0.8.04
"""

from pathlib import Path
import yaml
import markdown
from pelican import signals
from pelican.urlwrappers import Category, Tag

AUTHOR = 'Jim Collinsworth'
SITENAME = 'Out of My Lane'
SITESUBTITLE = 'Jim Collinsworth'
SITEURL = ""

PATH = "content"
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["posts"]
STATIC_PATHS = ["media", "extra"]

# Default all articles and pages to draft status
DEFAULT_METADATA = {
    'status': 'draft',
}

TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

# Navigation Menu Configuration — strictly Home and About
MENUITEMS = (
    ('Home', '/index.html', 'index.html'),
    ('About', '/about.html', 'about'),
)

# Clean URL structure
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_HIDDEN_SAVE_AS = ''
INDEX_SAVE_AS = 'index.html'

# Category renamed to Lanes throughout the site
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = ''
CATEGORY_URL = 'lanes/{slug}.html'
CATEGORY_SAVE_AS = 'lanes/{slug}.html'
CATEGORIES_URL = 'lanes.html'
CATEGORIES_SAVE_AS = 'lanes.html'

# Tags for provenance and topics
TAG_URL = 'tags/{slug}.html'
TAG_SAVE_AS = 'tags/{slug}.html'
TAGS_URL = 'tags.html'
TAGS_SAVE_AS = 'tags.html'

# Disable unneeded index files
ARCHIVES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

# Custom Theme
THEME = 'themes/lakefront'

# Feed generation disabled for development
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False
RELATIVE_URLS = True

# Content template shortcodes and labels
TYPE_METADATA = {
    'post': {'code': 'POST', 'label': 'Post', 'icon': 'feather'},
    'idea': {'code': 'IDEA', 'label': 'Idea', 'icon': 'sparkle'},
    'link': {'code': 'LINK', 'label': 'Link', 'icon': 'link'},
    'photo': {'code': 'PHOTO', 'label': 'Photo', 'icon': 'camera'},
    'chat': {'code': 'CHAT', 'label': 'Chat', 'icon': 'message'},
    'project': {'code': 'APP', 'label': 'Application / Project', 'icon': 'box'},
    'til': {'code': 'TIL', 'label': 'Today I Learned', 'icon': 'bulb'},
    'read': {'code': 'READ', 'label': 'Book / Reading Note', 'icon': 'book'},
    'view': {'code': 'VIEW', 'label': 'Media / View Note', 'icon': 'film'},
    'spec': {'code': 'SPEC', 'label': 'Specification', 'icon': 'file-text'},
    'wip': {'code': 'WIP', 'label': 'Work In Progress', 'icon': 'clock'},
}

def merge_lane_and_tag_metadata(generator):
    """
    Merge Markdown prose and YAML frontmatter from content/lanes/<lane>.md
    and content/tags/<tag>.md into Pelican Category and Tag objects.
    Lanes are strictly defined by files present in content/lanes/.
    Zero phantom or starter categories are injected.
    """
    content_path = Path(generator.settings.get('PATH', 'content'))
    lanes_dir = content_path / 'lanes'
    if not lanes_dir.exists():
        lanes_dir = content_path / 'categories'
    tags_dir = content_path / 'tags'

    # Build category lookup from current generator categories
    cat_dict = {}
    for cat, arts in generator.categories:
        cat_dict[cat.slug] = (cat, arts)

    valid_lanes = set()
    if lanes_dir.exists():
        for lane_file in lanes_dir.glob('**/*.md'):
            raw = lane_file.read_text(encoding='utf-8')
            meta = {}
            body = raw
            if raw.startswith('---'):
                parts = raw.split('---', 2)
                if len(parts) >= 3:
                    try:
                        meta = yaml.safe_load(parts[1]) or {}
                    except Exception:
                        meta = {}
                    body = parts[2].strip()

            slug = meta.get('slug', lane_file.stem)
            title = meta.get('title', slug.replace('-', ' ').title())
            summary = meta.get('summary', '')
            if isinstance(summary, list):
                summary = ' '.join(str(s) for s in summary)
            intro_html = markdown.markdown(body) if body else ''

            valid_lanes.add(slug)

            if slug in cat_dict:
                cat, _ = cat_dict[slug]
            else:
                cat = Category(slug, generator.settings)
                cat_dict[slug] = (cat, [])
                generator.categories.append((cat, []))

            cat.slug = slug
            cat.name = title
            cat.title = title
            cat.summary = summary
            cat.intro_html = intro_html
            cat.meta = meta

            valid_lanes.add(slug)
            valid_lanes.add(cat.slug)

    # Strictly retain only categories that exist in content/lanes/
    generator.categories = [(cat, arts) for cat, arts in generator.categories if cat.slug in valid_lanes]

    # For any article whose category is not a valid lane, clear article.category to prevent 404 links
    if hasattr(generator, 'articles'):
        for art in generator.articles:
            if hasattr(art, 'category') and art.category and art.category.slug not in valid_lanes:
                art.category = None

    # Process tags similarly
    if hasattr(generator, 'tags') and tags_dir.exists():
        tag_dict = {tag.slug: tag for tag in generator.tags.keys()}
        for tag_file in tags_dir.glob('**/*.md'):
            raw = tag_file.read_text(encoding='utf-8')
            meta = {}
            body = raw
            if raw.startswith('---'):
                parts = raw.split('---', 2)
                if len(parts) >= 3:
                    try:
                        meta = yaml.safe_load(parts[1]) or {}
                    except Exception:
                        meta = {}
                    body = parts[2].strip()

            slug = meta.get('slug', tag_file.stem)
            title = meta.get('title', slug.replace('-', ' ').title())
            summary = meta.get('summary', '')
            if isinstance(summary, list):
                summary = ' '.join(str(s) for s in summary)
            intro_html = markdown.markdown(body) if body else ''

            if slug in tag_dict:
                tag = tag_dict[slug]
            else:
                tag = Tag(slug, generator.settings)
                tag_dict[slug] = tag
                generator.tags[tag] = []

            tag.slug = slug
            tag.name = title
            tag.title = title
            tag.summary = summary
            tag.intro_html = intro_html
            tag.meta = meta


signals.article_generator_finalized.connect(merge_lane_and_tag_metadata)


def collect_featured_items(generators):
    """
    Collect featured items across articles, pages, lanes (categories), and tags.
    Selects up to 3 items and injects featured_items and featured_slugs into template context.
    """
    featured_list = []

    for gen in generators:
        # Check articles
        if hasattr(gen, 'articles'):
            for art in gen.articles:
                feat = art.metadata.get('featured')
                if feat and str(feat).lower() not in ('false', '0', 'none', ''):
                    featured_list.append({
                        'type': 'article',
                        'title': art.title,
                        'slug': art.slug,
                        'url': art.url,
                        'date': art.date,
                        'template': getattr(art, 'template', getattr(art, 'type', 'post')),
                        'summary': getattr(art, 'summary', ''),
                        'photo_url': getattr(art, 'photo_url', getattr(art, 'featured_image', '')),
                        'caption': getattr(art, 'caption', ''),
                        'provenance': getattr(art, 'provenance', ', '.join(t.name for t in art.tags) if art.tags else ''),
                        'author': art.author,
                        'order': int(feat) if isinstance(feat, int) or (isinstance(feat, str) and str(feat).isdigit()) else 999,
                        'raw': art,
                    })

        # Check pages (excluding home and hidden)
        if hasattr(gen, 'pages'):
            for pg in gen.pages:
                if pg.slug == 'home':
                    continue
                feat = pg.metadata.get('featured')
                if feat and str(feat).lower() not in ('false', '0', 'none', ''):
                    featured_list.append({
                        'type': 'page',
                        'title': pg.title,
                        'slug': pg.slug,
                        'url': pg.url,
                        'date': getattr(pg, 'date', None),
                        'template': getattr(pg, 'template', 'page'),
                        'summary': getattr(pg, 'summary', ''),
                        'photo_url': getattr(pg, 'photo_url', getattr(pg, 'featured_image', '')),
                        'caption': getattr(pg, 'caption', ''),
                        'provenance': getattr(pg, 'provenance', ''),
                        'author': pg.author,
                        'order': int(feat) if isinstance(feat, int) or (isinstance(feat, str) and str(feat).isdigit()) else 999,
                        'raw': pg,
                    })

        # Check categories (lanes)
        if hasattr(gen, 'categories'):
            for cat, _ in gen.categories:
                meta = getattr(cat, 'meta', {})
                feat = meta.get('featured')
                if feat and str(feat).lower() not in ('false', '0', 'none', ''):
                    featured_list.append({
                        'type': 'lane',
                        'title': cat.name,
                        'slug': cat.slug,
                        'url': cat.url,
                        'date': None,
                        'template': 'lane',
                        'summary': getattr(cat, 'summary', ''),
                        'photo_url': meta.get('featured_image', meta.get('photo_url', '')),
                        'caption': '',
                        'provenance': '',
                        'author': None,
                        'order': int(feat) if isinstance(feat, int) or (isinstance(feat, str) and str(feat).isdigit()) else 999,
                        'raw': cat,
                    })

        # Check tags
        if hasattr(gen, 'tags'):
            for tag in gen.tags.keys():
                meta = getattr(tag, 'meta', {})
                feat = meta.get('featured')
                if feat and str(feat).lower() not in ('false', '0', 'none', ''):
                    featured_list.append({
                        'type': 'tag',
                        'title': tag.name,
                        'slug': tag.slug,
                        'url': tag.url,
                        'date': None,
                        'template': 'tag',
                        'summary': getattr(tag, 'summary', ''),
                        'photo_url': meta.get('featured_image', meta.get('photo_url', '')),
                        'caption': '',
                        'provenance': '',
                        'author': None,
                        'order': int(feat) if isinstance(feat, int) or (isinstance(feat, str) and str(feat).isdigit()) else 999,
                        'raw': tag,
                    })

    # Sort by order ascending, then date descending
    featured_list.sort(key=lambda x: (x['order'], -(x['date'].timestamp() if x['date'] else 0)))

    # Limit to top 3
    featured_items = featured_list[:3]
    featured_slugs = {item['slug'] for item in featured_items}

    # Inject into generator contexts
    for gen in generators:
        gen.context['featured_items'] = featured_items
        gen.context['featured_slugs'] = featured_slugs


signals.all_generators_finalized.connect(collect_featured_items)


