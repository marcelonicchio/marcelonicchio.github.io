# Billy authority rollout — wave 1 — 6 Sep 2026

This rollout promotes five mature entry pairs (10 PT/EN URLs) from staged Chapter Pages to normal search-discoverable authority pages.

## Promoted pairs

- Mirantte News — PT / EN
- CookieWEB — PT / EN
- Folhateen — Órfãos do Rock / Orphans of Rock — PT / EN
- Meia-Noite e Uns — PT / EN
- Melissa 1.0 — PT / EN

## Atomic policy

For every pair, promotion requires all of the following in the same production change:

- `data/entries.json` → `index,follow`;
- generated Chapter Page robots → `index,follow`;
- membership in `LAUNCH_INDEXABLE`;
- membership in `sitemap.xml` with Git-derived `lastmod`;
- self-canonical and reciprocal PT/EN hreflang;
- normal static links from every registered Reader/source target;
- green entry architecture and whole-site audit.

No autobiographical copy, factual claims, galleries, main-vertical robots or Full Biography robots are changed by this rollout.

## Staged separately

`O Buscador / The Seeker` remains outside wave 1 because it is biography-only. Its autonomous page is mature, but promotion requires the Full Biography generator to guarantee a static permalink to the standalone Chapter Page before it can pass the same indexation gate.

Projects remains staged and is not promoted by this rollout.
