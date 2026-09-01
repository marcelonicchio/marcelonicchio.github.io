#!/usr/bin/env python3
"""Install the disclosure loader on selected Reader Pages."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = '<script src="/assets/js/reader-disclosure-loader.js" defer></script>'
TARGETS = [
    "pt/biografia/index.html",
    "en/biography/index.html",
    "pt/internet/index.html",
    "en/internet/index.html",
    "pt/comunicacao/index.html",
    "en/communication/index.html",
    "pt/audiovisual/index.html",
    "en/audiovisual/index.html",
    "pt/ia-hai/index.html",
    "en/ai-hai/index.html",
]


def sync(path: Path, *, check: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    if SCRIPT in text:
        return False
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
    if args.check and changed:
        print("Reader disclosure loader is missing from:")
        for rel in changed:
            print(" -", rel)
        return 1
    if changed:
        print("Installed Reader disclosure loader in:")
        for rel in changed:
            print(" -", rel)
    else:
        print("Reader disclosure loader already synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
