# HUB Marcelo Nicchio — Guia de continuidade editorial e técnica

**Status deste documento:** **histórico/fundacional — snapshot de 27 de agosto de 2026**  
**Atualizado em:** 27 de agosto de 2026  

> Para o estado atual, leia primeiro `docs/README.md` e `docs/CURRENT-HUB-STATE.md`. Este guia preserva a constituição e o contexto do ciclo anterior; detalhes de implementação que mudaram depois de 27/08 não são autoridade de estado.  
**Site:** https://marcelonicchio.github.io  
**Repositório:** `marcelonicchio/marcelonicchio.github.io`

Este documento existe para evitar perda de contexto entre colaboradores, assistentes, ciclos de edição e futuras revisões do HUB. Ele deve ser lido antes de qualquer alteração estrutural relevante no site.

O objetivo não é congelar o projeto. O objetivo é preservar as decisões que já foram tomadas, explicitar a arquitetura e impedir regressões conceituais — especialmente a transformação do HUB em currículo convencional, página de auditoria, repositório de provas ou site excessivamente defensivo.

---

## 1. O que este site é

O HUB é a autobiografia pública, canônica e multidisciplinar de Marcelo Nicchio.

Ele organiza uma trajetória que começa no fim dos anos 1980 e atravessa, com sobreposições:

- Música;
- Comunicação e cultura;
- Internet & Performance;
- Audiovisual;
- pesquisa independente em IA / Human–AI Interaction.

A estrutura existe para mostrar **uma vida composta por campos que se cruzam**, e não várias carreiras isoladas.

O site deve funcionar simultaneamente como:

1. narrativa humana;
2. identidade canônica;
3. arquivo histórico progressivo;
4. referência semântica de autoridade;
5. ponto de reconciliação entre nomes, trabalhos, registros e presença pública.

O nome canônico é **Marcelo Nicchio**. Variantes históricas podem incluir Marcelo Henrique Nicchio, Marcelo H. Nicchio e Marcelo Minduim.

A prioridade editorial é sempre:

> **humanos primeiro, semântica depois.**

SEO, GEO, AEO, schema, arquivos estruturados e consistência de entidade são importantes, mas nunca devem transformar a leitura em um relatório técnico.

---

## 2. O que este site não é

O HUB **não é**:

- um CV tradicional;
- uma landing page profissional centrada apenas no emprego atual;
- uma página de auditoria;
- um repositório forense de evidências;
- uma defesa judicial da própria biografia;
- um inventário de “fatos comprovados versus não comprovados” apresentado ao visitante;
- um site cujo protagonista seja a documentação.

A documentação existe como **lastro**, não como protagonista.

### Regra permanente: sem estética forense

Evitar no texto público construções recorrentes como:

- “não há comprovação independente de...”;
- “isto não significa que...”;
- “esta publicação não representa validação...”;
- “não estamos afirmando X, Y ou Z...”;
- classificações visíveis de nível de evidência;
- disclaimers defensivos que não foram motivados por uma afirmação concreta.

Esse tipo de linguagem pode ser útil **nos bastidores editoriais**, mas não deve contaminar a autobiografia.

O fato de um trabalho ter DOI, estar em Zenodo, SSRN, OSF, PubPub, GitHub ou outra plataforma pode ser apresentado diretamente. Se um dia houver peer review, conferência, revista, prêmio, endosso público ou outra validação externa, o site passa a dizer isso quando existir.

Não é necessário adicionar um aviso dizendo que a ausência de endosso formal existe.

---

## 3. Arquitetura pública principal

O HUB está organizado em cinco campos temáticos:

1. **Música**
2. **Comunicação**
3. **Internet & Performance**
4. **Audiovisual**
5. **IA / HAI**

Além deles existem:

- Home;
- Biografia Completa;
- Publicações;
- Arquivo;
- Projetos selecionados;
- dados estruturados.

As páginas temáticas aprofundam cada campo. A **Biografia Completa** deve recompor os fatos em uma linha do tempo integrada.

---

## 4. Regra fundamental: a vertical é a fonte editorial

A evolução do projeto exige evitar duplicação manual entre as páginas temáticas e a Biografia Completa.

A regra é:

