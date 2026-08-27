# Full Biography — workflow editorial, sincronização e continuidade

**Status:** arquitetura operacional da Biografia Completa  
**Atualizado em:** 27 de agosto de 2026  
**Repositório:** `marcelonicchio/marcelonicchio.github.io`

Este documento complementa `docs/hub-continuity-guide.md` e registra especificamente a arquitetura da Biografia Completa, o mecanismo de paridade PT/EN e o procedimento de atualização futura.

---

## 1. Regra constitucional

A Biografia Completa não é uma soma temática do tipo:

`Música → Comunicação → Internet → Audiovisual → IA/HAI`.

Ela é uma única linha do tempo multidomínio.

**Biografia Completa = totalidade. Verticais = recortes temáticos.**

A ordem cronológica mistura os campos quando eles coexistem: música, rádio, BBS, internet, audiovisual, performance e IA/HAI aparecem conforme atravessam a trajetória.

A Biografia é um arquivo vivo: novas informações, fotos, vídeos, áudios e correções podem ser incorporados depois sem reconstrução manual da página inteira.

---

## 2. Fonte editorial única

A fonte autoral de cada episódio é a vertical temática correspondente.

Fluxo:

```text
entrada na vertical PT
        ↓
versão editorial equivalente EN
        ↓
checkpoint de paridade PT/EN
        ↓
sync_full_biography.py
        ↓
Full Bio PT + Full Bio EN
        ↓
audit
```

A região cronológica da Full Bio não deve ser editada manualmente.

Exemplo futuro:

```text
Mirantte News em /pt/internet/
Mirantte News em /en/internet/
        ↓
python tools/editorial_parity.py --accept internet-mirantte
        ↓
python tools/sync_full_biography.py
        ↓
/pt/biografia/ + /en/biography/
```

Se Petlove, Mirantte, CookieWEB, Meia-Noite e Uns ou qualquer outra entrada for enriquecida na vertical, a Full Bio deve herdar a mesma unidade editorial.

---

## 3. Arquivos centrais

- `data/full_biography.json` — manifesto cronológico e fontes.
- `data/editorial_parity.json` — checkpoints PT/EN aceitos.
- `tools/sync_full_biography.py` — gera a região gerenciada da Full Bio.
- `tools/audit_full_biography.py` — verifica cobertura, ordem e sincronização.
- `tools/editorial_parity.py` — bloqueia drift editorial entre PT/EN.
- `pt/biografia/index.html` — Full Bio PT.
- `en/biography/index.html` — Full Bio EN.

O manifesto controla ordem, período, domínio, source path, selector, eras e entradas especiais.

---

## 4. Paridade PT ↔ EN

O sistema não traduz automaticamente.

Ele mantém duas pistas editoriais:

```text
Vertical PT → Full Bio PT
Vertical EN → Full Bio EN
```

Cada unidade registrada possui um checkpoint com:

- número de revisão;
- hash do conteúdo PT;
- hash do conteúdo EN;
- data de aceite.

Comando de checagem:

```bash
python tools/editorial_parity.py --check
```

Se apenas o PT mudar, o audit deve falhar. Se apenas o EN mudar, também deve falhar. Se os dois mudarem, o audit continua falhando até revisão conjunta e aceite explícito:

```bash
python tools/editorial_parity.py --accept ENTRY_ID
```

O aceite não julga qualidade de tradução; ele registra que o par PT/EN foi editorialmente revisado.

Nunca usar o checkpoint como substituto de revisão humana.

---

## 5. Chapters grandes e subunidades

Uma vertical pode permanecer visualmente coesa mesmo quando a Full Bio precisa distribuir seus acontecimentos em anos diferentes.

Para isso existem subunidades com `data-bio-key`.

Exemplo: Música → `Palcos, discos e expansão` permanece um único chapter temático, mas a Full Bio pode extrair separadamente:

- circuito 1993–1995;
- Meu Querido Diário;
- Eu Não Tô Nem Aí;
- Olympia;
- Programa do Jô;
- atividade 2001–2003;
- encerramento 2003;
- reunião 2023.

Não quebrar a experiência visual da vertical apenas para atender a cronologia da Full Bio.

---

## 6. Cobertura obrigatória

