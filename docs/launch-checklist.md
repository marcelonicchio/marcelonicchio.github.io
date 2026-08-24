# Site v1 — launch checklist

This checklist tracks the first public release of the Marcelo Nicchio authority hub.

## 1. Editorial
- [x] Cross-check dates, names, titles and role descriptions against the current master biography / consolidated project record.
- [x] Distinguish public/external evidence from autobiographical material without overloading the prose.
- [x] Keep Work in Progress projects explicitly labeled.
- [x] Verify first-pass PT/EN factual parity while preserving natural language in each version.
- [x] Review historical name variants and spelling in source-specific contexts.
- [ ] Final whole-site editorial read after visual/source-asset insertion.

## 2. Archive and rights
- [ ] Select only source assets that materially strengthen the public record.
- [x] Establish rule not to publish IDs, signatures, private addresses, employment documents or full corporate records unnecessarily.
- [x] Establish rule to redact third-party personal data when a document excerpt is needed.
- [x] Establish rule to mark AI-generated historical reconstructions as reconstructions, never as original evidence.
- [ ] Check copyright/redistribution rights before uploading each scan, deck or third-party image.

## 3. Search and entity signals
- [ ] Final review of titles and meta descriptions page by page.
- [ ] Validate canonical URLs and PT/EN hreflang pairs mechanically / link-by-link.
- [x] Establish ProfilePage / Person + WebSite structured-data architecture.
- [ ] Validate structured data against the final rendered pages.
- [ ] Ensure ORCID and controlled external profiles link back to the official hub where possible.
- [x] Define staged indexation policy: a thematic page moves from `noindex,follow` only after editorial review.
- [x] Define sitemap rule: add a page pair only when it becomes indexable.
- [x] Keep one canonical work record when the same paper/version exists in multiple repositories.
- [x] Add machine-readable canonical entity, experience, timeline, publications and public-source records.

## 4. Visual and accessibility
- [x] Refine mobile navigation so long menus scroll horizontally instead of creating a tall multi-row header.
- [ ] Perform final rendered desktop/mobile inspection.
- [ ] Test long titles and narrow screens on actual rendered pages.
- [x] Add visible keyboard focus states.
- [x] Add reduced-motion handling.
- [x] Increase touch targets for coarse pointers.
- [ ] Check contrast on the final rendered pages.
- [ ] Add meaningful alt text when historical images are introduced.
- [ ] Confirm all primary actions and external source links work.
- [x] Add initial favicon / MN monogram.
- [x] Upgrade the 404 page and mark it `noindex,follow`.
- [ ] Create/review future raster social-preview image.

## 5. External profile alignment
- [x] Recheck the public Folha archive anchor.
- [x] Recheck the public HAL profile and document current consistency gaps.
- [x] Confirm the public SSRN record for PRO v1 is discoverable.
- [ ] Audit ORCID record contents manually/live when retrieval is reliable.
- [ ] Add the official hub as the primary website on controlled external profiles after launch.
- [ ] Reconcile any 2024/2025 wording differences between external profiles and the canonical research chronology.
- [x] Treat external-profile normalization as a post-launch authority task rather than a blocker for the first site release.

## 6. Technical QA
- [x] Add dependency-free audit tooling for titles/H1s, internal links, canonical/hreflang, JSON and sitemap/noindex consistency.
- [x] Add GitHub Actions workflow definition for the audit.
- [ ] Confirm an actual successful workflow run before treating CI as a release gate.
- [ ] Finish launch-page external-link QA.

## 7. Launch
- [ ] Final diff review in Pull Request #1.
- [ ] Confirm `main` is still the stable public source before merge.
- [ ] Decide which Stage B thematic pairs are ready for first-release indexing.
- [ ] Update `robots` meta + `sitemap.xml` for those pairs in the same release.
- [ ] Merge only after the first release is coherent as a whole.
- [ ] Verify GitHub Pages deployment after merge.
- [ ] Verify `/`, `/pt/`, `/en/`, `robots.txt`, `sitemap.xml`, `/data/` records and `llms.txt` live.
- [ ] Submit/refresh indexing through relevant webmaster tools after publication.

## Post-launch
- [ ] Add preserved audio/video as it is safely digitized and published.
- [ ] Expand archive nodes progressively rather than delaying the entire hub for perfect historical coverage.
- [ ] Align HAL, ORCID, GitHub repository metadata and other controlled profiles with the canonical hub.
- [ ] Revisit Stage B indexation as each PT/EN thematic pair clears its editorial and source gates.
