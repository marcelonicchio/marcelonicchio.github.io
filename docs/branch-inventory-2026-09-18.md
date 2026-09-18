# Branch inventory — 18 Sep 2026

Snapshot taken before any branch deletion. This is a governance aid, not an authorization to delete refs.

## Snapshot summary

At the time of inventory:

- approximately 200 remote branches existed;
- 166 branches were associated with at least one already-merged pull request;
- 5 branches had an open pull request at that snapshot, including active Kurt work;
- 27 branches had no associated pull request;
- after excluding `main` and the temporary Lighthouse branch created during this maintenance cycle, 25 older no-PR branches required classification.

The comparison below asks a narrow question: **does the branch tip contain commits not reachable from current `main`?**

## Older no-PR branches fully contained in main

These branches had no tip commits exclusive to the branch at the snapshot:

- `archive-business-cards`
- `benny/music-programa-jo-thread-photo`
- `billy/promote-seeker-communication-2026-09-06`
- `full-biography-chronology`
- `full-biography-parity`
- `full-biography-parity-active`
- `full-biography-parity-bootstrap`
- `full-biography-parity-current`
- `full-biography-parity-finalwork`
- `full-biography-parity-now`
- `full-biography-parity-work`
- `full-biography-parity-work2`
- `rollback/global-video-standard`
- `temp-never-use`
- `work/reader-cta-badge-test-2`
- `work/ux-performance-followup`

They are **cleanup candidates**, not automatically disposable. Before deletion, still confirm that no external workflow/reference depends on the branch name.

## Older no-PR branches with exclusive commits

Do not delete these without content inspection:

| Branch | Exclusive tip commits at snapshot |
|---|---:|
| `archive-minduim-bbs` | 5 |
| `archive-minduim-v2` | 1 |
| `billy/chapter-semantic-graph-2026-09-06` | 1 |
| `feat/video-media-wave1-music-20260914` | 12 |
| `media-home-portrait-v1` | 4 |
| `preview-block3a` | 2 |
| `work/chapter-page-seo-descriptions` | 5 |
| `work/chet-post-c8-closeout` | 21 |
| `work/mobile-nav-operational` | 11 |

“Exclusive” means Git commit ancestry differs; it does **not** prove the actual file content is still valuable or absent from main through another implementation. These nine require file-level inspection before any cleanup decision.

## File-level triage of the nine divergent branches

This second pass inspected the files introduced or changed by each branch's exclusive commit history.

| Branch | What the exclusive history contains | Triage |
|---|---|---|
| `archive-minduim-bbs` | one-shot reconstruction workflow/tool, temporary base64 chunk, Minduim image and early Archive/Internet integration | likely implementation precursor; current main already uses the Minduim reconstruction, but compare tooling before deletion |
| `archive-minduim-v2` | only `.tmp/minduim/chunk00.b64` | temporary upload artifact; strong cleanup candidate after confirming no recovery need |
| `billy/chapter-semantic-graph-2026-09-06` | Chapter Page generator semantic/schema experiment | preserve until current semantic work is complete; concept may contain reusable logic |
| `feat/video-media-wave1-music-20260914` | changes to Destemidos Limonadas content, Music/Full Bio renderings and CSS | editorial/media branch; inspect content diffs before deletion |
| `media-home-portrait-v1` | four temporary base64 portrait chunks only | upload artifact; strong cleanup candidate because the final portrait asset exists on main |
| `preview-block3a` | static preview copies of biography and internet pages | obsolete-looking preview artifact; safe only after confirming it is not a retained review fixture |
| `work/chapter-page-seo-descriptions` | Chapter Page metadata changes in `data/entries.json`, generated Folhateen/BEST pages and generator support | potentially useful SEO copy/logic; preserve for comparison |
| `work/chet-post-c8-closeout` | broad pre-clean closeout: workflows, JS, parity, entries, docs, page renderings and audit tools | high-volume precursor; likely superseded in part by later clean closeout, but requires content comparison before deletion |
| `work/mobile-nav-operational` | initial mobile-nav JS/CSS, sync/audit changes and site-wide loader insertion | precursor to the later approved mobile-nav rollout; likely superseded, but verify against current assets before deletion |

This classification is based on file history, not just branch names. “Likely precursor” is not deletion authorization.

## Open stale PRs at the snapshot

Two pre-Kurt open PRs remain strategically stale:

- **#102** — `billy/vertical-semantic-readiness-2026-09-06`: do not merge; selectively reimplement the useful semantic idea on current main.
- **#147** — `chore/sync-repo-workflow-docs`: current documentation work supersedes its operational purpose; review/close separately after the replacement docs land.

## Rule

No branch cleanup should be performed from branch count alone. Use this order:

1. check associated PR state;
2. compare branch tip ancestry with current main;
3. inspect exclusive file diffs where commits remain;
4. preserve anything with unresolved historical/media value;
5. delete only after an explicit cleanup decision.

This inventory deliberately performs no deletion.
