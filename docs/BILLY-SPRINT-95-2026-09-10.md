# Billy sprint to 95% — deadline 10 Sep 2026

Working window: night of 5 Sep through Thursday 10 Sep 2026 (BRT).

Goal: leave the HUB approximately **95% ready** in content/architecture/indexation/authority terms without destabilizing the production system or reopening resolved design decisions.

## Definition of 95%

By Thursday, the HUB should have:

- current documentation synchronized;
- substantive root entity page architecture defined and implemented;
- major known content gaps either completed or explicitly isolated as the remaining 5%;
- mature autonomous URLs and verticals on their intended indexation state;
- Full Biography pair moved to its intended non-competing state only after the autonomous graph is live;
- sitemap/audits synchronized;
- entity/schema layer coherent;
- external-profile alignment matrix ready and high-value nodes corrected where operator access permits;
- production CI green;
- final mobile/desktop QA completed.

## Non-negotiable invariants

- Humans first; semantics second.
- Full Biography = totality; verticals = thematic cuts.
- PT/EN factual/editorial parity, not literal translation.
- Internet + Search/Performance remain one vertical: Internet & Performance.
- Mídia & Cultura / Culture & Audiovisual remains the fused surface at canonical Communication paths.
- Biography-only entries do not imply new verticals.
- Chapter Pages remain selective, not mass-generated.
- Current mobile button/navigation solution and resolved visual direction are preserved.
- AI reconstructions remain labeled when materially necessary.
- Stable URLs are preserved; compatibility URLs do not become competing authority pages.
- Sitemap `lastmod` remains Git-derived.
- CI assertions are fixed at source/generator level, not weakened to obtain green builds.

## Sunday 6 Sep — map + foundation

### B0 close
- merge Billy baseline and SEO/GEO/AEO triage;
- freeze current-vs-destination terminology.

### B1/B3 inventory
- complete all-URL matrix;
- classify every URL by role, robots, canonical, hreflang, sitemap and destination state;
- identify static-link requirements for every Chapter Page promotion;
- identify schema/entity gaps that can be fixed without operator prose.

### Deliverable
- URL/indexation matrix as operational source of truth.

## Monday 7 Sep — content blockers

Priority order:

1. **Música / Music — Coitado do Próximo**: substantive missing historical content and archive connection;
2. **Internet & Performance**: fill the remaining substantive passages/gaps identified by Marcelo;
3. **Mídia & Cultura / Media & Culture**: targeted editorial corrections/adjustments;
4. PT/EN parity pass for all changed material.

Rule: do not promote a vertical solely because its HTML architecture is stable; content readiness comes first.

## Tuesday 8 Sep — entity root + semantic layer

### B1 Entity Page
- expand `/` from thin gateway into substantive entity surface without destroying the clean gateway function;
- preserve dedicated `/pt/` and `/en/` trajectory/index surfaces;
- avoid side-by-side duplicate bilingual prose as an SEO hack;
- strengthen internal links from root to the highest-value autonomous authority pages;
- refine `Person` / `ProfilePage` / `WebSite` schema from canonical data.

### B4 publications/concepts
- design scholarly-work structured data from `data/publications.json`;
- preserve the rule one work/version != multiple publications merely because multiple repository deposits exist;
- evaluate individual PRO/Melissa concept/work pages only where they have autonomous human value;
- no mass glossary/page generation.

## Wednesday 9 Sep — indexation + authority graph

### B3 controlled flip
- promote mature autonomous Chapter Page pairs to `index,follow` after static-link verification;
- promote mature vertical pairs after content pass;
- update `LAUNCH_INDEXABLE`, generated sitemap and registry/generator state atomically;
- once the autonomous graph is live, move Full Biography / Biografia Completa to `noindex,follow` and remove from sitemap;
- keep legacy audiovisual/search compatibility URLs `noindex,follow` with current canonicals.

### B2 external graph
- finalize platform-by-platform external profile matrix;
- use HUB root as canonical website where platform fields allow;
- align facts/chronology/identifiers without forcing verbatim biographies;
- prioritize ORCID, HAL, GitHub/research repositories, Zenodo/OSF/SSRN/PubPub, LinkedIn and other major public nodes;
- privacy cleanup remains operator-managed when platform settings require it.

## Thursday 10 Sep — 95% closeout

### B6 measurement and QA
- full Site Audit / generator consistency;
- mobile and desktop smoke tests;
- broken links, canonicals, hreflang, robots and sitemap validation;
- image dimensions/weight and Reader/runtime checks;
- verify external presence links;
- Search Console/Bing submission/checklist where operator access is required;
- record a baseline for entity-name, PRO-methodology and Melissa-framework discovery queries;
- produce Billy closeout with remaining 5% explicitly named.

## The likely remaining 5%

The remaining 5% may legitimately include:

- archive materials that have not yet been digitized/restored;
- long-tail external profile changes blocked by platform access or moderation;
- field Search/CWV observations that require time after deployment;
- later PRO v2 changes while the research object is still moving;
- future historical media lots.

These do not count as failure if the canonical architecture, content core and authority/indexation system are complete.

## Operator-dependent inputs

Billy should continue autonomously where repository evidence supports the work. Marcelo input is most valuable for:

- autobiographical facts/content not yet present in the repository;
- final voice/wording of the root entity prose where identity nuance matters;
- choosing among historical images when several editorially valid options exist;
- changes inside external platforms requiring account access.

Do not stop unrelated engineering while waiting for those inputs.
