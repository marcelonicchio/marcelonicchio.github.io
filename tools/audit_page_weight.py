#!/usr/bin/env python3
"""Report page-delivery image weight; warn by default, gate only with --strict."""
from __future__ import annotations
import argparse
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

def local_file(url: str | None) -> Path | None:
    if not url:
        return None
    url = url.strip()
    if url.startswith(('http://', 'https://', '//', 'data:')):
        return None
    rel = unquote(urlsplit(url).path).lstrip('/')
    return ROOT / rel if rel else None

def srcset_urls(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip().split()[0] for part in value.split(',') if part.strip()]

def mib(value: int) -> str:
    return f'{value / (1024 * 1024):.2f} MiB'

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--warn-mb', type=float, default=4.0)
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    threshold = int(args.warn_mb * 1024 * 1024)
    rows = []
    over = []
    missing = []
    for html in sorted(ROOT.rglob('*.html')):
        if '.git' in html.parts:
            continue
        soup = BeautifulSoup(html.read_text(encoding='utf-8'), 'html.parser')
        images = soup.find_all('img')
        src_files: set[Path] = set()
        chosen_max_files: set[Path] = set()
        for img in images:
            candidates = []
            src = local_file(img.get('src'))
            if src is not None:
                candidates.append(src)
                if src.exists():
                    src_files.add(src)
                else:
                    missing.append((str(html.relative_to(ROOT)), str(src.relative_to(ROOT))))
            for url in srcset_urls(img.get('srcset')):
                p = local_file(url)
                if p is not None:
                    candidates.append(p)
                    if not p.exists():
                        missing.append((str(html.relative_to(ROOT)), str(p.relative_to(ROOT))))
            existing = [p for p in candidates if p.exists()]
            if existing:
                chosen_max_files.add(max(existing, key=lambda p: p.stat().st_size))
        src_bytes = sum(p.stat().st_size for p in src_files)
        estimated = sum(p.stat().st_size for p in chosen_max_files)
        rel = str(html.relative_to(ROOT))
        rows.append((estimated, src_bytes, html.stat().st_size, len(images), rel))
        if estimated > threshold:
            over.append((rel, estimated))
    rows.sort(reverse=True)
    print(f'Page-weight report — warning threshold: {args.warn_mb:.2f} MiB')
    print('estimated=max local src/srcset candidate per image; linked archival masters are excluded')
    for estimated, src_bytes, html_bytes, count, rel in rows:
        print(f'{rel}: images={count}, estimated={mib(estimated)}, src-only={mib(src_bytes)}, html={html_bytes / 1024:.1f} KiB')
    for rel, size in over:
        print(f'::warning file={rel}::Estimated image payload {mib(size)} exceeds {args.warn_mb:.2f} MiB review threshold')
    for rel, asset in sorted(set(missing)):
        print(f'::warning file={rel}::Referenced local image candidate not found: {asset}')
    return 1 if args.strict and over else 0

if __name__ == '__main__':
    raise SystemExit(main())
