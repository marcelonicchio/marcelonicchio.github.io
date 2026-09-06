# CURRENT HUB STATE — Marcelo Nicchio

**Authoritative operational snapshot:** 5 Sep 2026 (BRT)  
**Coverage:** current `main` through the post-Chet cycle plus Marcelo's explicit Billy-cycle directives.  
**Precedence:** later explicit instruction from Marcelo → current `main` + green CI → this file → `BILLY-BASELINE-2026-09-05.md` / domain-specific current docs → dated historical handoffs.

This file is the shortest path into the live architecture. Dated Duke/Chet dossiers remain historical rationale, not current implementation contracts.

---

## 1. Constitution

The HUB is Marcelo Nicchio's public, canonical, multidisciplinary autobiography and authority/identity hub.

Permanent editorial rule:

> **Humans first; semantics second.**

Full Biography is the integral chronology. Thematic verticals are selective cuts through the same life and do not need to contain every episode. Autobiography does not need to become a public forensic proof system; sources, archive, schema and search infrastructure support the human narrative.

---

## 2. Public architecture

Primary PT/EN surfaces:

- Home / entity gateway;
- Full Biography / Biografia Completa;
- Music / Música;
- Mídia & Cultura / Media & Culture, with H1 **Cultura & Audiovisual / Culture & Audiovisual**;
- Internet & Performance;
- AI/HAI / IA/HAI;
- Publications / Publicações;
- Archive / Arquivo;
- Selected Projects / Projetos.

Settled architecture:

- Internet + Search/Performance remain one vertical: **Internet & Performance**;
- Search is a specialization inside the continuous digital trajectory, not a competing vertical;
- Communication + Audiovisual remain fused at canonical paths `/pt/comunicacao/` and `/en/communication/`;
- legacy Search/Audiovisual paths are compatibility surfaces;
- Livraria Cultura remains Full-Biography-only;
- biography-only autonomous chapters may exist without creating a thematic vertical.

Do not reopen these decisions casually.

---

## 3. Post-Chet UX/design baseline

Later Chet work advanced beyond the older 2 Sep snapshot.

- Mobile navigation now uses an explicit button/menu instead of relying on a hidden horizontally scrollable menu; the stronger mobile hierarchy and bold category treatment are approved baseline behavior.
- The featured Reader-card visual treatment that older documentation called unresolved was resolved in the later Chet work; it is no longer an open blocker.
- Reader disclosure remains progressive enhancement: complete text stays in delivered HTML and no-JS fallback remains readable.
- Path-specific rules remain valid: AI/HAI keeps Melissa open; Full Biography may use rich compact summaries selectively; Internet & Performance keeps its Reader treatment.

Do not regress the mobile menu or resolved Reader direction merely because an older handoff predates them.

---

## 4. Full Biography

Permanent structural rule:

> **Full Biography = totality. Verticals = thematic cuts.**

Managed chronology infrastructure remains source-controlled through:

- `data/full_biography.json`;
- `data/editorial_parity.json`;
- `tools/sync_full_biography.py`;
- `tools/audit_full_biography.py`;
- `tools/editorial_parity.py`;
- `pt/biografia/index.html`;
- `en/biography/index.html`.

PT/EN parity means factual/editorial equivalence, not literal translation.

### Robots: current vs destination

**Current implementation on `main`:** Full Biography PT/EN remains `index,follow` and is in the sitemap.

**Marcelo's new destination decision:** Full Biography / Biografia Completa should become **`noindex,follow`** after the standalone public-page discovery graph is safe.

Do not block these pages in `robots.txt`; crawlers must be able to read `noindex` and follow the page's ordinary links.

---

## 5. Entry / Chapter Page architecture

`data/entries.json` remains the registry for reusable entry metadata, Reader presentation and selective Chapter Pages. `data/tags.json` remains controlled taxonomy; a tag does not automatically imply a public URL.

Existing generated Chapter Page pairs include Folhateen, Mirantte News, CookieWEB, Meia-Noite e Uns, Melissa 1.0 and BEST/Kenshoo.

Later work added a distinct biography-only model:

- **Espiritualidade — “O Buscador” / Spirituality — “The Seeker”** has its own PT/EN URL and tags;
- it remains part of the Full Biography rather than creating a Spirituality vertical;
- it is linked from Home trajectory highlights;
- current implementation is still `noindex,follow`;
- Marcelo has explicitly decided that its autonomous URL belongs in the future indexable set.

Creating an autonomous page still requires real reader value. The new destination policy is broader indexation of legitimate autonomous pages, **not** mass page generation.

---

## 6. Indexation — implementation state and destination state

### Current `main`

Current indexable core still includes root/language surfaces, Full Biography, Publications, Archive, AI/HAI and BEST/Kenshoo PT/EN.

Music, Mídia & Cultura, Internet & Performance and Projects remain staged `noindex,follow` on current `main`. Most standalone Chapter Pages are also still staged `noindex,follow`.

### New operator destination

Marcelo's current target is:

- root `/`: indexable;
- `/pt/`, `/en/`: indexable;
- substantive thematic verticals: `index,follow`;
- legitimate autonomous Chapter Pages / biography-only URLs: `index,follow`;
- Publications and Archive: indexable;
- Full Biography / Biografia Completa: `noindex,follow`.