> **A entrada é escrita e mantida na vertical. A Biografia Completa é derivada dessa entrada.**

Exemplo:

```text
/pt/internet/ → Petlove
        ↓
sync_full_biography.py
        ↓
/pt/biografia/ → Petlove
```

Quando o texto de Petlove for melhorado na vertical, a Biografia deve ser regenerada a partir da mesma unidade editorial.

O objetivo é impedir duas versões divergentes do mesmo episódio.

### Arquivos centrais desta arquitetura

Quando a implementação da nova Full Bio estiver em `main`, os arquivos centrais serão:

- `data/full_biography.json`
- `tools/sync_full_biography.py`
- `tools/audit_full_biography.py`
- `pt/biografia/index.html`
- `en/biography/index.html`

O manifesto `data/full_biography.json` controla:

- ordem cronológica;
- domínio;
- período;
- fonte de cada entrada;
- selector da unidade editorial;
- eras;
- entradas especiais de contexto;
- PT/EN.

O sincronizador extrai o conteúdo das verticais e monta a área gerenciada da Biografia.

O auditor verifica que:

- as entradas declaradas existem;
- os seletores resolvem corretamente;
- PT e EN mantêm cobertura;
- novas unidades importantes não ficam órfãs;
- a Biografia está sincronizada.

---

## 5. Chapters grandes e subunidades invisíveis

Nem toda vertical deve ser quebrada visualmente em dezenas de blocos apenas para servir à Biografia.

Exemplo importante: **Música → Palcos, discos e expansão**.

Na vertical, o bloco pode permanecer editorialmente coeso. Internamente, subfases podem receber identificadores estáveis como:

```html
<div class="phase" data-bio-key="music-olympia-2000">...</div>
```

ou:

```html
<div data-bio-key="music-coitado-1992">...</div>
```

Isso permite à Biografia puxar unidades específicas sem destruir a composição temática da vertical.

### Casos já definidos no eixo Música

A Biografia deve poder tratar separadamente:

- 1992 — fundação e primeiro show;
- 1993–1995 — circuito paulistano;
- 1994 — demo-tape e Kid Vinil;
- 1997 — *Meu Querido Diário*;
- 1998–1999 — divulgação / festival;
- 1999–2000 — *Eu Não Tô Nem Aí*;
- julho de 2000 — Olympia;
- 21 de junho de 2001 — Programa do Jô;
- 2001–2003 — atividade contínua;
- 2003 — encerramento oficial;
- dezembro de 2023 — reunião pontual.

### Importante

Subunidades `data-bio-key` são infraestrutura editorial. Não devem aparecer como jargão técnico no texto público.

---

## 6. Coitado do Próximo — cronologia consolidada

### Regra geral

O **Coitado do Próximo** foi fundado em 1992, passou por diversas formações e permaneceu continuamente ativo até o encerramento oficial em 2003.

Marcelo Nicchio e o vocalista formaram o núcleo do projeto desde o início.

Não tratar 1993 como “início da banda”. 1993 marca o começo de apresentações mais estruturadas no circuito de casas noturnas.

### Primeiro show — informação confirmada por vídeo original

**Data:** 5 de julho de 1992  
**Local:** Escola Estadual “Barão Homem de Mello”  
**Endereço:** Rua Alfredo Pujol, 1555 — Santana — São Paulo, SP  
**Registro:** trecho da abertura do show, com marcação de data e hora da câmera  
**YouTube:** https://www.youtube.com/watch?v=7yjYTV1L0b0

Essa data não deve mais ser tratada como aproximada.

O vídeo é registro primário do próprio evento e pode ser usado como lastro audiovisual do primeiro show.

### Formulação recomendada na vertical

O texto deve deixar claro que:

- a banda foi fundada em 1992;
- o primeiro show conhecido/preservado aconteceu em 5 de julho de 1992;
- o registro de vídeo contém marcação de data e hora da câmera;
- em 1993 começam os shows mais estruturados;
- a atividade da banda prossegue continuamente até 2003.

---

## 7. Biografia Completa — princípio narrativo

A Biografia Completa não deve voltar ao formato:

> Música resumida → Comunicação resumida → Internet resumida → Audiovisual resumido → IA resumida.

