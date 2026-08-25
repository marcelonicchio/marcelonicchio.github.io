from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = "/assets/archive/minduim-bbs-1993-reconstruction.webp"


def replace_once(path: str, old: str, new: str) -> None:
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old[:90]!r}")
    file.write_text(text.replace(old, new, 1), encoding="utf-8")


pt_figure = f'''<figure class="archive-figure">
<img src="{ASSET}" width="1448" height="1086" loading="lazy" decoding="async" alt="Recriação por IA do quarto e da interface da Minduim BBS em 1993">
<figcaption><strong>Recriação por IA do ambiente e da interface da Minduim BBS, c. 1993.</strong> Recriação fiel do ambiente doméstico e da interface em que foi instalada e operada a Minduim BBS, construída a partir de elementos factuais e memória do período. Não se trata de fotografia ou captura de tela original.</figcaption>
</figure>'''

en_figure = f'''<figure class="archive-figure">
<img src="{ASSET}" width="1448" height="1086" loading="lazy" decoding="async" alt="AI reconstruction of the room and Minduim BBS interface in 1993">
<figcaption><strong>AI reconstruction of the Minduim BBS environment and interface, c. 1993.</strong> A faithful visual reconstruction of the domestic setting and interface in which Minduim BBS was installed and operated, built from factual elements and period memory. It is not an original photograph or screen capture.</figcaption>
</figure>'''

pt_bbs_old = '<p>Em paralelo, criou a <strong>Minduim BBS</strong>, uma experiência pessoal construída com o software RemoteAccess e duas linhas telefônicas. O projeto era experimental e não comercial. Não restaram prints, fotos ou backups conhecidos; qualquer futura imagem da Minduim será apresentada explicitamente como <em>reconstrução baseada em memória</em>, nunca como captura histórica.</p>'
pt_bbs_new = '<p>Em paralelo, criou a <strong>Minduim BBS</strong>, uma experiência pessoal construída com o software RemoteAccess e duas linhas telefônicas. O projeto era experimental e não comercial. Não restaram prints, fotos ou backups conhecidos; a reconstrução visual abaixo é apresentada explicitamente como <em>recriação por IA baseada em elementos factuais e memória</em>, nunca como captura histórica.</p>' + pt_figure
replace_once('pt/internet/index.html', pt_bbs_old, pt_bbs_new)

en_bbs_old = '<p>In parallel, he created <strong>Minduim BBS</strong>, a personal experiment built with RemoteAccess software and two telephone lines. The project was experimental and non-commercial. No screenshots, photographs or known backups survive; any future visual representation of Minduim will be explicitly labeled as a <em>memory-based reconstruction</em>, never as a historical capture.</p>'
en_bbs_new = '<p>In parallel, he created <strong>Minduim BBS</strong>, a personal experiment built with RemoteAccess software and two telephone lines. The project was experimental and non-commercial. No screenshots, photographs or known backups survive; the visual below is explicitly presented as an <em>AI reconstruction based on factual elements and period memory</em>, never as a historical capture.</p>' + en_figure
replace_once('en/internet/index.html', en_bbs_old, en_bbs_new)

pt_archive_old = '<div class="evidence"><div class="evidence-top"><strong>Tremonte / Minduim BBS</strong><span class="status">autobiográfico</span></div><p>Sem material visual sobrevivente conhecido. Não será criada falsa evidência.</p></div>'
pt_archive_new = '<div class="evidence"><div class="evidence-top"><strong>Tremonte / Minduim BBS</strong><span class="status">autobiográfico + recriação</span></div><p>Não há material visual original sobrevivente conhecido. A imagem abaixo é uma recriação por IA baseada em elementos factuais e memória do ambiente; não é evidência fotográfica.</p>' + pt_figure.replace('class="archive-figure"', 'class="archive-figure compact"') + '</div>'
replace_once('pt/internet/index.html', pt_archive_old, pt_archive_new)