This is a destination policy, not authorization for a blind one-release flip.

Promotion must remain reviewable by PT/EN pair where applicable and couple:

1. content maturity;
2. factual/editorial parity;
3. canonical/hreflang;
4. ordinary human-visible internal inlinks;
5. robots state;
6. sitemap membership;
7. audit allowlists/invariants.

Before Full Biography becomes `noindex`, standalone pages intended for Search must not depend exclusively on it for discovery.

`tools/build_sitemap.py` remains the canonical sitemap generator and real Git history remains the source for per-page `lastmod`.

---

## 7. Home / canonical entity page

Root `/` is still primarily a language/entity gateway and needs substantive human-readable entity content.

Current root already includes embedded JSON-LD with:

- `WebSite`;
- `ProfilePage`;
- `Person`;
- the 15-profile `sameAs` set.

Therefore older audit findings saying schema existed only in an external JSON file or that `sameAs` had only four profiles are stale.

Open semantic work includes:

- substantive entity prose;
- more specific/accurate `knowsAbout` and related Person semantics;
- review of root language/hreflang architecture once the new content is written;
- ensuring the root remains useful to humans rather than becoming a keyword/AI-target page.

Do not automatically use long side-by-side PT/EN translations merely for crawlers; dedicated language URLs remain part of the architecture.

---

## 8. Publications / structured research identity

`data/publications.json` remains the canonical internal publication inventory and preserves the rule:

> **one work/version, multiple repository instances are not multiple publications.**

Current repository code does not yet implement `ScholarlyArticle` structured data.

Future structured-data work should model the intellectual work and repository instances accurately rather than mechanically declaring every DOI `sameAs`. PRO v2 remains work in progress and must not be represented as a public publication before it exists publicly.

---

## 9. Content maturity queue

Known substantive priorities now include:

1. **Music / Música:** Coitado do Próximo and its historical archive;
2. **Internet & Performance:** incomplete/refinable passages;
3. **Mídia & Cultura / Media & Culture:** selected entry adjustments;
4. **Home:** canonical entity prose.

The previous assessment that a vertical was structurally ready for eventual indexing does not mean its content is finished. Marcelo's later content priorities govern sequencing.

---

## 10. External authority alignment

External profiles/records should point inward to the HUB as the canonical personal-site destination where platforms permit it.

Goal: factual and semantic compatibility, not verbatim SEO copy.

Align progressively:

- preferred public name;
- chronology/current positioning;
- official HUB URL;
- exact publication titles and version relationships;
- legitimate persistent identifiers/cross-links.

Privacy cleanup on third-party services remains operator-side where Marcelo considers it necessary. Do not replicate unnecessary direct contact details into the HUB/schema/docs.

See `external-profile-alignment.md` and `SEO-GEO-AEO-TRIAGE-2026-09-05.md`.

---

## 11. SEO / GEO / AEO triage

The externally prepared 3 Sep plan is useful planning input, not an implementation contract.

Current Billy triage:

- adopt the substantive entity page, semantic enrichment, publication modelling, external alignment, better internal discovery and measured indexation;
- adapt the proposed bilingual-root, concept-page, DOI and Scholar/Wikidata recommendations;
- defer low-value/experimental `llms-full.txt` and FAQ-schema work;
- reject inaccurate `Human–AI Interaction (HCI)` terminology, literal identical bios everywhere and Wikidata self-creation as an SEO shortcut.

See `SEO-GEO-AEO-TRIAGE-2026-09-05.md` for the detailed decision record.

---

## 12. Billy roadmap

B0–B6 is now recorded in `BILLY-BASELINE-2026-09-05.md`:

- **B0:** baseline, documentation and URL/indexation inventory;
- **B1:** substantive canonical Entity Page;
- **B2:** external knowledge graph/profile alignment;
- **B3:** controlled public indexation migration;
- **B4:** structured works, pilot evaluation and selective concept expansion;
- **B5:** archive as authority;
- **B6:** real-world search/citation/performance measurement.

---

## 13. CI invariants

Site Audit continues to protect navigation, gallery/media synchronization, PT/EN parity, Full Biography generation, Reader behavior, Chapter Page registry, fused Mídia & Cultura architecture, JavaScript/runtime behavior, performance/media observability, page-image weight reporting, generated sitemap freshness, HTML/JSON/sitemap integrity, external presence and analytics installation.

When policy intentionally changes, update source/generator/audits together. When CI catches an unintended regression, fix the source model rather than weakening assertions merely to get green.

---

## 14. What not to reopen casually

Preserve:

- Humans first; semantics second;
- Full Biography = totality / verticals = thematic cuts;
- PT/EN editorial parity;
- Internet & Performance fusion;
- Mídia & Cultura / audiovisual fusion at current canonical paths;
- biography-only chapter capability;
- selective, human-justified Chapter Pages rather than mass generation;
- honest labelling of AI reconstruction where material;
- Reader progressive enhancement;
- current mobile menu solution;
- resolved Reader visual direction;
- stable URLs;
- deterministic real-history sitemap freshness.

See the Billy baseline for the full B0–B6 working contract.
