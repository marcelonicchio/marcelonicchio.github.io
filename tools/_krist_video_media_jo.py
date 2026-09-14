from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PT = '''<div class="video-library" aria-labelledby="jo-2001-video-title">
  <div class="video-library__head">
    <strong id="jo-2001-video-title">Vídeos &amp; Mídia · 9</strong>
    <span>Programa do Jô · 27 jun. 2001</span>
  </div>
  <div class="video-library__group video-library__group--primary">
    <div class="video-library__label"><strong>Apresentação exibida na Globo</strong></div>
    <div class="video-library__actions"><a class="video-pill video-pill--primary" href="https://www.youtube.com/watch?v=VvHPQad2S48" target="_blank" rel="noopener noreferrer">Estava Comigo</a></div>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Bastidores</strong></div>
    <div class="video-library__actions">
      <a class="video-pill" href="https://youtu.be/c4VAEll1mM4?si=nKFKGSkl5gwMzboP" target="_blank" rel="noopener noreferrer">Parte 1</a>
      <a class="video-pill" href="https://youtu.be/h0GPkE5SBxM?si=HGG6GSlFBA1kJsOI" target="_blank" rel="noopener noreferrer">Parte 2</a>
      <a class="video-pill" href="https://youtu.be/ThxZrYgh1eY?si=SfmwuFaemfmYM5BY" target="_blank" rel="noopener noreferrer">Parte 3</a>
      <a class="video-pill" href="https://youtu.be/_7zttgW8qV8?si=H1gNfNWjGHKXrtH8" target="_blank" rel="noopener noreferrer">Parte 4</a>
      <a class="video-pill" href="https://youtu.be/cJYbbmOtRyI?si=8zNN0TjqPQbShaoI" target="_blank" rel="noopener noreferrer">Parte 5</a>
    </div>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Passagem de som</strong></div>
    <div class="video-library__actions">
      <a class="video-pill" href="https://youtu.be/MCjI0bA7CCc?si=k2paUz0x3WFi4rwm" target="_blank" rel="noopener noreferrer">A Enchente</a>
      <a class="video-pill" href="https://youtu.be/zrXzdmsIMjg?si=si9xEgOO_oQGIT-B" target="_blank" rel="noopener noreferrer">Um Anjo do Céu</a>
      <a class="video-pill" href="https://youtu.be/Nu8R3TlK8Kc?si=qbhQKx1QmCqfoZf3" target="_blank" rel="noopener noreferrer">Mulher SP</a>
    </div>
  </div>
</div>'''

EN = '''<div class="video-library" aria-labelledby="jo-2001-video-title-en">
  <div class="video-library__head">
    <strong id="jo-2001-video-title-en">Videos &amp; Media · 9</strong>
    <span>Programa do Jô · 27 Jun 2001</span>
  </div>
  <div class="video-library__group video-library__group--primary">
    <div class="video-library__label"><strong>Broadcast performance on Globo</strong></div>
    <div class="video-library__actions"><a class="video-pill video-pill--primary" href="https://www.youtube.com/watch?v=VvHPQad2S48" target="_blank" rel="noopener noreferrer">Estava Comigo</a></div>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Backstage</strong></div>
    <div class="video-library__actions">
      <a class="video-pill" href="https://youtu.be/c4VAEll1mM4?si=nKFKGSkl5gwMzboP" target="_blank" rel="noopener noreferrer">Part 1</a>
      <a class="video-pill" href="https://youtu.be/h0GPkE5SBxM?si=HGG6GSlFBA1kJsOI" target="_blank" rel="noopener noreferrer">Part 2</a>
      <a class="video-pill" href="https://youtu.be/ThxZrYgh1eY?si=SfmwuFaemfmYM5BY" target="_blank" rel="noopener noreferrer">Part 3</a>
      <a class="video-pill" href="https://youtu.be/_7zttgW8qV8?si=H1gNfNWjGHKXrtH8" target="_blank" rel="noopener noreferrer">Part 4</a>
      <a class="video-pill" href="https://youtu.be/cJYbbmOtRyI?si=8zNN0TjqPQbShaoI" target="_blank" rel="noopener noreferrer">Part 5</a>
    </div>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Soundcheck</strong></div>
    <div class="video-library__actions">
      <a class="video-pill" href="https://youtu.be/MCjI0bA7CCc?si=k2paUz0x3WFi4rwm" target="_blank" rel="noopener noreferrer">A Enchente</a>
      <a class="video-pill" href="https://youtu.be/zrXzdmsIMjg?si=si9xEgOO_oQGIT-B" target="_blank" rel="noopener noreferrer">Um Anjo do Céu</a>
      <a class="video-pill" href="https://youtu.be/Nu8R3TlK8Kc?si=qbhQKx1QmCqfoZf3" target="_blank" rel="noopener noreferrer">Mulher SP</a>
    </div>
  </div>
</div>'''

