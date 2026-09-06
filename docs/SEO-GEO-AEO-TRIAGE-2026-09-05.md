# SEO / GEO / AEO TRIAGE — Billy

**Date:** 5 Sep 2026 (BRT)  
**Input:** external SEO/GEO/AEO plan supplied by Marcelo after a 3 Sep 2026 audit.  
**Rule:** planning input, not automatic specification.

## 1. Already implemented / stale findings

The supplied plan predates parts of current `main`.

Already true today:

- root HTML already embeds `WebSite` + `ProfilePage` + `Person` JSON-LD;
- root `sameAs` already contains the full 15-profile set also present in `data/person.json`;
- `robots.txt` and generated `sitemap.xml` already exist;
- root, PT and EN pages already have canonical/hreflang infrastructure;
- the site already has an explicit external-profile alignment document.

Do not reimplement these as if absent.

## 2. Adopt

### Substantive root entity page

Yes. Root `/` needs real human-readable entity content and should become the strongest canonical personal-site destination.

### Broader public indexation destination

Yes, per Marcelo's later instruction: substantive verticals and real autonomous chapter URLs should move toward `index,follow`; Full Biography PT/EN should ultimately become `noindex,follow`.

### Internal discovery before biography noindex

Yes. Any autonomous page intended for indexation must have ordinary human-visible internal links from indexable surfaces. Sitemap membership alone is not the desired architecture.

### Person semantic enrichment

Yes, especially more specific `knowsAbout` terms where they accurately describe public work. Keep the existing embedded schema/data-source architecture and avoid creating a second truth.

### Publication structured data

Yes, after modelling review. `ScholarlyArticle`/Article semantics can strengthen machine-readable publication identity, author links, DOI/version metadata and the one-work/multiple-instance rule.

### External profile reconciliation

Yes. Make the HUB the primary personal-site destination where possible and align factual identity, chronology and publication metadata across legitimate nodes.

### Internet & Performance historical specificity

Yes. Dates, named products/companies/events, archive links and primary historical context are strong both for readers and entity resolution.

### Monitoring

Yes. Search Console and Bing Webmaster Tools should become the primary measured discovery surfaces when data is available.

## 3. Adopt with modification

### Home language / hreflang design

Do **not** automatically adopt two long side-by-side translated biography blocks. Google states that it determines page language from visible content and recommends using one language for content/navigation on each localized page rather than side-by-side translations.

Current root already works as `x-default` gateway with PT/EN alternates. When adding substantive entity copy, design the root as a distinct global/entity surface and preserve dedicated language URLs. Reassess the exact hreflang cluster only when the new root content is written; no promise can guarantee that every branded search in every locale will always return `/`.

Reference: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites

### Sitemap hreflang

Do not duplicate hreflang into the sitemap by default. Google treats HTML and sitemap implementations as equivalent and says there is no Search benefit to maintaining both. Current HTML annotations are already the preferred source unless an audit shows a reason to move them.

Reference: https://developers.google.com/search/docs/specialty/international/localized-versions

### Standalone biography-only discovery

The proposed `/ensaios/` or `/essays/` index is one possible solution, but “O Buscador” is not automatically an essay and a new quasi-vertical should not be created just for crawlers. Prefer contextual links from Home/language hubs/relevant surfaces; create a chapter index only if it is genuinely useful to readers.

### Scholarly work identity

Do not blindly use `sameAs` to collapse every repository DOI. Schema.org defines `sameAs` as unambiguous identity. The HUB's “one work/version, multiple repository instances” model may be better represented by a canonical work plus identifiers and/or `workExample`/`exampleOfWork` relationships after testing.

References:
- https://schema.org/ScholarlyArticle
- https://schema.org/workExample

### Concept pages and glossary

PRO and Melissa may justify standalone concept pages because they have substantial reader value. A glossary can be useful if there is a genuine controlled vocabulary. Do not mass-split content solely because a model is assumed to need one URL per concept; current Google guidance explicitly says AI Search does not require content chunking.

Reference: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

### Nomenclature discipline

Use disambiguating forms such as `Punk Rock Orchestra (PRO) methodology` where context requires it, especially first occurrences. Do not force the same phrase mechanically into every page or profile. Factual consistency matters more than literal repetition.

