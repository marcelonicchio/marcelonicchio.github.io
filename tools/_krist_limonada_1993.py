#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

replacements = {
    'pt/musica/index.html': [
        (
            'A relação não ficou restrita àquele encontro. Nos anos seguintes, Limonada se tornaria uma ponte recorrente entre amizade, repertório e circulação do Coitado do Próximo. Em 1994, levaria Nicchio até Kid Vinil na 97FM Rock;',
            'A relação não ficou restrita àquele encontro. Nos anos seguintes, Limonada se tornaria uma ponte recorrente entre amizade, repertório e circulação do Coitado do Próximo. Já em <strong>1993</strong>, nos ensaios e nos shows, o Coitado do Próximo passou a tocar <strong>“Ela Só Gosta de Pizza”</strong>, dos Destemidos Limonadas &amp; Punkecas. Em 1994, Limonada levaria Nicchio até Kid Vinil na 97FM Rock;'
        ),
        (
            'Os shows eram marcados em pequenas casas e bares, com repertório que mesclava músicas autorais e covers de Ramones, 365, Magazine, Garotos Podres, The Clash e Misfits, entre outros.</p>',
            'Os shows eram marcados em pequenas casas e bares, com repertório que mesclava músicas autorais e covers de Ramones, 365, Magazine, Garotos Podres, The Clash e Misfits, entre outros. Entre as versões daquele período estava também <strong>“Ela Só Gosta de Pizza”</strong>, dos <strong>Destemidos Limonadas &amp; Punkecas</strong>, incorporada ao repertório após a aproximação com Roberto Limonada.</p>'
        ),
    ],
    'en/music/index.html': [
        (
            'The relationship did not end with that encounter. Over the following years, Limonada became a recurring bridge between friendship, repertoire and the circulation of Coitado do Próximo. In 1994, he would take Nicchio to meet Kid Vinil at 97FM Rock;',
            'The relationship did not end with that encounter. Over the following years, Limonada became a recurring bridge between friendship, repertoire and the circulation of Coitado do Próximo. By <strong>1993</strong>, in rehearsals and live shows, Coitado do Próximo had begun playing <strong>“Ela Só Gosta de Pizza”</strong>, by Destemidos Limonadas &amp; Punkecas. In 1994, Limonada would take Nicchio to meet Kid Vinil at 97FM Rock;'
        ),
        (
            'Shows were booked in small venues and bars, with sets combining original songs and covers of bands such as Ramones, 365, Magazine, Garotos Podres, The Clash and Misfits, among others.</p>',
            'Shows were booked in small venues and bars, with sets combining original songs and covers of bands such as Ramones, 365, Magazine, Garotos Podres, The Clash and Misfits, among others. The repertoire from that period also included <strong>“Ela Só Gosta de Pizza”</strong>, by <strong>Destemidos Limonadas &amp; Punkecas</strong>, added after the connection with Roberto Limonada.</p>'
        ),
    ],
}

for rel, pairs in replacements.items():
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if old not in text:
            raise RuntimeError(f'{rel}: expected text not found')
        text = text.replace(old, new, 1)
    path.write_text(text, encoding='utf-8')

subprocess.run(['python', 'tools/sync_full_biography.py'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--accept', 'music-limonada-1992'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/build_sitemap.py'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/sync_full_biography.py', '--check'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--check'], cwd=ROOT, check=True)
