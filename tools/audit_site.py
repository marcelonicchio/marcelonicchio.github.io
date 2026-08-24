#!/usr/bin/env python3
"""Small dependency-free audit for the static authority hub.

Checks structural SEO/entity basics without trying to score content quality.
"""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://marcelonicchio.github.io"


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

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
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


def target_exists(href: str, source: Path) -> bool:
    if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
        return True
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return True
    if clean.startswith("/"):
        target = ROOT / clean.lstrip("/")
    else:
        target = source.parent / clean
    if target.is_dir():
        target = target / "index.html"
    elif target.suffix == "":
        target = target / "index.html"
    return target.exists()


def meta_values(parser: PageParser, name: str) -> list[str]:
    wanted = name.lower()
    return [attrs.get("content", "").strip() for attrs in parser.metas if attrs.get("name", "").lower() == wanted]


def robots_value(parser: PageParser) -> str:
    values = meta_values(parser, "robots")
    return values[0].lower() if values else ""


def audit_html(errors: list[str], warnings: list[str]) -> dict[str, str]:
    robots_by_url = {}
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT).as_posix()
        url = page_url(path)
        robots_by_url[url] = robots_value(parser)

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

        descriptions = meta_values(parser, "description")
        if rel != "404.html":
            if len(descriptions) != 1 or not descriptions[0]:
                errors.append(f"{rel}: expected exactly one non-empty meta description")
            elif len(descriptions[0]) < 70:
                warnings.append(f"{rel}: meta description is short ({len(descriptions[0])} chars)")
            elif len(descriptions[0]) > 190:
                warnings.append(f"{rel}: meta description is long ({len(descriptions[0])} chars)")

        robots = meta_values(parser, "robots")
        if rel != "404.html" and len(robots) != 1:
            errors.append(f"{rel}: expected exactly one robots meta tag")

        if rel != "404.html":
            if len(parser.canonicals) != 1:
                errors.append(f"{rel}: expected exactly one canonical URL")
            elif parser.canonicals[0] != url:
                errors.append(f"{rel}: canonical {parser.canonicals[0]!r} does not match expected {url!r}")

        for href in parser.links:
            if not target_exists(href, path):
                errors.append(f"{rel}: broken internal link {href!r}")

        if rel.startswith("pt/") or rel.startswith("en/"):
            langs = {lang for lang, _ in parser.alternates}
            for expected in {"pt-BR", "en", "x-default"}:
                if expected not in langs:
                    errors.append(f"{rel}: missing hreflang {expected}")

        if rel in {"index.html", "pt/index.html", "en/index.html"}:
            if "noindex" in robots_value(parser):
                errors.append(f"{rel}: launch foundation page must not be noindex")
        elif rel not in {"404.html"} and (rel.startswith("pt/") or rel.startswith("en/")):
            if "noindex" not in robots_value(parser):
                warnings.append(f"{rel}: thematic page is indexable; confirm this is intentional")

    return robots_by_url


def audit_json(errors: list[str]) -> None:
    data_dir = ROOT / "data"
    for path in sorted(data_dir.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def audit_sitemap(errors: list[str], robots_by_url: dict[str, str]) -> None:
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
    for url in urls:
        if not url.startswith(SITE + "/"):
            errors.append(f"sitemap.xml: non-canonical host {url}")
        if "noindex" in robots_by_url.get(url, ""):
            errors.append(f"sitemap.xml: includes noindex page {url}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    robots_by_url = audit_html(errors, warnings)
    audit_json(errors)
    audit_sitemap(errors, robots_by_url)

    print(f"HTML/SEO audit completed: {len(errors)} error(s), {len(warnings)} warning(s).")
    for item in warnings:
        print("WARNING:", item)
    for item in errors:
        print("ERROR:", item)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
