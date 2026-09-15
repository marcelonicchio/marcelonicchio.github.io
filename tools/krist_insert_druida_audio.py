from pathlib import Path

BASE = "/assets/archive/music/coitado-do-proximo/1993-estudios-e-shows/"

PT = '''<div class="video-library audio-library" aria-label="Áudios de ensaio" aria-labelledby="music-druida-1993-audio-title">
  <div class="video-library__head">
    <strong id="music-druida-1993-audio-title">Áudio de Ensaio · 3</strong>
    <span>Estúdio Druida · Vila Maria · 1993</span>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Acabou</strong></div>
    <p class="video-library__description">Registro sonoro preservado de ensaio do Coitado do Próximo no Estúdio Druida, em 1993.</p>
    <audio class="audio-library__player" controls preload="none"><source src="'''+BASE+'''acabou-ensaio-estudio-druida-1993.mp3" type="audio/mpeg">Seu navegador não suporta reprodução de áudio HTML5.</audio>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Pegue o Seu Celular</strong></div>
    <p class="video-library__description">Registro sonoro preservado de ensaio do Coitado do Próximo no Estúdio Druida, em 1993.</p>
    <audio class="audio-library__player" controls preload="none"><source src="'''+BASE+'''pegue-o-seu-celular-ensaio-estudio-druida-1993.mp3" type="audio/mpeg">Seu navegador não suporta reprodução de áudio HTML5.</audio>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Mulher SP</strong></div>
    <p class="video-library__description">Registro sonoro preservado de ensaio do Coitado do Próximo no Estúdio Druida, em 1993.</p>
    <audio class="audio-library__player" controls preload="none"><source src="'''+BASE+'''mulher-sp-ensaio-estudio-druida-1993.mp3" type="audio/mpeg">Seu navegador não suporta reprodução de áudio HTML5.</audio>
  </div>
</div>'''

EN = '''<div class="video-library audio-library" aria-label="Rehearsal audio" aria-labelledby="music-druida-1993-audio-title">
  <div class="video-library__head">
    <strong id="music-druida-1993-audio-title">Rehearsal Audio · 3</strong>
    <span>Estúdio Druida · Vila Maria · 1993</span>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Acabou</strong></div>
    <p class="video-library__description">Preserved audio recording from a Coitado do Próximo rehearsal at Estúdio Druida in 1993.</p>
    <audio class="audio-library__player" controls preload="none"><source src="'''+BASE+'''acabou-ensaio-estudio-druida-1993.mp3" type="audio/mpeg">Your browser does not support HTML5 audio playback.</audio>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Pegue o Seu Celular</strong></div>
    <p class="video-library__description">Preserved audio recording from a Coitado do Próximo rehearsal at Estúdio Druida in 1993.</p>
    <audio class="audio-library__player" controls preload="none"><source src="'''+BASE+'''pegue-o-seu-celular-ensaio-estudio-druida-1993.mp3" type="audio/mpeg">Your browser does not support HTML5 audio playback.</audio>
  </div>
  <div class="video-library__group">
    <div class="video-library__label"><strong>Mulher SP</strong></div>
    <p class="video-library__description">Preserved audio recording from a Coitado do Próximo rehearsal at Estúdio Druida in 1993.</p>
    <audio class="audio-library__player" controls preload="none"><source src="'''+BASE+'''mulher-sp-ensaio-estudio-druida-1993.mp3" type="audio/mpeg">Your browser does not support HTML5 audio playback.</audio>
  </div>
</div>'''

for path, section_id, block in [
    (Path("pt/musica/index.html"), 'id="estudios-shows-1993"', PT),
    (Path("en/music/index.html"), 'id="studios-shows-1993"', EN),
]:
    text = path.read_text(encoding="utf-8")
    if 'id="music-druida-1993-audio-title"' in text:
        raise SystemExit(f"Audio block already present in {path}")
    start = text.find(section_id)
    if start < 0:
        raise SystemExit(f"Section not found in {path}: {section_id}")
    close = text.find("</figure>", start)
    if close < 0:
        raise SystemExit(f"First figure not found in {path}")
    insert_at = close + len("</figure>")
    text = text[:insert_at] + block + text[insert_at:]
    # Placement guard: audio must precede the section's existing shows paragraph.
    section_end = text.find('</div></div>', insert_at)
    if section_end < 0 or text.find('music-druida-1993-audio-title', start, section_end) < 0:
        raise SystemExit(f"Placement guard failed for {path}")
    path.write_text(text, encoding="utf-8")

print("Inserted Druida 1993 rehearsal audio block in PT/EN Music only.")
