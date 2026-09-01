# Bilingual factual/editorial parity status

**Status:** continuous operational discipline  
**Updated:** 1 Sep 2026 (BRT)

PT/EN parity is no longer a one-time “v1 pass”. The HUB is a living autobiography, so parity is maintained entry by entry whenever public narrative changes.

## Current paired surfaces

- Hub home: PT / EN
- Full Biography: PT / EN
- Music: PT / EN
- Communication: PT / EN
- **Internet & Performance: PT / EN**
- Audiovisual: PT / EN
- AI/HAI: PT / EN
- Publications: PT / EN
- Archive: PT / EN
- Selected Projects: PT / EN

The former standalone Search/Performance architecture is not a current thematic pair. Search is integrated into Internet & Performance; legacy Search paths are compatibility/redirect surfaces and must not be treated as a second editorial vertical.

## Entry-level parity infrastructure

Current managed workflow uses:

- `data/editorial_parity.json`;
- `tools/editorial_parity.py`;
- thematic PT/EN editorial sources;
- `tools/sync_full_biography.py`;
- `tools/audit_full_biography.py`.

A changed managed entry should not silently pass just because the other language still exists. The affected PT/EN pair must be editorially reviewed and its checkpoint accepted before the Full Biography synchronization is considered complete.

## What parity means

Parity means agreement on materially equivalent:

- dates/periods;
- roles;
- project status;
- causal relationships;
- titles/names;
- version relationships;
- media/resource meaning;
- epistemic caveats where they are part of the subject.

It does **not** require literal sentence-by-sentence translation.

## Current AI/HAI examples

The following are deliberately mirrored in meaning across PT/EN:

- newest→oldest research order: PRO v2 → PRO v1 → Melissa 1.0;
- PRO v1 as first public formulation, not final methodology;
- 54-interaction pilot and its explicit limitation;
- Melissa 11 sessions / ~63 hours / 518 prompts;
- reasoning-trace framing and EIP caveat;
- Melissa authorship of the six Framework layers;
- four DOI works + repository;
- selective rich collapsed Melissa preview;
- topic labels and curated internal-content indicators.

## Rich Reader previews

When a structured `reader_preview` exists, PT/EN should be equivalent in information even when character counts differ.

Current density rule:

- maximum 1,650 visible-copy characters per language;
- normal design center ~1,300–1,320 characters;
- shorter is allowed;
- title/date/tags/indicators/CTA are outside the copy budget.

See `docs/reader-summary-model.md`.

## Rule

Any factual/editorial correction in one language triggers a counterpart review. New publication outcomes, DOIs, repositories or project-status changes must be reflected in both languages when they become public facts.

Parity review remains separate from robots/indexation, rights/privacy review and final visual QA.
