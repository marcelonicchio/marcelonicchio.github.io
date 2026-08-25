#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
profiles = json.loads((ROOT / "data" / "presence.json").read_text(encoding="utf-8"))["profiles"]
rendered = [p for p in profiles if p.get("render", True)]
hidden = [p for p in profiles if not p.get("render", True)]
expected = {p["url"] for p in rendered}
identity = {p["url"] for p in rendered if p.get("sameAs")}
hidden_urls = {p["url"] for p in hidden}
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
        errors.append(f"{rel}: missing {len(missing)} rendered presence link(s)")
    unexpected_hidden = sorted(hidden_urls & urls)
    if unexpected_hidden:
        errors.append(f"{rel}: contains {len(unexpected_hidden)} profile(s) marked render=false")
    for url in expected & urls:
        link_re = re.compile(r'<a[^>]+href="' + re.escape(url) + r'"[^>]*>', re.I)
        m = link_re.search(block)
        if not m:
            continue
        tag = m.group(0)
        if 'target="_blank"' not in tag:
            errors.append(f"{rel}: external presence link missing target=_blank: {url}")
        rel_match = re.search(r'rel="([^"]+)"', tag, flags=re.I)
        rel_tokens = set(rel_match.group(1).split()) if rel_match else set()
        if not {"noopener", "noreferrer"}.issubset(rel_tokens):
            errors.append(f"{rel}: external presence link missing safe rel tokens: {url}")
        if url in identity and "me" not in rel_tokens:
            errors.append(f"{rel}: identity presence link missing rel=me: {url}")
        if ' title=' in tag.lower():
            errors.append(f"{rel}: redundant title attribute remains on presence link: {url}")

person = json.loads((ROOT / "data" / "person.json").read_text(encoding="utf-8"))
expected_same_as = [p["url"] for p in profiles if p.get("sameAs")]
if person.get("sameAs") != expected_same_as:
    errors.append("data/person.json: sameAs is not synchronized with data/presence.json")

if errors:
    print(f"Presence audit: {len(errors)} error(s) across {checked} HTML file(s).")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"Presence audit: 0 errors across {checked} HTML file(s); {len(rendered)} rendered profile(s), {len(identity)} identity link(s).")
