#!/usr/bin/env python3
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dave_music_flatten as m

for lang, path, sid in [
    ('pt', m.PT_PATH, 'palcos'),
    ('en', m.EN_PATH, 'stages'),
]:
    text = path.read_text(encoding='utf-8')
    _, _, block = m.find_section_by_id(text, sid)
    _, inner, _ = m.phase_list_inner(block)
    children, residue = m.direct_phase_children(inner)
    print(f'{lang}: {len(children)} children residue={residue.strip()!r}')
    for i, frag in enumerate(children, 1):
        opening = re.match(r'\s*<(div|section)\b([^>]*)>', frag, flags=re.I|re.S)
        root = opening.group(0).replace('\n',' ')[:260] if opening else 'NO ROOT'
        try:
            key = m.key_of(frag)
        except Exception:
            key = 'MISSING'
        try:
            title = m.heading_text(frag)
        except Exception:
            title = 'NO HEADING'
        print(f'{i:02d} key={key} title={title!r} root={root!r}')
