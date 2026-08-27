#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/galleries.json"
DIV_TAG = re.compile(r"<div\b[^>]*>|</div>", re.I)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_gallery(gallery: dict, lang: str) -> str:
    gallery_id = gallery["id"]
    items = gallery["items"]
    count = len(items)
    title = gallery.get("title", {}).get(lang, "Fotos" if lang == "pt" else "Photos")
    if lang == "pt":
        previous = "Fotos anteriores"
        following = "Próximas fotos"
        enlarge = "Ampliar"
    else:
        previous = "Previous photos"
        following = "Next photos"
        enlarge = "Enlarge"

    title_id = f"{gallery_id}-gallery-title"
    lines = [
        f'<!-- gallery:{gallery_id}:start -->',
        f'<div class="record-gallery" data-gallery="{esc(gallery_id)}" aria-labelledby="{esc(title_id)}">',
        f'  <div class="record-gallery__head"><strong id="{esc(title_id)}">{esc(title)} · {count}</strong></div>',
        '  <div class="record-gallery__rail">',
        f'    <button class="record-gallery__arrow record-gallery__arrow--prev" type="button" data-gallery-prev hidden aria-label="{esc(previous)}">‹</button>',
        '    <div class="record-gallery__strip" data-gallery-strip tabindex="0">',
    ]

    for item in items:
        caption = item["caption"][lang]
        alt = item.get("alt", {}).get(lang, caption)
        derivatives = item.get("derivatives", {})
        if not derivatives:
            raise ValueError(f"{gallery_id}/{item['id']} has no generated derivatives")
        candidates = sorted(derivatives.values(), key=lambda meta: int(meta["width"]))
        primary = candidates[0]
        src = "/" + primary["path"]
        srcset = ", ".join(f"/{meta['path']} {meta['width']}w" for meta in candidates)
        original = "/" + gallery["sourceRoot"].rstrip("/") + "/" + item["source"]
        lines.extend([
            f'      <a class="record-gallery__item" href="{esc(original)}" data-caption="{esc(caption)}" aria-label="{esc(enlarge + ": " + caption)}">',
            f'        <img src="{esc(src)}" srcset="{esc(srcset)}" sizes="(max-width: 580px) min(72vw, 330px), 152px" width="{primary["width"]}" height="{primary["height"]}" loading="lazy" decoding="async" alt="{esc(alt)}">',
            '      </a>',
        ])

    lines.extend([
        '    </div>',
        f'    <button class="record-gallery__arrow record-gallery__arrow--next" type="button" data-gallery-next hidden aria-label="{esc(following)}">›</button>',
        '  </div>',
        '</div>',
        f'<!-- gallery:{gallery_id}:end -->',
    ])
    return "\n".join(lines)


def replace_balanced_gallery(text: str, gallery_id: str, replacement: str) -> str:
    start_marker = f"<!-- gallery:{gallery_id}:start -->"
    end_marker = f"<!-- gallery:{gallery_id}:end -->"
    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start) + len(end_marker)
        return text[:start] + replacement + text[end:]

    placeholder = f"<!-- gallery:{gallery_id} -->"
    if placeholder in text:
        return text.replace(placeholder, replacement, 1)

    needle = f'<div class="record-gallery" data-gallery="{gallery_id}"'
    start = text.find(needle)
    if start < 0:
        raise ValueError(f"gallery {gallery_id} not found and no placeholder exists")

    depth = 0
    end = None
    for match in DIV_TAG.finditer(text, start):
        token = match.group(0).lower()
        if token.startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = match.end()
                break
    if end is None:
        raise ValueError(f"unbalanced gallery markup for {gallery_id}")
    return text[:start] + replacement + text[end:]


def synchronize(check: bool) -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    changed: list[str] = []
    errors: list[str] = []

    for gallery in data.get("galleries", []):
        for lang, targets in gallery.get("targets", {}).items():
            try:
                rendered = render_gallery(gallery, lang)
            except Exception as exc:
                errors.append(f"{gallery['id']} ({lang}): {exc}")
                continue
            for rel in targets:
                path = ROOT / rel
                if not path.exists():
                    errors.append(f"{gallery['id']}: missing target {rel}")
                    continue
                original = path.read_text(encoding="utf-8")
                try:
                    updated = replace_balanced_gallery(original, gallery["id"], rendered)
                except Exception as exc:
                    errors.append(f"{rel}: {exc}")
                    continue
                if updated != original:
                    changed.append(rel)
                    if not check:
                        path.write_text(updated, encoding="utf-8")

    if errors:
        print("Gallery synchronization errors:")
        for error in errors:
            print(" -", error)
        return 1

    if check and changed:
        print("Gallery markup is not synchronized:")
        for rel in sorted(set(changed)):
            print(" -", rel)
        return 1

    if check:
        print("Gallery synchronization check passed.")
    elif changed:
        print("Updated gallery markup in:")
        for rel in sorted(set(changed)):
            print(" -", rel)
    else:
        print("Gallery markup already synchronized.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize registered galleries into PT/EN HTML targets.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return synchronize(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