Esse desenho falha porque transforma uma trajetória simultânea em cinco mini-CVs.

A nova arquitetura deve apresentar uma **única linha cronológica**, permitindo alternância entre domínios.

Exemplo de leitura correta:

```text
Música
→ BBS
→ Comunicação
→ Música
→ Rádio
→ Internet
→ Música
→ Audiovisual
→ PSINet
→ Olympia
→ Livraria Cultura
→ Folha
→ Programa do Jô
→ ...
```

O leitor deve perceber que esses campos coexistiam.

### Entradas separadas aprovadas

Olympia, Programa do Jô e reunião de 2023 podem e devem ser entradas independentes quando isso melhora a história.

### Eras

As eras servem como respiração visual e organização, não como caixas rígidas de carreira.

A arquitetura experimental utiliza faixas como:

- 1989–1991 — Formação;
- 1992–2000 — Música, BBS, rádio, internet e audiovisual em paralelo;
- 2001–2008 — presença pública, comunicação, televisão e produto digital;
- 2008–2015 — Search, performance e escala operacional;
- 2016–2024 — operações, audiovisual e retornos;
- 2025–2026 — pesquisa independente em IA/HAI.

Essas faixas podem ser refinadas editorialmente, mas o princípio de cronologia integrada deve ser preservado.

---

## 8. IA / HAI — política editorial

A página IA/HAI apresenta a produção independente de pesquisa de Marcelo Nicchio.

Os trabalhos e seus registros devem ser descritos diretamente.

### O que não deve voltar

Foi removida em agosto de 2026 a linguagem defensiva do tipo:

- “Publicação não é validação automática”;
- “Escopo preciso” usado como disclaimer;
- listas do que o site “não está afirmando”;
- links de “Rigor editorial” que transformavam a página em auditoria.

Essa remoção é deliberada e permanente salvo razão editorial específica futura.

### Regra

Se os trabalhos estão depositados em repositórios e possuem DOI, o site pode dizer isso.

Se futuramente houver publicação formal em revista, conferência, peer review, convite institucional, citação relevante ou endosso público, acrescenta-se a nova informação factual.

Não antecipar validações futuras, mas também não inserir avisos desnecessários sobre a ausência delas.

### Melissa / PRO

A arquitetura atual reconhece:

- série Melissa 1.0;
- Punk Rock Orchestra v1;
- Punk Rock Orchestra v2 em desenvolvimento;
- múltiplos repositórios como instâncias do mesmo trabalho/versão, não como “cinco publicações diferentes”.

DOI/deposit não deve ser chamado automaticamente de peer review.

---

## 9. Internet & Performance — vertical única

Search não é uma vertical separada.

O campo permanente é **Internet & Performance**.

A narrativa correta começa antes de Google Ads:

1. BBS / SP Online-STI / Mandic / Minduim;
2. transição para internet comercial;
3. PSINet / hosting;
4. Mirantte News / produto digital / aquisição;
5. SEM / Google Advertising Professional;
6. CookieWEB;
7. Petlove;
8. Clickland;
9. BEST / Kenshoo;
10. Ad.Dialetto;
11. operações independentes;
12. Driven.cx.

O argumento editorial é de continuidade entre redes, sistemas online, produto digital, audiência, aquisição, Search, Social, analytics e performance.

### URLs

Canônicas:

- `/pt/internet/`
- `/en/internet/`

Legadas:

- `/pt/search-performance/`
- `/en/search-performance/`

As legadas devem permanecer apenas como redirects de compatibilidade, `noindex,follow`.

---

## 10. Clickland e Driven — nuance obrigatória

### Clickland

- fundada em setembro de 2012 por Marcelo Nicchio e Carlos Portela;
- atividade comercial regular diminuiu posteriormente;
- empresa não foi encerrada;
- permanece como estrutura operacional/de apoio;
- pode aparecer como 2012–presente;
- não deve ser apresentada como ocupação profissional principal atual.

### Driven.cx

- 2023–2024;
- operação full-time remota;
- é posterior cronologicamente à fundação da Clickland;
- encerrou em 2024.

Não ordenar a trajetória de modo que Clickland pareça obrigatoriamente o último emprego apenas porque juridicamente continua existente.

