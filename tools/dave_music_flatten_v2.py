#!/usr/bin/env python3
"""Safe wrapper for the temporary Music hierarchy migration.

Preserves root attributes while promoting legacy phases, repairs the inherited
1993 studios entry that never received a biography key, gives every promoted
chapter a stable id, and removes legacy parent anchors after flattening.
"""

from __future__ import annotations

import html
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

    key_match = re.search(r'data-bio-key=["\']([^"\']+)["\']', attrs)
    if not key_match:
        raise RuntimeError("promoted Music entry still lacks data-bio-key")
    key = key_match.group(1)

    if not re.search(r'\bid=["\'][^"\']+["\']', attrs):
        attrs += f' id="{key}"'

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

    migration.key_of(fragment)
    if not migration.id_of(fragment):
        raise RuntimeError(f"promoted Music chapter {key} has no id")
    return fragment


def safe_mp3_section(lang: str) -> str:
    if lang == "pt":
        title, body = migration.MP3_PT_TITLE, migration.MP3_PT
    else:
        title, body = migration.MP3_EN_TITLE, migration.MP3_EN
    return (
        f'<section class="chapter music-entry" id="{migration.MP3_KEY}" '
        f'data-bio-key="{migration.MP3_KEY}">'
        f'<div class="phase-year">2000</div><h2>{html.escape(title, quote=False)}</h2>'
        f'<p>{html.escape(body, quote=False)}</p></section>'
    )


_original_rewrite_music_page = migration.rewrite_music_page


def safe_rewrite_music_page(path, lang, label_to_key=None):
    meta, labels = _original_rewrite_music_page(path, lang, label_to_key)
    first_id = meta[labels["destemidos"]]["id"]
    if not first_id:
        raise RuntimeError("Destemidos entry unexpectedly has no id")
    text = path.read_text(encoding="utf-8")
    if lang == "pt":
        text = re.sub(
            r'<a\s+href=["\']#palcos["\'][^>]*>.*?</a>',
            f'<a href="#{first_id}">Cronologia do Coitado</a>',
            text,
            flags=re.I | re.S,
        )
    else:
        text = re.sub(
            r'<a\s+href=["\']#stages["\'][^>]*>.*?</a>',
            f'<a href="#{first_id}">Coitado chronology</a>',
            text,
            flags=re.I | re.S,
        )
    path.write_text(text, encoding="utf-8")
    return meta, labels


_original_update_manifest = migration.update_manifest


def update_manifest_with_studios(pt_meta, en_meta) -> None:
    _original_update_manifest(pt_meta, en_meta)
    manifest = json.loads(migration.MANIFEST_PATH.read_text(encoding="utf-8"))

    def promote_selector(spec: dict, meta: dict) -> None:
        selector = spec.get("selector", "")
        km = re.search(r"data-bio-key=['\"]([^'\"]+)['\"]", selector)
        if not km:
            return
        key = km.group(1)
        target = meta.get(key)
        if not target or not target.get("id"):
            raise RuntimeError(f"cannot resolve chapter id for manifest key {key}")
        spec["selector"] = f"#{target['id']}"

    for entry in manifest.get("entries", []):
        for lang, target_path, meta in (
            ("pt", "pt/musica/index.html", pt_meta),
            ("en", "en/music/index.html", en_meta),
        ):
            spec = entry.get("source", {}).get(lang)
            if spec and spec.get("path") == target_path and spec.get("kind") == "section":
                promote_selector(spec, meta)

    if not any(entry.get("id") == STUDIOS_KEY for entry in manifest.get("entries", [])):
        pt_id = pt_meta[STUDIOS_KEY].get("id")
        en_id = en_meta[STUDIOS_KEY].get("id")
        if not pt_id or not en_id:
            raise RuntimeError("Studios entry lacks PT/EN chapter id")
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
                "pt": {"path": "pt/musica/index.html", "kind": "section", "selector": f"#{pt_id}"},
                "en": {"path": "en/music/index.html", "kind": "section", "selector": f"#{en_id}"},
            },
        }
        insert_at = None
        for i, entry in enumerate(manifest["entries"]):
            if entry.get("id") == "music-limonada-1992":
                insert_at = i + 1
                break
        if insert_at is None:
            raise RuntimeError("music-limonada-1992 not found in Full Biography manifest")
        manifest["entries"].insert(insert_at, studios_entry)

    for entry in manifest["entries"]:
        if entry.get("id") == migration.MP3_KEY:
            entry["source"]["pt"]["selector"] = f"#{pt_meta[migration.MP3_KEY]['id']}"
            entry["source"]["en"]["selector"] = f"#{en_meta[migration.MP3_KEY]['id']}"
            break

    migration.MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


migration.promote = safe_promote
migration.mp3_section = safe_mp3_section
migration.rewrite_music_page = safe_rewrite_music_page
migration.update_manifest = update_manifest_with_studios

if __name__ == "__main__":
    migration.migrate()
