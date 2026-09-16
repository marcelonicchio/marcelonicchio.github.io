#!/usr/bin/env python3
"""Safe wrapper for the temporary Music hierarchy migration.

Overrides only the legacy phase -> section promotion routine so root attributes
(data-bio-key, id, etc.) are preserved verbatim except for the class/tag change.
"""

from __future__ import annotations

import re

import dave_music_flatten as migration


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

    # Guard: promotion must never strip the biography key.
    migration.key_of(fragment)
    return fragment


migration.promote = safe_promote

if __name__ == "__main__":
    migration.migrate()
