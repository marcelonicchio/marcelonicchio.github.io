# Current repository status

_Last updated: 2026-09-11_

This document is an operational checkpoint for the live Marcelo Nicchio personal hub.

## Source of truth

- `main` is the public branch and current source of truth.
- Active development should use short-lived branches such as `feat/*`, `fix/*`, and `chore/*`, with pull requests targeting `main`.
- `site-v1` is a historical pre-launch branch. It is retained for reference and must not be treated as the current development base without an explicit reconciliation decision.

## Current state

- The hub is already live on GitHub Pages.
- The project is bilingual (PT/EN) and includes thematic pages, structured data, archive assets, evidence records, automation, and machine-readable discovery files.
- Recent development has been concentrated on the historical music archive, especially Coitado do Próximo and Programa do Jô material, with PT/EN synchronization and Full Biography parity.
- Repository quality controls include static site audit tooling and GitHub Actions workflows.

## Recent checkpoint

As of 2026-09-10, the latest merged work on `main` added and synchronized all eight Programa do Jô backstage videos. The latest merge commit on `main` is `44a382011714393ed3ae003310c37b63b4011b72`.

## Operating priorities

1. Continue archive expansion without breaking PT/EN factual parity.
2. Keep `main` clean and use reviewable pull requests for changes.
3. Maintain consistency between thematic pages, Full Biography, structured data, sitemap/indexation decisions, and evidence records.
4. Review and progressively modernize internal documentation that still reflects the pre-launch workflow.
5. Perform periodic rendered QA on desktop/mobile and validate live metadata/structured data.
6. Preserve rights, provenance, and explicit labeling of AI reconstructions versus original historical evidence.

## Known housekeeping

- `README.md` previously described `site-v1` as the active development branch and referred to Pull Request #1 as the review surface. That description is obsolete and is being corrected.
- `docs/launch-checklist.md` is useful as launch history but includes pre-launch items and branch assumptions that should not be interpreted as the current workflow.

## Safety rule for repository changes

When in doubt, create a short-lived branch from current `main`, make the smallest coherent change, review the diff, run available checks, and merge only after verification.
