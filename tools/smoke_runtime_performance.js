#!/usr/bin/env node
/**
 * Local Chrome observability probe for Reader/media runtime behavior.
 *
 * This is deliberately NOT field Core Web Vitals. External requests are blocked
 * so the test isolates repository HTML/CSS/JS/media behavior. It reports lab LCP,
 * initial CLS, long tasks, JS heap (when Chromium exposes it), image loading/decode,
 * full-scroll behavior and a two-rAF Reader interaction-latency proxy.
 */

const fs = require('fs');
const http = require('http');
const path = require('path');
const { URL } = require('url');

const playwrightPath = process.env.PLAYWRIGHT_CORE_PATH || 'playwright-core';
const { chromium } = require(playwrightPath);

const ROOT = path.resolve(__dirname, '..');
const HOST = '127.0.0.1';
const PORT = Number(process.env.RUNTIME_PERF_PORT || 8767);
const BASE = `http://${HOST}:${PORT}`;
const CHROME = process.env.CHROME_PATH || '/usr/bin/google-chrome';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.mp4': 'video/mp4',
};

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function localFileFor(rawUrl) {
  const parsed = new URL(rawUrl, BASE);
  let pathname = decodeURIComponent(parsed.pathname);
  if (pathname.endsWith('/')) pathname += 'index.html';
  const candidate = path.resolve(ROOT, `.${pathname}`);
  if (!(candidate === ROOT || candidate.startsWith(`${ROOT}${path.sep}`))) return null;
  return candidate;
}

function createServer() {
  return http.createServer((req, res) => {
    const file = localFileFor(req.url || '/');
    if (!file || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      res.writeHead(404, {'content-type': 'text/plain; charset=utf-8'});
      res.end('Not found');
      return;
    }
    const type = MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
    res.writeHead(200, {'content-type': type, 'cache-control': 'no-store'});
    fs.createReadStream(file).pipe(res);
  });
}

async function blockExternal(page) {
  await page.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    if (url.hostname === HOST && Number(url.port || 80) === PORT) await route.continue();
    else await route.abort();
  });
}

async function installObservers(page) {
  await page.addInitScript(() => {
    window.__mnRuntimePerf = {
      lcp: 0,
      lcpSize: 0,
      cls: 0,
      longTaskCount: 0,
      longTaskTotal: 0,
      longTaskMax: 0,
    };
    try {
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          window.__mnRuntimePerf.lcp = entry.startTime || 0;
          window.__mnRuntimePerf.lcpSize = entry.size || 0;
        }
      }).observe({type: 'largest-contentful-paint', buffered: true});
    } catch (_) {}
    try {
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) window.__mnRuntimePerf.cls += entry.value || 0;
        }
      }).observe({type: 'layout-shift', buffered: true});
    } catch (_) {}
    try {
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          const duration = entry.duration || 0;
          window.__mnRuntimePerf.longTaskCount += 1;
          window.__mnRuntimePerf.longTaskTotal += duration;
          window.__mnRuntimePerf.longTaskMax = Math.max(window.__mnRuntimePerf.longTaskMax, duration);
        }
      }).observe({type: 'longtask', buffered: true});
    } catch (_) {}
  });
}

async function snapshot(page) {
  return page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0] || {};
    const images = [...document.images];
    const loaded = (img) => img.complete && img.naturalWidth > 0;
    const resources = performance.getEntriesByType('resource');
    const perf = window.__mnRuntimePerf || {};
    return {
      navigation: {
        domContentLoaded: nav.domContentLoadedEventEnd || 0,
        load: nav.loadEventEnd || 0,
      },
      lcp: perf.lcp || 0,
      lcpSize: perf.lcpSize || 0,
      cls: perf.cls || 0,
      longTasks: {
        count: perf.longTaskCount || 0,
        total: perf.longTaskTotal || 0,
        max: perf.longTaskMax || 0,
      },
      heap: performance.memory ? {
        used: performance.memory.usedJSHeapSize,
        total: performance.memory.totalJSHeapSize,
        limit: performance.memory.jsHeapSizeLimit,
      } : null,
      images: {
        total: images.length,
        lazy: images.filter((img) => img.loading === 'lazy').length,
        loaded: images.filter(loaded).length,
        loadedLazy: images.filter((img) => img.loading === 'lazy' && loaded(img)).length,
        missingIntrinsic: images.filter((img) => !img.hasAttribute('width') || !img.hasAttribute('height')).length,
        resourceRequests: resources.filter((entry) => entry.initiatorType === 'img').length,
      },
      layout: {
        scrollHeight: document.documentElement.scrollHeight,
        viewportHeight: window.innerHeight,
        horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      },
    };
  });
}

async function readerLatencyProxy(page) {
  return page.evaluate(async () => {
    const summary = document.querySelector('details.reader-disclosure > summary');
    if (!summary) return null;
    const details = summary.parentElement;
    const initial = details.open;
    const started = performance.now();
    summary.click();
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const elapsed = performance.now() - started;
    details.open = initial;
    return elapsed;
  });
}

