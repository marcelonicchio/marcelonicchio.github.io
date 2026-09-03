#!/usr/bin/env python3
"""Synchronize fragment-backed entry bodies into canonical thematic verticals.

This is the first source-of-truth migration layer for promoted entries. It is
intentionally incremental: only entries registered with source.kind=fragment
are managed here. Full Biography remains downstream of the thematic verticals
and must be synchronized after this script.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "entries.json"


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def marker_start(entry_id: str) -> str:
    return f"<!-- entry-source:{entry_id}:start -->"


def marker_end(entry_id: str) -> str:
    return f"<!-- entry-source:{entry_id}:end -->"


def fragment_path(entry: dict[str, Any], lang: str) -> Path:
    key = f"{lang}_path"
    raw = entry["source"].get(key)
    if not raw:
        raise RuntimeError(f"{entry['id']}:{lang}: fragment source has no {key}")
    path = ROOT / raw
    if not path.exists():
        raise RuntimeError(f"{entry['id']}:{lang}: missing fragment {raw}")
    return path


def vertical_target(entry: dict[str, Any], lang: str) -> dict[str, str]:
    targets = entry.get("reader_targets", {}).get(lang, [])
    biography_token = "/biografia/" if lang == "pt" else "/biography/"
    for target in targets:
        normalized = "/" + target["path"].strip("/") + "/"
        if biography_token not in normalized:
            return target
    raise RuntimeError(f"{entry['id']}:{lang}: no thematic vertical reader target")


def section_pattern(section_id: str) -> re.Pattern[str]:
    escaped = re.escape(section_id)
    return re.compile(
        rf'(<section\b(?=[^>]*\bid=["\']{escaped}["\'])[^>]*>)(.*?)(</section>)',
        flags=re.S | re.I,
    )


def chapter_page_href(entry: dict[str, Any], lang: str) -> str | None:
    page = entry.get("chapter_page", {})
    if page.get("status") != "pilot":
        return None
    raw = page.get(f"{lang}_path")
    if not raw:
        return None
    rel = raw[:-10] if raw.endswith("index.html") else raw
    return "/" + rel.lstrip("/")


def render_heading(heading_html: str, entry: dict[str, Any], lang: str) -> str:
    href = chapter_page_href(entry, lang)
    if not href or 'class="entry-title-permalink"' in heading_html:
        return heading_html
    match = re.fullmatch(r'(<h2\b[^>]*>)(.*)(</h2>)', heading_html, flags=re.S | re.I)
    if not match:
        raise RuntimeError(f"{entry['id']}:{lang}: could not render Chapter Page permalink in h2")
    opening, inner, closing = match.groups()
    return f'{opening}<a class="entry-title-permalink" href="{href}">{inner}</a>{closing}'


def render_managed_section(text: str, entry: dict[str, Any], lang: str) -> str:
    entry_id = entry["id"]
    target = vertical_target(entry, lang)
    selector = target["selector"]
    if not selector.startswith("#"):
        raise RuntimeError(f"{entry_id}:{lang}: fragment sync currently requires an id selector")
    section_id = selector[1:]
    pattern = section_pattern(section_id)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{entry_id}:{lang}: section #{section_id} matched {len(matches)} times")

    match = matches[0]
    opening, inner, closing = match.groups()
    heading = re.search(r'<h2\b[^>]*>.*?</h2>', inner, flags=re.S | re.I)
    if heading is None:
        raise RuntimeError(f"{entry_id}:{lang}: target section has no h2")

    fragment = fragment_path(entry, lang).read_text(encoding="utf-8").strip()
    rendered_heading = render_heading(heading.group(0), entry, lang)
    managed = (
        f"{opening}{rendered_heading}"
        f"{marker_start(entry_id)}\n{fragment}\n{marker_end(entry_id)}{closing}"
    )
    return text[: match.start()] + managed + text[match.end() :]


def sync_file(entry: dict[str, Any], lang: str, *, check: bool) -> bool:
    target = vertical_target(entry, lang)
    path = ROOT / target["path"]
    if not path.exists():
        raise RuntimeError(f"{entry['id']}:{lang}: missing target {target['path']}")
    original = path.read_text(encoding="utf-8")
    updated = render_managed_section(original, entry, lang)
    changed = updated != original
    if changed and not check:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if fragment-backed verticals are out of sync")
    args = parser.parse_args()

    registry = load_registry()
    changed: list[str] = []
    for entry in registry.get("entries", []):
        if entry.get("source", {}).get("kind") != "fragment":
            continue
        if entry.get("reader_scope") == "biography-only":
            continue
        for lang in ("pt", "en"):
            if sync_file(entry, lang, check=args.check):
                changed.append(f"{entry['id']}:{lang}")

    if args.check and changed:
        print("Entry source synchronization required:")
        for item in changed:
            print(" -", item)
        return 1

    if changed:
        print("Synchronized fragment-backed entries:")
        for item in changed:
            print(" -", item)
    else:
        print("Fragment-backed entries already synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
