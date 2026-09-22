#!/usr/bin/env python3
"""Audit the explicit research chronology on AI / HCI / HAI verticals."""

from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "pt": ROOT / "pt/ia-hai/index.html",
    "en": ROOT / "en/ai-hai/index.html",
}
EXPECTED = {
    "pro2": "2026",
    "pro1": "2026",
    "melissa": "2025",
}
AI_CSS = "/assets/ai-editorial.css?v=20260922-v1"


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


def audit(path: Path) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    stylesheets = [node.get("href") for node in soup.select('link[rel="stylesheet"][href]')]
    if AI_CSS not in stylesheets:
        raise AssertionError(f"{path.relative_to(ROOT)}: dedicated AI chronology stylesheet missing")

    for section_id, year in EXPECTED.items():
        section = soup.select_one(f"article.article-body > section#{section_id}")
        if section is None:
            raise AssertionError(f"{path.relative_to(ROOT)}: #{section_id} missing")
        phase = direct_child(section, cls="phase-year")
        heading = direct_child(section, tag="h2")
        if phase is None or phase.get_text(" ", strip=True) != year:
            found = None if phase is None else phase.get_text(" ", strip=True)
            raise AssertionError(
                f"{path.relative_to(ROOT)}#{section_id}: expected chronology year {year!r}, found {found!r}"
            )
        if heading is None:
            raise AssertionError(f"{path.relative_to(ROOT)}#{section_id}: direct h2 missing")
        children = [child for child in section.children if getattr(child, "name", None)]
        if children.index(phase) > children.index(heading):
            raise AssertionError(f"{path.relative_to(ROOT)}#{section_id}: year must precede h2")

    for context_id in ("ciclo", "cycle", "identidade", "identity"):
        section = soup.select_one(f"#{context_id}")
        if section is not None and direct_child(section, cls="phase-year") is not None:
            raise AssertionError(
                f"{path.relative_to(ROOT)}#{context_id}: contextual section must remain outside project chronology"
            )


def main() -> int:
    for path in TARGETS.values():
        audit(path)
    print("AI / HCI / HAI chronology OK: Melissa=2025; PRO v1=2026; PRO 2.0=2026 in PT/EN.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