pt_no_record_old = '<p>O site não vai criar falsa precisão para preencher essas lacunas. Uma reconstrução visual, quando existir — como uma futura imagem da Minduim BBS — será marcada como <strong>reconstrução baseada em memória</strong>.</p>'
pt_no_record_new = '<p>O site não cria falsa precisão para preencher essas lacunas. A reconstrução visual da Minduim BBS publicada neste arquivo é identificada de forma explícita como <strong>recriação por IA baseada em elementos factuais e memória</strong>, e não como registro histórico original.</p>'
replace_once('pt/arquivo/index.html', pt_no_record_old, pt_no_record_new)

pt_archive_insert = '<section id="sem-registro" class="chapter"><h2>Fatos sem documentação sobrevivente conhecida</h2>'
pt_archive_block = '<section id="reconstrucoes" class="chapter"><h2>Reconstruções visuais</h2><div class="evidence-list"><div class="evidence"><div class="evidence-top"><strong>Minduim BBS — c. 1993</strong><span class="status">recriação por IA</span></div><p>Recriação fiel do ambiente doméstico e da interface em que foi instalada e operada a Minduim BBS. A composição combina elementos factuais da configuração — microcomputador 486, monitor CRT, RemoteAccess e duas linhas telefônicas — com memória do ambiente e do período. Não é fotografia nem captura de tela original.</p>' + pt_figure.replace('class="archive-figure"', 'class="archive-figure compact"') + '</div></div></section>\n' + pt_archive_insert
replace_once('pt/arquivo/index.html', pt_archive_insert, pt_archive_block)
replace_once('pt/arquivo/index.html', '<a href="#sem-registro">Sem registro sobrevivente</a>', '<a href="#reconstrucoes">Reconstruções</a><a href="#sem-registro">Sem registro sobrevivente</a>')

en_no_record_old = '<p>The site will not manufacture false precision to fill those gaps. Any visual reconstruction — such as a future image of Minduim BBS — will be clearly labeled as a <strong>memory-based reconstruction</strong>.</p>'
en_no_record_new = '<p>The site does not manufacture false precision to fill those gaps. The Minduim BBS visual reconstruction published in this archive is explicitly identified as an <strong>AI reconstruction based on factual elements and period memory</strong>, not as an original historical record.</p>'
replace_once('en/archive/index.html', en_no_record_old, en_no_record_new)

en_archive_insert = '<section id="no-record" class="chapter"><h2>Facts with no known surviving documentation</h2>'
en_archive_block = '<section id="reconstructions" class="chapter"><h2>Visual reconstructions</h2><div class="evidence-list"><div class="evidence"><div class="evidence-top"><strong>Minduim BBS — c. 1993</strong><span class="status">AI reconstruction</span></div><p>A faithful reconstruction of the domestic setting and interface in which Minduim BBS was installed and operated. The composition combines factual elements of the setup — a 486 computer, CRT monitor, RemoteAccess and two telephone lines — with memory of the room and period. It is not an original photograph or screen capture.</p>' + en_figure.replace('class="archive-figure"', 'class="archive-figure compact"') + '</div></div></section>\n' + en_archive_insert
replace_once('en/archive/index.html', en_archive_insert, en_archive_block)
replace_once('en/archive/index.html', '<a href="#no-record">No surviving record</a>', '<a href="#reconstructions">Reconstructions</a><a href="#no-record">No surviving record</a>')

styles = ROOT / 'styles.css'
css = styles.read_text(encoding='utf-8')
marker = '/* Accessibility and QA refinements */'
component = '''/* Documentary and reconstructed archive visuals */
.archive-figure{margin:28px 0 36px}
.archive-figure img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:16px;background:var(--panel);box-shadow:0 14px 38px rgba(0,0,0,.22)}
.archive-figure figcaption{margin-top:10px;color:var(--muted);font-size:.82rem;line-height:1.55}
.archive-figure figcaption strong{color:var(--soft);font-weight:760}
.archive-figure.compact{margin:16px 0 0}
.archive-figure.compact img{border-radius:12px}
@media(max-width:580px){.archive-figure{margin:22px 0 30px}.archive-figure figcaption{font-size:.79rem}}

'''
if '.archive-figure{' not in css:
    if marker not in css:
        raise SystemExit('CSS insertion marker not found')
    css = css.replace(marker, component + marker, 1)
    styles.write_text(css, encoding='utf-8')

print('Minduim reconstruction applied to PT/EN Internet and Archive pages.')
