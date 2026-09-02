from pathlib import Path


def patch(path, replacements):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    for old, new in replacements:
        if old not in text:
            if new in text:
                continue
            raise SystemExit(f'{path}: expected text not found: {old[:90]!r}')
        text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')

patch('docs/CURRENT-HUB-STATE.md', [
    ('- Communication / Comunicação;\n- Internet & Performance;\n- Audiovisual;', '- Cultura & Audiovisual / Culture & Audiovisual;\n- Internet & Performance;'),
])

patch('tools/sync_full_biography.py', [
    ('<p>Música, comunicação, internet, performance, audiovisual e IA/HAI aparecem aqui na ordem em que atravessaram a trajetória, inclusive quando ocorreram em paralelo.</p>', '<p>Música, Cultura & Audiovisual, Internet & Performance e IA/HAI aparecem aqui na ordem em que atravessaram a trajetória, inclusive quando ocorreram em paralelo.</p>'),
    ('<p>Music, communication, internet, performance, audiovisual work and AI/HAI appear here in the order they crossed the trajectory, including periods in which they happened in parallel.</p>', '<p>Music, Culture & Audiovisual, Internet & Performance and AI/HAI appear here in the order they crossed the trajectory, including periods in which they happened in parallel.</p>'),
])

patch('pt/biografia/index.html', [
    ('Biografia completa de Marcelo Nicchio: música, comunicação, Internet & Performance, audiovisual e pesquisa independente em Human–AI Interaction.', 'Biografia completa de Marcelo Nicchio: música, Cultura & Audiovisual, Internet & Performance e pesquisa independente em Human–AI Interaction.'),
    ('Marcelo Nicchio é um criador brasileiro cuja trajetória atravessa música autoral, comunicação, Internet & Performance, audiovisual e, mais recentemente, pesquisa independente em Human–AI Interaction.', 'Marcelo Nicchio é um criador brasileiro cuja trajetória atravessa música autoral, Cultura & Audiovisual, Internet & Performance e, mais recentemente, pesquisa independente em Human–AI Interaction.'),
])

patch('en/biography/index.html', [
    ('Full biography of Marcelo Nicchio: music, communication, Internet & Performance, audiovisual work and independent Human–AI Interaction research.', 'Full biography of Marcelo Nicchio: music, Culture & Audiovisual, Internet & Performance and independent Human–AI Interaction research.'),
    ('Complete biography of Marcelo Nicchio: music, communication, Internet & Performance, audiovisual work and independent Human–AI Interaction research.', 'Complete biography of Marcelo Nicchio: music, Culture & Audiovisual, Internet & Performance and independent Human–AI Interaction research.'),
    ('Marcelo Nicchio is a Brazilian creator whose trajectory spans original music, communication, Internet & Performance, audiovisual work and, more recently, independent Human–AI Interaction research.', 'Marcelo Nicchio is a Brazilian creator whose trajectory spans original music, Culture & Audiovisual, Internet & Performance and, more recently, independent Human–AI Interaction research.'),
])

patch('pt/audiovisual/index.html', [
    ('href="/en/audiovisual/">EN</a>', 'href="/en/communication/">EN</a>'),
    ('href="/en/audiovisual/">English version</a>', 'href="/en/communication/">English version</a>'),
])
patch('en/audiovisual/index.html', [
    ('href="/pt/audiovisual/">PT</a>', 'href="/pt/comunicacao/">PT</a>'),
    ('href="/pt/audiovisual/">Versão em português</a>', 'href="/pt/comunicacao/">Versão em português</a>'),
])
