#!/usr/bin/env python3
"""Audit the Music-style editorial hierarchy on Internet & Performance.

The date/title split is a paired PT/EN structural contract and must remain synchronized.
The undated closing synthesis remains outside the dated entry sequence.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "pt": ROOT / "pt/internet/index.html",
    "en": ROOT / "en/internet/index.html",
}
EXPECTED_IDS = {
    "pt": [
        "bbs", "internet", "psinet", "mirantte", "sem", "cookieweb",
        "clickland", "petlove", "best", "dialetto", "independente", "driven",
    ],
    "en": [
        "bbs", "internet", "psinet", "mirantte", "sem", "cookieweb",
        "clickland", "petlove", "best", "dialetto", "independent", "driven",
    ],
}
CLOSING_ID = {"pt": "continuidade", "en": "continuity"}
YEAR_RE = re.compile(r"(?:19|20)\d{2}")
INTERNET_CSS = "/assets/internet-editorial.css?v=20260922-v1"
DESKTOP_GALLERY_SIZE = "210px"


def direct_child(section, tag=None, cls=None):
    for child in section.children:
        if not getattr(child, "name", None):
            continue
        if tag and child.name != tag:
            continue
        if cls and cls not in (child.get("class") or []):
            continue
        return child
    return None


def audit(lang: str, path: Path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    article = soup.select_one("article.article-body")
    if article is None:
        raise AssertionError(f"{path.relative_to(ROOT)}: article.article-body missing")

    stylesheets = [node.get("href") for node in soup.select('link[rel="stylesheet"][href]')]
    if INTERNET_CSS not in stylesheets:
        raise AssertionError(
            f"{path.relative_to(ROOT)}: dedicated Internet stylesheet missing: {INTERNET_CSS}"
        )

    entries = []
    for section in article.find_all("section", class_="chapter", recursive=False):
        if "internet-entry" not in (section.get("class") or []):
            continue
        sid = section.get("id")
        phase = direct_child(section, cls="phase-year")
        heading = direct_child(section, tag="h2")
        if not sid:
            raise AssertionError(f"{path.relative_to(ROOT)}: internet-entry without id")
        if phase is None:
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: missing direct .phase-year")
        if heading is None:
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: missing direct h2")
        phase_text = phase.get_text(" ", strip=True)
        heading_text = heading.get_text(" ", strip=True)
        if not YEAR_RE.search(phase_text):
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: phase-year has no year: {phase_text!r}")
        if re.match(r"^(?:[^—]*?(?:19|20)\d{2}[^—]*?)\s+—\s+", heading_text):
            raise AssertionError(f"{path.relative_to(ROOT)}#{sid}: date leaked back into h2: {heading_text!r}")
        entries.append(sid)

    expected = EXPECTED_IDS[lang]
    if entries != expected:
        raise AssertionError(
            f"{path.relative_to(ROOT)}: Internet entry order mismatch; expected={expected}, found={entries}"
        )

    closing = article.select_one(f"#{CLOSING_ID[lang]}")
    if closing is None:
        raise AssertionError(f"{path.relative_to(ROOT)}: closing synthesis #{CLOSING_ID[lang]} missing")
    if "internet-entry" in (closing.get("class") or []):
        raise AssertionError(
            f"{path.relative_to(ROOT)}#{CLOSING_ID[lang]}: closing synthesis must not become a dated Internet entry"
        )
    if direct_child(closing, cls="phase-year") is not None:
        raise AssertionError(
            f"{path.relative_to(ROOT)}#{CLOSING_ID[lang]}: closing synthesis must remain undated"
        )

    for image in article.select(".record-gallery__item img[sizes]"):
        sizes = image.get("sizes", "")
        if DESKTOP_GALLERY_SIZE not in sizes:
            raise AssertionError(
                f"{path.relative_to(ROOT)}: gallery image keeps legacy desktop sizes hint: {sizes!r}"
            )
    return entries


def main() -> int:
    results = {lang: audit(lang, path) for lang, path in TARGETS.items()}
    canonical_en = ["independente" if item == "independent" else item for item in results["en"]]
    if results["pt"] != canonical_en:
        raise AssertionError(
            f"PT/EN Internet entry order differs: pt={results['pt']}, en={results['en']}"
        )
    print(f"Internet editorial structure OK: {len(results['pt'])} dated entries in PT/EN; closing synthesis remains undated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
