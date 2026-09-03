#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOBILE_NAV_VERSION = '20260903-mobile1'
MOBILE_NAV_CSS = f'<link rel="stylesheet" href="/assets/mobile-nav.css?v={MOBILE_NAV_VERSION}">'
MOBILE_NAV_JS = f'<script src="/assets/js/mobile-nav.js?v={MOBILE_NAV_VERSION}" defer></script>'
MOBILE_NAV_CSS_RE = re.compile(r'<link rel="stylesheet" href="/assets/mobile-nav\.css\?v=[^"]+">')
MOBILE_NAV_JS_RE = re.compile(r'<script src="/assets/js/mobile-nav\.js\?v=[^"]+" defer></script>')


def normalize_nav_block(block: str, lang: str) -> str:
    if lang == "pt":
        internet_href = '/pt/internet/'
        search_pattern = r'<a href="/pt/search-performance/">[^<]*</a>'
        internet_anchor = '<a href="/pt/internet/">Internet & Performance</a>'
        media_href = '/pt/comunicacao/'
        av_pattern = r'<a href="/pt/audiovisual/">[^<]*</a>'
        media_anchor = '<a href="/pt/comunicacao/">Mídia & Cultura</a>'
        internet_repl = (
            ('href="/pt/internet/">Internet</a>', 'href="/pt/internet/">Internet & Performance</a>'),
            ('href="/pt/internet/">Internet & Cultura Digital</a>', 'href="/pt/internet/">Internet & Performance</a>'),
        )
        media_repl = (
            ('href="/pt/comunicacao/">Comunicação</a>', 'href="/pt/comunicacao/">Mídia & Cultura</a>'),
            ('href="/pt/comunicacao/">Comunicação & Cultura</a>', 'href="/pt/comunicacao/">Mídia & Cultura</a>'),
            ('href="/pt/comunicacao/">Cultura & Audiovisual</a>', 'href="/pt/comunicacao/">Mídia & Cultura</a>'),
        )
    else:
        internet_href = '/en/internet/'
        search_pattern = r'<a href="/en/search-performance/">[^<]*</a>'
        internet_anchor = '<a href="/en/internet/">Internet & Performance</a>'
        media_href = '/en/communication/'
        av_pattern = r'<a href="/en/audiovisual/">[^<]*</a>'
        media_anchor = '<a href="/en/communication/">Media & Culture</a>'
        internet_repl = (
            ('href="/en/internet/">Internet</a>', 'href="/en/internet/">Internet & Performance</a>'),
            ('href="/en/internet/">Internet & Digital Culture</a>', 'href="/en/internet/">Internet & Performance</a>'),
        )
        media_repl = (
            ('href="/en/communication/">Communication</a>', 'href="/en/communication/">Media & Culture</a>'),
            ('href="/en/communication/">Communication & Culture</a>', 'href="/en/communication/">Media & Culture</a>'),
            ('href="/en/communication/">Culture & Audiovisual</a>', 'href="/en/communication/">Media & Culture</a>'),
        )
    had_internet = f'href="{internet_href}"' in block
    had_search = re.search(search_pattern, block) is not None
    for old, new in internet_repl:
        block = block.replace(old, new)
    if had_search and not had_internet:
        block = re.sub(search_pattern, internet_anchor, block, count=1)
    elif had_search:
        block = re.sub(search_pattern, '', block)
    had_media = f'href="{media_href}"' in block
    had_av = re.search(av_pattern, block) is not None
    for old, new in media_repl:
        block = block.replace(old, new)
    if had_av and not had_media:
        block = re.sub(av_pattern, media_anchor, block, count=1)
    elif had_av:
        block = re.sub(av_pattern, '', block)
    return block


def normalize_other_links(text: str, lang: str) -> str:
    pairs = [
        ('/pt/search-performance/', '/pt/internet/', 'Internet & Performance') if lang == 'pt' else ('/en/search-performance/', '/en/internet/', 'Internet & Performance'),
        ('/pt/audiovisual/', '/pt/comunicacao/', 'Mídia & Cultura') if lang == 'pt' else ('/en/audiovisual/', '/en/communication/', 'Media & Culture'),
    ]
    for old, target, label_out in pairs:
        pattern = rf'<a([^>]*?)href="{re.escape(old)}([^"]*)"([^>]*)>([^<]*)</a>'
        def repl(match):
            before, suffix, after, label = match.groups()
            if label.strip() in {'Search', 'Search & Performance', 'Search &amp; Performance', 'Audiovisual'}:
                label = label_out
            return f'<a{before}href="{target}{suffix}"{after}>{label}</a>'
        text = re.sub(pattern, repl, text)
    return text


def install_mobile_nav_assets(text: str) -> str:
    if MOBILE_NAV_CSS_RE.search(text):
        text = MOBILE_NAV_CSS_RE.sub(MOBILE_NAV_CSS, text, count=1)
    elif '</head>' in text:
        text = text.replace('</head>', f'  {MOBILE_NAV_CSS}\n</head>', 1)
    else:
        raise RuntimeError('Page has no </head> for mobile navigation stylesheet')

    if MOBILE_NAV_JS_RE.search(text):
        text = MOBILE_NAV_JS_RE.sub(MOBILE_NAV_JS, text, count=1)
    elif '</body>' in text:
        text = text.replace('</body>', f'{MOBILE_NAV_JS}\n</body>', 1)
    else:
        raise RuntimeError('Page has no </body> for mobile navigation script')
    return text


def normalize(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    rel = path.relative_to(ROOT).as_posix()
    lang = 'pt' if rel.startswith('pt/') else 'en' if rel.startswith('en/') else ''
    if not lang:
        return False
    text = re.sub(r'<nav class="nav-links"[^>]*>.*?</nav>', lambda m: normalize_nav_block(m.group(0), lang), text, flags=re.S)
    text = normalize_other_links(text, lang)
    if '<header class="site-header">' in text and '<nav class="nav-links"' in text:
        text = install_mobile_nav_assets(text)
    if text == original:
        return False
    path.write_text(text, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    paths = sorted(set([*ROOT.glob('pt/**/*.html'), *ROOT.glob('en/**/*.html'), ROOT / 'pt/index.html', ROOT / 'en/index.html']))
    for path in paths:
        if path.exists() and normalize(path):
            changed.append(path.relative_to(ROOT).as_posix())
    if args.check and changed:
        print('Navigation is not synchronized:')
        for item in changed:
            print(' -', item)
        return 1
    if changed:
        print('Updated navigation in:')
        for item in changed:
            print(' -', item)
    else:
        print('Navigation already synchronized.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
