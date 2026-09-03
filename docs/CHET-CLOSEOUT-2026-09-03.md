# CHET CLOSEOUT — 3 Sep 2026

This is the operational supplement after C0–C8. It records only work completed after the C8 baseline and decisions that materially affect the next implementation cycle. Historical dossiers remain useful rationale; `main` + green CI remain the implementation truth.

## 1. Technical closeout

The post-C8 audit was completed against both repository output and the deployed GitHub Pages baseline.

Permanent changes:

- every local raster `<img>` delivered in the audited HTML now carries explicit intrinsic `width` and `height`;
- Reader preview image definitions carry intrinsic dimensions and the runtime applies them to generated preview images;
- the archive lightbox seeds and updates intrinsic dimensions for its runtime image;
- `tools/audit_image_dimensions.py` is a permanent blocking gate;
- `tools/smoke_runtime_performance.js` now fails when intrinsic image dimensions are missing on initial render or after full expansion/scroll;
- gallery palette/transparency handling is normalized before RGB/WebP conversion, removing the prior Pillow warning at the source;
- Reader and archive-lightbox cache versions were advanced, and the Reader loader synchronizer can replace an older loader version rather than appending a duplicate;
- permanent GitHub Actions use the current action generations adopted in this closeout and Node 24 for JavaScript/browser QA.

Validated closeout baseline:

- 811 local raster HTML images audited with intrinsic dimensions;
- 10 Reader preview definitions audited with intrinsic dimensions;
- 43 PT/EN editorial source units match accepted parity checkpoints;
- Full Biography: 38 chronological entries + 5 context entries, PT/EN coverage complete;
- Reader UX browser smoke: pass;
- English rich Reader summary smoke: pass;
- runtime performance/media smoke: pass;
- sitemap generator/check: pass;
- HTML/SEO audit: 0 errors, 0 warnings;
- Full Biography mobile probe: no horizontal overflow, 0 missing intrinsic images, CLS 0 in the closeout run;
- Internet & Performance desktop probe: no horizontal overflow, 0 missing intrinsic images, CLS approximately 0.0088 in the closeout run.

The runtime numbers above are local CI regression signals, not field Core Web Vitals and not real INP.

## 2. Live deployment baseline

The live baseline was rechecked during closeout before packaging. The following public surfaces returned HTTP 200 and the expected post-C8 content markers:

- `/`;
- `/pt/` and `/en/`;
- Full Biography PT/EN;
- Internet & Performance PT/EN;
- BEST/Kenshoo PT/EN Chapter Pages;
- Mídia & Cultura / Media & Culture PT/EN;
- AI/HAI PT/EN;
- `robots.txt`;
- `sitemap.xml`;
- `llms.txt`;
- `data/person.json`.

JSON-LD on the audited HTML surfaces parsed successfully.

## 3. Thematic-vertical readiness

This is a readiness assessment only. **No robots/indexation state was changed in this closeout.** The existing Home-first sequencing remains in force.

### READY after substantive Home

- **Mídia & Cultura / Media & Culture** — technically mature, continuous-reading presentation intentional, fused architecture stable.
- **Internet & Performance** — technically mature, Reader architecture stable, entry and Chapter Page relationships established.
- **Music / Música** — structurally and editorially viable as an authority vertical even though its archive will continue growing. Archive incompleteness alone should not block eventual indexation.

### HOLD

- **Selected Projects / Projetos** — currently useful as a transversal project/card index, but not yet as deep an authority surface as the three verticals above. Do not include it automatically in the first thematic-indexation promotion batch.

Promotion still requires an atomic PT/EN release: robots + sitemap + audit whitelist + canonical/hreflang/internal-link verification.

## 4. BEST/Kenshoo pilot

BEST/Kenshoo remains the only standalone Chapter Page pair intentionally promoted to `index,follow` in the current experiment.

Do not promote another Chapter Page merely for symmetry. Lack of immediate public-search confirmation is not evidence of a technical failure; use Search Console/normal observation before expanding the experiment.

## 5. PR #9 archaeology

The old business-card PR #9 was closed without merge.

Reason: the relevant cards are already represented by selected public derivatives in the current archive architecture. Reintroducing the old raw JPG set would conflict with the current media policy, which does not import raw masters by default merely because an older PR contains them.

## 6. External authority maintenance queue

Checked again on 3 Sep 2026:

- **HAL** still needs operator-side alignment: its public presentation still describes full-time AI/HCI research as beginning in 2024 and its website/contact section should be reviewed so the official HUB is the canonical personal-site destination. Reconcile `career transition`, `research interest` and the later public research cycle rather than forcing them into one date.
- **SSRN** remains a useful public PRO v1 authority node, but its public author/contact area exposes more direct personal contact information than the HUB should reproduce. Review SSRN privacy/profile settings where the platform permits it; preserve the research record.

Do not copy external personal contact details into HUB prose, schema or documentation.

## 7. Operator-gated / intentionally untouched

The closeout did **not** change:

- substantive Home/entity prose — Marcelo-authored;
- featured-card palette;
- operator-selected replacement preview images for Mirantte/CookieWEB/Meia-Noite;
- Coitado do Próximo archive expansion or other new editorial/media lots;
- thematic vertical robots/indexation;
- Full Biography robots/indexation.

Full Biography robots remain a separate explicit Marcelo/Xará decision if ever revisited.

## 8. State after closeout

C0–C8 are complete. The post-C8 engineering closeout is complete once this branch passes the permanent Site Audit, is merged to `main`, and the resulting GitHub Pages deployment is verified.

After that point, there is no hidden Chet engineering backlog from the C0–C8 cycle. New work can begin from Marcelo's next editorial/visual/archive instructions without first paying down an inherited technical closeout.
