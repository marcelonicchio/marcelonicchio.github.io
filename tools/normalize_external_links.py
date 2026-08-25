#!/usr/bin/env python3
"""Normalize external-link behavior across the static HTML site.

Rules:
- Links to external http(s) hosts open in a new browsing context via target="_blank".
- External links carry rel="noopener noreferrer" for safety/privacy.
- Internal links to marcelonicchio.github.io retain normal same-tab navigation.
- The persistent ORCID shown in the root gateway is linked to the canonical ORCID URL.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_HOSTS = {"marcelonicchio.github.io"}
ORCID = "0009-0002-5626-8973"
ORCID_URL = f"https://orcid.org/{ORCID}"

ANCHOR_RE = re.compile(
    r"<a\b(?P<attrs>[^>]*?\bhref=(?P<quote>['\"])(?P<href>(?:https?:)?//[^'\"]+)(?P=quote)[^>]*)>",
    flags=re.IGNORECASE,
)
ATTR_RE_TPL = r"\s{attr}\s*=\s*(['\"])(.*?)\1"


def _set_attr(attrs: str, attr: str, value: str) -> str:
    pattern = re.compile(ATTR_RE_TPL.format(attr=re.escape(attr)), re.IGNORECASE)
    if pattern.search(attrs):
        return pattern.sub(f' {attr}="{value}"', attrs, count=1)
    return attrs.rstrip() + f' {attr}="{value}"'


def _merge_rel(attrs: str) -> str:
    pattern = re.compile(ATTR_RE_TPL.format(attr="rel"), re.IGNORECASE)
    match = pattern.search(attrs)
    required = ["noopener", "noreferrer"]
    if not match:
        return attrs.rstrip() + ' rel="noopener noreferrer"'
    tokens = match.group(2).split()
    lowered = {token.lower() for token in tokens}
    for token in required:
        if token not in lowered:
            tokens.append(token)
    return pattern.sub(' rel="' + " ".join(tokens) + '"', attrs, count=1)


def normalize_anchor(match: re.Match[str]) -> str:
    href = match.group("href")
    parsed = urlparse("https:" + href if href.startswith("//") else href)
    host = (parsed.hostname or "").lower()
    if host in SITE_HOSTS:
        return match.group(0)

    attrs = match.group("attrs")
    attrs = _set_attr(attrs, "target", "_blank")
    attrs = _merge_rel(attrs)
    return "<a" + attrs + ">"


def normalize_html(path: Path) -> tuple[bool, int]:
    original = path.read_text(encoding="utf-8")
    text = original

    if path == ROOT / "index.html":
        plain = f"<strong>ORCID {ORCID}</strong>"
        linked = f'<strong><a href="{ORCID_URL}">ORCID {ORCID}</a></strong>'
        text = text.replace(plain, linked)

    text, link_count = ANCHOR_RE.subn(normalize_anchor, text)
    changed = text != original
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed, link_count


def main() -> int:
    changed_files = []
    anchors_scanned = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        changed, count = normalize_html(path)
        anchors_scanned += count
        if changed:
            changed_files.append(path.relative_to(ROOT).as_posix())

    print(f"Scanned {anchors_scanned} absolute http(s) anchors.")
    print(f"Changed {len(changed_files)} HTML files.")
    for item in changed_files:
        print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
