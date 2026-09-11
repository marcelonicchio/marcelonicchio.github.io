#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

PT_1992 = '''<div class="phase" data-bio-key="music-limonada-1992" id="destemidos-limonadas-punkecas-1992"><div class="phase-year">1992</div><div><h3>Destemidos Limonadas &amp; Punkecas</h3><p>Em 1992, quando o <strong>Coitado do Próximo</strong> ainda estava no começo, um encontro casual ampliou o horizonte musical de Nicchio. Num dia em que havia cabulado aula e passava o tempo lendo jornal na banca de <strong>Márcio</strong>, amigo e dono da banca, Márcio chamou sua atenção para um homem que passava: <strong>Roberto Sassano</strong>, conhecido na cena como <strong>Roberto Limonada</strong> — ou simplesmente Limonada.</p><p>Roberto era proprietário de um <strong>posto Esso na Avenida Brás Leme</strong>, a mesma avenida onde Nicchio morava, e tocava com os <strong>Destemidos Limonadas &amp; Punkecas</strong>. A banda estava prestes a se apresentar no <strong>Café Piu-Piu</strong>, no Bexiga, e aparecia com foto em uma matéria do extinto <em>Diário de São Paulo</em>. Márcio abriu o jornal e apontou para a imagem: <q>Olha quem é esse cara, olha eles aqui.</q></p><p>Da conversa nasceu uma convivência musical. Nicchio ainda estava muito ligado ao thrash metal — com <strong>Ratos de Porão</strong> entre as referências mais presentes — enquanto Limonada tinha um conhecimento profundo de punk rock. <strong>Ramones</strong>, paixão que Nicchio já carregava, para Roberto era quase uma religião. Nicchio passou a frequentar o escritório do posto Esso para ouvir rádio e conversar sobre bandas, discos e a cena.</p><p>Em uma dessas noites, ao chegar em casa, ouviu da mãe que Roberto havia telefonado: uma entrevista com a banda seria exibida naquela noite no <strong>Jô Soares Onze e Meia</strong>, no SBT. Ver uma banda punk ligada a alguém que ele conhecia pessoalmente chegar à televisão nacional foi um divisor de águas. Um universo que parecia distante ganhou proximidade e possibilidade.</p><p>A relação não ficou restrita àquele encontro. Nos anos seguintes, Limonada se tornaria uma ponte recorrente entre amizade, repertório e circulação do Coitado do Próximo. Em 1994, levaria Nicchio até Kid Vinil na 97FM Rock; em <strong>9 de março de 1995</strong>, estaria entre as grandes surpresas do aniversário de 18 anos organizado pela mãe de Nicchio; em 1998, o Coitado do Próximo incorporaria ao repertório uma versão de <strong>“Ali Babão”</strong>, dos Destemidos Limonadas &amp; Punkecas; e, por volta de <strong>2000/2001</strong>, Limonada seria convidado a participar de um show da banda no <strong>Rock n Roll Bar</strong>, de Paulão de Carvalho, das Velhas Virgens. A música específica dessa participação ainda não está identificada no arquivo.</p><p>Segundo a lembrança de Nicchio, a versão de <strong>“Ali Babão”</strong> ficou entre as músicas mais aplaudidas da noite em que foi apresentada em 1998 e recebeu elogios do próprio <strong>Paulão de Carvalho</strong>, que também cantou naquela noite.</p></div></div>'''