async function decodeLoadedLocalImages(page) {
  return page.evaluate(async () => {
    const local = [...document.images].filter((img) => {
      if (!(img.complete && img.naturalWidth > 0)) return false;
      try { return new URL(img.currentSrc || img.src, location.href).origin === location.origin; }
      catch (_) { return false; }
    });
    let failures = 0;
    for (const img of local) {
      try { await img.decode(); }
      catch (_) { failures += 1; }
    }
    return {attempted: local.length, failures};
  });
}

async function expandAndScroll(page) {
  await page.evaluate(() => {
    document.querySelectorAll('details.reader-disclosure').forEach((node) => { node.open = true; });
  });
  const height = await page.evaluate(() => document.documentElement.scrollHeight);
  const viewport = await page.evaluate(() => window.innerHeight);
  const step = Math.max(300, Math.floor(viewport * 0.8));
  for (let y = 0; y < height; y += step) {
    await page.evaluate((target) => window.scrollTo(0, target), y);
    await page.waitForTimeout(25);
  }
  await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await page.waitForTimeout(400);
}

function warn(label, message) {
  console.log(`::warning title=Runtime performance ${label}::${message}`);
}

async function probe(browser, config) {
  const context = await browser.newContext({viewport: config.viewport});
  const page = await context.newPage();
  await blockExternal(page);
  await installObservers(page);
  await page.goto(`${BASE}${config.path}`, {waitUntil: 'networkidle'});
  await page.waitForTimeout(250);

  const initial = await snapshot(page);
  const latency = await readerLatencyProxy(page);
  const initialDecode = await decodeLoadedLocalImages(page);

  assert(!initial.layout.horizontalOverflow, `${config.label}: horizontal overflow on initial render`);
  assert(initialDecode.failures === 0, `${config.label}: ${initialDecode.failures} loaded local image decode failure(s)`);
  if (latency !== null) assert(latency < 300, `${config.label}: Reader two-rAF latency proxy ${latency.toFixed(1)} ms >= 300 ms`);

  if (config.expectDeferredLazy && initial.images.lazy >= 10) {
    assert(initial.images.loadedLazy < initial.images.lazy, `${config.label}: all ${initial.images.lazy} lazy images loaded before scroll`);
  }

  if (initial.cls > 0.1) warn(config.label, `initial local CLS ${initial.cls.toFixed(4)} > 0.10; inspect before treating as field CLS.`);
  if (initial.lcp > 2500) warn(config.label, `local LCP ${initial.lcp.toFixed(1)} ms > 2500 ms; external network is blocked, so compare only against this probe over time.`);
  if (initial.longTasks.max > 200) warn(config.label, `max local long task ${initial.longTasks.max.toFixed(1)} ms > 200 ms.`);
  assert(initial.images.missingIntrinsic === 0, `${config.label}: ${initial.images.missingIntrinsic} image(s) lack explicit width/height attributes on initial render`);

  await expandAndScroll(page);
  const afterScroll = await snapshot(page);
  const afterDecode = await decodeLoadedLocalImages(page);

  assert(!afterScroll.layout.horizontalOverflow, `${config.label}: horizontal overflow after full Reader expansion/scroll`);
  assert(afterScroll.images.loaded >= initial.images.loaded, `${config.label}: loaded image count regressed after scroll`);
  assert(afterScroll.images.missingIntrinsic === 0, `${config.label}: ${afterScroll.images.missingIntrinsic} image(s) lack explicit width/height attributes after full expansion/scroll`);
  assert(afterDecode.failures === 0, `${config.label}: ${afterDecode.failures} local image decode failure(s) after scroll`);

  const heapDelta = initial.heap && afterScroll.heap ? afterScroll.heap.used - initial.heap.used : null;
  console.log(JSON.stringify({
    label: config.label,
    path: config.path,
    viewport: config.viewport,
    initial,
    readerLatencyProxyMs: latency,
    initialDecode,
    afterScroll,
    afterScrollDecode: afterDecode,
    heapDeltaBytes: heapDelta,
    note: 'Local repository-runtime probe; not field Core Web Vitals and not real INP.',
  }, null, 2));

  await context.close();
}

async function main() {
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, HOST, resolve));
  let browser;
  try {
    browser = await chromium.launch({executablePath: CHROME, headless: true});
    await probe(browser, {
      label: 'Full Biography mobile',
      path: '/pt/biografia/',
      viewport: {width: 390, height: 844},
      expectDeferredLazy: true,
    });
    await probe(browser, {
      label: 'Internet & Performance desktop',
      path: '/pt/internet/',
      viewport: {width: 1365, height: 900},
      expectDeferredLazy: true,
    });
    console.log('Runtime performance/media observability smoke passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
