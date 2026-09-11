#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.youtube.com/watch?v=_LBHqq8xF1c"

patches = {
    'pt/musica/index.html': (
        '<p>Roberto era proprietário de um <strong>posto Esso na Avenida Brás Leme</strong>, a mesma avenida onde Nicchio morava, e tocava com os <strong>Destemidos Limonadas &amp; Punkecas</strong>. A banda estava prestes a se apresentar no <strong>Café Piu-Piu</strong>, no Bexiga, e aparecia com foto em uma matéria do extinto <em>Diário de São Paulo</em>. Márcio abriu o jornal e apontou para a imagem: <q>Olha quem é esse cara, olha eles aqui.</q></p>',
        '<p>Roberto era proprietário de um <strong>posto Esso na Avenida Brás Leme</strong>, a mesma avenida onde Nicchio morava, e tocava com os <strong>Destemidos Limonadas &amp; Punkecas</strong>. A banda estava prestes a se apresentar no <strong>Café Piu-Piu</strong>, no Bexiga, e aparecia com foto em uma matéria do extinto <em>Diário de São Paulo</em>. Márcio abriu o jornal e apontou para a imagem: <q>Olha quem é esse cara, olha eles aqui.</q></p><p>O próprio posto também virou matéria-prima para o humor da banda em <strong>“O Posto”</strong>, um rock de duplo sentido registrado em apresentação na TV Cultura de São Paulo.</p><div class="evidence-links inline-links"><a href="' + URL + '" target="_blank" rel="noopener noreferrer">Assistir “O Posto” · TV Cultura ↗</a></div>'
    ),
    'en/music/index.html': (
        '<p>Roberto owned an <strong>Esso gas station on Avenida Brás Leme</strong>, the same avenue where Nicchio lived, and played with <strong>Destemidos Limonadas &amp; Punkecas</strong>. The band was about to perform at <strong>Café Piu-Piu</strong> in Bexiga and had appeared with a photograph in the now-defunct <em>Diário de São Paulo</em>. Márcio opened the paper and pointed at the picture: <q>Look who this guy is — look, they\'re right here.</q></p>',
        '<p>Roberto owned an <strong>Esso gas station on Avenida Brás Leme</strong>, the same avenue where Nicchio lived, and played with <strong>Destemidos Limonadas &amp; Punkecas</strong>. The band was about to perform at <strong>Café Piu-Piu</strong> in Bexiga and had appeared with a photograph in the now-defunct <em>Diário de São Paulo</em>. Márcio opened the paper and pointed at the picture: <q>Look who this guy is — look, they\'re right here.</q></p><p>The gas station itself also became material for the band\'s humor in <strong>“O Posto”</strong>, a double-entendre rock song preserved in a performance recorded by TV Cultura in São Paulo.</p><div class="evidence-links inline-links"><a href="' + URL + '" target="_blank" rel="noopener noreferrer">Watch “O Posto” · TV Cultura ↗</a></div>'
    ),
}

for rel, (old, new) in patches.items():
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'{rel}: target paragraph not found')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')

subprocess.run(['python', 'tools/sync_full_biography.py'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--accept', 'music-limonada-1992'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/build_sitemap.py'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/sync_full_biography.py', '--check'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--check'], cwd=ROOT, check=True)