---

## 11. Livraria Cultura

Passagem curta, fora dos eixos profissionais principais:

- aproximadamente outubro de 2000 a janeiro de 2001;
- cerca de três meses;
- *summer job*;
- venda de livros técnicos;
- Shopping Villa-Lobos.

Ela pertence à **Biografia Completa** como parêntese cronológico.

Não criar uma vertical para isso.

Na arquitetura de Full Bio, conteúdo exclusivo desse tipo pode existir como fragmento interno `.inc`, e não como falsa página `.html` pública.

---

## 12. Audiovisual — escopo e cautela

Não inflar o eixo audiovisual para sugerir uma carreira cinematográfica contínua que não existiu.

O campo registra episódios concretos de criação, produção, direção, televisão e projetos audiovisuais.

### Meia-Noite e Uns

Registros públicos preservados no YouTube:

- Bloco 1 — `kLQAlzgwmy0`
- Bloco 2 — `f-JZfMoHh1I`
- Bloco 3 — `6s6843Mq5MA`
- vinheta/créditos — `tIGlLDpzQ7E`

Créditos confirmados diretamente:

- Marcelo Nicchio — Direção Artística;
- co-Produção Executiva com Cristiano Gonçales;
- Dreamsnetwork.tv — realização.

Outros elementos autobiográficos podem ser apresentados com cuidado quando ainda não houver crédito externo independente, sem inserir disclaimers obsessivos.

### O Arquiteto da Apoteose

- iniciado em 2019;
- documentário sobre Sidnei França;
- filmado parcialmente;
- não finalizado;
- permanece WIP;
- making-of não publicado existe no arquivo.

### Autópsia

- concebido e produzido em 2021;
- projeto audiovisual gravado, não lançado publicamente;
- apresentação oficial preservada;
- apresentação pública selecionada é permitida;
- materiais de terceiros/direitos controlados não devem ser publicados indiscriminadamente.

---

## 13. Arquitetura de fotografias

Existem dois papéis editoriais diferentes.

### Tipo 1 — imagem editorial dentro da narrativa

Características:

- aparece no fluxo da história;
- ilustra a entrada;
- quebra muralha de texto;
- não é um bloco de “acervo”;
- pode ser uma colagem ou imagem narrativa.

Primeiro caso aprovado: colagem de **Meia-Noite e Uns**.

Tamanho aprovado no piloto:

- desktop: ~58% da largura;
- tablet: ~72%;
- mobile: 100%.

Não alterar esse piloto sem motivo.

### Tipo 2 — galeria associada a um registro

Características:

- 1 ou várias imagens associadas a uma entrada;
- interface de galeria;
- horizontal quando há volume;
- sem autoplay;
- navegação controlada pelo usuário;
- scroll snap;
- lazy loading;
- lightbox acessível;
- teclado;
- Escape;
- retorno de foco;
- legenda;
- contador;
- fallback sem JavaScript.

### Política por quantidade

Uma única arquitetura, adaptada pela quantidade:

- 1 foto → apresentação simples;
- 2–4 → pequeno grid;
- 5+ → trilho horizontal/galeria.

### V2 aprovada conceitualmente

Após teste desktop/mobile do piloto Meia-Noite:

- manter tamanho das thumbs desktop;
- setas desktop mais visíveis, fundo branco/ícone escuro;
- cabeçalho horizontal da galeria;
- PT: `Fotos · N` + `Navegue pelas fotos`;
- mobile: `Fotos · N` + `Deslize para ver mais`;
- thumbs mobile maiores, aproximadamente 70–75% da largura útil;
- deixar parte da próxima imagem aparente;
- lightbox mobile quase full-width;
- legenda maior e legível;
- swipe nativo no mobile;
- sem autoplay.

### Galeria de Meia-Noite e Uns

Primeiro piloto Type 2, com 22 fotos.

Arquivos e derivados são controlados por:

- `data/galleries.json` ou registro equivalente em uso;
- `tools/build_gallery_media.py`;
- `tools/sync_galleries.py`;
- `tools/audit_galleries.py`.

Não duplicar a colagem Type 1 dentro da galeria Type 2.

---

