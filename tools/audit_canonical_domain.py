#!/usr/bin/env python3
"""Protect the HUB's canonical-domain cutover to marcelonicchio.com.

Historical handoff/docs may legitimately mention the old GitHub Pages hostname.
This audit intentionally targets only public/machine-readable surfaces plus the
small set of generators/auditors that define the canonical host.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "marcelonicchio.com"
LEGACY = "marcelonicchio.github.io"

PUBLIC_TEXT = [
    ROOT / "README.md",
    ROOT / "robots.txt",
    ROOT / "sitemap.xml",
    ROOT / "llms.txt",
]

HOST_SOURCE_FILES = [
    ROOT / "tools" / "audit_site.py",
    ROOT / "tools" / "audit_person_schema.py",
    ROOT / "tools" / "audit_llms_map.py",
    ROOT / "tools" / "audit_authority_vertical_schema.py",
    ROOT / "tools" / "audit_entries.py",
    ROOT / "tools" / "audit_full_bio_cutover.py",
    ROOT / "tools" / "audit_language_pair_indexation.py",
    ROOT / "tools" / "audit_media_culture_fusion.py",
    ROOT / "tools" / "build_chapter_pages.py",
    ROOT / "tools" / "normalize_external_links.py",
]


def public_files() -> list[Path]:
    files = set(PUBLIC_TEXT)
    files.update(ROOT.rglob("*.html"))
    files.update((ROOT / "data").glob("*.json"))
    return sorted(
        path
        for path in files
        if path.is_file()
        and ".git" not in path.parts
        and "docs" not in path.parts
    )


def line_hits(path: Path, needle: str) -> list[int]:
    hits: list[int] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            hits.append(number)
    return hits


def main() -> int:
    errors: list[str] = []

    scanned = public_files()
    for path in scanned:
        hits = line_hits(path, LEGACY)
        if hits:
            rel = path.relative_to(ROOT)
            errors.append(
                f"{rel}: legacy canonical host {LEGACY!r} remains on line(s) "
                + ", ".join(map(str, hits[:12]))
            )

    for path in HOST_SOURCE_FILES:
        if not path.is_file():
            errors.append(f"missing canonical-host source/audit: {path.relative_to(ROOT)}")
            continue
        hits = line_hits(path, LEGACY)
        if hits:
            errors.append(
                f"{path.relative_to(ROOT)}: legacy host survives in canonical source logic "
                f"on line(s) {', '.join(map(str, hits[:12]))}"
            )

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    expected_sitemap = f"Sitemap: https://{CANONICAL}/sitemap.xml"
    if expected_sitemap not in robots:
        errors.append(f"robots.txt: missing canonical sitemap declaration {expected_sitemap!r}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"https://{CANONICAL}/" not in sitemap:
        errors.append("sitemap.xml: canonical host is absent")

    person = (ROOT / "data" / "person.json").read_text(encoding="utf-8")
    expected_person_id = f"https://{CANONICAL}/#marcelo-nicchio"
    if expected_person_id not in person:
        errors.append(f"data/person.json: canonical Person @id {expected_person_id!r} is absent")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    if f"Canonical person page: https://{CANONICAL}/" not in llms:
        errors.append("llms.txt: canonical person page does not use marcelonicchio.com")

    if errors:
        print(f"Canonical-domain audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print(
        f"Canonical-domain cutover OK: {len(scanned)} public file(s) use {CANONICAL}; "
        f"{LEGACY} is allowed only in historical/non-public documentation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
