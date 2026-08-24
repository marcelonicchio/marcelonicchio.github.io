# Site v1 — launch checklist

This checklist tracks the first public release of the Marcelo Nicchio authority hub.

## 1. Editorial
- [x] Cross-check dates, names, titles and role descriptions against the current master biography / consolidated project record.
- [x] Distinguish public/external evidence from autobiographical material without overloading the prose.
- [x] Keep Work in Progress projects explicitly labeled.
- [x] Verify first-pass PT/EN factual parity while preserving natural language in each version.
- [x] Review historical name variants and spelling in source-specific contexts.
- [x] Replace launch-blocking working-copy language on the Full Biography with a living-archive note suitable for publication.
- [ ] Final whole-site editorial read after future visual/source-asset insertion.

## 2. Archive and rights
- [ ] Select future source assets only when they materially strengthen the public record.
- [x] Establish rule not to publish IDs, signatures, private addresses, employment documents or full corporate records unnecessarily.
- [x] Establish rule to redact third-party personal data when a document excerpt is needed.
- [x] Establish rule to mark AI-generated historical reconstructions as reconstructions, never as original evidence.
- [ ] Check copyright/redistribution rights before uploading each future scan, deck or third-party image.

## 3. Search and entity signals
- [x] Review titles and meta descriptions for the first-release indexable set.
- [x] Validate canonical URLs and required PT/EN/x-default hreflang mechanically.
- [x] Establish ProfilePage / Person + WebSite structured-data architecture.
- [x] Lock first-release indexable set in `tools/audit_site.py`.
- [x] Move Full Biography, Publications, Press & Archive, and AI/HAI PT/EN to `index,follow`.
- [x] Expand `sitemap.xml` to the same indexable set.
- [ ] Validate structured data against the live rendered pages after launch.
- [ ] Ensure ORCID and controlled external profiles link back to the official hub where possible after launch.
- [x] Keep one canonical work record when the same paper/version exists in multiple repositories.
- [x] Add machine-readable canonical entity, experience, timeline, publications and public-source records.
- [x] Keep Music, Communication, Internet, Audiovisual, Search and Selected Projects available to readers but `noindex,follow` in the first release.

## 4. Visual and accessibility
- [x] Refine mobile navigation so long menus scroll horizontally instead of creating a tall multi-row header.
- [x] Add visible keyboard focus states.
- [x] Add reduced-motion handling.
- [x] Increase touch targets for coarse pointers.
- [x] Add initial favicon / MN monogram.
- [x] Upgrade the 404 page and mark it `noindex,follow`.
- [ ] Perform post-launch rendered desktop/mobile inspection on the live GitHub Pages build.
- [ ] Check contrast on the live rendered pages.
- [ ] Add meaningful alt text when historical images are introduced.
- [ ] Create/review future raster social-preview image.

## 5. External profile alignment
- [x] Recheck the public Folha archive anchor.
- [x] Recheck the public HAL profile and document current consistency gaps.
- [x] Confirm the public SSRN record for PRO v1 is discoverable.
- [x] Add a privacy review note for unnecessary personal contact exposure on external research-profile pages; do not reproduce those details in the hub.
- [ ] Audit ORCID record contents manually/live when retrieval is reliable.
- [ ] Add the official hub as the primary website on controlled external profiles after launch.
- [ ] Reconcile any 2024/2025 wording differences between external profiles and the canonical research chronology.
- [x] Treat external-profile normalization as a post-launch authority task rather than a blocker for the first site release.

## 6. Technical QA
- [x] Add dependency-free audit tooling for titles/H1s, internal links, canonical/hreflang, JSON and sitemap/noindex consistency.
- [x] Add GitHub Actions workflow definition for the audit.
- [x] Strengthen the audit to check HTML language declarations, robots metadata and description presence/length.
- [x] Lock the intended first-release indexable set in the audit and require exact sitemap coverage.
- [x] Confirm clean pre-launch GitHub Actions result after indexation changes: Site audit run #64 completed with 0 errors and 0 warnings.
- [x] Confirm the official Folha source resolves during launch QA.
- [x] Record that automated retrieval of some YouTube/Zenodo targets was inconclusive; do not misstate that as a successful HTTP validation.
- [ ] Review the non-blocking GitHub Actions Node-version deprecation warning separately from site QA.

## 7. Launch
- [x] Decide which Stage B thematic pairs are ready for first-release indexing.
- [x] Change those eight Stage B pages to `index,follow` and add them to `sitemap.xml` together.
- [x] Confirm the PR is structurally mergeable before publication.
- [ ] Merge Pull Request #1 into `main`.
- [ ] Verify GitHub Pages deployment after merge.
- [ ] Verify `/`, `/pt/`, `/en/`, Stage B pages, `robots.txt`, `sitemap.xml`, `/data/` records and `llms.txt` live.
- [ ] Submit/refresh indexing through relevant webmaster tools after publication.

## Post-launch
- [ ] Perform rendered desktop/mobile inspection on the live site and fix any visual regressions.
- [ ] Add preserved audio/video as it is safely digitized and published.
- [ ] Expand archive nodes progressively rather than delaying the entire hub for perfect historical coverage.
- [ ] Align HAL, ORCID, GitHub repository metadata and other controlled profiles with the canonical hub.
- [ ] Revisit Stage C indexation as each PT/EN thematic pair clears its editorial and source gates.