CSS = r'''

/* Video & Media library — compact ghost controls */
.video-library{margin:28px 0 8px;padding:14px 16px 16px;border:1px solid rgba(255,255,255,.14);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.032),rgba(255,255,255,.014));box-shadow:inset 3px 0 0 rgba(211,164,160,.46)}
.video-library__head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:11px;border-bottom:1px solid rgba(255,255,255,.09)}
.video-library__head strong{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text)}
.video-library__head span{font-size:.78rem;color:#c7c2b9;font-weight:680}
.video-library__group{padding-top:13px}
.video-library__group + .video-library__group{margin-top:12px;border-top:1px solid rgba(255,255,255,.07)}
.video-library__label{margin-bottom:8px}
.video-library__label strong{font-size:.69rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-soft);font-weight:820}
.video-library__actions{display:flex;flex-wrap:wrap;gap:8px}
.video-pill{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-height:38px;padding:7px 12px;border:1px solid rgba(243,239,231,.48);border-radius:999px;background:rgba(243,239,231,.065);color:rgba(243,239,231,.96)!important;font-size:.82rem;font-weight:760;text-decoration:none!important;line-height:1.1;box-shadow:inset 0 1px 0 rgba(255,255,255,.055);transition:background .16s ease,color .16s ease,border-color .16s ease,transform .16s ease,box-shadow .16s ease}
.video-pill::before{content:"▶";font-size:.66em;line-height:1;color:var(--accent-soft)}
.video-pill--primary{background:rgba(241,223,163,.09);border-color:rgba(241,223,163,.58);padding-inline:14px}
.video-pill--primary::before{color:#f1dfa3}
.video-pill:hover,.video-pill:focus-visible{opacity:1;background:#f1dfa3;color:#101011!important;border-color:#f6e7ae;transform:translateY(-1px);box-shadow:0 5px 16px rgba(241,223,163,.14)}
.video-pill:hover::before,.video-pill:focus-visible::before{color:#8e5f16}
.video-pill:focus-visible{outline:2px solid #f6e7ae;outline-offset:3px}
@media(max-width:580px){
  .video-library{padding:13px 13px 14px;margin:24px 0 8px}
  .video-library__head{align-items:flex-start;flex-direction:column;gap:2px}
  .video-library__head strong{font-size:.8rem}
  .video-library__head span{font-size:.8rem;color:var(--muted)}
  .video-library__actions{gap:7px}
  .video-pill{min-height:40px;padding:8px 11px;font-size:.84rem}
}
@media(prefers-reduced-motion:reduce){.video-pill{transition:none}.video-pill:hover,.video-pill:focus-visible{transform:none}}
'''


def replace_block(path: Path, block: str):
    text = path.read_text(encoding='utf-8')
    marker = '<!-- gallery:programa-do-jo-2001:end -->'
    pos = text.find(marker)
    if pos < 0:
        raise SystemExit(f'marker not found in {path}')
    start = text.find('<div class="evidence-links inline-links">', pos)
    if start < 0:
        raise SystemExit(f'video link block not found in {path}')
    end = text.find('</div>', start)
    if end < 0:
        raise SystemExit(f'video link block end not found in {path}')
    end += len('</div>')
    text = text[:start] + block + text[end:]
    path.write_text(text, encoding='utf-8')

replace_block(ROOT / 'pt/musica/index.html', PT)
replace_block(ROOT / 'en/music/index.html', EN)

style_path = ROOT / 'styles.css'
styles = style_path.read_text(encoding='utf-8')
marker = '/* Video & Media library — compact ghost controls */'
if marker not in styles:
    styles += CSS
style_path.write_text(styles, encoding='utf-8')
print('Applied Jô 2001 video media component to PT/EN music pages and styles.')
