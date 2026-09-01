#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/galleries.json"
GALLERY_ID_RE = re.compile(r'data-gallery="([^"]+)"')


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors: list[str] = []
    gallery_ids: set[str] = set()
    target_pairs: set[tuple[str, str]] = set()
    controller_checked_targets: set[str] = set()

    for gallery in data.get("galleries", []):
        gid = gallery.get("id", "")
        if not gid or gid in gallery_ids:
            errors.append(f"duplicate or empty gallery id: {gid!r}")
            continue
        gallery_ids.add(gid)
        source_root = ROOT / gallery.get("sourceRoot", "")
        item_ids: set[str] = set()

        for item in gallery.get("items", []):
            iid = str(item.get("id", ""))
            if not iid or iid in item_ids:
                errors.append(f"{gid}: duplicate or empty item id {iid!r}")
                continue
            item_ids.add(iid)
            captions = item.get("caption", {})
            for lang in ("pt", "en"):
                if not captions.get(lang):
                    errors.append(f"{gid}/{iid}: missing {lang} caption")
            source = source_root / item.get("source", "")
            if not source.exists():
                errors.append(f"{gid}/{iid}: missing source {source.relative_to(ROOT) if source.is_absolute() else source}")
            if not isinstance(item.get("width"), int) or not isinstance(item.get("height"), int):
                errors.append(f"{gid}/{iid}: missing source dimensions in registry")
            derivatives = item.get("derivatives", {})
            for required in ("480", "768"):
                meta = derivatives.get(required)
                if not meta:
                    errors.append(f"{gid}/{iid}: missing {required}px derivative metadata")
                    continue
                rel = meta.get("path", "")
                try:
                    rel.encode("ascii")
                except UnicodeEncodeError:
                    errors.append(f"{gid}/{iid}: derivative path is not ASCII: {rel}")
                if not (ROOT / rel).exists():
                    errors.append(f"{gid}/{iid}: missing derivative file {rel}")
                if not isinstance(meta.get("width"), int) or not isinstance(meta.get("height"), int):
                    errors.append(f"{gid}/{iid}: invalid derivative dimensions for {required}px")

        for lang, targets in gallery.get("targets", {}).items():
            if lang not in {"pt", "en"}:
                errors.append(f"{gid}: unsupported language target {lang}")
            for rel in targets:
                target_pairs.add((gid, rel))
                path = ROOT / rel
                if not path.exists():
                    errors.append(f"{gid}: missing target {rel}")
                    continue
                text = path.read_text(encoding="utf-8")
                if path.suffix.lower() in {".html", ".htm"} and rel not in controller_checked_targets:
                    controller_checked_targets.add(rel)
                    if "/assets/js/archive-lightbox.js" not in text:
                        errors.append(f"{rel}: rendered gallery page does not load archive-lightbox.js")
                start = f"<!-- gallery:{gid}:start -->"
                end = f"<!-- gallery:{gid}:end -->"
                if text.count(start) != 1 or text.count(end) != 1:
                    errors.append(f"{rel}: expected exactly one synchronized marker pair for {gid}")
                    continue
                block = text[text.index(start): text.index(end) + len(end)]
                if block.count('class="record-gallery__item"') != len(gallery.get("items", [])):
                    errors.append(f"{rel}: item count differs from registry for {gid}")
                if f'data-gallery="{gid}"' not in block:
                    errors.append(f"{rel}: missing data-gallery id {gid}")
                for item in gallery.get("items", []):
                    original = "/" + gallery["sourceRoot"].rstrip("/") + "/" + item["source"]
                    if f'href="{original}"' not in block:
                        errors.append(f"{rel}: original lightbox href missing for {gid}/{item['id']}")
                    primary = item.get("derivatives", {}).get("480", {})
                    src = "/" + primary.get("path", "")
                    if f'src="{src}"' not in block:
                        errors.append(f"{rel}: responsive thumbnail src missing for {gid}/{item['id']}")
                    if 'srcset=' not in block:
                        errors.append(f"{rel}: srcset missing in {gid}")
                        break
                    if f'width="{primary.get("width")}"' not in block or f'height="{primary.get("height")}"' not in block:
                        errors.append(f"{rel}: explicit dimensions missing for {gid}/{item['id']}")
                if re.search(r'<img[^>]+src="/assets/archive/audiovisual/meia-noite-e-uns/', block):
                    errors.append(f"{rel}: gallery thumbnail still points at a full-size Meia-Noite source")

    # Every rendered gallery must be registered, even if a future page is added manually.
    for path in sorted([*ROOT.glob("pt/**/*.html"), *ROOT.glob("en/**/*.html")]):
        text = path.read_text(encoding="utf-8")
        for gid in GALLERY_ID_RE.findall(text):
            if gid not in gallery_ids:
                errors.append(f"{path.relative_to(ROOT)}: unregistered gallery id {gid}")

    if errors:
        print("Gallery audit failed:")
        for error in errors:
            print(" -", error)
        return 1

    print(f"Gallery audit passed: {len(gallery_ids)} galleries, {len(target_pairs)} rendered targets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
