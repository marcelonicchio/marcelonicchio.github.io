#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data/entries.json"

LANG = {
    "pt": {
        "page": "pt/ia-hai/index.html",
        "selector": "melissa",
        "fragment": "content/entries/pt/hai-melissa.inc",
    },
    "en": {
        "page": "en/ai-hai/index.html",
        "selector": "melissa",
        "fragment": "content/entries/en/hai-melissa.inc",
    },
}


def extract_body(page: Path, section_id: str) -> str:
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    section = soup.find("section", id=section_id)
    if not isinstance(section, Tag):
        raise RuntimeError(f"Missing section #{section_id} in {page}")
    heading = section.find("h2", recursive=False)
    if not isinstance(heading, Tag):
        raise RuntimeError(f"Missing direct h2 in section #{section_id} of {page}")
    heading.extract()
    return section.decode_contents().strip() + "\n"


def main() -> int:
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entry = next((item for item in data.get("entries", []) if item.get("id") == "hai-melissa"), None)
    if entry is None:
        raise RuntimeError("hai-melissa entry not found")

    for lang, spec in LANG.items():
        fragment = ROOT / spec["fragment"]
        fragment.parent.mkdir(parents=True, exist_ok=True)
        fragment.write_text(extract_body(ROOT / spec["page"], spec["selector"]), encoding="utf-8")

    entry["source"] = {
        "kind": "fragment",
        "pt_path": LANG["pt"]["fragment"],
        "en_path": LANG["en"]["fragment"],
    }
    entry["chapter_page"] = {
        "status": "pilot",
        "indexing": "noindex,follow",
        "description": {
            "pt": "Melissa 1.0: caso de interação prolongada de Marcelo Nicchio com Gemini 2.5 Pro, reasoning traces, escala EIP, Melissa Framework e quatro trabalhos públicos.",
            "en": "Melissa 1.0: Marcelo Nicchio’s extended Gemini 2.5 Pro interaction case, reasoning traces, EIP scale, Melissa Framework and four public works.",
        },
        "pt_path": "pt/ia-hai/melissa-1-0/index.html",
        "en_path": "en/ai-hai/melissa-1-0/index.html",
    }

    ENTRIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Melissa promoted to neutral PT/EN fragments and Chapter Page pilot metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
