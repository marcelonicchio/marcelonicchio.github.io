#!/usr/bin/env python3
"""Generate sitemap.xml from the audited indexable set with real per-page lastmod dates.

`lastmod` is derived from Git history for each indexable HTML file. When an HTML
file is dirty in the working tree, the current UTC date is used so generation
before a commit remains stable after that same-day commit lands.

This deliberately avoids global/fabricated freshness dates.
"""
from __future__ import annotations

import argparse
import difflib
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from audit_site import LAUNCH_INDEXABLE, ROOT, page_url

SITEMAP = ROOT / "sitemap.xml"


def run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def page_lastmod(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        raise FileNotFoundError(rel)

    dirty = run_git("status", "--porcelain", "--", rel)
    if dirty:
        return datetime.now(timezone.utc).date().isoformat()

    committed = run_git("log", "-1", "--format=%cs", "--", rel)
    if not committed:
        raise RuntimeError(f"no Git history found for indexable page: {rel}")
    return committed


def render() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel in sorted(LAUNCH_INDEXABLE):
        url = page_url(ROOT / rel)
        lines.extend(
            [
                "  <url>",
                f"    <loc>{escape(url)}</loc>",
                f"    <lastmod>{page_lastmod(rel)}</lastmod>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if sitemap.xml is not generated state")
    args = parser.parse_args()

    expected = render()
    actual = SITEMAP.read_text(encoding="utf-8") if SITEMAP.exists() else ""

    if args.check:
        if actual == expected:
            print("sitemap.xml is synchronized with indexable pages and Git-derived lastmod dates.")
            return 0
        print("sitemap.xml is stale. Regenerate with: python tools/build_sitemap.py")
        print(
            "".join(
                difflib.unified_diff(
                    actual.splitlines(keepends=True),
                    expected.splitlines(keepends=True),
                    fromfile="sitemap.xml",
                    tofile="generated sitemap.xml",
                )
            )
        )
        return 1

    if actual != expected:
        SITEMAP.write_text(expected, encoding="utf-8")
        print("Updated sitemap.xml with Git-derived per-page lastmod dates.")
    else:
        print("sitemap.xml already synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
