# Billy authority state — 6 Sep 2026

Operational checkpoint after B1, publication schema rollout, Chapter Page wave 1, O Buscador / The Seeker promotion and Culture & Audiovisual promotion.

This file records the **current deployed/indexation contract**, not merely the destination plan. The earlier URL matrix remains useful as the pre-rollout baseline.

## Current launch-indexable count

`LAUNCH_INDEXABLE`: **27 HTML URLs**.

### Entity / language / core surfaces — 13 URLs

- `/`
- `/pt/`
- `/en/`
- `/pt/biografia/`
- `/en/biography/`
- `/pt/publicacoes/`
- `/en/publications/`
- `/pt/arquivo/`
- `/en/archive/`
- `/pt/ia-hai/`
- `/en/ai-hai/`
- `/pt/internet/best-kenshoo/`
- `/en/internet/best-kenshoo/`

### Chapter Page authority wave 1 — 10 URLs

- `/pt/internet/mirantte-news/`
- `/en/internet/mirantte-news/`
- `/pt/internet/cookieweb/`
- `/en/internet/cookieweb/`
- `/pt/comunicacao/folhateen-orfaos-do-rock/`
- `/en/communication/folhateen-orphans-of-rock/`
- `/pt/comunicacao/meia-noite-e-uns/`
- `/en/communication/meia-noite-e-uns/`
- `/pt/ia-hai/melissa-1-0/`
- `/en/ai-hai/melissa-1-0/`

### Biography-only authority pair — 2 URLs

- `/pt/biografia/espiritualidade-o-buscador/`
- `/en/biography/spirituality-the-seeker/`

`O Buscador / The Seeker` remains biography-only. No artificial `/ensaios/` or `/essays/` vertical was created.

### Culture & Audiovisual top-level vertical — 2 URLs

- `/pt/comunicacao/`
- `/en/communication/`

The vertical was promoted because its remaining work is targeted enrichment/correction, not structural completion. The promotion changed robots, sitemap membership and the launch contract only; editorial copy was not changed.

---

## Structured publications state

The PT/EN Publications pages now expose a canonical scholarly graph:

- 5 published works represented as `ScholarlyArticle`;
- 4 Melissa 1.0 works;
- The Punk Rock Orchestra v1 as **one work**, even though it has multiple repository/DOI instances;
- PRO v2 remains excluded while WIP.

`tools/audit_publication_schema.py` protects PT/EN identity, titles, DOI sets, versions and work count against `data/publications.json`.

---

## Still intentionally staged

### Music / Música

- `/pt/musica/`
- `/en/music/`

Remain `noindex,follow` pending substantive Coitado do Próximo work: formations/collaborators, repertoire/authorship map, album-level depth, archive integration, 2001–2003 closing phase and 2023 reunion depth.

### Internet & Performance

- `/pt/internet/`
- `/en/internet/`

Remain `noindex,follow` pending the principal autobiographical/content arc:

**Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto**

Mirantte News, CookieWEB and BEST/Kenshoo already have autonomous indexable authority pages, so the remaining blocker is the top-level narrative continuity rather than absence of searchable evidence.

### Selected Projects

- `/pt/projetos/`
- `/en/projects/`

Remain staged. Authority/search value still needs an explicit final decision; no need to promote merely to increase URL count.

### Full Biography

- `/pt/biografia/`
- `/en/biography/`

Remain `index,follow` **for now**.

Destination remains `noindex,follow`, but the flip should happen only after Music and Internet top-level authority surfaces are ready. Full Biography remains a first-class human navigation/Reader surface after that future change.

---

## Legacy compatibility surfaces

These remain `noindex,follow`, outside the sitemap, and canonicalize to their current authority verticals:

- `/pt/audiovisual/` → `/pt/comunicacao/`
- `/en/audiovisual/` → `/en/communication/`
- `/pt/search-performance/` → `/pt/internet/`
- `/en/search-performance/` → `/en/internet/`

They are compatibility surfaces, not authority pages.

---

## Current shortest path to the ~95% target

Technical work that can proceed without new autobiographical copy:

1. keep machine-readable entity/publication/navigation layers synchronized;
2. audit internal authority graph and sitemap after each promotion;
3. prepare but do not execute the Full Biography `noindex,follow` cutover;
4. preserve Projects as staged until its search role is justified;
5. continue whole-site QA and CI hardening.

Author-dependent work beginning with Marcelo's interventions:

1. Coitado do Próximo / Music depth;
2. Internet 2012–2015 autobiographical arc;
3. targeted Culture & Audiovisual corrections/enrichment if any;
4. final voice/factual review before the last indexation wave.

## Expected destination count

If Music and Internet PT/EN verticals are promoted and Full Biography PT/EN is then removed from indexation while Projects remains staged:

- current: **27 indexable URLs**;
- + Music PT/EN: **29**;
- + Internet PT/EN: **31**;
- − Full Biography PT/EN after authority cutover: **29 final indexable URLs**.

This matches the destination model in the baseline matrix with Projects left staged.
