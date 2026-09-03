#!/usr/bin/env python3
"""Temporary helper: register the spirituality fragment and regenerate Full Biography."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "full_biography.json"
PARITY = ROOT / "data" / "editorial_parity.json"
ENTRY_ID = "spirituality-seeker"

ENTRY = {
    "id": ENTRY_ID,
    "era": "expansao-2001-2008",
    "date": "2006–jan. 2007",
    "domain": "context",
    "source": {
        "pt": {"path": "content/full-biography/pt/spirituality-seeker.inc", "kind": "fragment"},
        "en": {"path": "content/full-biography/en/spirituality-seeker.inc", "kind": "fragment"},
    },
    "date_en": "2006–Jan. 2007",
}


def normalized_fragment_hash(rel_path: str) -> str:
    soup = BeautifulSoup((ROOT / rel_path).read_text(encoding="utf-8"), "html.parser")
    node = soup.find("section")
    if node is None:
        raise RuntimeError(f"fragment has no section: {rel_path}")
    text = str(node)
    text = re.sub(r">\s+<", "><", text)
    text = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest["entries"]
    entries[:] = [entry for entry in entries if entry.get("id") != ENTRY_ID]
    anchor = next(i for i, entry in enumerate(entries) if entry.get("id") == "audiovisual-meia-noite")
    entries.insert(anchor + 1, ENTRY)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    parity = json.loads(PARITY.read_text(encoding="utf-8"))
    parity.setdefault("entries", {})[ENTRY_ID] = {
        "revision": 1,
        "pt_hash": normalized_fragment_hash(ENTRY["source"]["pt"]["path"]),
        "en_hash": normalized_fragment_hash(ENTRY["source"]["en"]["path"]),
        "accepted_on": "2026-09-03",
    }
    PARITY.write_text(json.dumps(parity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, str(ROOT / "tools" / "sync_full_biography.py")], check=True, cwd=ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