## 14. Meia-Noite e Uns — composição completa ainda requer revisão

Mesmo com a galeria funcionando, a entrada inteira ainda deve ser revista como composição.

Problema já identificado em teste visual:

> imagem editorial + título + descrição + cartão + galeria podem parecer uma “salada” sem limites claros.

Essa revisão deve ocorrer **depois** de estabilizar o componente global de galeria.

Possível decisão futura: remover ou reposicionar o cartão Dreamsnetwork caso ele se torne redundante.

Não misturar a validação do componente de galeria com a revisão da hierarquia inteira da entrada.

---

## 15. Documentação e evidência

A política interna de rigor continua existindo, mas o visitante não precisa assistir ao processo de auditoria.

### Princípio

> **Documentação é lastro, não protagonista.**

### Fontes possíveis

- vídeos originais;
- fotos históricas;
- créditos de programa;
- matérias de imprensa;
- cartões profissionais;
- páginas antigas;
- registros em repositórios;
- documentos profissionais;
- acervo pessoal;
- depoimento autobiográfico do autor.

### Distinção interna útil

Nos bastidores, diferenciar:

- fato diretamente confirmado por fonte pública/registro;
- fato sustentado por acervo privado;
- memória autobiográfica ainda sem documento localizado;
- reconstrução ilustrativa.

Essa classificação **não deve virar uma legenda forense recorrente no site**.

---

## 16. Reconstruções por IA

Reconstruções visuais feitas por IA podem ser usadas para reconstituir ambientes históricos quando não há fotografia original.

Exemplo: Minduim BBS.

Regra obrigatória:

- sempre rotular como reconstrução/recriação;
- nunca apresentar como fotografia original;
- nunca usar como evidência do fato;
- deixar claro que a composição se baseia em memória + elementos factuais do setup.

---

## 17. Privacidade e publicação de documentos

Não publicar documentos integrais que exponham desnecessariamente:

- CPF;
- RG;
- assinatura;
- endereço residencial;
- telefone pessoal;
- dados bancários;
- dados societários sensíveis;
- informações de terceiros sem necessidade editorial.

Contratos e documentos societários, quando usados, devem ser redigidos ou apresentados apenas em recortes seguros.

Carteira de trabalho pode servir como lastro interno sem virar scan público integral.

---

## 18. Arquivo — direção futura

O Arquivo deve evoluir para um espaço histórico e humano.

Existe ainda linguagem antiga que lembra site de “prova” ou auditoria, com termos como:

- fontes preservadas;
- fatos sem documentação;
- método;
- classes de fonte;
- disclaimers.

Essa área ainda precisa de reescrita.

Não tratar essa limpeza como concluída até que PT e EN sejam efetivamente revisados.

---

## 19. Indexação

A indexação é deliberadamente gradual.

Páginas historicamente priorizadas para indexação:

- raiz;
- home PT/EN;
- biografia;
- publicações;
- arquivo;
- IA/HAI.

Verticais em construção podem permanecer `noindex,follow` até maturidade editorial suficiente.

Não alterar política de robots em massa sem revisar o plano de indexação.

---

## 20. Navegação

Navegação principal deve refletir os cinco campos.

Não reintroduzir Search como vertical separada.

Links internos devem abrir na mesma aba.

Links externos normalmente:

```html
target="_blank" rel="noopener noreferrer"
```

Perfis de identidade podem usar `rel="me"` quando apropriado.

A navegação global é sincronizada por script e auditada.

---

## 21. Presença externa e identidade

O footer agrega perfis públicos e deve permanecer consistente com `data/presence.json` e scripts de sync/audit correspondentes.

Não adicionar perfis sem verificar:

- se pertencem à pessoa correta;
- se a URL está estável;
- se têm valor real de identidade/produção;
- se a inclusão não expõe informação que o autor não deseja publicar.

---

## 22. Fluxo obrigatório de GitHub

Antes de **qualquer write relevante**:

1. buscar o HEAD atual de `main`;
2. verificar se houve upload/commit paralelo do autor;
3. para tarefas de mídia, relistar a pasta correspondente;
4. criar branch a partir da `main` mais recente;
5. fazer alterações pequenas e rastreáveis;
6. rodar auditorias;
7. abrir PR;
8. confirmar CI;
9. mergear apenas quando apropriado;
10. confirmar GitHub Pages antes de dizer que está publicado.

