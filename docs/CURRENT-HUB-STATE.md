# CURRENT HUB STATE — Marcelo Nicchio

**Read this first in a new editing/architecture session.**  
**Snapshot:** 1 Sep 2026 (BRT)  
**Production baseline captured before this documentation batch:** `5f4ce03d6ee1a7b038229c3777d44ec3d2f9c83c` (PR #52 merged)  
**Current architecture cycle covered here:** PR #24 through PR #52, with PR #23 as the older continuity baseline.

This is the authoritative current-state handoff. Older planning, continuity and pilot documents remain useful as historical records, but when they describe a pre-implementation state this file wins unless Marcelo gives a later explicit instruction.

---

## 1. HUB constitution

The HUB is Marcelo Nicchio's public, canonical, multidisciplinary autobiography and authority/identity hub.

It is **not** a conventional CV, a proof site, a defensive biography or a forensic archive presented to the reader.

Permanent editorial priority:

> **Humans first; semantics second.**

Documentation, sources, schema, SEO/GEO/AEO and archive material support the narrative. They do not become the protagonist of the public experience.

Canonical identity: **Marcelo Nicchio**. Historical variants may include Marcelo Henrique Nicchio, Marcelo H. Nicchio and Marcelo Minduim.

### Publicability rule

> **Information with a useful source → publish the information and the source.**  
> **Autobiographical information without an external source → publish it normally, without inventing a disclaimer.**

Absence of external corroboration is not a generic gate. Privacy, copyright, uncertainty in the author's own memory and third-party reputational/legal exposure are separate editorial questions.

---

## 2. Public information architecture

Primary PT/EN surfaces remain:

- Home;
- Full Biography / Biografia Completa;
- Music / Música;
- Communication / Comunicação;
- Internet & Performance;
- Audiovisual;
- AI/HAI / IA/HAI;
- Publications / Publicações;
- Archive / Arquivo;
- Selected Projects / Projetos.

### Internet & Performance is one vertical

The former Internet and Search/Performance axes were structurally merged into **Internet & Performance**.

The intended narrative is continuous: BBS / pre-Web network culture → commercial internet → infrastructure/hosting and digital products → Search → Social → analytics → media/performance operations.

Legacy Search URLs exist only for compatibility/redirect behavior. Do not recreate Search as a competing vertical.

### Livraria Cultura rule

Livraria Cultura belongs to the Full Biography in its chronological position but not to Internet & Performance or another thematic vertical merely because of chronology.

### Next vertical consolidation — Communication + Audiovisual

Communication & Culture and Audiovisual are approved for structural fusion because the two axes overlap editorially and each carries relatively few top-level threads in isolation.

Approved public naming separates navigation economy from editorial precision:

- menu PT: **Mídia & Cultura**;
- menu EN: **Media & Culture**;
- page H1/title PT: **Cultura & Audiovisual**;
- page H1/title EN: **Culture & Audiovisual**.

The established canonical vertical paths are deliberately preserved as **`/pt/comunicacao/`** and **`/en/communication/`**. The Folhateen Chapter Page therefore remains at its current Communication path. The old standalone `/pt/audiovisual/` and `/en/audiovisual/` paths become permanent compatibility stubs when the fusion ships.

Treat the fusion as the same class of change as Internet + Search/Performance: one menu item, one coherent thematic chronology, PT/EN parity, internal links adjusted, and no competing duplicate verticals. The Full Biography remains the integral chronology and is not merged or shortened by this change. See `docs/url-policy.md`.

---

## 3. Full Biography constitution

Permanent rule:

> **Full Biography = totality. Verticals = thematic cuts through the same life.**

The Full Biography is a single integrated chronology. It is not a concatenation of verticals and must not be shortened merely because Reader disclosure or Chapter Pages exist.

Canonical infrastructure:

- `data/full_biography.json`
- `data/editorial_parity.json`
- `tools/sync_full_biography.py`
- `tools/audit_full_biography.py`
- `tools/editorial_parity.py`
- `pt/biografia/index.html`
- `en/biography/index.html`

Do **not** hand-edit the managed Full Biography region.

### PT/EN workflow

1. edit/review PT editorial source;
2. create/review the deliberate EN equivalent;
3. compare meaning, dates, roles and framing;
4. run parity check;
5. explicitly accept the affected parity revision;
6. regenerate Full Biography;
7. run the complete audits.

Parity means factual/editorial equivalence, not literal translation.

---

## 4. Entry/source architecture

`data/entries.json` and `data/tags.json` provide reusable entry metadata and controlled taxonomy without becoming a second autobiography.

Three source roles remain valid:

### A. Reader-section source

The vertical remains the editorial source. Use this when the same complete body does not yet need to feed an autonomous generated Chapter Page.

### B. Neutral shared fragment

For deliberately promoted entries only:

`content/entries/<lang>/<entry>.inc`

The fragment can feed the thematic vertical and a generated Chapter Page; the vertical then feeds Full Biography through the normal sync.

Current fragment-backed pilot entries include Folhateen and BEST/Kenshoo.

**No broad `.inc` migration.** Source migration happens entry by entry only when reuse justifies it.

### C. Landmark/composite subject

A semantic relationship may span multiple chronological entries without physically moving them together. Goobec/GAP is the canonical example.

---

## 5. Reader UX — current production state

The Reader architecture is no longer merely an opt-in prototype.

### Default disclosure surfaces

Normal public URLs use compact/disclosure reading by default on:

- `/pt/biografia/` + `/en/biography/`;
- `/pt/internet/` + `/en/internet/`.

Complete autobiographical text remains in delivered HTML. JavaScript progressively constructs the Reader presentation; no-JS fallback remains the original readable page.

### Opt-in laboratory surfaces

Communication and Audiovisual remain accessible as disclosure experiments through `?ux=disclosure` rather than being promoted site-wide by default.

### AI/HAI selective mode

AI/HAI is a special case.

The page remains **open by default as an editorial rule**. It does not use blanket chapter disclosure.

The current exception is **Melissa 1.0**, used as the selective rich-summary pilot. Only Melissa is transformed into a collapsed/expanded two-state entry on `/pt/ia-hai/` and `/en/ai-hai/`. PRO v2, PRO v1, the research-cycle opener and research identity remain openly rendered.

No global “Open all / Collapse all” controls appear on AI/HAI while only one selective disclosure exists.

### Reader guarantees

- native `<details>/<summary>` semantics;
- multiple entries can remain open;
- deep links auto-open the containing chapter;
- keyboard operation;
- print exposes complete content;
- no-JS fallback remains readable;
- full body is never fetched only after a click;
- Chrome smoke tests cover desktop/mobile behavior.

---

## 6. Reader presentation states

`reader_presentation.state` currently supports:

- `normal` — ordinary closed entry;
- `always-open` — Type 1 entry remains permanently open and scroll-only;
- `featured` — dense/editorially important entry starts closed but receives stronger visual treatment.

Featured visual treatment is state-dependent: it exists only while the entry is collapsed. Opening a featured entry restores the normal dark Reader treatment; collapsing it restores the highlight.

Current experimental matrix includes:

- Minduim/BBS → `always-open`;
- Folha de S.Paulo / “Órfãos do Rock” → `always-open`;
- Mirantte News → `featured`;
- CookieWEB → `featured`;
- Meia-Noite e Uns → `featured`.

The CTA text weight is currently normal (`500`), and the red CTA background is a darker translucent red. Those choices are not the final answer for the featured-card color system.

`always-open` is Type 1: the entry stays as ordinary open HTML, scroll-only, with no top or bottom expand/collapse controls and no participation in global Reader open/collapse actions.

---

## 7. Rich collapsed thread-summary model — accepted baseline

Melissa 1.0 established the first accepted **page-summary of a thread**.

The compact state is not a teaser and not a clipping of the opening paragraphs. It is a separately written concise version of the complete entry, designed under the assumption that **most visitors may never expand it**.

### Editorial model

- Version A = complete expanded post;
- Version B = autonomous concise post shown while collapsed.

Version B should communicate the principal arc even if the reader never clicks.

### Density guardrail

Melissa after calibration contains four paragraphs and is the **upper-density reference**:

- PT visible preview copy: about **1,638 characters**;
- EN visible preview copy: about **1,616 characters**.

Adopted rule for future rich previews:

- **maximum:** 1,650 visible-copy characters per language;
- **preferred design center:** about 1,300 characters (roughly 20% below the ceiling);
- shorter is fine when the subject does not justify the target;
- the number of paragraphs is not a rigid rule, but Melissa's four short paragraphs are the current upper-density visual reference.

Title, date/meta, topic tags, internal-content indicators and CTA do not count toward this text budget.

`tools/audit_entries.py` should enforce the 1,650-character maximum whenever a structured `reader_preview` exists.

### Visual/semantic structure

A rich compact summary may include:

- optional cover/editorial image;
- concise editorial copy;
- selective bold emphasis;
- **topic labels** describing what the entry is about;
- **internal-content indicators** describing what the reader will find after expansion;
- expand CTA.

Melissa's image sizing is approved. Do not alter it as part of generic Reader work.

### Two kinds of labels

**Topic labels** are taxonomy and future URL/SEO planning data. Melissa currently uses:

`AI · HAI · HCI · Prompt Engineering · Melissa 1.0`

They use a neutral light/translucent surface so they read distinctly from internal-content indicators.

**Internal-content indicators** are UX promises about what exists inside the full post. Melissa currently uses:

`2 images · 1 download link · 4 DOI documents · 1 repository link`

They retain the red treatment.

Curated indicators are allowed for rich entries when automatic media counting cannot express meaningful resources such as DOI documents, downloads or repositories.

See `docs/reader-summary-model.md` for the dedicated specification.

---

## 8. Three active Reader UX problems

These were explicitly identified and must remain visible in future work.

### Problem 1 — featured-card color language

The current yellow reads too beige and the current red still reads too wine-like. New tests are required.

Desired direction:

- yellow → clearer/lighter yellow;
- red → more genuinely red, probably translucent even if this reduces raw emphasis.

Button border removal and lighter text weight are hypotheses, not settled decisions.

### Problem 1.1 — color must describe the collapsed state

Current featured treatment remains colored even after the post opens.

Desired rule:

> **Collapsed:** color may signal “this dense/important entry is worth opening.”  
> **Expanded:** return to the normal black/dark post background.

The color is an invitation/state cue, not permanent identity for the full expanded entry.

### Problem 2 — collapsed state must carry real content

This problem is now substantially solved by the Melissa model.

The next step is to apply the model selectively to other dense entries, adapting content and image use rather than cloning Melissa mechanically.

Likely high-value candidates include Mirantte News, CookieWEB and Meia-Noite e Uns.

---

## 9. AI/HAI editorial state

AI/HAI reads in reverse chronology for the recent research cycle:

1. contextual opener;
2. Punk Rock Orchestra v2 — in development;
3. Punk Rock Orchestra v1 — May 2026;
4. Melissa 1.0 — September 2025 case / January 2026 publication cycle;
5. research identity.

### PRO v2

The block currently remains editorially light because the methodology is still being developed. It already uses the approved conceptual 2:1 illustration:

`assets/media/thread/thepunkrockorchestra_V2_1000x500_300kb.jpg`

The image is explicitly an AI-generated conceptual illustration, not research evidence.

### PRO v1

The public entry is intentionally substantive but concise. It is framed as the **first public formulation**, not the final methodology.

It touches N1/N2/N3, Robotic/Dialogical, Blue/Red/Forensic, Sterling, context poisoning and Cognitive Jelly without taking depth away from v2. It records the 54-interaction pilot and the paper's explicit limitation: adversarial epistemic integrity/stability was tested; superior open-ended differentiated cognition was not demonstrated.

Current architecture figure:

`assets/media/thread/pro_v1_diagrama01.jpg`

### Melissa 1.0 complete entry

The full entry remains intentionally dense and includes:

- origin as a functional Gemini 2.5 Pro headhunter persona;
- Sep 12–19 2025, 11 sessions, ~63 hours, 518 prompts;
- reasoning traces as observable displayed behavior;
- EIP taxonomy with explicit epistemic caveat;
- six-layer Melissa Framework authored by Melissa during the interaction;
- Melissa v8.7 signature;
- four public DOI works;
- full GitHub repository and original Framework directory;
- self-portrait and dissolution image;
- original Portuguese image prompt inside a small native disclosure.

The page does not claim metaphysically robust consciousness. It also must not casually erase the reasoning-trace material, because that is core documented evidence in the research narrative.

Current self-portrait CSS remains 65% desktop / 100% mobile for the **expanded** entry. The underlying image was manually replaced with a thinner-frame version while preserving the same filename and layout.

---

## 10. Media architecture

Two image roles remain distinct:

1. **editorial image inside the thread** — large/in-flow narrative image used to give visual rhythm and break long text;
2. **associated record gallery** — potentially many images below a record, using reusable thumbnails/lightbox/lazy-loading infrastructure.

Do not turn ordinary personal photographs into evidence bureaucracy.

Useful metadata such as provenance, credit, period, alt and caption should be applied when appropriate. Explicit labels remain important for AI reconstructions, scans/captures, video frames and redacted versions.

AI reconstruction from memory is illustration, never historical evidence. Minduim BBS remains the canonical example.

---

## 11. Chapter Pages and indexing

Current generated Chapter Page pilots:

- Folhateen PT/EN;
- BEST/Kenshoo PT/EN.

They remain `noindex,follow` and self-canonical with reciprocal hreflang and breadcrumbs.

No mass Chapter Page generation or tag-page generation is authorized.

A single controlled indexation pilot remains reasonable after deliberate review. Xará specifically identified the current all-`noindex` state as producing no Search observation data. Do not turn that observation into automatic mass indexation.

Current indexable core surfaces include Full Biography, Publications, Archive and AI/HAI in PT/EN. Internet & Performance remains `noindex,follow` while it is still being editorially/UX refined.

See `docs/indexation-plan.md` for the current staged plan.

---

## 12. Performance and known technical follow-ups

A reproducible pre-Reader Lighthouse baseline exists in `docs/lighthouse-baseline-2026-08-29.md`.

Known observation from that baseline: Full Biography mobile LCP was about **4.13 s** in the recorded lab run.

The Full Biography has since crossed static image-weight warnings and carries many images. This does not prove equivalent initial transfer because media is lazy-loaded, but it is enough to justify a same-protocol Lighthouse remeasurement before inventing a thumbnail-materialization redesign.

Other live follow-ups:

- native Ctrl+F can still be awkward in Firefox/Safari when `<details>` is closed; test real-reader behavior before replacing the architecture;
- AI/HAI schema can later become richer (for example an `ItemList` of scholarly works with DOI identifiers) once PRO v2 stabilizes;
- one Chapter Page indexing pilot remains available as a controlled SEO experiment;
- long metadata descriptions are low-priority cleanup, not architecture blockers.

---

## 13. Known editorial follow-ups

- **CookieWEB title:** do not keep “Beleza na Web e CookieWEB” as the final thread title. CookieWEB is the entry axis; Beleza na Web should retain strong internal subtitle/text treatment.
- apply rich compact summaries selectively to dense entries after Melissa, using the 1,650/≈1,300 character model;
- continue PRO v2 only when its deeper research content is ready; do not inflate PRO v1 to compensate;
- preserve AI/HAI newest→oldest order.

---

## 14. GitHub working discipline

Before any write, refetch current `main`; Marcelo may upload assets manually between sessions.

Expected sequence:

1. refetch current `main`;
2. create dedicated branch;
3. keep diff scoped;
4. run relevant sync/parity/build/audit steps;
5. open PR;
6. require green Site Audit/browser smoke;
7. merge;
8. confirm post-merge Site Audit;
9. confirm GitHub Pages build/deploy;
10. only then describe the change as published.

Temporary workflows may be used for repository-side transformations when necessary, but must be removed before the PR is finalized.

---

## 15. Document precedence

For conflicts, use this order:

1. explicit later instruction from Marcelo;
2. current `main` implementation + green CI invariants;
3. this `CURRENT-HUB-STATE.md`;
4. `docs/reader-summary-model.md` for compact-thread UX;
5. `docs/entry-authoring-workflow.md` for source/registry/Chapter Page mechanics;
6. `docs/full-biography-workflow.md` for Full Biography/parity mechanics;
7. `docs/visual-archive-plan.md` for media/archive mechanics;
8. `docs/DUKE-LEGACY-DOSSIER-2026-09-01.md` for the implementation-cycle narrative and handoff detail;
9. dated plans/addenda/continuity documents for historical rationale.

Older documents do not regain authority merely because they are more detailed.
