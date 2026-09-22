#!/usr/bin/env python3
"""Audit the compact editorial layout contract for Full Biography PT/EN."""

from pathlib import Path
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/full_biography.json"
TARGETS = {
    "pt": ROOT / "pt/biografia/index.html",
    "en": ROOT / "en/biography/index.html",
}
CSS = "/assets/full-biography-editorial.css?v=20260922-v1"


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


def audit(lang: str, path: Path, manifest: dict) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    body = soup.body
    if body is None or "full-biography-page" not in (body.get("class") or []):
        raise AssertionError(f"{path.relative_to(ROOT)}: Full Biography body class missing")

    stylesheets = [node.get("href") for node in soup.select('link[rel="stylesheet"][href]')]
    if CSS not in stylesheets:
        raise AssertionError(f"{path.relative_to(ROOT)}: dedicated Full Biography stylesheet missing")

    chronology_ids = [entry["id"] for entry in manifest["entries"]]
    context_ids = [entry["id"] for entry in manifest["context_entries"]]

    for entry_id in chronology_ids:
        section = soup.select_one(f'#bio-{entry_id}')
        if section is None:
            raise AssertionError(f"{path.relative_to(ROOT)}: chronological entry {entry_id!r} missing")
        meta = direct_child(section, cls="bio-entry-meta")
        heading = direct_child(section, tag="h2")
        if meta is None or heading is None:
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: direct meta/h2 contract missing"
            )
        spans = meta.find_all("span", recursive=False)
        if len(spans) != 2:
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: chronology meta requires date + domain; found {len(spans)} spans"
            )
        if not all(span.get_text(" ", strip=True) for span in spans):
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: chronology meta contains an empty label"
            )
        if direct_child(section, cls="phase-year") is not None:
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: vertical phase-year leaked into Full Biography"
            )

    for entry_id in context_ids:
        section = soup.select_one(f'#bio-{entry_id}')
        if section is None:
            raise AssertionError(f"{path.relative_to(ROOT)}: context entry {entry_id!r} missing")
        meta = direct_child(section, cls="bio-entry-meta")
        heading = direct_child(section, tag="h2")
        if meta is None or heading is None:
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: direct context meta/h2 contract missing"
            )
        spans = meta.find_all("span", recursive=False)
        if len(spans) != 1:
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: context meta must remain domain-only; found {len(spans)} spans"
            )
        if not spans[0].get_text(" ", strip=True):
            raise AssertionError(
                f"{path.relative_to(ROOT)}#bio-{entry_id}: context domain label is empty"
            )

    era_breaks = soup.select(".bio-era-break")
    if len(era_breaks) != len(manifest["eras"]):
        raise AssertionError(
            f"{path.relative_to(ROOT)}: expected {len(manifest['eras'])} era breaks, found {len(era_breaks)}"
        )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for lang, path in TARGETS.items():
        audit(lang, path, manifest)
    print(
        "Full Biography layout OK: "
        f"{len(manifest['entries'])} chronological + {len(manifest['context_entries'])} context entries "
        "use the compact PT/EN editorial contract."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
