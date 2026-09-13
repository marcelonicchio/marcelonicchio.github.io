#!/usr/bin/env python3
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASE = Path('assets/archive/music/coitado-do-proximo/1992-destemidos-limonadas-roberto-limonada')
ABS_BASE = ROOT / BASE
GAL = ABS_BASE / 'galeria'
GALLERY_ID = 'destemidos-limonadas-1992'

THREAD_1 = 'destemidoslimonadas_thread01.jpg'
THREAD_2 = 'destemidoslimonadas_thread02.jpg'


def dims(rel):
    with Image.open(ROOT / rel) as im:
        im = ImageOps.exif_transpose(im)
        return im.size


def fig(lang, filename, kind):
    rel = '/' + (BASE / filename).as_posix()
    w, h = dims(BASE / filename)
    if kind == 1 and lang == 'pt':
        aria = 'Abrir imagem restaurada de Roberto Limonada no Jô Soares Onze e Meia em tamanho maior'
        alt = 'Roberto Limonada cantando no Jô Soares Onze e Meia, SBT, em junho de 1992. Imagem restaurada por IA.'
        strong = 'Roberto Limonada · Jô Soares Onze e Meia · SBT · jun. 1992.'
        note = 'Imagem restaurada por IA a partir do registro original em vídeo.'
        open_label = 'Abrir imagem em tamanho maior ↗'
    elif kind == 1:
        aria = 'Open the restored image of Roberto Limonada on Jô Soares Onze e Meia at full size'
        alt = 'Roberto Limonada performing on Jô Soares Onze e Meia, SBT, in June 1992. AI-restored image.'
        strong = 'Roberto Limonada · Jô Soares Onze e Meia · SBT · Jun. 1992.'
        note = 'AI restoration made from the original video record.'
        open_label = 'Open image at full size ↗'
    elif lang == 'pt':
        aria = 'Abrir foto de Marcelo Nicchio e Roberto Limonada cerca de 25 anos depois em tamanho maior'
        alt = 'Marcelo Nicchio e Roberto Limonada juntos cerca de 25 anos depois do encontro de 1992.'
        strong = 'Marcelo Nicchio e Roberto Limonada · cerca de 25 anos depois.'
        note = 'A amizade iniciada em 1992 atravessou décadas para além da relação musical.'
        open_label = 'Abrir imagem em tamanho maior ↗'
    else:
        aria = 'Open the photo of Marcelo Nicchio and Roberto Limonada about 25 years later at full size'
        alt = 'Marcelo Nicchio and Roberto Limonada together about 25 years after their 1992 meeting.'
        strong = 'Marcelo Nicchio and Roberto Limonada · about 25 years later.'
        note = 'The friendship that began in 1992 continued for decades beyond the musical connection.'
        open_label = 'Open image at full size ↗'
    return (f'<figure class="thread-media thread-media--linked"><a aria-label="{aria}" href="{rel}" rel="noopener noreferrer" target="_blank">'
            f'<img alt="{alt}" decoding="async" loading="lazy" src="{rel}" width="{w}" height="{h}"/></a>'
            f'<figcaption><strong>{strong}</strong><span class="thread-media-note">{note}</span>'
            f'<a class="thread-media-open" href="{rel}" rel="noopener noreferrer" target="_blank">{open_label}</a></figcaption></figure>')