### Nunca presumir que um SHA antigo ainda é HEAD

O autor pode enviar arquivos diretamente ao repositório durante a conversa.

### Alterações globais ou estruturais

Devem preferencialmente ocorrer em branch separada.

### Alterações experimentais

Não publicar em `main` antes da revisão visual/editorial do autor quando a tarefa tiver sido explicitamente tratada como piloto.

### Arquivos temporários de workflow

Podem ser usados para transformações mecânicas em branch, mas devem ser removidos antes do merge quando não forem parte permanente da infraestrutura.

---

## 23. Auditorias importantes

A infraestrutura atual utiliza auditores para evitar regressões.

Entre os controles existentes ou previstos:

- navegação sincronizada;
- HTML/SEO;
- presença externa;
- analytics;
- derivados de galeria;
- sincronização de galerias;
- integridade de galerias;
- sincronização da Full Bio;
- cobertura da Full Bio PT/EN.

Uma mudança que “parece certa” mas quebra o audit deve ser corrigida; não desabilitar o audit por conveniência sem compreender a razão.

---

## 24. Estado da nova Full Bio em 27/08/2026

Branch de desenvolvimento:

`full-biography-chronology`

A nova arquitetura já conseguiu gerar e auditar uma composição integrada com dezenas de entradas cronológicas e entradas de contexto em PT/EN.

Ela **não deve ser considerada publicada até merge + Pages**.

Antes da aprovação final do autor, revisar:

- ordem cronológica;
- duplicação visual de datas;
- títulos limpos;
- separação 1992 / 1994 no Coitado;
- respiração entre entradas;
- comportamento de galerias dentro da Bio;
- composição mobile;
- índice lateral.

### Estado específico do Coitado na branch

A unidade inicial foi dividida internamente em:

- `music-coitado-1992`
- `music-coitado-1994`

Isso corrige o problema de fatos de 1994 aparecerem antes de eventos de 1993 na linha do tempo integrada.

A entrada `music-coitado-1992` deve usar agora a data exata **5 de julho de 1992**.

---

## 25. Prioridades editoriais após a Full Bio

Ordem sugerida:

1. finalizar e validar a nova Full Bio;
2. consolidar o padrão global de galeria Type 2;
3. revisar a composição completa de Meia-Noite e Uns;
4. melhorar respiração visual entre entradas da timeline/thread;
5. revisar paridade entre verticais e Full Bio;
6. limpar a linguagem forense do Arquivo PT/EN;
7. incorporar novos lotes de materiais históricos;
8. continuar Comunicação, Música, Audiovisual e Internet com fotos/áudios/vídeos recuperados.

---

## 26. Inventário de materiais históricos já conhecido

### Coitado do Próximo

Há ou pode haver:

- vídeo do primeiro show — 5/7/1992;
- demo-tape de 1994 em áudio;
- vídeos de gravação da demo;
- entrevista com Kid Vinil / 97FM em MP3;
- vídeo do Café Piu Piu;
- registros dos álbuns de 1997 e 1999/2000;
- Olympia;
- Programa do Jô;
- reunião de 2023.

### Comunicação

- entrevista completa do Metrópole com Velhas Virgens em MP3;
- scans e arquivo oficial da Folha;
- corpus de Sinal Verde.

### Internet & Performance

- fotos de equipe PSINet;
- Mirantte;
- cartões e materiais CookieWEB / Clickland;
- Petlove — documentação profissional;
- BEST/Kenshoo — vídeos de workshop;
- Ad.Dialetto — cartão;
- Driven — registros profissionais quando disponíveis.

### Audiovisual

- Homens na Cozinha no YouTube;
- Meia-Noite e Uns — vídeos + 22 fotos + colagem;
- O Arquiteto da Apoteose — making-of não publicado;
- Autópsia — apresentação pública selecionada + material filmado sob controle de direitos.

### IA/HAI

- trabalhos Melissa;
- Punk Rock Orchestra;
- repositórios e DOIs;
- registros em ORCID/HAL e plataformas correlatas.

---

