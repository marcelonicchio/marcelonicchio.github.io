#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/galleries.json"


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def expected_derivative(gallery_id: str, item_id: str, width: int, output_root: str) -> Path:
    # The filename width is a maximum-width profile, not a promise to upscale smaller sources.
    return ROOT / output_root / gallery_id / f"{gallery_id}-{item_id}-{width}.webp"


def expected_size(source_w: int, source_h: int, max_w: int) -> tuple[int, int]:
    target_w = min(source_w, max_w)
    target_h = max(1, round(source_h * target_w / source_w))
    return target_w, target_h


def build(check: bool) -> int:
    data = load_registry()
    policy = data["derivativePolicy"]
    widths = [int(value) for value in policy["widths"]]
    quality = int(policy.get("quality", 78))
    output_root = policy["outputRoot"]
    errors: list[str] = []
    total_source = 0
    total_derived = 0
    totals_by_profile: dict[int, int] = defaultdict(int)

    for gallery in data.get("galleries", []):
        gallery_id = gallery["id"]
        source_root = ROOT / gallery["sourceRoot"]
        seen_ids: set[str] = set()

        for item in gallery.get("items", []):
            item_id = str(item["id"])
            if item_id in seen_ids:
                errors.append(f"{gallery_id}: duplicate item id {item_id}")
                continue
            seen_ids.add(item_id)

            source = source_root / item["source"]
            if not source.exists():
                errors.append(f"{gallery_id}/{item_id}: missing source {source.relative_to(ROOT)}")
                continue
            total_source += source.stat().st_size

            with Image.open(source) as opened:
                image = ImageOps.exif_transpose(opened)
                source_w, source_h = image.size
                # Pillow warns when palette transparency stored as bytes is converted
                # directly to RGB. Normalize through RGBA first so transparent palette
                # sources are handled deterministically before WebP conversion.
                if image.mode == "P" and "transparency" in image.info:
                    image = image.convert("RGBA")
                working = image.convert("RGB")

            expected_meta = {"width": source_w, "height": source_h}
            if check:
                if item.get("width") != source_w or item.get("height") != source_h:
                    errors.append(f"{gallery_id}/{item_id}: source dimensions in registry are stale")
            else:
                item.update(expected_meta)
                item["derivatives"] = {}

            for width in widths:
                target_w, target_h = expected_size(source_w, source_h, width)
                out = expected_derivative(gallery_id, item_id, width, output_root)
                rel = out.relative_to(ROOT).as_posix()
                try:
                    rel.encode("ascii")
                except UnicodeEncodeError:
                    errors.append(f"{gallery_id}/{item_id}: derivative path is not ASCII: {rel}")
                    continue

                expected = {"path": rel, "width": target_w, "height": target_h}
                if check:
                    meta = item.get("derivatives", {}).get(str(width), {})
                    if meta != expected:
                        errors.append(f"{gallery_id}/{item_id}: derivative metadata {width}px is stale")
                    if not out.exists():
                        errors.append(f"{gallery_id}/{item_id}: missing derivative {rel}")
                        continue
                    try:
                        with Image.open(out) as derived:
                            if derived.format != "WEBP":
                                errors.append(f"{gallery_id}/{item_id}: {rel} is not WebP")
                            if derived.size != (target_w, target_h):
                                errors.append(f"{gallery_id}/{item_id}: {rel} has wrong dimensions {derived.size}")
                    except Exception as exc:
                        errors.append(f"{gallery_id}/{item_id}: cannot read {rel}: {exc}")
                    size = out.stat().st_size
                    total_derived += size
                    totals_by_profile[width] += size
                    continue

                out.parent.mkdir(parents=True, exist_ok=True)
                resized = working if (target_w, target_h) == (source_w, source_h) else working.resize((target_w, target_h), Image.Resampling.LANCZOS)
                resized.save(out, "WEBP", quality=quality, method=6, optimize=True)
                size = out.stat().st_size
                total_derived += size
                totals_by_profile[width] += size
                item["derivatives"][str(width)] = expected

    if errors:
        print("Gallery media errors:")
        for error in errors:
            print(" -", error)
        return 1

    if not check:
        REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Gallery derivatives generated and registry dimensions updated.")
    else:
        print("Gallery derivative check passed.")

    print(f"Source bytes: {total_source:,}")
    for width in widths:
        print(f"Max-{width} profile bytes: {totals_by_profile[width]:,}")
    print(f"All generated derivative bytes: {total_derived:,}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build responsive WebP derivatives for registered galleries without upscaling source images.")
    parser.add_argument("--check", action="store_true", help="Validate derivatives and registry metadata without writing files.")
    args = parser.parse_args()
    return build(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