def block(lang):
    t1 = fig(lang, THREAD_1, 1)
    t2 = fig(lang, THREAD_2, 2)
    if lang == 'pt':
        return f'''<div class="phase" data-bio-key="music-limonada-1992" id="destemidos-limonadas-punkecas-1992"><div class="phase-year">1992</div><div><h3>Destemidos Limonadas &amp; Punkecas / Roberto Limonada</h3><p>Em 1992, quando o <strong>Coitado do Próximo</strong> ainda estava no começo, um encontro casual ampliou o horizonte musical de Nicchio. Num dia em que havia cabulado aula e passava o tempo lendo jornal na banca de <strong>Márcio</strong>, amigo e dono da banca, Márcio chamou sua atenção para um homem que passava: <strong>Roberto Sassano</strong>, conhecido na cena como <strong>Roberto Limonada</strong> — ou simplesmente Limonada.</p><p>Nicchio tinha entre 15 e 16 anos e atravessava um período de desorientação pessoal depois da separação dos pais. Já tocava e começava a compor, mas ainda procurava uma identidade musical própria. A aproximação com Roberto passou a representar algo maior do que conhecer um músico mais experiente: abriu uma possibilidade concreta de pertencimento, repertório e vida ligada ao punk rock.</p><p>Roberto era proprietário de um <strong>posto Esso na Avenida Brás Leme</strong>, a mesma avenida onde Nicchio morava, e tocava com os <strong>Destemidos Limonadas &amp; Punkecas</strong>. A banda estava prestes a se apresentar no <strong>Café Piu Piu</strong>, no Bexiga, e aparecia com foto em uma matéria do extinto <em>Diário de São Paulo</em>. Márcio abriu o jornal e apontou para a imagem: <q>Olha quem é esse cara, olha eles aqui.</q></p><p>O próprio posto também virou matéria-prima para o humor da banda em <strong>“O Posto”</strong>, um rock de duplo sentido registrado em apresentação na TV Cultura de São Paulo.</p><div class="evidence-links inline-links"><a href="https://www.youtube.com/watch?v=_LBHqq8xF1c" target="_blank" rel="noopener noreferrer">Assistir “O Posto” · TV Cultura ↗</a></div><p>Da conversa nasceu uma amizade alimentada principalmente por <strong>Ramones</strong> e punk rock. Nicchio ainda vinha de uma escuta muito marcada pelo thrash metal — com <strong>Ratos de Porão</strong> entre as referências mais presentes — enquanto Roberto possuía um conhecimento profundo da história e da cena punk. Ramones, paixão que Nicchio já carregava, para Limonada era quase uma religião. Nicchio passou a frequentar o escritório do posto para ouvir rádio e conversar sobre bandas, discos, shows e a cena paulistana.</p><p>Em <strong>junho de 1992</strong>, Roberto telefonou para avisar que os Destemidos seriam entrevistados naquela noite no <strong>Jô Soares Onze e Meia</strong>, no SBT. Para um adolescente que ainda tentava encontrar seu lugar, ver na televisão nacional uma banda punk ligada a alguém que havia acabado de entrar em sua vida teve um efeito decisivo: um universo antes distante ganhou proximidade e possibilidade.</p>{t1}<p>Na mesma passagem pelo programa, os Destemidos apresentaram <strong>“Ela Só Gosta de Pizza”</strong>, música que já começava a ligar a trajetória da banda à de Kid Vinil.</p><div class="evidence-links inline-links"><a href="https://www.youtube.com/watch?v=giklH5greAc" target="_blank" rel="noopener noreferrer">Assistir “Ela Só Gosta de Pizza” · Jô Soares Onze e Meia · jun. 1992 ↗</a></div><p>Os Destemidos já mantinham também uma ligação com <strong>Kid Vinil</strong>. O baixista da banda era amigo de longa data de Kid, que enxergou em <strong>“Ela Só Gosta de Pizza”</strong> uma música com força para integrar sua retomada artística. A canção passou ao repertório de Kid Vinil e Verminose e se tornaria o elo mais visível entre as duas bandas. Essa história ganharia um capítulo próprio em 1993, quando Roberto levaria Nicchio a um show de Kid no Café Piu Piu.</p><p>A convivência de Nicchio com os Destemidos continuou em ensaios e shows, inclusive no circuito do Aeroanta. A influência também atravessou diretamente o repertório do <strong>Coitado do Próximo</strong>: a partir de <strong>1993</strong>, a banda passou a tocar <strong>“Ela Só Gosta de Pizza”</strong> em ensaios e apresentações. Em <strong>9 de março de 1995</strong>, Limonada esteve entre as grandes surpresas da festa de 18 anos de Nicchio; em 1998, o Coitado incorporou uma versão de <strong>“Ali Babão”</strong>, dos Destemidos, que segundo a lembrança de Nicchio ficou entre as músicas mais aplaudidas daquela noite e recebeu elogios de <strong>Paulão de Carvalho</strong>; e, por volta de <strong>2000/2001</strong>, Roberto foi convidado a participar de um show do Coitado no <strong>Rock n Roll Bar</strong>, ligado a Paulão e às Velhas Virgens. A música específica dessa participação ainda não está identificada no arquivo.</p>{t2}<!-- gallery:{GALLERY_ID} --><div class="evidence-links inline-links"><a href="https://www.youtube.com/watch?v=OUBzN8HYuVA" target="_blank" rel="noopener noreferrer">Entrevista no Jô · Parte 1 ↗</a><a href="https://www.youtube.com/watch?v=PyTBtNAU3RE" target="_blank" rel="noopener noreferrer">Entrevista no Jô · Parte 2 ↗</a><a href="https://www.youtube.com/watch?v=wzsS-G6ywqc" target="_blank" rel="noopener noreferrer">“Herói do Brasil” · participação de Kid Vinil ↗</a></div></div></div>'''
    return f'''<div class="phase" data-bio-key="music-limonada-1992" id="destemidos-limonadas-punkecas-1992"><div class="phase-year">1992</div><div><h3>Destemidos Limonadas &amp; Punkecas / Roberto Limonada</h3><p>In 1992, while <strong>Coitado do Próximo</strong> was still taking shape, a chance encounter widened Nicchio's musical horizon. One day, after skipping class and spending time reading newspapers at the newsstand run by his friend <strong>Márcio</strong>, Márcio called his attention to a man passing by: <strong>Roberto Sassano</strong>, known in the scene as <strong>Roberto Limonada</strong> — or simply Limonada.</p><p>Nicchio was between 15 and 16 years old and going through a period of personal disorientation after his parents' separation. He was already playing music and beginning to write songs, but he had not yet found a musical identity of his own. Becoming close to Roberto came to mean more than simply meeting a more experienced musician: it opened up a concrete possibility of belonging, repertoire and a life connected to punk rock.</p><p>Roberto owned an <strong>Esso gas station on Avenida Brás Leme</strong>, the same avenue where Nicchio lived, and played with <strong>Destemidos Limonadas &amp; Punkecas</strong>. The band was about to perform at <strong>Café Piu Piu</strong> in Bexiga and had appeared with a photograph in the now-defunct <em>Diário de São Paulo</em>. Márcio opened the paper and pointed at the picture: <q>Look who this guy is — look, they're right here.</q></p><p>The gas station itself also became material for the band's humor in <strong>“O Posto”</strong>, a double-entendre rock song preserved in a performance recorded by TV Cultura in São Paulo.</p><div class="evidence-links inline-links"><a href="https://www.youtube.com/watch?v=_LBHqq8xF1c" target="_blank" rel="noopener noreferrer">Watch “O Posto” · TV Cultura ↗</a></div><p>A friendship grew out of that conversation, held together above all by <strong>Ramones</strong> and punk rock. Nicchio still came from listening habits strongly shaped by thrash metal — with <strong>Ratos de Porão</strong> among his closest references — while Roberto had a deep knowledge of punk history and the local scene. Ramones, already a passion for Nicchio, were almost a religion to Limonada. Nicchio began spending time in the gas station office listening to the radio and talking about bands, records, shows and the São Paulo scene.</p><p>In <strong>June 1992</strong>, Roberto called to say that the Destemidos would be interviewed that night on <strong>Jô Soares Onze e Meia</strong> on SBT. For a teenager still trying to find his place, seeing on national television a punk band connected to someone who had just entered his life had a decisive effect: a world that had seemed distant suddenly felt close and possible.</p>{t1}<p>During the same appearance, the Destemidos performed <strong>“Ela Só Gosta de Pizza”</strong>, the song that was already beginning to connect the band's trajectory with Kid Vinil's.</p><div class="evidence-links inline-links"><a href="https://www.youtube.com/watch?v=giklH5greAc" target="_blank" rel="noopener noreferrer">Watch “Ela Só Gosta de Pizza” · Jô Soares Onze e Meia · Jun. 1992 ↗</a></div><p>The Destemidos already had a connection with <strong>Kid Vinil</strong>. The band's bassist was a longtime friend of Kid, who saw in <strong>“Ela Só Gosta de Pizza”</strong> a song strong enough to become part of his artistic comeback. The song entered the repertoire of Kid Vinil e Verminose and would become the most visible link between the two bands. That story would gain a chapter of its own in 1993, when Roberto took Nicchio to a Kid Vinil show at Café Piu Piu.</p><p>Nicchio's contact with the Destemidos continued through rehearsals and shows, including the Aeroanta circuit. Their influence also crossed directly into the repertoire of <strong>Coitado do Próximo</strong>: starting in <strong>1993</strong>, the band began playing <strong>“Ela Só Gosta de Pizza”</strong> in rehearsals and live performances. On <strong>March 9, 1995</strong>, Limonada was among the biggest surprises at Nicchio's 18th-birthday party; in 1998, Coitado added a version of <strong>“Ali Babão”</strong>, by the Destemidos, which Nicchio remembers as one of the most applauded songs of that night and as drawing praise from <strong>Paulão de Carvalho</strong>; and around <strong>2000/2001</strong>, Roberto was invited to join Coitado onstage at the <strong>Rock n Roll Bar</strong>, associated with Paulão and Velhas Virgens. The specific song from that guest appearance has not yet been identified in the archive.</p>{t2}<!-- gallery:{GALLERY_ID} --><div class="evidence-links inline-links"><a href="https://www.youtube.com/watch?v=OUBzN8HYuVA" target="_blank" rel="noopener noreferrer">Jô interview · Part 1 ↗</a><a href="https://www.youtube.com/watch?v=PyTBtNAU3RE" target="_blank" rel="noopener noreferrer">Jô interview · Part 2 ↗</a><a href="https://www.youtube.com/watch?v=wzsS-G6ywqc" target="_blank" rel="noopener noreferrer">“Herói do Brasil” · featuring Kid Vinil ↗</a></div></div></div>'''


