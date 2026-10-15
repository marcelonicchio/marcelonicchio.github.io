#!/usr/bin/env python3
"""Install or refresh the disclosure loader on selected Reader Pages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOADER_RE = re.compile(r'<script src="/assets/js/reader-disclosure-loader\.js\?v=[^"]+" defer></script>')
SCRIPT = '<script src="/assets/js/reader-disclosure-loader.js?v=20260921-reader16" defer></script>'
TARGETS = [
    "pt/biografia/index.html",
    "en/biography/index.html",
    "pt/ia-hai/index.html",
    "en/ai-hai/index.html",
]
NO_READER_TARGETS = [
    "pt/internet/index.html",
    "en/internet/index.html",
]


def remove_legacy_loader(path: Path, *, check: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    updated, count = LOADER_RE.subn("", text)
    if count > 1:
        raise RuntimeError(f"Duplicate legacy reader loaders: {path.relative_to(ROOT)}")
    if count and not check:
        path.write_text(updated, encoding="utf-8")
    return bool(count)


def sync(path: Path, *, check: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    if SCRIPT in text:
        return False
    if LOADER_RE.search(text):
        updated = LOADER_RE.sub(SCRIPT, text, count=1)
    else:
        if "</body>" not in text:
            raise RuntimeError(f"{path.relative_to(ROOT)} has no </body>")
        updated = text.replace("</body>", SCRIPT + "\n</body>", 1)
    if not check:
        path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            raise RuntimeError(f"Missing Reader Page: {rel}")
        if sync(path, check=args.check):
            changed.append(rel)
    stray = []
    for rel in NO_READER_TARGETS:
        path = ROOT / rel
        if not path.exists():
            raise RuntimeError(f"Missing open editorial page: {rel}")
        if remove_legacy_loader(path, check=args.check):
            stray.append(rel)
    if args.check and (changed or stray):
        if changed:
            print("Reader disclosure loader is stale or missing from:")
            for rel in changed:
                print(" -", rel)
        if stray:
            print("Open Internet editorial pages must not contain a Reader loader:")
            for rel in stray:
                print(" -", rel)
        return 1
    if changed:
        print("Installed/refreshed Reader disclosure loader in:")
        for rel in changed:
            print(" -", rel)
    if stray:
        print("Removed legacy Reader loader from:")
        for rel in stray:
            print(" -", rel)
    if not changed and not stray:
        print("Reader disclosure loader already synchronized; Internet remains fully open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
