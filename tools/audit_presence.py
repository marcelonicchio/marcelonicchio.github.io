#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
profiles = json.loads((ROOT / "data" / "presence.json").read_text(encoding="utf-8"))["profiles"]
expected = {p["url"] for p in profiles}
errors = []
checked = 0

for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    checked += 1
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    if '<div class="wrap presence-panel">' not in text:
        errors.append(f"{rel}: missing presence panel")
        continue
    block_match = re.search(r'<!-- presence:start -->(.*?)<!-- presence:end -->', text, flags=re.S)
    if not block_match:
        errors.append(f"{rel}: missing presence markers")
        continue
    block = block_match.group(1)
    urls = set(re.findall(r'href="([^"]+)"', block))
    missing = sorted(expected - urls)
    if missing:
        errors.append(f"{rel}: missing {len(missing)} canonical presence link(s)")
    for url in expected & urls:
        link_re = re.compile(r'<a[^>]+href="' + re.escape(url) + r'"[^>]*>', re.I)
        m = link_re.search(block)
        if not m:
            continue
        tag = m.group(0)
        if 'target="_blank"' not in tag or 'rel="noopener noreferrer"' not in tag:
            errors.append(f"{rel}: external presence link missing safe new-tab attributes: {url}")

person = json.loads((ROOT / "data" / "person.json").read_text(encoding="utf-8"))
expected_same_as = [p["url"] for p in profiles if p.get("sameAs")]
if person.get("sameAs") != expected_same_as:
    errors.append("data/person.json: sameAs is not synchronized with data/presence.json")

if errors:
    print(f"Presence audit: {len(errors)} error(s) across {checked} HTML file(s).")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"Presence audit: 0 errors across {checked} HTML file(s); {len(profiles)} profiles synchronized.")