### Google Scholar

Potentially useful academic identity node, but not a guaranteed LLM-ranking mechanism and not “the most read node by LLMs” as a documented fact. Evaluate profile eligibility, corpus fit and maintenance value before treating it as a priority dependency.

## 4. Reject or defer

### “Same phrase word-for-word everywhere”

Reject. External profiles should be compatible, not copied verbatim for ranking. Google explicitly advises against rewriting content only for generative search and against inauthentic mention strategies.

### Long bilingual root because English is “the language LLMs train on”

Reject as the technical justification. Root language is an editorial/search architecture decision, not an LLM-training-language optimization rule.

### `FAQPage` as an AEO/GEO lever

Low priority. Human-useful Q&A blocks may be added, but FAQ rich results are now generally limited to authoritative government/health sites. Do not add FAQ markup merely as an AI hack.

Reference: https://developers.google.com/search/blog/2023/08/howto-faq-changes

### `llms-full.txt` as a high-impact SEO/GEO task

Defer. Keep the existing `llms.txt` if useful to other systems, but Google Search states that it does not use `llms.txt` for visibility/ranking. A larger derivative file is therefore optional maintenance, not foundation work.

Reference: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

### Wikidata as a self-created SEO shortcut

Reject. Wikidata is community governed and current guidance warns strongly against self-promotional item creation. Only pursue if a policy-compliant notability/independent-creation path exists; do not create person/works items merely to manufacture a graph signal.

References:
- https://www.wikidata.org/wiki/Wikidata:Notability
- https://www.wikidata.org/wiki/Wikidata:Self-promotion

### `Human–AI Interaction (HCI)`

Reject terminology. **HCI = Human–Computer Interaction. HAI = Human–AI Interaction.** If both are useful, express the relationship accurately, for example Human–AI Interaction within the broader HCI field; do not redefine the acronym.

### `affiliation` as a fabricated “Independent” organization

Do not create an Organization merely to fill schema. If there is no institutional affiliation, omit affiliation or model occupation/status accurately.

### `nationality/address = São Paulo, Brazil`

Do not conflate nationality with location. Avoid unnecessary residential/address data. Location semantics should be minimal and accurate if used at all.

### “Pageviews/time/followers do not matter”

Too absolute. They are not primary authority/indexation KPIs, but human usage metrics may still help evaluate whether the HUB works for readers.

## 5. Major plan correction: vertical priorities

The supplied plan says Music and Mídia & Cultura need no new content now. Marcelo's later instruction overrides that sequencing.

Current content priorities include:

1. Music — Coitado do Próximo and substantive archive/history;
2. Internet & Performance — incomplete/refinable passages;
3. Mídia & Cultura — selected entry corrections;
4. Home — substantive entity content.

Indexation rollout must respect this content work rather than treating existing structure as proof of content completion.

## 6. Recommended implementation order

1. **B0 inventory:** URL/indexation/schema/internal-link matrix.
2. **B1 Home:** substantive entity content + schema review.
3. **Content pass:** Music, Internet & Performance, Mídia & Cultura priority gaps.
4. **B3 indexation:** promote mature verticals/autonomous pages in PT/EN-safe batches; ensure internal inlinks and sitemap/audit sync.
5. **Full Biography:** move to `noindex,follow` only after the standalone discovery graph is safe.
6. **B4 structured works:** publication schema and selective concept pages.
7. **B2 external graph:** profile URL/description/publication reconciliation in parallel where operator access is required.
8. **B5 archive:** continue historical-source expansion.
9. **B6 measurement:** Search Console, Bing, index coverage and stable citation-query tests.

## 7. Success criteria

Primary:

- root becomes a useful canonical entity page;
- intended public URLs are indexable without orphaning;
- branded and semantic queries increasingly surface the HUB or canonical research records;
- external profiles point coherently back to the HUB;
- publication/version identity remains accurate;
- search/AI citation visibility can be observed rather than guessed.

Secondary:

- structured data validates;
- PT/EN remain editorially coherent;
- no design/mobile/Reader regression is introduced during search work.
