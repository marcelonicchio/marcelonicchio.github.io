#!/usr/bin/env python3
"""Audit the historical preservation epigraph on the PT Archive page."""

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "pt" / "arquivo" / "index.html"
QUOTE = "A memória cultural de nosso país é a grande vítima com tudo isso."
TARGET = "/pt/comunicacao/prateleira-cultural-revista-sinal-verde/#desespero-2003"
CSS = "/assets/archive-editorial.css?v=20260922-epigraph1"


def main() -> int:
    soup = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")

    stylesheet_hrefs = {
        link.get("href")
        for link in soup.find_all("link", rel=lambda value: value and "stylesheet" in value)
    }
    if CSS not in stylesheet_hrefs:
        raise AssertionError("Archive epigraph stylesheet is not loaded")

    hero = soup.select_one("section.article-hero")
    body = soup.select_one("article.article-body")
    epigraph = soup.select_one("blockquote.archive-epigraph")
    principle = soup.select_one("article.article-body > .note")
    if hero is None or body is None or epigraph is None or principle is None:
        raise AssertionError("Archive hero/body/epigraph/principle structure incomplete")

    body_children = [child for child in body.children if getattr(child, "name", None)]
    if not body_children or body_children[0] is not epigraph:
        raise AssertionError("Archive epigraph must be the first editorial object below the hero")
    if len(body_children) < 2 or body_children[1] is not principle:
        raise AssertionError("Archive principle note must remain directly after the epigraph")

    quote_text = epigraph.get_text(" ", strip=True)
    if QUOTE not in quote_text:
        raise AssertionError("Archive epigraph quote changed or disappeared")
    if "março de 2003" not in quote_text or "Desespero" not in quote_text:
        raise AssertionError("Archive epigraph attribution/date missing")

    link = epigraph.find("a", href=TARGET)
    if link is None:
        raise AssertionError("Archive epigraph must link directly to the Desespero column anchor")

    print("Archive epigraph OK: 2003 preservation quote precedes the archive principle and links to Desespero.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
