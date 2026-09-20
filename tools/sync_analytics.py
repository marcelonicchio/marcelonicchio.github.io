#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "analytics.json"
START = "<!-- google-analytics:start -->"
END = "<!-- google-analytics:end -->"


def load_measurement_id() -> str:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    measurement_id = data.get("measurementId", "").strip()
    if not re.fullmatch(r"G-[A-Z0-9]+", measurement_id):
        raise SystemExit("Invalid GA4 measurementId in data/analytics.json")
    if not data.get("enabled", False):
        raise SystemExit("Analytics is disabled in data/analytics.json")
    return measurement_id


def render_block(measurement_id: str) -> str:
    return f'''{START}
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{measurement_id}');
</script>
{END}'''


def is_redirect_stub(text: str) -> bool:
    has_refresh = re.search(r'<meta\s+http-equiv=["\']refresh["\']', text, flags=re.I) is not None
    has_noindex = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', text, flags=re.I) is not None
    return has_refresh and has_noindex


def main() -> None:
    measurement_id = load_measurement_id()
    block = render_block(measurement_id)
    block_re = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    changed = []

    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        original = text

        # Compatibility redirect stubs should not generate analytics pageviews.
        if is_redirect_stub(text):
            text = block_re.sub("", text)
            text = re.sub(r"\n{3,}", "\n\n", text)
        # Replace our managed block when present; otherwise insert exactly once after <head>.
        elif START in text:
            text = block_re.sub(block, text)
        else:
            if measurement_id in text:
                raise SystemExit(f"{path.relative_to(ROOT)} already contains unmanaged GA4 measurement ID")
            head = re.search(r"<head(?:\s[^>]*)?>", text, flags=re.I)
            if not head:
                raise SystemExit(f"{path.relative_to(ROOT)} has no <head> element")
            pos = head.end()
            text = text[:pos] + "\n" + block + text[pos:]

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())

    print(f"Analytics sync: {len(changed)} HTML file(s) changed; measurement ID {measurement_id}.")
    for rel in changed:
        print(f"  - {rel}")


if __name__ == "__main__":
    main()
