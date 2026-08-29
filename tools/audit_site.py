#!/usr/bin/env python3
"""Small dependency-free audit for the static authority hub.

Checks structural SEO/entity basics without trying to score content quality.
"""
from __future__ import annotations

from collections import Counter
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://marcelonicchio.github.io"
SITE_HOST = "marcelonicchio.github.io"

LAUNCH_INDEXABLE = {
    "index.html",
    "pt/index.html",
    "en/index.html",
    "pt/biografia/index.html",
    "en/biography/index.html",
    "pt/publicacoes/index.html",
    "en/publications/index.html",
    "pt/arquivo/index.html",
    "en/archive/index.html",
    "pt/ia-hai/index.html",
    "en/ai-hai/index.html",
}

LEGACY_CANONICAL = {
    "pt/search-performance/index.html": SITE + "/pt/internet/",
    "en/search-performance/index.html": SITE + "/en/internet/",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_count = 0
        self.in_title = False
        self.title_text = []
        self.links = []
        self.canonicals = []
        self.alternates = []
        self.metas = []
        self.h1_count = 0
        self.html_lang = ""
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"].strip())
        if tag == "html":
            self.html_lang = attrs.get("lang", "").strip()
        elif tag == "title":
            self.title_count += 1
            self.in_title = True
        elif tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        elif tag == "link":
            rel = attrs.get("rel", "")
            if rel == "canonical" and attrs.get("href"):
                self.canonicals.append(attrs["href"])
            if rel == "alternate" and attrs.get("hreflang") and attrs.get("href"):
                self.alternates.append((attrs["hreflang"], attrs["href"]))
        elif tag == "meta":
            self.metas.append(attrs)
        elif tag == "h1":
            self.h1_count += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[:-10]
    return SITE + "/" + rel


def resolve_local_target(href: str, source: Path) -> tuple[Path, str] | None:
    """Resolve a same-site link to a repository path + decoded fragment.

    External HTTP(S), mailto, tel and javascript targets are outside this static
    repository audit and return None. Absolute links to this site's own host are
    audited exactly like root-relative links.
    """
    if not href:
        return None
    lowered = href.lstrip().lower()
    if lowered.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlsplit(href)
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        if parsed.hostname != SITE_HOST:
            return None
    elif parsed.scheme:
        return None

    clean_path = unquote(parsed.path or "")
    fragment = unquote(parsed.fragment or "")

    if not clean_path:
        target = source
    elif clean_path.startswith("/"):
        target = ROOT / clean_path.lstrip("/")
    else:
        target = source.parent / clean_path

    target = target.resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return target, fragment

    if target.is_dir() or clean_path.endswith("/") or (clean_path and target.suffix == ""):
        target = target / "index.html"
    return target, fragment


def parse_page(path: Path, cache: dict[Path, PageParser]) -> PageParser | None:
    resolved = path.resolve()
    if resolved in cache:
        return cache[resolved]
    if not resolved.exists() or not resolved.is_file() or resolved.suffix.lower() not in {".html", ".htm"}:
        return None
    parser = PageParser()
    parser.feed(resolved.read_text(encoding="utf-8"))
    cache[resolved] = parser
    return parser


def audit_local_reference(
    href: str,
    source: Path,
    source_rel: str,
    errors: list[str],
    page_cache: dict[Path, PageParser],
    *,
    label: str = "internal link",
) -> None:
    resolved = resolve_local_target(href, source)
    if resolved is None:
        return
    target, fragment = resolved
    try:
        target.relative_to(ROOT)
    except ValueError:
        errors.append(f"{source_rel}: {label} escapes repository root {href!r}")
        return
    if not target.exists():
        errors.append(f"{source_rel}: broken {label} {href!r}")
        return
    if not fragment:
        return
    parser = parse_page(target, page_cache)
    if parser is None:
        return
    if fragment not in set(parser.ids):
        errors.append(f"{source_rel}: broken fragment in {label} {href!r} (missing id={fragment!r})")


def meta_values(parser: PageParser, name: str) -> list[str]:
    wanted = name.lower()
    return [attrs.get("content", "").strip() for attrs in parser.metas if attrs.get("name", "").lower() == wanted]


def robots_value(parser: PageParser) -> str:
    values = meta_values(parser, "robots")
    return values[0].lower() if values else ""


def audit_html(errors: list[str], warnings: list[str]) -> dict[str, str]:
    robots_by_url = {}
    page_cache: dict[Path, PageParser] = {}
    pages = sorted(path for path in ROOT.rglob("*.html") if ".git" not in path.parts)

    # Parse once up front so cross-page fragment checks do not repeatedly read HTML.
    for path in pages:
        parse_page(path, page_cache)

    for path in pages:
        parser = page_cache[path.resolve()]
        rel = path.relative_to(ROOT).as_posix()
        url = page_url(path)
        robots = robots_value(parser)
        robots_by_url[url] = robots

        if parser.title_count != 1:
            errors.append(f"{rel}: expected exactly one <title>, found {parser.title_count}")
        if parser.h1_count != 1:
            errors.append(f"{rel}: expected exactly one <h1>, found {parser.h1_count}")
        if not parser.html_lang:
            errors.append(f"{rel}: missing html lang attribute")
        elif rel.startswith("pt/") and parser.html_lang.lower() != "pt-br":
            errors.append(f"{rel}: expected lang=pt-BR, found {parser.html_lang!r}")
        elif rel.startswith("en/") and not parser.html_lang.lower().startswith("en"):
            errors.append(f"{rel}: expected English lang attribute, found {parser.html_lang!r}")

        duplicate_ids = sorted(ident for ident, count in Counter(parser.ids).items() if ident and count > 1)
        for ident in duplicate_ids:
            errors.append(f"{rel}: duplicate id {ident!r}")

        descriptions = meta_values(parser, "description")
        if rel != "404.html":
            if len(descriptions) != 1 or not descriptions[0]:
                errors.append(f"{rel}: expected exactly one non-empty meta description")
            elif len(descriptions[0]) < 70:
                warnings.append(f"{rel}: meta description is short ({len(descriptions[0])} chars)")
            elif len(descriptions[0]) > 190:
                warnings.append(f"{rel}: meta description is long ({len(descriptions[0])} chars)")

        robots_tags = meta_values(parser, "robots")
        if rel != "404.html" and len(robots_tags) != 1:
            errors.append(f"{rel}: expected exactly one robots meta tag")

        if rel != "404.html":
            expected_canonical = LEGACY_CANONICAL.get(rel, url)
            if len(parser.canonicals) != 1:
                errors.append(f"{rel}: expected exactly one canonical URL")
            elif parser.canonicals[0] != expected_canonical:
                errors.append(f"{rel}: canonical {parser.canonicals[0]!r} does not match expected {expected_canonical!r}")
            else:
                audit_local_reference(parser.canonicals[0], path, rel, errors, page_cache, label="canonical target")

        for href in parser.links:
            audit_local_reference(href, path, rel, errors, page_cache)

        if rel.startswith("pt/") or rel.startswith("en/"):
            lang_counts = Counter(lang for lang, _ in parser.alternates)
            for expected in {"pt-BR", "en", "x-default"}:
                if lang_counts[expected] == 0:
                    errors.append(f"{rel}: missing hreflang {expected}")
                elif lang_counts[expected] > 1:
                    errors.append(f"{rel}: duplicate hreflang {expected}")
            for lang, href in parser.alternates:
                audit_local_reference(href, path, rel, errors, page_cache, label=f"hreflang {lang}")

        if rel in LAUNCH_INDEXABLE:
            if "noindex" in robots:
                errors.append(f"{rel}: launch-indexable page must not be noindex")
        elif rel != "404.html" and (rel.startswith("pt/") or rel.startswith("en/")):
            if "noindex" not in robots:
                warnings.append(f"{rel}: non-launch thematic page is indexable; confirm this is intentional")

    return robots_by_url


def audit_json(errors: list[str]) -> None:
    data_dir = ROOT / "data"
    for path in sorted(data_dir.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def audit_sitemap(errors: list[str], warnings: list[str], robots_by_url: dict[str, str]) -> None:
    path = ROOT / "sitemap.xml"
    try:
        tree = ET.parse(path)
    except Exception as exc:
        errors.append(f"sitemap.xml: invalid XML: {exc}")
        return
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text.strip() for node in tree.findall(".//s:loc", ns) if node.text]
    if len(urls) != len(set(urls)):
        errors.append("sitemap.xml: duplicate URLs found")
    sitemap_urls = set(urls)
    for url in urls:
        if not url.startswith(SITE + "/"):
            errors.append(f"sitemap.xml: non-canonical host {url}")
        if "noindex" in robots_by_url.get(url, ""):
            errors.append(f"sitemap.xml: includes noindex page {url}")

    expected_launch_urls = {page_url(ROOT / rel) for rel in LAUNCH_INDEXABLE}
    missing = sorted(expected_launch_urls - sitemap_urls)
    extra = sorted(sitemap_urls - expected_launch_urls)
    for url in missing:
        errors.append(f"sitemap.xml: missing launch-indexable URL {url}")
    for url in extra:
        warnings.append(f"sitemap.xml: URL is outside launch-indexable set {url}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    robots_by_url = audit_html(errors, warnings)
    audit_json(errors)
    audit_sitemap(errors, warnings, robots_by_url)

    print(f"HTML/SEO audit completed: {len(errors)} error(s), {len(warnings)} warning(s).")
    for item in warnings:
        print("WARNING:", item)
    for item in errors:
        print("ERROR:", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
