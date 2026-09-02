#!/usr/bin/env python3
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
errors = []
def text(p): return (ROOT / p).read_text(encoding='utf-8')
pairs = [
    ('pt/comunicacao/index.html', ['bbs','radio','homens','cinema','folha','sinal-verde','meia-noite','arquiteto','autopsia','temas','nomes'], 'Cultura & Audiovisual'),
    ('en/communication/index.html', ['bbs','radio','homens','film','folha','sinal-verde','meia-noite','architect','autopsia','themes','names'], 'Culture & Audiovisual'),
]
for path, ids, title in pairs:
    t = text(path)
    if f'<h1>{title}</h1>' not in t: errors.append(f'{path}: combined H1 missing')
    pos = []
    for item in ids:
        p = t.find(f'id="{item}"')
        if p < 0: errors.append(f'{path}: missing #{item}')
        pos.append(p)
    if all(p >= 0 for p in pos) and pos != sorted(pos): errors.append(f'{path}: chronology/order drift')
for path, target, title in [
    ('pt/audiovisual/index.html','/pt/comunicacao/','Cultura & Audiovisual'),
    ('en/audiovisual/index.html','/en/communication/','Culture & Audiovisual'),
]:
    t = text(path)
    for token in ['noindex,follow', f'url={target}', f'https://marcelonicchio.github.io{target}', f"location.replace('{target}')"]:
        if token not in t: errors.append(f'{path}: stub missing {token}')
    if f'<h1>{title}</h1>' not in t: errors.append(f'{path}: stub title missing')
entries = text('data/entries.json'); full = text('data/full_biography.json'); galleries = text('data/galleries.json')
for name, t in [('entries',entries),('full biography',full),('galleries',galleries)]:
    if '"path": "pt/audiovisual/index.html"' in t or '"path": "en/audiovisual/index.html"' in t or '"pt/audiovisual/index.html"' in t or '"en/audiovisual/index.html"' in t:
        errors.append(f'{name}: legacy Audiovisual is still an active data target')
if '"domain": "audiovisual"' in entries or '"domain": "audiovisual"' in full:
    errors.append('registry/manifest still exposes audiovisual as independent domain')
for path in [*ROOT.glob('pt/**/*.html'), *ROOT.glob('en/**/*.html'), ROOT/'pt/index.html', ROOT/'en/index.html']:
    if path.as_posix().endswith('/audiovisual/index.html'):
        continue
    t = path.read_text(encoding='utf-8')
    nav = re.search(r'<nav class="nav-links"[^>]*>(.*?)</nav>', t, re.S)
    if nav and ('href="/pt/audiovisual/"' in nav.group(1) or 'href="/en/audiovisual/"' in nav.group(1)):
        errors.append(f'{path.relative_to(ROOT)}: legacy Audiovisual remains in top navigation')
if errors:
    print('Media/Culture fusion audit failed:')
    for e in errors: print(' -', e)
    sys.exit(1)
print('Media/Culture fusion audit passed.')
