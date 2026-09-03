#!/usr/bin/env python3
"""Require explicit intrinsic dimensions for local raster images.

This protects layout stability on static HTML and Reader preview images. Gallery
registry dimensions are audited separately by audit_galleries.py.
"""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RASTER = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() == 'img':
            self.images.append(dict(attrs))


def valid_dimension(value: str | None) -> bool:
    try:
        return int(value or '0') > 0
    except ValueError:
        return False


def local_raster(src: str) -> bool:
    if not src.startswith('/'):
        return False
    path = Path(src.split('?', 1)[0].split('#', 1)[0])
    return path.suffix.lower() in RASTER


def audit_html(errors: list[str]) -> int:
    count = 0
    for path in sorted(ROOT.rglob('*.html')):
        if '.git' in path.parts:
            continue
        parser = ImageParser()
        parser.feed(path.read_text(encoding='utf-8'))
        rel = path.relative_to(ROOT).as_posix()
        for image in parser.images:
            src = image.get('src', '')
            if not local_raster(src):
                continue
            count += 1
            if not valid_dimension(image.get('width')) or not valid_dimension(image.get('height')):
                errors.append(f'{rel}: local raster image lacks valid width/height: {src}')
    return count


def audit_reader_previews(errors: list[str]) -> int:
    path = ROOT / 'data/entries.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    count = 0
    for entry in data.get('entries', []):
        for lang, preview in (entry.get('reader_preview') or {}).items():
            if not isinstance(preview, dict) or not preview.get('image'):
                continue
            if not local_raster(preview['image']):
                continue
            count += 1
            if not valid_dimension(str(preview.get('width', ''))) or not valid_dimension(str(preview.get('height', ''))):
                errors.append(f"data/entries.json: {entry.get('id')} {lang} Reader preview lacks valid width/height")
    return count


def main() -> int:
    errors: list[str] = []
    html_count = audit_html(errors)
    preview_count = audit_reader_previews(errors)
    if errors:
        print('Intrinsic image dimension errors:')
        for error in errors:
            print(' -', error)
        return 1
    print(f'Intrinsic image dimension audit passed: {html_count} local raster HTML image(s), {preview_count} Reader preview definition(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
