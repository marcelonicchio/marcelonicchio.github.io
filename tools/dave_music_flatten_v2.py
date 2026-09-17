#!/usr/bin/env python3
"""Safe wrapper for the temporary Music hierarchy migration.

Preserves root attributes while promoting legacy phases and repairs the one
inherited Music entry (1993 studios/shows) that never received a biography key.
"""

from __future__ import annotations

import json
import re

import dave_music_flatten as migration

STUDIOS_KEY = "music-studios-1993"


def safe_promote(fragment: str) -> str:
    root = re.match(r"(\s*)<(div|section)\b([^>]*)>", fragment, flags=re.I | re.S)
    if not root:
        raise RuntimeError("unknown phase child root element")

    leading, tag, attrs = root.groups()
    tag = tag.lower()
    class_match = re.search(r"\bclass=([\"'])(.*?)\1", attrs, flags=re.I | re.S)
    if not class_match:
        raise RuntimeError("Music phase root has no class attribute")

    classes = class_match.group(2).split()
    classes = [c for c in classes if c != "phase"]
    if "chapter" not in classes:
        classes.insert(0, "chapter")
    if "music-entry" not in classes:
        classes.append("music-entry")
    class_value = " ".join(classes)
    attrs = attrs[:class_match.start(2)] + class_value + attrs[class_match.end(2):]

    # Historical exception: the 1993 studios/shows block has an id but never
    # received data-bio-key, which also kept it outside Full Biography sync.
    if "data-bio-key=" not in attrs:
        title = migration.heading_text(fragment)
        root_id = re.search(r'\bid=["\']([^"\']+)["\']', attrs)
        root_id_value = root_id.group(1) if root_id else ""
        is_studios = (
            root_id_value in {"estudios-shows-1993", "studios-shows-1993"}
            or "Estúdios e Shows" in title
            or "Studios and Shows" in title
            or "Studios & Shows" in title
        )
        if not is_studios:
            raise RuntimeError(f"Music entry lacks data-bio-key and is not the known studios exception: {title}")
        attrs += f' data-bio-key="{STUDIOS_KEY}"'

    if tag == "div":
        outer_end = migration.find_balanced_tag_end(fragment, root.start(2) - 1, "div")
        close_start = fragment.rfind("</div>", root.end(), outer_end)
        if close_start < 0:
            raise RuntimeError("legacy phase outer close not found")
        fragment = (
            fragment[:root.start()]
            + leading
            + "<section"
            + attrs
            + ">"
            + fragment[root.end():close_start]
            + "</section>"
            + fragment[outer_end:]
        )
    else:
        fragment = fragment[:root.start()] + leading + "<section" + attrs + ">" + fragment[root.end():]

    fragment = migration.unwrap_phase_body(fragment)
    fragment = re.sub(r"<h3\b([^>]*)>", r"<h2\1>", fragment, count=1, flags=re.I)
    fragment = re.sub(r"</h3>", "</h2>", fragment, count=1, flags=re.I)

    # Guard: every promoted entry must leave this routine with a biography key.
    migration.key_of(fragment)
    return fragment


_original_update_manifest = migration.update_manifest


def update_manifest_with_studios(pt_meta, en_meta) -> None:
    _original_update_manifest(pt_meta, en_meta)
    manifest = json.loads(migration.MANIFEST_PATH.read_text(encoding="utf-8"))
    if any(entry.get("id") == STUDIOS_KEY for entry in manifest.get("entries", [])):
        return

    studios_entry = {
        "id": STUDIOS_KEY,
        "era": "cruzamentos-1992-2000",
        "date": "1993",
        "domain": "music",
        "title": {
            "pt": str(pt_meta[STUDIOS_KEY]["title"]),
            "en": str(en_meta[STUDIOS_KEY]["title"]),
        },
        "source": {
            "pt": {
                "path": "pt/musica/index.html",
                "kind": "section",
                "selector": f"[data-bio-key='{STUDIOS_KEY}']",
            },
            "en": {
                "path": "en/music/index.html",
                "kind": "section",
                "selector": f"[data-bio-key='{STUDIOS_KEY}']",
            },
        },
    }

    # Place it directly after Destemidos and before Kid Vinil/Café Piu Piu,
    # matching Marcelo's requested Music-thread order.
    insert_at = None
    for i, entry in enumerate(manifest["entries"]):
        if entry.get("id") == "music-limonada-1992":
            insert_at = i + 1
            break
    if insert_at is None:
        raise RuntimeError("music-limonada-1992 not found in Full Biography manifest")
    manifest["entries"].insert(insert_at, studios_entry)
    migration.MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


migration.promote = safe_promote
migration.update_manifest = update_manifest_with_studios

if __name__ == "__main__":
    migration.migrate()