EN_1992 = '''<div class="phase" data-bio-key="music-limonada-1992" id="destemidos-limonadas-punkecas-1992"><div class="phase-year">1992</div><div><h3>Destemidos Limonadas &amp; Punkecas</h3><p>In 1992, while <strong>Coitado do Próximo</strong> was still taking shape, a chance encounter widened Nicchio's musical horizon. One day, after skipping class and spending time reading newspapers at the newsstand run by his friend <strong>Márcio</strong>, Márcio called his attention to a man passing by: <strong>Roberto Sassano</strong>, known in the scene as <strong>Roberto Limonada</strong> — or simply Limonada.</p><p>Roberto owned an <strong>Esso gas station on Avenida Brás Leme</strong>, the same avenue where Nicchio lived, and played with <strong>Destemidos Limonadas &amp; Punkecas</strong>. The band was about to perform at <strong>Café Piu-Piu</strong> in Bexiga and had appeared with a photograph in the now-defunct <em>Diário de São Paulo</em>. Márcio opened the paper and pointed at the picture: <q>Look who this guy is — look, they're right here.</q></p><p>A musical friendship grew out of that conversation. Nicchio was still strongly connected to thrash metal — with <strong>Ratos de Porão</strong> among his most immediate references — while Limonada had a deep knowledge of punk rock. <strong>Ramones</strong>, already a passion for Nicchio, were almost a religion to Roberto. Nicchio began spending time in the Esso station office listening to the radio and talking about bands, records and the scene.</p><p>One evening, when he got home, his mother told him Roberto had called: an interview with the band would air that night on <strong>Jô Soares Onze e Meia</strong> on SBT. Seeing a punk band connected to someone he actually knew reach national television became a turning point. A world that had seemed distant suddenly felt close and possible.</p><p>The relationship did not end with that encounter. Over the following years, Limonada became a recurring bridge between friendship, repertoire and the circulation of Coitado do Próximo. In 1994, he would take Nicchio to meet Kid Vinil at 97FM Rock; on <strong>March 9, 1995</strong>, he would be among the biggest surprises at Nicchio's 18th-birthday party organized by his mother; in 1998, Coitado do Próximo would add a version of <strong>“Ali Babão”</strong>, by Destemidos Limonadas &amp; Punkecas, to its repertoire; and around <strong>2000/2001</strong>, Limonada would be invited to join the band onstage at the <strong>Rock n Roll Bar</strong>, associated with Paulão de Carvalho of Velhas Virgens. The specific song from that guest appearance has not yet been identified in the archive.</p><p>According to Nicchio's recollection, the band's version of <strong>“Ali Babão”</strong> was among the most applauded songs of the night when it was performed in 1998 and drew praise from <strong>Paulão de Carvalho</strong>, who also sang that night.</p></div></div>'''

PT_1994 = '''<div data-bio-key="music-coitado-1994"><p>Em 1994, <strong>Roberto Limonada</strong> levou Nicchio à <strong>97FM Rock</strong> e o apresentou a <strong>Kid Vinil</strong>. Os dois foram entrevistados no programa de Kid e, naquela ocasião, Nicchio levou a primeira demo-tape do <strong>Coitado do Próximo</strong>, gravada no <strong>Estúdio Anonimato</strong>. Foi a primeira vez que <strong>“Mulher SP”</strong> foi apresentada no rádio.</p><p>Em <strong>9 de março de 1995</strong>, quando Nicchio completou 18 anos, Limonada apareceu entre as dezenas de convidados de uma festa surpresa organizada por sua mãe, reunindo familiares, vizinhos, amigos de infância, integrantes da banda e novas amizades. A presença de Limonada marcou a passagem de uma referência musical conhecida em 1992 para uma amizade já incorporada à vida pessoal.</p></div>'''

EN_1994 = '''<div data-bio-key="music-coitado-1994"><p>In 1994, <strong>Roberto Limonada</strong> took Nicchio to <strong>97FM Rock</strong> and introduced him to <strong>Kid Vinil</strong>. The two were interviewed on Kid's program and, on that occasion, Nicchio brought Coitado do Próximo's first demo tape, recorded at <strong>Estúdio Anonimato</strong>. It was the first time <strong>“Mulher SP”</strong> was played on the radio.</p><p>On <strong>March 9, 1995</strong>, when Nicchio turned 18, Limonada was among the dozens of guests at a surprise party organized by Nicchio's mother, bringing together relatives, neighbors, childhood friends, band members and newer friendships. Limonada's presence marked the transition from a musical reference first met in 1992 to a friendship already woven into Nicchio's personal life.</p></div>'''


def replace_phase(text: str, key: str, replacement: str) -> str:
    pattern = re.compile(rf'<div class="phase" data-bio-key="{re.escape(key)}".*?(?=\n<div class="phase"|\n</div></section>)', re.S)
    new, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"phase {key}: matched {count}")
    return new


def replace_subunit(text: str, key: str, replacement: str) -> str:
    pattern = re.compile(rf'<div data-bio-key="{re.escape(key)}">.*?</div>', re.S)
    new, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"subunit {key}: matched {count}")
    return new

for rel, phase, subunit in [
    ('pt/musica/index.html', PT_1992, PT_1994),
    ('en/music/index.html', EN_1992, EN_1994),
]:
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    text = replace_phase(text, 'music-limonada-1992', phase)
    text = replace_subunit(text, 'music-coitado-1994', subunit)
    path.write_text(text, encoding='utf-8')

subprocess.run(['python', 'tools/sync_full_biography.py'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--accept', 'music-limonada-1992'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--accept', 'music-coitado-1994'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/build_sitemap.py'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/sync_full_biography.py', '--check'], cwd=ROOT, check=True)
subprocess.run(['python', 'tools/editorial_parity.py', '--check'], cwd=ROOT, check=True)
