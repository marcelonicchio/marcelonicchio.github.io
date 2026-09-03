#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc=["\']([^"\']+)["\']', re.IGNORECASE)
ATTR_RE = lambda name: re.compile(rf'\b{name}=["\']([^"\']+)["\']', re.IGNORECASE)
RASTER = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


def dims_for(src: str) -> tuple[int, int] | None:
    if not src.startswith('/'):
        return None
    p = ROOT / src.lstrip('/')
    if p.suffix.lower() not in RASTER or not p.exists():
        return None
    try:
        with Image.open(p) as im:
            return im.width, im.height
    except Exception:
        return None


def patch_img_tag(tag: str) -> str:
    m = SRC_RE.search(tag)
    if not m:
        return tag
    dims = dims_for(m.group(1))
    if not dims:
        return tag
    w, h = dims
    has_w = ATTR_RE('width').search(tag)
    has_h = ATTR_RE('height').search(tag)
    if has_w and has_h:
        return tag
    attrs = ''
    if not has_w:
        attrs += f' width="{w}"'
    if not has_h:
        attrs += f' height="{h}"'
    if tag.endswith('/>'):
        return tag[:-2] + attrs + '/>'
    return tag[:-1] + attrs + '>'


def patch_markup(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    new = IMG_RE.sub(lambda m: patch_img_tag(m.group(0)), text)
    if new == text:
        return False
    path.write_text(new, encoding='utf-8')
    return True


def patch_all_markup() -> list[str]:
    changed=[]
    candidates=[]
    candidates += list(ROOT.glob('*.html'))
    candidates += list((ROOT/'pt').rglob('*.html'))
    candidates += list((ROOT/'en').rglob('*.html'))
    candidates += list((ROOT/'content').rglob('*.inc'))
    for p in candidates:
        if patch_markup(p):
            changed.append(p.relative_to(ROOT).as_posix())
    return changed


def patch_reader_registry() -> bool:
    p=ROOT/'data/entries.json'
    data=json.loads(p.read_text(encoding='utf-8'))
    changed=False
    for entry in data.get('entries',[]):
        for preview in (entry.get('reader_preview') or {}).values():
            if not isinstance(preview, dict) or not preview.get('image'):
                continue
            dims=dims_for(preview['image'])
            if not dims:
                continue
            w,h=dims
            if preview.get('width') != w:
                preview['width']=w; changed=True
            if preview.get('height') != h:
                preview['height']=h; changed=True
    if changed:
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    return changed


def patch_reader_js() -> bool:
    p=ROOT/'assets/js/reader-disclosure.js'
    text=p.read_text(encoding='utf-8')
    old="""          image.src = readerPreview.image;
          image.alt = readerPreview.alt || '';
          image.loading = 'lazy';
          image.decoding = 'async';
"""
    new="""          image.src = readerPreview.image;
          image.alt = readerPreview.alt || '';
          if (readerPreview.width) image.width = readerPreview.width;
          if (readerPreview.height) image.height = readerPreview.height;
          image.loading = 'lazy';
          image.decoding = 'async';
"""
    if new in text:
        return False
    if old not in text:
        raise RuntimeError('Reader preview image block not found')
    p.write_text(text.replace(old,new,1),encoding='utf-8')
    return True


def patch_runtime_gate() -> bool:
    p=ROOT/'tools/smoke_runtime_performance.js'
    text=p.read_text(encoding='utf-8')
    old="""  if (initial.images.missingIntrinsic > 0) warn(config.label, `${initial.images.missingIntrinsic} image(s) lack explicit width/height attributes.`);

  await expandAndScroll(page);
"""
    new="""  assert(initial.images.missingIntrinsic === 0, `${config.label}: ${initial.images.missingIntrinsic} image(s) lack explicit width/height attributes on initial render`);

  await expandAndScroll(page);
"""
    if old in text:
        text=text.replace(old,new,1)
    elif new not in text:
        raise RuntimeError('Runtime intrinsic warning block not found')
    old2="""  assert(afterScroll.images.loaded >= initial.images.loaded, `${config.label}: loaded image count regressed after scroll`);
  assert(afterDecode.failures === 0, `${config.label}: ${afterDecode.failures} local image decode failure(s) after scroll`);
"""
    new2="""  assert(afterScroll.images.loaded >= initial.images.loaded, `${config.label}: loaded image count regressed after scroll`);
  assert(afterScroll.images.missingIntrinsic === 0, `${config.label}: ${afterScroll.images.missingIntrinsic} image(s) lack explicit width/height attributes after full expansion/scroll`);
  assert(afterDecode.failures === 0, `${config.label}: ${afterDecode.failures} local image decode failure(s) after scroll`);
"""
    if old2 in text:
        text=text.replace(old2,new2,1)
    elif new2 not in text:
        raise RuntimeError('Runtime post-scroll assertion block not found')
    p.write_text(text,encoding='utf-8')
    return True


def patch_gallery_palette() -> bool:
    p=ROOT/'tools/build_gallery_media.py'
    text=p.read_text(encoding='utf-8')
    old="""                image = ImageOps.exif_transpose(opened)
                source_w, source_h = image.size
                working = image.convert("RGB")
"""
    new="""                image = ImageOps.exif_transpose(opened)
                source_w, source_h = image.size
                # Pillow warns when palette transparency stored as bytes is converted
                # directly to RGB. Normalize through RGBA first so transparent palette
                # sources are handled deterministically before WebP conversion.
                if image.mode == "P" and "transparency" in image.info:
                    image = image.convert("RGBA")
                working = image.convert("RGB")
"""
    if new in text:
        return False
    if old not in text:
        raise RuntimeError('Gallery conversion block not found')
    p.write_text(text.replace(old,new,1),encoding='utf-8')
    return True


def patch_workflow(path: str, replacements: list[tuple[str,str]]) -> bool:
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    new=text
    for old,repl in replacements:
        new=new.replace(old,repl)
    if new==text:
        return False
    p.write_text(new,encoding='utf-8')
    return True


def ensure_dimension_audit_step() -> bool:
    p=ROOT/'.github/workflows/site-audit.yml'
    text=p.read_text(encoding='utf-8')
    marker="""      - name: Audit gallery registry and rendering
        run: python tools/audit_galleries.py
"""
    block=marker+"""      - name: Audit intrinsic image dimensions
        run: python tools/audit_image_dimensions.py
"""
    if 'Audit intrinsic image dimensions' in text:
        return False
    if marker not in text:
        raise RuntimeError('Gallery audit workflow anchor not found')
    p.write_text(text.replace(marker,block,1),encoding='utf-8')
    return True


def main() -> int:
    changed=patch_all_markup()
    if patch_reader_registry(): changed.append('data/entries.json')
    if patch_reader_js(): changed.append('assets/js/reader-disclosure.js')
    if patch_runtime_gate(): changed.append('tools/smoke_runtime_performance.js')
    if patch_gallery_palette(): changed.append('tools/build_gallery_media.py')
    if patch_workflow('.github/workflows/site-audit.yml', [
        ('actions/checkout@v4','actions/checkout@v7'),
        ('actions/setup-python@v5','actions/setup-python@v7'),
        ('actions/setup-node@v4','actions/setup-node@v7'),
        ("node-version: '22'","node-version: '24'"),
    ]): changed.append('.github/workflows/site-audit.yml')
    if ensure_dimension_audit_step(): changed.append('.github/workflows/site-audit.yml')
    if patch_workflow('.github/workflows/media-build.yml', [
        ('actions/checkout@v4','actions/checkout@v7'),
        ('actions/setup-python@v5','actions/setup-python@v7'),
    ]): changed.append('.github/workflows/media-build.yml')
    print(f'Initial closeout patch touched {len(changed)} files.')
    for item in sorted(set(changed)): print(' -',item)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
