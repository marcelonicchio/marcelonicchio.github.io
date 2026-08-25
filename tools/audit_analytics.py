#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "analytics.json"
START = "<!-- google-analytics:start -->"
END = "<!-- google-analytics:end -->"

data = json.loads(CONFIG.read_text(encoding="utf-8"))
measurement_id = data.get("measurementId", "").strip()
errors = []
checked = 0

if not re.fullmatch(r"G-[A-Z0-9]+", measurement_id):
    errors.append("data/analytics.json: invalid GA4 measurementId")
if not data.get("enabled", False):
    errors.append("data/analytics.json: analytics must be enabled for this audit")

for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    checked += 1
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()

    if text.count(START) != 1 or text.count(END) != 1:
        errors.append(f"{rel}: expected exactly one managed Google Analytics block")
        continue

    block_match = re.search(re.escape(START) + r"(.*?)" + re.escape(END), text, flags=re.S)
    if not block_match:
        errors.append(f"{rel}: malformed Google Analytics block")
        continue
    block = block_match.group(1)

    if f"https://www.googletagmanager.com/gtag/js?id={measurement_id}" not in block:
        errors.append(f"{rel}: missing GA4 loader for {measurement_id}")
    if f"gtag('config', '{measurement_id}');" not in block:
        errors.append(f"{rel}: missing GA4 config for {measurement_id}")
    if text.count(measurement_id) != 2:
        errors.append(f"{rel}: expected measurement ID exactly twice (loader + config)")

    head = re.search(r"<head(?:\s[^>]*)?>", text, flags=re.I)
    if head:
        block_pos = text.find(START)
        if block_pos < head.end() or block_pos - head.end() > 3:
            errors.append(f"{rel}: Google tag is not immediately after <head>")

if errors:
    print(f"Analytics audit: {len(errors)} error(s) across {checked} HTML file(s).")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"Analytics audit: 0 errors across {checked} HTML file(s); measurement ID {measurement_id} installed once per page.")
