# HUB documentation map

**Current documentation index — 1 Sep 2026 (BRT)**

The `/docs` directory contains both living operational documentation and dated historical plans. This index exists so a future collaborator does not accidentally treat an older proposal as the current implementation.

## Read first

1. **`CURRENT-HUB-STATE.md`** — authoritative current architecture/editorial snapshot.
2. **`reader-summary-model.md`** — accepted compact-thread / rich collapsed summary model after the Melissa 1.0 pilot.
3. **`entry-authoring-workflow.md`** — current source, registry, Reader and Chapter Page authoring workflow.
4. **`full-biography-workflow.md`** — Full Biography chronology/parity/synchronization mechanics.
5. **`visual-archive-plan.md`** — media preservation/delivery policy.
6. **`DUKE-LEGACY-DOSSIER-2026-09-01.md`** — implementation-cycle handoff, decisions, milestones and unresolved work.

## Current supporting references

- `lighthouse-baseline-2026-08-29.md` — reproducible pre-Reader Lighthouse lab baseline; still useful as a comparison point, not field data.
- `block4-readiness-map.md` — preparation notes for Petlove → Clickland → BEST/Kenshoo → Ad.Dialetto; use with the current authoring workflow.
- `indexation-plan.md` — current staged indexation policy.
- `parity-status.md` — current PT/EN parity policy/status.
- `launch-checklist.md` — broad release checklist; current implementation/CI always wins if a specific old item conflicts.
- `editorial-fact-audit.md` and `external-profile-alignment.md` — targeted editorial/supporting audits; not replacements for current-state rules.

## Historical architecture / rationale documents

These remain useful because they record why choices were made, but they are **not current-state specifications**:

- `hub-continuity-guide.md` — foundational 27 Aug continuity snapshot;
- `hub-continuity-addendum-2026-08-29.md` — 29 Aug transition snapshot;
- `ux-seo-architecture-v1.md` — pre-implementation Reader/SEO plan;
- `entry-architecture-pilot.md` — original six-case implementation pilot record;
- older handoff/readiness documents that explicitly carry earlier dates/baselines.

Do not delete dated historical documents merely because the implementation advanced. Mark them as historical and preserve their rationale.

## Document precedence

When two documents disagree:

1. explicit later instruction from Marcelo;
2. current `main` implementation and green CI invariants;
3. `CURRENT-HUB-STATE.md`;
4. domain-specific current docs (`reader-summary-model.md`, `entry-authoring-workflow.md`, `full-biography-workflow.md`, `visual-archive-plan.md`);
5. the Duke legacy dossier for handoff/context;
6. dated historical plans and continuity records.

**Humans first; semantics second.** Documentation exists to preserve continuity, not to turn the HUB into an audit artifact.
