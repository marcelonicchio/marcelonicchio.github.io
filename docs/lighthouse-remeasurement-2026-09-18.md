# Lighthouse remeasurement — 18 Sep 2026

Reference: 2026-09-18 BRT  
Protocol: same Lighthouse performance protocol established on 29 Aug and repeated on 1 Sep, with Music added as a new surface.  
Measurement source: Lighthouse CLI in GitHub Actions against the public GitHub Pages deployment.

This is **lab data, not CrUX field data**. Lighthouse was pinned to 13.4.1. Each case ran three times; the table reports the median. The mobile runs showed meaningful run-to-run variance, so direction should be interpreted together with the individual values rather than from one score alone.

## Environment

- Lighthouse: 13.4.1
- Chrome: 152
- First fetch: 2026-09-18T05:04:38Z
- Mobile: Lighthouse default performance profile
- Desktop: `--preset=desktop`
- Chrome flags: `--headless --no-sandbox --disable-gpu`

## Median results

| Surface | Mode | Score | FCP | LCP | CLS | TBT | Speed Index | TTI | Transfer | Requests |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Full Biography PT | mobile | 80 | 1429 ms | 4198 ms | 0.0875 | 180 ms | 3085 ms | 4390 ms | 0.86 MiB | 22 |
| Full Biography PT | desktop | 100 | 388 ms | 468 ms | 0.0000 | 0 ms | 417 ms | 469 ms | 1.21 MiB | 30 |
| Internet & Performance PT | mobile | 94 | 1108 ms | 2819 ms | 0.0875 | 93 ms | 1108 ms | 3453 ms | 0.60 MiB | 22 |
| Internet & Performance PT | desktop | 100 | 342 ms | 742 ms | 0.0147 | 0 ms | 366 ms | 749 ms | 0.54 MiB | 22 |
| Music PT | mobile | 98 | 1155 ms | 1212 ms | 0.0875 | 85 ms | 1419 ms | 3444 ms | 0.88 MiB | 19 |
| Music PT | desktop | 100 | 364 ms | 734 ms | 0.0000 | 0 ms | 504 ms | 734 ms | 0.85 MiB | 19 |

## Comparison with 1 Sep median

| Surface | Mode | 1 Sep LCP | 18 Sep LCP | Delta |
|---|---|---:|---:|---:|
| Full Biography PT | mobile | 2761 ms | 4198 ms | +1437 ms |
| Full Biography PT | desktop | 682 ms | 468 ms | -214 ms |
| Internet & Performance PT | mobile | 1022 ms | 2819 ms | +1797 ms |
| Internet & Performance PT | desktop | 745 ms | 742 ms | -3 ms |

Music has no earlier same-protocol baseline; 18 Sep is its baseline.

## Mobile run variance

LCP by individual run:

- Full Biography PT: **4198 / 1444 / 4350 ms**
- Internet & Performance PT: **4352 / 1085 / 2819 ms**
- Music PT: **4401 / 1212 / 1151 ms**

The first two surfaces therefore do not support a confident claim of a deterministic mobile regression from this three-run sample alone. Music also had one slow outlier, but two of three runs clustered near 1.2 s. The continuous local-Chrome runtime probe remains the better regression guard for repository behavior; Lighthouse remains a dated production lab benchmark.

## Interpretation

- Music enters the measured baseline in strong shape: median **98 mobile / 100 desktop**, with median LCP **1.21 s / 0.73 s**.
- Internet desktop remains effectively unchanged from 1 Sep.
- Full Biography desktop improved in this lab sample.
- Mobile Full Biography and Internet were materially noisier than the 1 Sep medians. Re-measure before attributing that change to page architecture.
- The 18 Sep indexation cutover changed robots/sitemap/authority policy, not body layout or media architecture, so it is not a plausible direct cause of the Lighthouse timing spread.

## Relationship to other evidence

Keep separate:

1. `tools/audit_page_weight.py` — potential full-scroll image payload;
2. this Lighthouse report — dated public-production lab benchmark;
3. `tools/smoke_runtime_performance.js` — continuous CI runtime regression probe, now including Music mobile and desktop.

Do not remove archive content merely to reduce the static full-scroll inventory without measured runtime evidence.
