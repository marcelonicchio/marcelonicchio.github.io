#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "entries.json"
IDS = {
    "music-demo-tape-1994", "music-album-1997", "audiovisual-homens",
    "music-festival-1998-1999", "music-album-1999-2000", "internet-psinet",
    "music-programa-jo", "communication-sinal-verde", "internet-sem",
    "internet-clickland", "internet-petlove", "hai-pro1", "hai-pro2",
}

data = json.loads(PATH.read_text(encoding="utf-8"))
for entry in data["entries"]:
    if entry.get("id") not in IDS:
        continue
    for lang in ("pt", "en"):
        text = entry.get("summary", {}).get(lang)
        if text:
            entry["summary"][lang] = re.sub(r"\s+([,.;:!?])", r"\1", text)
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Normalized Phase 2 summary punctuation.")
