#!/usr/bin/env python3
"""Audit the path-scoped Reader visual policy for rich Full Biography previews."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data" / "entries.json"
THEME = ROOT / "assets" / "reader-yellow-outline-test.css"
LOADER = ROOT / "assets" / "js" / "reader-disclosure-loader.js"

FULL_BIO = {
    "pt": "pt/biografia/index.html",
    "en": "en/biography/index.html",
}
HAI_VERTICAL = {
    "pt": "pt/ia-hai/index.html",
    "en": "en/ai-hai/index.html",
}


def preview_active(entry: dict, language: str, path: str) -> bool:
    preview = entry.get("reader_preview", {}).get(language)
    if not preview:
        return False
    allowed = entry.get("reader_preview_paths", {}).get(language)
    return not isinstance(allowed, list) or path in allowed


def presentation_for(entry: dict, path: str) -> str:
    presentation = entry.get("reader_presentation", {})
    if path in presentation.get("always_open_paths", []):
        return "always-open"
    return presentation.get("state", "normal")


def main() -> int:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    by_id = {entry.get("id"): entry for entry in entries}

    errors: list[str] = []
    rich_ids_by_language: dict[str, set[str]] = {}

    for language, path in FULL_BIO.items():
        rich_ids = {
            entry.get("id")
            for entry in entries
            if entry.get("id") and preview_active(entry, language, path)
        }
        rich_ids_by_language[language] = rich_ids
        if "hai-melissa" not in rich_ids:
            errors.append(f"Melissa rich preview is not active on {path}")
        if len(rich_ids) < 5:
            errors.append(f"Expected at least five rich Full Biography previews on {path}; found {len(rich_ids)}")

    if rich_ids_by_language.get("pt") != rich_ids_by_language.get("en"):
        errors.append("PT/EN Full Biography rich-preview sets differ")

    melissa = by_id.get("hai-melissa")
    if not melissa:
        errors.append("Missing hai-melissa entry")
    else:
        for language, path in HAI_VERTICAL.items():
            if presentation_for(melissa, path) != "always-open":
                errors.append(f"Melissa must remain always-open on {path}")

    theme = THEME.read_text(encoding="utf-8")
    required_theme_tokens = [
        "section.bio-entry .reader-disclosure:has(.reader-disclosure__preview)",
        "border:1.5px solid rgba(255,239,153,.78)",
        "background:rgba(255,255,255,.82)",
        "font-weight:800",
    ]
    for token in required_theme_tokens:
        if token not in theme:
            errors.append(f"Reader theme policy token missing: {token}")

    loader = LOADER.read_text(encoding="utf-8")
    if "reader-yellow-outline-test.css?v=20260903-yellow3" not in loader:
        errors.append("Reader theme cache-buster is not synchronized with visual policy revision")

    if errors:
        print("Reader visual policy audit failed:")
        for error in errors:
            print(" -", error)
        return 1

    ids = sorted(rich_ids_by_language.get("pt", set()))
    print(f"Reader visual policy OK: {len(ids)} rich Full Biography preview(s) share the highlighted outline.")
    print("Rich preview entries:", ", ".join(ids))
    print("Melissa remains always-open on PT/EN HAI verticals.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
