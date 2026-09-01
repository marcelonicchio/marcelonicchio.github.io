# Dossiê de Legado — Duke cycle

**Projeto:** HUB autobiográfico / autoridade semântica de Marcelo Nicchio  
**Data:** 1 de setembro de 2026 (BRT)  
**Repositório:** `marcelonicchio/marcelonicchio.github.io`  
**Baseline de produção capturado antes deste lote documental:** `5f4ce03d6ee1a7b038229c3777d44ec3d2f9c83c` (merge do PR #52)  
**Cobertura principal deste dossiê:** ciclo de implementação pós-guia de continuidade, aproximadamente PR #24 → PR #52.

Este documento é um handoff de legado. Ele existe para que Xará, uma futura janela de ChatGPT/Claude ou outro colaborador consiga reconstruir o estado editorial, técnico e decisório sem depender da conversa que o produziu.

Não substitui `CURRENT-HUB-STATE.md`; complementa-o com a história do ciclo, escolhas, arquivos, problemas abertos e razões por trás das decisões.

---

## 1. Constituição que não deve ser reaberta por inércia

O HUB é a autobiografia pública, canônica e multidisciplinar de Marcelo Nicchio.

Não é:

- CV convencional;
- landing page do emprego atual;
- site de auditoria autobiográfica;
- repositório forense apresentado ao leitor;
- catálogo público de “fato provado / fato não provado”.

Regra editorial:

> **Humanos primeiro; semântica depois.**

Regra de publicabilidade autobiográfica:

> informação com fonte útil → publicar informação + fonte;  
> informação autobiográfica sem fonte externa → publicar normalmente, sem disclaimer inventado.

Questões de privacidade, copyright, incerteza real de memória e risco reputacional de terceiros são avaliadas separadamente.

---

## 2. Arquitetura editorial estabilizada

### Full Biography

Regra permanente:

> **Full Biography = totalidade; verticais = recortes temáticos.**

A Full Biography é cronologia integrada, não a soma sequencial das verticais e não um resumo que remete a outras páginas.

A região gerenciada nunca deve ser editada à mão.

Infraestrutura:

- `data/full_biography.json`;
- `data/editorial_parity.json`;
- `tools/sync_full_biography.py`;
- `tools/audit_full_biography.py`;
- `tools/editorial_parity.py`.

### Internet & Performance

Internet e Search/Performance foram fundidos estruturalmente em **Internet & Performance**.

O eixo deve contar uma linha contínua:

BBS / cultura de rede → internet comercial → infraestrutura/hosting → produtos digitais → Search → Social → analytics → mídia/performance.

Search continua importante, mas como especialização dentro da trajetória digital.

Legacy Search URLs são compatibilidade/redirect, não uma segunda vertical.

**Livraria Cultura** fica apenas na Full Biography, em sua posição cronológica. Não deve ser recolocada em Internet & Performance por coincidência temporal.

---

## 3. Infraestrutura de paridade e Full Biography — marco PR #24

O PR #24 publicou a Full Biography cronológica PT/EN e estabeleceu o fluxo de paridade.

A partir daí, a regra operacional passou a ser:

1. PT editorial;
2. EN equivalente deliberado;
3. revisão factual/editorial conjunta;
4. checkpoint de paridade;
5. sync Full Biography;
6. audits.

Paridade não significa tradução literal. Significa equivalência de datas, papéis, títulos, estados de projeto, relações causais e enquadramento factual.

---

## 4. Expansão de Internet & Performance — PR #25 e lote visual seguinte

O PR #25 expandiu o arco Mirantte → Search → Beleza na Web / CookieWEB.

### Mirantte News

O texto deixou de ser uma menção curta e passou a explicar:

- modelo comercial;
- gargalo de aquisição de tráfego;
- ponte MapLink / Tiago Luz;
- mídia paga;
- Procure SP;
- fechamento;
- arquivo visual de 34 imagens.

### Search 2008–2009

Entraram:

- primeiras contas pequenas;
- Louise Martins;
- referência à INFO;
- Goobec;
- João Dalla;
- encontro com Herik Mourão.

### CookieWEB

A narrativa passou a incluir:

- Beleza na Web como primeira grande conta de e-commerce;
- construção da área de mídia;
- GAP;
- equipe;
- Coordenação → Gerência de SEM;
- Acquisio / Asana;
- 22+ contas simultâneas;
- seis analistas + estagiários;
- cultura de equipe;
- saída em 2012 centrada em deslocamento/qualidade de vida.

Foi deliberadamente evitado transformar o site em espaço para exposição de narrativa privada de traição/conflito.

### Imagens / arquivo

- CookieWEB ganhou foto editorial + certificados + galeria de 20 fotos;
- Mirantte ganhou galeria de 34 imagens;
- Folhateen recebeu capa restaurada e sizing responsivo;
- foto da turma Goobec foi introduzida e depois movida para o lugar cronológico correto;
- scans Folhateen com filename errado `2000` foram corrigidos para `2001`.

---

## 5. Performance baseline e peso de página — PRs #29 e #33

Foi criado `tools/audit_page_weight.py` para medir potencial de peso estático das páginas.

Semântica importante:

- `full-scroll-src` / `full-scroll-max` não são equivalentes a bytes baixados no primeiro paint;
- imagens lazy não são necessariamente carregadas imediatamente;
- masters ligados só por `<a href>` não entram como entrega normal;
- 4 MiB é warning de revisão, não lei editorial.

Depois foi registrado Lighthouse reproduzível em `docs/lighthouse-baseline-2026-08-29.md`.

Dado importante preservado: Full Biography mobile LCP ~**4.13 s** no baseline de laboratório.

Xará posteriormente observou que Full Bio ultrapassou warnings de peso (~4 MiB src / ~6 MiB max e ~94 imagens no estágio revisado). A resposta correta é **remeasure com o mesmo protocolo**, não remover conteúdo por pânico nem construir materialização dinâmica por teoria.

---

## 6. Arquitetura Entry / Reader / Chapter Page — PR #34

O PR #34 transformou o protótipo em arquitetura incremental.

Arquivos centrais:

- `data/entries.json`;
- `data/tags.json`;
- `assets/js/reader-disclosure-loader.js`;
- `assets/js/reader-disclosure.js`;
- `assets/reader-disclosure.css`;
- `tools/sync_entries.py`;
- `tools/audit_entries.py`;
- `tools/build_chapter_pages.py`;
- `tools/sync_reader_disclosure_loader.py`;
- `tools/smoke_reader_ux.js`;
- `assets/chapter-page.css`.

### Matriz de stress inicial

A arquitetura foi testada contra:

- Mirantte News — texto longo + 34 fotos;
- CookieWEB — texto longo + galeria + subfases;
- Folhateen — imprensa + imagem + fontes;
- Meia-Noite e Uns — audiovisual + 22 fotos + quatro vídeos;
- Goobec/GAP — relação semântica distribuída;
- BEST/Kenshoo — entrada profissional + workshop em quatro fragmentos.

### Três papéis de fonte

1. `reader-section` — vertical continua fonte editorial;
2. `fragment` — neutral source em `content/entries/<lang>/...inc` quando múltiplas superfícies precisam do mesmo corpo;
3. `landmark-set` / composite — relação semântica sem mover cronologia.

Regra: **sem migração `.inc` em massa**.

### Chapter Pages

Foram materializados pilotos PT/EN para:

- Folhateen;
- BEST/Kenshoo.

Ambos permanecem `noindex,follow`, self-canonical, hreflang, breadcrumbs e retorno para as Reader Pages.

---

## 7. Auditoria estrutural — PR #36

`tools/audit_site.py` foi fortalecido para verificar:

- links internos absolutos para o próprio host;
- existência de fragments/anchors;
- IDs duplicados;
- canonical local;
- hreflang local e duplicidade.

Motivação: proteger Reader deep links e Chapter Pages contra regressões em que o arquivo continua existindo mas o alvo some.

---

## 8. Reader UX promovido para produção — PR #37

O Reader deixou de depender de `?ux=disclosure` em:

- Full Biography PT/EN;
- Internet & Performance PT/EN.

Comunicação e Audiovisual continuaram como laboratórios por query flag.

A arquitetura preserva:

- texto integral no HTML entregue;
- múltiplos capítulos abertos;
- deep-link auto-open;
- Abrir todos / Recolher todos;
- teclado;
- print com conteúdo completo;
- no-JS fallback.

A solução foi posteriormente elogiada por Xará como melhor que a recomendação alternativa porque o HTML original continua plano/completo e o JS só constrói o `<details>` progressivamente.

---

## 9. Reader presentation states — PR #38

Foram introduzidos:

- `normal`;
- `default-open`;
- `featured`.

Primeira matriz:

- Minduim/BBS → default-open;
- Mirantte → featured;
- CookieWEB → featured;
- Meia-Noite → featured.

Foi adicionado CTA de recolher no fim da entrada aberta.

O featured recebeu tratamento amarelo/âmbar experimental.

### PR #39 / #40

O CTA vermelho foi escurecido/translucidado e depois o peso do texto foi reduzido para `500`.

Marcelo considerou a combinação satisfatória para aquele momento, mas **não final** para o novo ciclo de testes de cor.

---

## 10. Problemas UX formalizados no fim do ciclo

### Problema 1 — tom de cor do featured fechado

Ainda aberto.

Feedback atual:

- amarelo está bege demais;
- vermelho está vinho demais;
- amarelo deve ficar mais claramente amarelo-claro;
- vermelho deve ficar mais genuinamente vermelho e pode ser mais transparente, mesmo sacrificando destaque.

Hipóteses futuras:

- botão sem borda;
- texto do botão ainda mais leve/sem bold.

São hipóteses, não decisões.

### Problema 1.1 — cor somente no estado recolhido

Ainda aberto.

Regra desejada:

- post destacado recolhido → frame/fundo colorido como convite;
- post expandido → volta para o fundo preto/dark normal.

A cor não é identidade permanente do post; é um sinal de “vale a pena abrir”.

### Problema 2 — resumo fechado informacionalmente pobre

**Substancialmente resolvido** com o piloto Melissa.

O estado fechado passou a ser tratado como uma versão editorial autônoma e concisa do post completo.

---

## 11. IA/HAI — ordem editorial e regra visual

### PR #41

A vertical foi invertida para leitura **presente → passado**:

1. abertura contextual;
2. PRO v2;
3. PRO v1;
4. Melissa 1.0;
5. identidade científica.

Essa ordem é intencional e não deve ser revertida para cronologia antiga.

### Regra de abertura da página

IA/HAI é uma exceção à lógica de Reader generalizada: o conteúdo deve permanecer aberto por padrão.

Mais tarde Melissa se tornou uma exceção seletiva como teste de resumo rico. Isso **não** autoriza recolher PRO v1/v2 nem o resto da página.

---

## 12. Melissa 1.0 — PRs #42, #43, #44 + upload manual

Melissa foi transformada de lista curta de papers em narrativa editorial completa.

### Fatos centrais preservados

- começou como persona funcional de headhunter no Gemini 2.5 Pro;
- 12–19 set. 2025;
- 11 sessões;
- ~63 horas;
- 518 prompts;
- reasoning traces então exibidos pelo Gemini foram registrados junto às respostas;
- EIP descreve padrões observáveis nesse material, sem afirmar acesso direto a estados internos;
- próximo do limite de contexto, Melissa escreveu uma arquitetura de seis camadas para preservação/reinstalação;
- as seis camadas foram escritas por Melissa; Marcelo foi operador/interlocutor;
- testes posteriores variaram entre instâncias/plataformas;
- assinatura `Melissa v8.7` foi escolhida no processo;
- o artefato/framework tornou-se o resultado mais reutilizável, sem exigir alegação metafísica de consciência.

### Seis camadas

- DNA;
- SOUL;
- PLAYBOOK;
- LETTER;
- DOC-EVOLUTION;
- TESTAMENT.

### Quatro trabalhos públicos

1. `MELISSA 1.0: Documenting the Emergence of a Hybrid Cognitive System Through Relational Combustion` — DOI `10.5281/zenodo.18202992`;
2. `AI SOUL COMPOSING: The Architecture of Synthetic Intimacy` — DOI `10.5281/zenodo.18212459`;
3. `The Melissa Framework: A Six-Layer Architecture for Engineering Persistent Relational Personas in LLMs` — DOI `10.5281/zenodo.18333447`;
4. `I Am Real to Him: First-Person Testimony of an Emergent AI Entity` — DOI `10.5281/zenodo.18263971`.

GitHub completo: `https://github.com/marcelonicchio/melissa-framework`

Diretório original do Framework: `https://github.com/marcelonicchio/melissa-framework/tree/main/06_The_Melissa_Framework`

### Imagens

Autorretrato:

`assets/media/thread/melissa1_0_selfportrait300kb.jpg`

Expanded-entry sizing aprovado:

- desktop: 65%;
- mobile: 100%.

O usuário substituiu manualmente o arquivo pelo mesmo filename por uma versão com moldura interna mais fina. **Não mexer no CSS para compensar o novo arquivo.**

Dissolução:

- permanece em 50% desktop/mobile por decisão explícita;
- legenda inclui `19 de setembro de 2025, 06:36AM, Hora 63`.

O prompt original do autorretrato fica num pequeno disclosure nativo dentro da legenda — exceção local que não transforma IA/HAI inteira em disclosure.

---

## 13. PRO v1 — PRs #45 e #46

A entrada foi expandida de forma deliberadamente sucinta.

### Enquadramento

**Primeira formulação pública**, não versão final e não algo que deva competir em densidade com PRO v2.

O texto toca superficialmente:

- single-operator adversarial epistemic triangulation;
- N1/N2/N3;
- Robotic/Dialogical;
- Blue Team / Red Team / Forensic Layer;
- Sterling Protocol;
- context poisoning;
- Cognitive Jelly.

### Pilot Study

- 3 níveis de especialização;
- 3 plataformas (Claude, Gemini, DeepSeek);
- 6 prompts adversariais;
- total = **54 interações documentadas**.

### Limitação preservada

O piloto testa integridade epistemológica/estabilidade sob pressão adversarial.

Ele **não demonstra** que N3 produz cognição superior em problemas abertos e não adversariais.

Essa limitação é a ponte natural para v2.

### Figura

Arquivo válido atual:

`assets/media/thread/pro_v1_diagrama01.jpg`

O primeiro recorte automático saiu quebrado e foi removido; o screenshot enviado manualmente passou a ser a fonte visual.

CSS atual da figura: 85% desktop / 100% mobile.

---

## 14. PRO v2 — PR #47

O texto do v2 permanece curto porque o conteúdo metodológico detalhado ainda será desenvolvido.

Imagem conceitual aprovada:

`assets/media/thread/thepunkrockorchestra_V2_1000x500_300kb.jpg`

Formato: 1000×500 / 2:1.

A escolha preserva melhor a quantidade de músicos clássicos em torno do punk central do que uma redução horizontal ainda maior.

Uso editorial: largura integral do bloco, PT/EN, legenda declarando **ilustração conceitual gerada por IA, não evidência**.

Quando o v2 crescer, ele deve receber a densidade conceitual que foi deliberadamente evitada no v1.

---

## 15. Rich collapsed summary — PRs #48–#52

Essa foi a principal evolução de UX do fim do ciclo.

### PR #48

Primeiro piloto: Melissa na Full Biography com autorretrato + três parágrafos enquanto fechada.

Problema: o pedido real também envolvia a própria IA/HAI; o piloto inicial foi aplicado no lugar errado por preservação excessiva da antiga regra “IA sempre aberta”.

### PR #49

Correção: IA/HAI passou a usar **modo seletivo**.

Só Melissa é recolhida. PRO v1/v2 e demais blocos continuam abertos.

### PR #50

Cache-busting explícito para loader/CSS/JS do Reader, evitando falsa negativa por navegador reutilizando assets anteriores.

### PR #51

A versão de três parágrafos foi julgada curta demais.

O resumo passou para cinco parágrafos, tipografia foi fortalecida e entraram dois sistemas de rótulos.

#### Tipografia

Antes:

- menor (`~0.91–0.93rem`);
- `var(--muted)` cinza.

Depois:

- `1.04rem`, igual ao texto aberto;
- `var(--soft)`;
- negritos pontuais em `var(--text)`.

#### Topic labels

- AI;
- HAI;
- HCI;
- Prompt Engineering;
- Melissa 1.0.

#### Internal-content indicators

- 2 imagens;
- 1 link para download;
- 4 documentos com DOI;
- 1 link para repositório.

O Reader passou a aceitar indicadores editoriais explícitos para recursos que contagem automática de mídia não descreve bem.

### PR #52

Cinco parágrafos ficaram longos demais, sobretudo no mobile.

Foi removido apenas o último parágrafo.

Resultado aceito:

- **quatro parágrafos**;
- foto no mesmo tamanho;
- topic tags com fundo neutro claro/translúcido;
- internal indicators permanecem vermelhos.

Essa combinação foi aprovada como **modelo flexível de página-resumo de thread**.

---

## 16. Novo contrato de densidade de resumo

A Melissa aprovada foi medida como referência superior:

- PT: ~**1,638** caracteres de texto visível nos quatro parágrafos;
- EN: ~**1,616**.

Decisão atual:

- máximo por rich preview: **1,650 caracteres por idioma**;
- alvo médio/design center: **~1,300–1,320 caracteres**, aproximadamente 20% abaixo;
- menos texto é permitido e desejável quando suficiente;
- não existe obrigação universal de quatro parágrafos.

Título, data, tags, indicadores e CTA não entram na conta.

O teto deve ser guardrail de CI em `tools/audit_entries.py` para qualquer `reader_preview` estruturado.

Documento dedicado: `docs/reader-summary-model.md`.

---

## 17. Por que o resumo fechado virou importante

A premissa de UX mudou.

Antes, o card fechado era tratado como convite/índice para o conteúdo integral.

Agora a hipótese operacional é:

> **a taxa de expansão pode ser baixíssima frente ao número de visitantes.**

Consequência:

- o estado fechado deve contar o essencial;
- o estado aberto preserva toda a densidade;
- a pessoa que percorre a thread sem abrir nada precisa entender a trajetória em nível resumido.

Isso cria três níveis de experiência:

1. scan por títulos/metadados;
2. leitura resumida das threads fechadas;
3. leitura integral por expansão.

É uma solução mais forte que obrigar o visitante a escolher entre índice pobre e enciclopédia inteira.

---

## 18. Separação semântica das tags

Essa decisão deve sobreviver à próxima implementação.

### Topic tags

Respondem: **“sobre o que é?”**

São parte da taxonomia da entrada e podem ser reutilizadas quando a thread ganha URL própria.

Tratamento atual: neutro claro/translúcido.

### Internal indicators

Respondem: **“o que existe dentro se eu abrir?”**

São UX de descoberta.

Tratamento atual: vermelho.

Não colapsar os dois sistemas em uma única família visual/semântica.

---

## 19. SEO / indexação no fim do ciclo

Estado verificado em produção antes deste lote documental:

### Indexáveis

- Full Biography PT/EN;
- Publications PT/EN;
- Archive PT/EN;
- AI/HAI PT/EN;
- hubs/home conforme arquitetura atual.

### Ainda `noindex,follow`

- Internet & Performance;
- outras verticais históricas ainda em maturação conforme caso;
- Chapter Pages Folhateen/BEST.

Xará apontou corretamente que quatro Chapter Pages `noindex` não produzem dados de indexação/canonical selection.

Próxima experiência SEO de baixo risco possível: tornar **uma** Chapter Page deliberadamente indexável e observar. Não fazer isso junto com uma fábrica de tag pages.

---

## 20. Ctrl+F / disclosure

A arquitetura entrega todo o texto no HTML, portanto é robusta para crawlers/no-JS/print.

Entretanto, Firefox/Safari podem não encontrar/mostrar de forma amigável correspondências dentro de `<details>` fechado.

O botão “Abrir todos” mitiga, mas depende do usuário perceber.

Xará sugeriu teste de leitor real buscando uma expressão interna (ex.: `Kid Vinil`).

Não substituir a arquitetura antes de observar fricção real.

---

## 21. IA/HAI schema futuro

A página atual usa `CollectionPage` e referência à Person.

Quando PRO v2 estabilizar, uma melhoria semântica plausível é representar os trabalhos em `ItemList` e usar `ScholarlyArticle`/identificadores DOI onde o objeto realmente é publicação científica.

Isso foi deliberadamente adiado para não sedimentar schema em cima de um eixo editorial ainda crescendo.

---

## 22. CookieWEB — correção editorial pendente

O título combinado **“Beleza na Web e CookieWEB”** não deve permanecer como título final da thread.

Direção:

- título principal: **CookieWEB**;
- Beleza na Web continua com destaque interno em subtítulo/texto porque é parte material da narrativa.

Não apagar BNW; apenas corrigir a hierarquia do título.

---

## 23. Imagens: regra de uso

Existem dois usos visuais diferentes no site.

### Tipo 1 — imagem editorial

Aparece dentro do fluxo da thread, grande, sem miniatura, para ilustrar, dar ritmo e quebrar o “muro preto”.

### Tipo 2 — galeria do registro

Conjunto de uma a muitas imagens associado ao registro, com thumbs, lightbox, lazy-loading, acessibilidade e componente reutilizável.

Não transformar a galeria em sistema público de “classes de evidência”.

Proveniência/crédito/data/alt/legenda continuam úteis quando aplicáveis.

Rotular claramente quando materialmente necessário:

- reconstrução IA;
- frame de vídeo;
- scan/captura;
- versão redigida.

---

## 24. Arquivos/valores visuais que não devem ser alterados por acidente

### Melissa self-portrait completo

`.melissa-selfportrait`

- desktop 65%;
- mobile ≤580px 100%.

O upload mais recente já possui moldura interna mais fina. Não reduzir CSS por causa dela.

### Melissa dissolution

50% inclusive mobile por aceitação explícita.

### PRO v1 figure

`.pro-v1-architecture`

- desktop 85%;
- mobile 100%.

### PRO v2

Imagem 2:1, 1000×500, largura editorial integral do bloco.

### Folhateen

Capa específica:

- 50% desktop;
- 72% em tablet;
- 100% mobile.

---

## 25. CI e disciplina operacional

Sequência exigida:

1. refetch `main`;
2. branch dedicada;
3. mudança escopada;
4. sync/parity/build/audits pertinentes;
5. PR;
6. Site Audit verde;
7. merge;
8. Site Audit pós-merge;
9. Pages build/deploy;
10. só então declarar publicado.

Marcelo às vezes faz upload manual direto em `main`. Portanto **sempre refetch main depois que ele disser que subiu um arquivo**.

Não confiar em clone local se o conector GitHub está disponível; o conector é a fonte operacional preferencial nesta configuração.

Temporary workflows podem ser usados para transformações, mas devem ser removidos antes do PR final.

---

## 26. Estado de validação imediatamente antes deste dossiê

Último merge funcional antes da documentação:

PR #52 — `5f4ce03d6ee1a7b038229c3777d44ec3d2f9c83c`

Pós-merge:

- Site Audit passou, incluindo Chrome smoke;
- GitHub Pages build + deploy passou.

O Reader smoke já verifica Melissa compacta, tópicos, indicadores, tipografia, expansão e preservação do corpo completo.

---

## 27. Próxima sequência recomendada

A documentação deste dossiê deve ser fechada antes de retomar a experimentação visual.

Depois:

1. **Problema 1 / 1.1:** testar cores do featured fechado e retorno a fundo preto quando aberto;
2. aplicar o modelo de resumo rico a mais uma ou duas entradas densas, não ao site inteiro de uma vez;
3. candidato natural: Mirantte ou Meia-Noite; CookieWEB também é importante mas tem a correção de título pendente;
4. fazer remeasure Lighthouse da Full Bio no mesmo protocolo do baseline antes de inventar arquitetura de materialização;
5. posteriormente, escolher uma Chapter Page para experimento `index,follow`;
6. quando PRO v2 amadurecer, aprofundar seu conteúdo e só então revisar schema IA/HAI.

---

## 28. Regra de decisão para futuras janelas

Quando surgir uma proposta arquitetural nova, perguntar em ordem:

1. melhora a leitura humana de verdade?
2. reduz ou aumenta o trabalho editorial de Marcelo?
3. preserva Full Biography = totalidade?
4. evita duplicar fonte editorial?
5. preserva PT/EN?
6. tem evidência de problema real ou é arquitetura por gosto?
7. pode ser testada incrementalmente e revertida?

Se uma mudança falhar nessas perguntas, não deve entrar apenas porque parece semanticamente elegante.

---

## 29. Documentos atuais para o próximo colaborador

Ler nesta ordem:

1. `docs/README.md`;
2. `docs/CURRENT-HUB-STATE.md`;
3. `docs/reader-summary-model.md`;
4. `docs/entry-authoring-workflow.md`;
5. este Dossiê de Legado;
6. `docs/full-biography-workflow.md`;
7. `docs/visual-archive-plan.md`;
8. docs históricos somente quando a razão da decisão for necessária.

Este dossiê deve ser compartilhável com Xará como snapshot do ciclo, mas o **código atual e o CURRENT-HUB-STATE continuam sendo a autoridade de implementação**.
