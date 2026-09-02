# Runtime performance and media observability

**Introduced:** 2 Sep 2026 (C7)

The HUB already had static full-scroll image-weight reporting and dated Lighthouse lab runs. C7 adds a third layer: a reproducible local-Chrome runtime probe that exercises the current Reader and media behavior on every Site Audit run.

## What the probe measures

`tools/smoke_runtime_performance.js` reports, for selected Reader surfaces:

- local navigation timing;
- Largest Contentful Paint observed by Chromium;
- initial Cumulative Layout Shift;
- long-task count/total/max;
- JS heap usage when Chromium exposes `performance.memory`;
- total/lazy/loaded image counts before scrolling;
- actual image resource requests;
- image decode success for loaded same-origin assets;
- horizontal overflow;
- a two-`requestAnimationFrame` Reader open/close latency proxy;
- the same media/heap snapshot after expanding Reader entries and scrolling the page.

Current probes cover:

- Full Biography on a mobile viewport;
- Internet & Performance on a desktop viewport.

## What it does NOT claim

This is **not field Core Web Vitals**.

External requests are blocked so the test isolates repository HTML/CSS/JS/media behavior. Consequently:

- local LCP is useful for regression comparison, not as a substitute for production-user LCP;
- the script reports initial CLS as a lab structural signal;
- the Reader timing is an interaction-latency proxy, **not INP**;
- real INP requires genuine field interactions/telemetry;
- network/CDN/font/analytics behavior is intentionally outside this probe.

Do not publish these CI numbers as real-user performance data.

## Blocking vs warning behavior

The probe blocks regressions that are structural and comparatively deterministic:

- horizontal overflow;
- decode failure of already-loaded same-origin images;
- Reader interaction proxy reaching 300 ms or more;
- on a long image-heavy Reader page, all lazy images loading before any scroll;
- loaded-image count decreasing after expansion/full scroll.

It emits review warnings rather than hard failures for more environment-sensitive signals:

- local CLS above 0.10;
- local LCP above 2.5 s;
- a local long task above 200 ms;
- images lacking explicit width/height attributes.

Warnings are intended to create visibility before thresholds become policy.

## Relationship to existing performance evidence

Keep three concepts separate:

1. `tools/audit_page_weight.py` — static potential full-scroll image payload; not initial transfer;
2. Lighthouse dated documents — reproducible point-in-time lab benchmarks;
3. `tools/smoke_runtime_performance.js` — continuous CI regression/observability probe of current runtime behavior.

A static page becoming heavier does not automatically mean its initial transfer or LCP regressed. Measure before redesigning media architecture.

## Future extension

If real-user performance collection is introduced later, field metrics should be kept separate from CI output and should prefer privacy-conscious aggregate telemetry. In particular, true INP should not be inferred from synthetic clicks.
