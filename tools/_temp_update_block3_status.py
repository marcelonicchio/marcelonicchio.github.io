#!/usr/bin/env python3
from pathlib import Path

p = Path('docs/full-biography-workflow.md')
s = p.read_text(encoding='utf-8')
s = s.replace('**Atualizado em:** 27 de agosto de 2026', '**Atualizado em:** 28 de agosto de 2026')
s = s.replace('## 8. Estado editorial em 27/08/2026', '## 8. Estado editorial em 28/08/2026')
s = s.replace('Exemplo já implementado: Meia-Noite e Uns, com imagem editorial, quatro vídeos e galeria de 22 fotos.', 'Exemplos já implementados: Meia-Noite e Uns, com imagem editorial, quatro vídeos e galeria de 22 fotos; e CookieWEB, com imagem editorial, três certificados GAP e galeria cronológica de 20 fotos.')
old = '''### Bloco 3 — ainda requer aprofundamento autoral

O conteúdo-base já existe, mas a revisão autobiográfica detalhada ainda precisa ser feita. Próximo arco prioritário:

`Mirantte News → Tiago Luz → Search → especialização → contas → Herik Mourão → CookieWEB → Beleza na Web → Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto`.

Não tratar o texto atual desse período como versão final. Ele é uma base cronológica funcional.'''
new = '''### Bloco 3A — revisado: Mirantte News → CookieWEB

A primeira metade do arco de Internet & Performance recebeu expansão autobiográfica detalhada em 28/08/2026 e passou pelo fluxo PT/EN → paridade → sync → audits.

O trecho agora cobre, em sequência causal:

- Mirantte News, seu modelo comercial e o gargalo de tráfego;
- a ponte da MapLink com Tiago Luz e as primeiras aquisições de tráfego;
- primeiras contas de Search em 2008;
- Louise Martins e a percepção de uma escala internacional de operação;
- Goobec em 2009, João Dalla e o encontro com Herik Mourão;
- Beleza na Web e a primeira conta de grande porte;
- criação e crescimento da área de mídia da CookieWEB;
- certificações Google Advertising Professional — GAP;
- formação de equipe, passagem de Coordenação a Gerência de SEM, Acquisio e Asana;
- mais de 22 contas simultâneas e seis analistas, além de estagiários;
- cultura de equipe, festa junina e Hopi Hari;
- encerramento do ciclo CookieWEB em julho de 2012 por decisão de qualidade de vida.

A entrada CookieWEB também incorpora três certificados GAP, uma imagem editorial de equipe e galeria cronológica de 20 fotos com derivados responsivos PT/EN.

### Bloco 3B — ainda requer aprofundamento autoral

O conteúdo-base posterior continua funcional, mas ainda precisa da mesma expansão autobiográfica detalhada. Próximo arco prioritário:

`Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto`.

Não tratar essas quatro entradas atuais como versões finais; elas permanecem como base cronológica até a próxima rodada autoral.'''
if old not in s:
    raise SystemExit('Expected Block 3 status text not found')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
