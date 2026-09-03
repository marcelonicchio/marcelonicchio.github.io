# HUB documentation map

**Current documentation index — 3 Sep 2026 (BRT)**

The `/docs` directory mixes living operational documentation with dated historical plans. Use this map so an older handoff is not mistaken for the current implementation.

## Read first

1. **`CURRENT-HUB-STATE.md`** — authoritative C0–C8 architecture/editorial snapshot.
2. **`CHET-CLOSEOUT-2026-09-03.md`** — post-C8 engineering closeout, live-audit results, thematic readiness and remaining operator-gated work.
3. **`reader-summary-model.md`** — selective rich compact-summary model and current rollout state.
4. **`reader-presentation-policy.md`** — path-specific Reader behavior, Full Biography rich-preview emphasis and the approved visual palette rule.
5. **`entry-authoring-workflow.md`** — source, registry, Reader and Chapter Page authoring workflow.
6. **`full-biography-workflow.md`** — Full Biography chronology/parity/synchronization mechanics.
7. **`visual-archive-plan.md`** — media preservation/delivery policy.
8. **`indexation-plan.md`** — staged indexing policy, including the live BEST/Kenshoo pilot.

## Current supporting references

- `runtime-performance-observability.md` — C7 local-Chrome runtime/media observability, scope and non-field-CWV limitations.
- `url-policy.md` — permanent URL/stub policy and Culture + Audiovisual name/URL separation.
- `lighthouse-baseline-2026-08-29.md` — pre-Reader reproducible lab baseline.
- `lighthouse-remeasurement-2026-09-01.md` — post-Reader/post-media same-protocol comparison.
- `block4-readiness-map.md` — historical preparation notes for Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto; current implementation wins where this file is stale.
- `parity-status.md` — PT/EN parity policy/status.
- `launch-checklist.md` — broad release checklist.
- `editorial-fact-audit.md` and `external-profile-alignment.md` — targeted supporting audits.

## Historical handoffs / rationale

These remain useful to understand why choices were made, but are not current-state specifications:

- `DUKE-LEGACY-DOSSIER-2026-09-01.md`;
- `CHET-ADDENDUM-2026-09-02.md` — pre-C1/C2/C3 bridge, superseded by the current-state + closeout pair for operational state;
- `hub-continuity-guide.md`;
- `hub-continuity-addendum-2026-08-29.md`;
- `ux-seo-architecture-v1.md`;
- `entry-architecture-pilot.md`;
- other dated readiness/handoff documents.

Do not delete dated historical documents merely because implementation advanced. Preserve rationale, but do not import their old backlog/state as truth.

## Document precedence

When two sources disagree:

1. explicit later instruction from Marcelo;
2. current `main` implementation and green CI invariants;
3. `CURRENT-HUB-STATE.md` plus `CHET-CLOSEOUT-2026-09-03.md` for the later post-C8 delta;
4. domain-specific current docs;
5. dated dossiers/addenda for historical context only.

**Humans first; semantics second.** Documentation preserves continuity; it must not turn the HUB into an audit artifact.
