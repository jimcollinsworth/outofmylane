"""
pelicanconf.py — Pelican Static Site Generator Configuration
for out of my lane (outofmylane)
"""

AUTHOR = 'jim collinsworth'
SITENAME = 'out of my lane'
SITESUBTITLE = 'Jim Collinsworth'
SITEURL = ""

PATH = "content"
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["posts"]

TIMEZONE = 'America/Chicago'
DEFAULT_LANG = 'en'

# Navigation Menu Configuration
MENUITEMS = (
    ('Home', '/index.html', 'index.html'),
    ('About', '/about.html', 'about'),
)

# Clean URL structure
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
INDEX_SAVE_AS = 'index.html'

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