def replace_entry(path, lang):
    text = path.read_text(encoding='utf-8')
    start_token = '<div class="phase" data-bio-key="music-limonada-1992"'
    next_token = '\n<div class="phase" data-bio-key="music-kid-vinil-1993"'
    start = text.index(start_token)
    end = text.index(next_token, start)
    path.write_text(text[:start] + block(lang) + text[end:], encoding='utf-8')


def register_gallery():
    p = ROOT / 'data/galleries.json'
    data = json.loads(p.read_text(encoding='utf-8'))
    ia = sorted(x.name for x in GAL.glob('destemidoslimonadas*_IA_300Kb.jpg'))
    originals = sorted(x.name for x in GAL.glob('destemidoslimonadasok_*.jpg'))
    if len(ia) != 5 or len(originals) != 14:
        raise RuntimeError(f'Expected 5 AI restorations + 14 originals; found {len(ia)} + {len(originals)}')
    items = []
    for idx, name in enumerate(ia + originals, 1):
        is_ai = idx <= 5
        if is_ai:
            pt = f'Destemidos Limonadas & Punkecas · restauração por IA a partir de registro original em vídeo · imagem {idx}.'
            en = f'Destemidos Limonadas & Punkecas · AI restoration from an original video record · image {idx}.'
        else:
            n = idx - 5
            pt = f'Destemidos Limonadas & Punkecas · frame original do conjunto de registros do Jô Soares Onze e Meia e da TV Cultura · imagem {n}.'
            en = f'Destemidos Limonadas & Punkecas · original frame from the Jô Soares Onze e Meia and TV Cultura video records · image {n}.'
        items.append({'id': f'{idx:02d}', 'source': name, 'caption': {'pt': pt, 'en': en}})
    gallery = {
        'id': GALLERY_ID,
        'sourceRoot': BASE.joinpath('galeria').as_posix(),
        'targets': {'pt': ['pt/musica/index.html'], 'en': ['en/music/index.html']},
        'title': {'pt': 'Arquivo visual — Jô Soares e TV Cultura', 'en': 'Visual archive — Jô Soares and TV Cultura'},
        'items': items,
    }
    galleries = data['galleries']
    existing = next((i for i,g in enumerate(galleries) if g.get('id') == GALLERY_ID), None)
    if existing is None:
        galleries.append(gallery)
    else:
        galleries[existing] = gallery
    data['updated'] = '2026-09-13'
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    keep = GAL / '.gitkeep'
    if keep.exists():
        keep.unlink()


replace_entry(ROOT / 'pt/musica/index.html', 'pt')
replace_entry(ROOT / 'en/music/index.html', 'en')
register_gallery()
print('Destemidos narrative, thread images, gallery registry and video links staged.')
