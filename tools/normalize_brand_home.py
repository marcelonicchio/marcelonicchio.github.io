#!/usr/bin/env python3
"""Make the site brand/logo return to the root language gateway.

Language-section navigation remains unchanged; only the Marcelo Nicchio brand
link in the header is normalized to the top-level home (/).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(
    r'<a\s+class="brand"\s+href="/(?:pt|en)/"(?:\s+aria-current="page")?\s*>Marcelo Nicchio</a>'
)

changed: list[str] = []
seen = 0

for lang, aria in (
    ("pt", "Voltar à página inicial e seleção de idioma"),
    ("en", "Back to home and language selection"),
):
    replacement = f'<a class="brand" href="/" aria-label="{aria}">Marcelo Nicchio</a>'
    for path in sorted((ROOT / lang).rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        matches = len(PATTERN.findall(text))
        if matches:
            seen += matches
            updated = PATTERN.sub(replacement, text)
            if updated != text:
                path.write_text(updated, encoding="utf-8")
                changed.append(path.relative_to(ROOT).as_posix())

if seen == 0:
    raise SystemExit("No language-section brand links matched the expected pattern.")

leftovers: list[str] = []
for lang in ("pt", "en"):
    for path in sorted((ROOT / lang).rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if re.search(r'<a\s+class="brand"\s+href="/(?:pt|en)/"', text):
            leftovers.append(path.relative_to(ROOT).as_posix())

if leftovers:
    raise SystemExit("Brand links still point to language hubs: " + ", ".join(leftovers))

print(f"Normalized {seen} brand link(s) across {len(changed)} HTML file(s).")
for item in changed:
    print(f"  - {item}")