O CI deve impedir que um chapter biográfico novo surja em uma vertical e fique esquecido na Biografia Completa.

O audit precisa verificar:

- selectors resolvendo exatamente uma unidade;
- cobertura PT e EN;
- ausência de entradas órfãs;
- ausência de entradas duplicadas;
- Full Bio regenerada e sincronizada;
- paridade editorial aceita.

A regra prática é: **nenhuma nova entrada biográfica está concluída enquanto PT, EN, Full Bio PT, Full Bio EN e audits não estiverem alinhados.**

---

## 7. Mídia

Galerias e mídias integrantes de uma entrada acompanham a unidade editorial quando importada pela Full Bio.

Para galerias Type 2, usar `data/galleries.json`, `tools/sync_galleries.py`, `tools/build_gallery_media.py` e `tools/audit_galleries.py`.

As thumbs devem usar derivados responsivos; originais ficam para lightbox/fallback. PT e EN compartilham o mesmo conjunto visual, com alt/caption localizados.

Exemplo já implementado: Meia-Noite e Uns, com imagem editorial, quatro vídeos e galeria de 22 fotos.

---

## 8. Estado editorial em 27/08/2026

A nova Full Bio foi reconstruída em cronologia integrada e contém conteúdo de todas as cinco verticais, mais entradas cronológicas exclusivas como Livraria Cultura.

### Bloco 1 — revisado

Inclui:

- Mocidade Alegre aos 12 anos;
- primeiro desfile em 4/2/1989;
- Conservatório Antonino Simalha / João Conde;
- violão autodidata e primeiras composições;
- fundação do Coitado do Próximo;
- primeiro show confirmado em 5/7/1992 no Barão Homem de Mello;
- BBS / Minduim;
- Tremonte;
- circuito musical;
- demo-tape no Estúdio Anonimato;
- Kid Vinil;
- Metrópole;
- transição para internet comercial.

### Bloco 2 — revisado em versão provisória viva

Inclui:

- Meu Querido Diário, gravação 1997 e lançamento independente em CD em 1998;
- participações de Paulão de Carvalho, Finho e Grupo Emosamba;
- Eu Não Tô Nem Aí, lançado em 2000, releituras e versão de `Ciúmes` do Ultraje a Rigor;
- Olympia em 25/6/2000, sold out, público estimado em cerca de 6 mil pessoas;
- Folhateen / Folha de S.Paulo como matéria de capa;
- Programa do Jô em 21/6/2001, gravado e exibido no mesmo dia, com Globo Internacional;
- atividade contínua do Coitado até 2003;
- Prateleira Cultural / Sinal Verde em linguagem autobiográfica;
- Mirantte News com MapLink/UOL, geolocalização/rotas, fotografia profissional, Tatiana Cavalcanti e indexação por categorias;
- Meia-Noite e Uns integral.

Esses textos podem e devem crescer quando novas memórias e registros forem incorporados.

### Bloco 3 — ainda requer aprofundamento autoral

O conteúdo-base já existe, mas a revisão autobiográfica detalhada ainda precisa ser feita. Próximo arco prioritário:

`Mirantte News → Tiago Luz → Search → especialização → contas → Herik Mourão → CookieWEB → Beleza na Web → Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto`.

Não tratar o texto atual desse período como versão final. Ele é uma base cronológica funcional.

---

## 9. Regra para futuras sessões

Ao retomar o projeto:

1. ler `docs/hub-continuity-guide.md`;
2. ler este documento;
3. buscar a `main` atual antes de escrever;
4. atualizar a entrada primeiro na vertical PT;
5. produzir/revisar a versão EN equivalente;
6. rodar `editorial_parity.py --check` e confirmar que o drift é detectado;
7. aceitar explicitamente a nova revisão com `--accept ENTRY_ID`;
8. regenerar a Full Bio;
9. rodar os audits completos;
10. publicar apenas após verificar CI e Pages.

Nunca duplicar manualmente conteúdo da vertical na Full Bio.

---

## 10. Princípio editorial permanente

O HUB continua sendo autobiografia, não auditoria.

Documentação é lastro, não protagonista.

A Full Bio deve preservar simultaneidade, continuidade e densidade humana. A infraestrutura existe para impedir divergência e esquecimento — não para transformar o texto público em relatório técnico.