## 27. Linguagem editorial

Preferir:

- prosa clara;
- datas concretas quando conhecidas;
- nomes próprios corretos;
- títulos de obras preservados;
- relações causais apenas quando sustentadas;
- contexto suficiente para o leitor entender por que o episódio importa.

Evitar:

- autopromoção inflada;
- superlativos não demonstrados;
- tom de defesa;
- tom cartorial;
- repetição de disclaimers;
- transformar cada cartão/foto em “prova”.

O autor do site pode fazer afirmações autobiográficas sobre a própria trajetória. Elas não precisam ser acompanhadas por um parágrafo pedindo desculpas por ainda não terem validação externa.

---

## 28. Regra para incerteza factual

Quando o autor diz “acho”, “por volta de”, “talvez”, não converter automaticamente em data exata.

Exemplo histórico:

O primeiro show do Coitado era lembrado como possivelmente em julho de 1992. O mês não foi congelado até que o vídeo original fosse localizado.

Em 27/08/2026, o vídeo foi conferido e a marcação da câmera confirmou **5 de julho de 1992**.

A partir desse momento a data pode ser exata.

Esse é o comportamento esperado para outras lacunas futuras.

---

## 29. Regra para novas entradas futuras

Quando o autor trouxer um novo emprego, projeto, show, publicação ou episódio:

1. decidir qual vertical é a fonte editorial;
2. escrever/melhorar a entrada na vertical;
3. integrar mídia e registros organicamente;
4. criar subunidade `data-bio-key` se a entrada precisar ser repartida cronologicamente;
5. registrar a unidade no manifesto da Full Bio;
6. executar sync;
7. executar audit de cobertura PT/EN;
8. revisar a composição humana;
9. somente então publicar.

A Full Bio não deve virar o lugar onde fatos são escritos pela primeira vez, salvo conteúdo realmente exclusivo de contexto, como o parêntese Livraria Cultura.

---

## 30. Checklist para o próximo colaborador

Antes de editar:

- [ ] Li este documento.
- [ ] Confirmei o HEAD atual da `main`.
- [ ] Entendi qual vertical é a fonte da entrada.
- [ ] Verifiquei se existe branch experimental em andamento.
- [ ] Não estou reintroduzindo Search como vertical.
- [ ] Não estou reintroduzindo disclaimers forenses em IA/HAI.
- [ ] Não estou duplicando manualmente conteúdo da Full Bio.
- [ ] Não estou tratando reconstrução por IA como evidência histórica.
- [ ] Não estou publicando PII desnecessário.
- [ ] Mantive PT/EN coerentes.
- [ ] Rodei os auditores relevantes.
- [ ] Confirmei Pages depois do merge.

---

## 31. Resumo executivo

Se for necessário lembrar apenas cinco regras:

1. **O HUB é uma autobiografia multidisciplinar, não um CV nem um site de provas.**
2. **Verticais são a fonte editorial; a Full Bio é sincronizada a partir delas.**
3. **Documentação é lastro, não protagonista.**
4. **Não reintroduzir disclaimers defensivos ou tom de auditoria.**
5. **Toda mudança relevante passa por HEAD atual → branch → audit → PR → merge → Pages.**

---

## 32. Registro de decisão — 27/08/2026

Decisões adicionadas nesta revisão:

- Coitado do Próximo confirmado como ativo continuamente de 1992 a 2003;
- primeiro show confirmado em **5 de julho de 1992**;
- local confirmado: Escola Estadual “Barão Homem de Mello”, Rua Alfredo Pujol, 1555, Santana, São Paulo;
- vídeo original localizado no YouTube: `7yjYTV1L0b0`;
- a data exata deve substituir a formulação anterior aproximada;
- Olympia, Programa do Jô e reunião de 2023 podem ser entradas independentes na Full Bio;
- IA/HAI deve permanecer sem o disclaimer “Publicação não é validação automática” e sem equivalentes defensivos;
- Full Bio passa a ser construída por sincronização a partir das verticais;
- cobertura PT/EN deve ser auditada automaticamente;
- chapters temáticos podem conter subunidades invisíveis para composição cronológica;
- este documento passa a ser a referência de continuidade para futuros colaboradores.
