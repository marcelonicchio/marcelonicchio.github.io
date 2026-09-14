from pathlib import Path
import sys

BASE = "/assets/archive/music/coitado-do-proximo/1994-primeira-demo-tape-estudio-anonimato"
MULHER = BASE + "/mulher-sp-demo-1994-anonimato.mp3"
CELULAR = BASE + "/pegue-o-seu-celular-demo-1994-anonimato.mp3"
FORBIDDEN = "the trips"

PT_ANCHOR = '<p>Parte da filmagem dessas sessões sobreviveu. O vídeo atualmente publicado traz <strong>1993</strong> no título, mas o registro correto é de <strong>1994</strong>.</p>'
EN_ANCHOR = '<p>Part of the footage from these sessions survives. The currently published video is titled as <strong>1993</strong>, but the correct year of the recording is <strong>1994</strong>.</p>'

PT_BLOCK = f'''<div class="video-library audio-library" aria-label="Áudios e mídia" aria-labelledby="music-demo-audio-title">
  <div class="video-library__head">
    <strong id="music-demo-audio-title">Áudio &amp; Mídia · 2</strong>
    <span>Demo-tape · Estúdio Anonimato · 1994</span>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Lado A · Mulher SP</strong></div>
    <p class="video-library__description">Digitalização preservada da fita cassete da primeira demo. O master original foi registrado em ADAT; esta cópia apresenta as limitações sonoras do suporte e da digitalização.</p>
    <audio class="audio-library__player" controls preload="metadata">
      <source src="{MULHER}" type="audio/mpeg">
      Seu navegador não suporta reprodução de áudio HTML5.
    </audio>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Lado B · Pegue o Seu Celular</strong></div>
    <p class="video-library__description">Digitalização preservada da mesma demo-tape de 1994, mantida sem intervenção restaurativa.</p>
    <audio class="audio-library__player" controls preload="metadata">
      <source src="{CELULAR}" type="audio/mpeg">
      Seu navegador não suporta reprodução de áudio HTML5.
    </audio>
  </div>
  <p class="audio-library__note"><strong>Nota de arquivo:</strong> a qualidade sonora reflete a cópia digital disponível atualmente. O áudio foi preservado sem restauração para manter o registro histórico.</p>
</div>'''

EN_BLOCK = f'''<div class="video-library audio-library" aria-label="Audio and media" aria-labelledby="music-demo-audio-title">
  <div class="video-library__head">
    <strong id="music-demo-audio-title">Audio &amp; Media · 2</strong>
    <span>Demo tape · Estúdio Anonimato · 1994</span>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Side A · Mulher SP</strong></div>
    <p class="video-library__description">Preserved cassette digitization of the first demo. The original master was recorded on ADAT; this copy reflects the sonic limitations of the cassette source and digitization.</p>
    <audio class="audio-library__player" controls preload="metadata">
      <source src="{MULHER}" type="audio/mpeg">
      Your browser does not support HTML5 audio playback.
    </audio>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Side B · Pegue o Seu Celular</strong></div>
    <p class="video-library__description">Preserved digitization from the same 1994 demo tape, kept without restorative intervention.</p>
    <audio class="audio-library__player" controls preload="metadata">
      <source src="{CELULAR}" type="audio/mpeg">
      Your browser does not support HTML5 audio playback.
    </audio>
  </div>
  <p class="audio-library__note"><strong>Archive note:</strong> the sound quality reflects the digital copy currently available. The audio has been preserved without restoration in order to retain the historical record.</p>
</div>'''

CSS_MARKER = "/* Audio archive — native player inside media library */"
CSS_BLOCK = '''\n\n/* Audio archive — native player inside media library */
.audio-library__player{display:block;width:100%;max-width:640px;height:42px;margin-top:9px;accent-color:var(--accent-soft)}
.audio-library .audio-library__note{margin:14px 0 0!important;padding-top:12px;border-top:1px solid rgba(255,255,255,.07);color:var(--muted)!important;font-size:.78rem!important;line-height:1.5!important}
.audio-library__note strong{color:var(--soft)}
@media(max-width:580px){.audio-library__player{max-width:none;height:44px}}
'''


def patch():
    for rel in [MULHER.lstrip('/'), CELULAR.lstrip('/')]:
        if not Path(rel).exists():
            raise SystemExit(f"Missing neutral public audio alias: {rel}")

    specs = [
        (Path('pt/musica/index.html'), PT_ANCHOR, PT_BLOCK),
        (Path('en/music/index.html'), EN_ANCHOR, EN_BLOCK),
    ]
    for path, anchor, block in specs:
        text = path.read_text(encoding='utf-8')
        if 'audio-library__player' in text:
            continue
        count = text.count(anchor)
        if count != 1:
            raise SystemExit(f"{path}: expected exactly one demo insertion anchor, found {count}")
        path.write_text(text.replace(anchor, block + anchor, 1), encoding='utf-8')

    css = Path('styles.css')
    css_text = css.read_text(encoding='utf-8')
    if CSS_MARKER not in css_text:
        css.write_text(css_text + CSS_BLOCK, encoding='utf-8')


def guard():
    targets = [
        Path('pt/musica/index.html'), Path('en/music/index.html'),
        Path('pt/biografia/index.html'), Path('en/biography/index.html'),
    ]
    for path in targets:
        text = path.read_text(encoding='utf-8')
        if FORBIDDEN in text.lower():
            raise SystemExit(f"Forbidden alternate name leaked into public HTML: {path}")
        if 'music-demo-tape-1994' in text and 'mulher-sp-demo-1994-anonimato.mp3' not in text:
            raise SystemExit(f"Expected demo audio missing from synchronized surface: {path}")
    print('Audio integration guards passed.')


if __name__ == '__main__':
    if '--guard' in sys.argv:
        guard()
    else:
        patch()
