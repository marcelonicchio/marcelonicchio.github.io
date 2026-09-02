# Permanent URL policy

**Status:** current operational policy · 1 Sep 2026

The HUB treats a published URL as a durable public contract. Display names, menu labels and editorial titles may change without forcing the URL to change. Prefer preserving an established path when the path remains semantically serviceable.

## When a published path must change

Because GitHub Pages does not provide repository-level HTTP redirects, the old path remains in the repository permanently as a compatibility stub.

Every compatibility stub must:

- use `noindex,follow`;
- contain `<link rel="canonical">` pointing to the definitive new URL;
- redirect immediately with `<meta http-equiv="refresh" content="0; url=…">`;
- provide a normal visible link to the destination as a fallback;
- preserve the correct language counterpart/hreflang when applicable;
- stay out of `sitemap.xml`;
- never compete as a second content surface.

Stubs are not temporary cleanup files. Once an old public URL has been replaced, its compatibility stub is retained indefinitely unless the hosting platform later gains a verified server-side redirect mechanism and migration is deliberately reviewed.

## Name and URL are independent decisions

A navigation label, page H1 and URL slug do not need to be identical. Prefer the shortest useful navigation label, the most precise editorial H1, and the most stable existing URL.

Current application approved for the Communication + Audiovisual consolidation:

- menu PT: **Mídia & Cultura**;
- menu EN: **Media & Culture**;
- H1/title PT: **Cultura & Audiovisual**;
- H1/title EN: **Culture & Audiovisual**;
- canonical vertical paths remain **`/pt/comunicacao/`** and **`/en/communication/`**.

Therefore the Folhateen Chapter Page keeps its existing path. Only the former standalone Audiovisual vertical paths will require compatibility stubs when the fusion is implemented.
