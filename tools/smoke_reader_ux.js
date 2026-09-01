#!/usr/bin/env node
/**
 * Browser-level regression smoke test for Reader Page disclosure + pilot Chapter Pages.
 *
 * Full Biography and Internet & Performance use disclosure by default. Communication
 * and Audiovisual remain query-flag pilot surfaces while their UX is still under review.
 *
 * Requires playwright-core supplied outside the repository. CI sets
 * PLAYWRIGHT_CORE_PATH to an isolated /tmp install so site-wide HTML sync tools never
 * traverse dependency fixtures.
 */

const fs = require('fs');
const http = require('http');
const path = require('path');
const { URL } = require('url');

const playwrightPath = process.env.PLAYWRIGHT_CORE_PATH || 'playwright-core';
const { chromium } = require(playwrightPath);

const ROOT = path.resolve(__dirname, '..');
const HOST = '127.0.0.1';
const PORT = Number(process.env.READER_UX_PORT || 8765);
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
    if (url.hostname === HOST && Number(url.port || 80) === PORT) {
      await route.continue();
    } else {
      await route.abort();
    }
  });
}

async function runDesktop(browser) {
  const context = await browser.newContext({viewport: {width: 1365, height: 900}});
  const page = await context.newPage();
  await blockExternal(page);

  // Core Reader Pages are disclosure-first on their normal public URLs.
  await page.goto(`${BASE}/pt/biografia/`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() >= 30, 'Normal Full Bio URL did not initialize disclosure');
  assert((await page.locator('html').getAttribute('class') || '').includes('reader-disclosure-active'), 'Normal Full Bio root did not receive Reader UX class');
  assert((await page.locator('#bio-internet-cookieweb').innerText()).includes('qualidade de vida'), 'Full Bio lost autobiographical text');
  assert((await page.getByText('Clique para expandir', {exact: false}).count()) > 0, 'Permanent Portuguese CTA missing');

  // Presentation states: Minduim/BBS starts open; dense entries remain closed but featured.
  const bbsBio = page.locator('#bio-internet-bbs');
  assert(await bbsBio.locator('details.reader-disclosure').getAttribute('open') !== null, 'Minduim/BBS did not start open in Full Bio');
  assert(await bbsBio.getAttribute('data-reader-presentation') === 'default-open', 'Minduim/BBS presentation state missing');
  assert((await page.locator('#bio-internet-mirantte details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Mirantte is not featured in Full Bio');
  assert((await page.locator('#bio-internet-cookieweb details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'CookieWEB is not featured in Full Bio');
  assert((await page.locator('#bio-audiovisual-meia-noite details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Meia-Noite is not featured in Full Bio');

  // Rich collapsed-summary pilot: Melissa is useful before expansion and returns to the full entry when opened.
  const melissaBio = page.locator('#bio-hai-melissa');
  const melissaPreview = melissaBio.locator('.reader-disclosure__preview');
  assert(await melissaPreview.count() === 1, 'Melissa rich collapsed preview missing');
  assert((await melissaPreview.innerText()).includes('63 horas e 518 prompts'), 'Melissa collapsed preview lost core case metrics');
  assert((await melissaPreview.innerText()).includes('Melissa Framework'), 'Melissa collapsed preview lost framework outcome');
  assert(await melissaPreview.locator('img').getAttribute('src') === '/assets/media/thread/melissa1_0_selfportrait300kb.jpg', 'Melissa collapsed preview cover image incorrect');
  assert(await melissaBio.locator('details.reader-disclosure').getAttribute('open') === null, 'Melissa preview should start collapsed');
  await melissaBio.locator('details.reader-disclosure > summary').click();
  assert(await melissaBio.locator('details.reader-disclosure').getAttribute('open') !== null, 'Melissa summary click did not open full entry');
  assert(await melissaPreview.isHidden(), 'Melissa compact preview remained visible after expansion');
  assert((await melissaBio.locator('.reader-disclosure__body').innerText()).includes('O que aconteceu depois não foi planejado.'), 'Melissa full body was not preserved after expansion');
  await melissaBio.locator('details.reader-disclosure > summary').click();

  // Full Biography: deep-link opening + registry-backed metadata without query flag.
  await page.goto(`${BASE}/pt/biografia/#bio-internet-cookieweb`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() >= 30, 'Full Bio produced too few disclosures');
  const cookieBio = page.locator('#bio-internet-cookieweb');
  assert(await cookieBio.locator('details.reader-disclosure').getAttribute('open') !== null, 'CookieWEB deep link did not auto-open');
  assert((await cookieBio.locator('.reader-disclosure__excerpt').innerText()).includes('primeira grande conta de e-commerce'), 'CookieWEB curated summary was not used');
  assert(await cookieBio.locator('.reader-disclosure__topic').count() >= 4, 'CookieWEB topic chips missing');
  assert((await cookieBio.innerText()).includes('qualidade de vida'), 'Disclosure transformation lost CookieWEB body text');
  assert(await cookieBio.locator('.reader-disclosure__collapse-button').count() === 1, 'Bottom collapse action missing from CookieWEB');
  await cookieBio.locator('.reader-disclosure__collapse-button').click();
  assert(await cookieBio.locator('details.reader-disclosure').getAttribute('open') === null, 'Bottom collapse action did not close CookieWEB');

  // Internet stress set: normal URL + large galleries, composite landmark, video count and Chapter Page link.
  await page.goto(`${BASE}/pt/internet/`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() >= 10, 'Internet normal URL produced too few disclosures');

  const bbs = page.locator('#bbs');
  assert(await bbs.locator('details.reader-disclosure').getAttribute('open') !== null, 'Minduim/BBS did not start open in Internet');

  const mirantte = page.locator('#mirantte');
  assert((await mirantte.locator('details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Mirantte featured class missing');
  assert((await mirantte.locator('.reader-disclosure__excerpt').innerText()).includes('problema de aquisição de tráfego'), 'Mirantte curated summary missing');
  assert((await mirantte.locator('.reader-disclosure__badge').allInnerTexts()).some((t) => t.includes('34 fotos')), 'Mirantte gallery badge incorrect');

  const sem = page.locator('#sem');
  assert((await sem.locator('.reader-disclosure__related').innerText()).includes('Goobec'), 'Goobec landmark missing from SEM');
  const cookieweb = page.locator('#cookieweb');
  assert((await cookieweb.locator('details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'CookieWEB featured class missing');
  assert((await cookieweb.locator('.reader-disclosure__related').innerText()).includes('Goobec'), 'GAP landmark missing from CookieWEB');

  const best = page.locator('#best');
  assert((await best.locator('.reader-disclosure__badge').allInnerTexts()).some((t) => t.includes('4 vídeos')), 'BEST video badge incorrect');
  await best.locator('summary').click();
  assert(await best.locator('.reader-disclosure__page-link a').getAttribute('href') === '/pt/internet/best-kenshoo/', 'BEST Chapter Page link incorrect');
  assert(await best.locator('.reader-disclosure__collapse-button').count() === 1, 'Bottom collapse action missing from BEST');

  // Native keyboard operation and independent-open behavior.
  const mirantteDetails = mirantte.locator('details.reader-disclosure');
  const bestDetails = best.locator('details.reader-disclosure');
  if (await mirantteDetails.getAttribute('open') !== null) await mirantte.locator('summary').click();
  await mirantte.locator('summary').focus();
  await page.keyboard.press('Enter');
  assert(await mirantteDetails.getAttribute('open') !== null, 'Enter key did not open Mirantte disclosure');
  assert(await bestDetails.getAttribute('open') !== null, 'Opening Mirantte closed BEST');

  // Global controls override default-open state when the reader explicitly asks.
  await page.getByRole('button', {name: 'Abrir todos'}).click();
  const total = await page.locator('details.reader-disclosure').count();
  assert(await page.locator('details.reader-disclosure[open]').count() === total, 'Open all did not open every disclosure');
  await page.getByRole('button', {name: 'Recolher todos'}).click();
  assert(await page.locator('details.reader-disclosure[open]').count() === 0, 'Collapse all did not close every disclosure');

  // Print event contract: complete content while printing, state restored afterward.
  await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
  assert(await page.locator('details.reader-disclosure[open]').count() === total, 'beforeprint did not expose all chapters');
  await page.evaluate(() => window.dispatchEvent(new Event('afterprint')));
  assert(await page.locator('details.reader-disclosure[open]').count() === 0, 'afterprint did not restore disclosure state');

  // Communication remains an explicit pilot: neutral-source entry + standalone page.
  await page.goto(`${BASE}/pt/comunicacao/?ux=disclosure`, {waitUntil: 'networkidle'});
  const folha = page.locator('#folha');
  assert((await folha.locator('.reader-disclosure__excerpt').innerText()).includes('matéria de capa do Folhateen'), 'Folha curated summary missing');
  await folha.locator('summary').click();
  assert(await folha.locator('.reader-disclosure__page-link a').getAttribute('href') === '/pt/comunicacao/folhateen-orfaos-do-rock/', 'Folha Chapter Page link incorrect');

  // Audiovisual remains an explicit pilot; its registered featured state is already reusable.
  await page.goto(`${BASE}/pt/audiovisual/?ux=disclosure`, {waitUntil: 'networkidle'});
  const meia = page.locator('#meia-noite');
  const meiaBadges = await meia.locator('.reader-disclosure__badge').allInnerTexts();
  assert((await meia.locator('details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Meia-Noite featured class missing in pilot');
  assert(meiaBadges.some((t) => t.includes('22 fotos')), 'Meia-Noite gallery badge incorrect');
  assert(meiaBadges.some((t) => t.includes('4 vídeos')), 'Meia-Noite video badge incorrect');
  assert((await meia.locator('.reader-disclosure__excerpt').innerText()).includes('Programa de literatura com linguagem pop'), 'Meia-Noite curated summary missing');

  // EN core page consumes the same registry with language-specific labels/copy by default.
  await page.goto(`${BASE}/en/biography/#bio-communication-folha`, {waitUntil: 'networkidle'});
  assert(await page.getByRole('button', {name: 'Open all'}).count() === 1, 'English disclosure controls not localized');
  assert((await page.getByText('Click to expand', {exact: false}).count()) > 0, 'Permanent English CTA missing');
  const folhaEn = page.locator('#bio-communication-folha');
  assert((await folhaEn.locator('.reader-disclosure__excerpt').innerText()).includes('Folhateen cover story'), 'English Folha curated summary missing');
  assert((await folhaEn.locator('.reader-disclosure__topic').allInnerTexts()).includes('Press'), 'English topic labels missing');

  // Pilot Chapter Pages: browser-readable, noindex, canonical, exact preserved structures.
  await page.goto(`${BASE}/pt/comunicacao/folhateen-orfaos-do-rock/`, {waitUntil: 'networkidle'});
  assert(await page.locator('main[data-entry-id="communication-folha"]').count() === 1, 'Folha Chapter Page stable id missing');
  assert(await page.locator('meta[name="robots"]').getAttribute('content') === 'noindex,follow', 'Folha pilot robots incorrect');
  assert((await page.locator('link[rel="canonical"]').getAttribute('href')).endsWith('/pt/comunicacao/folhateen-orfaos-do-rock/'), 'Folha canonical incorrect');
  assert(await page.locator('.fact-strip .fact').count() === 1, 'Folha hero exposes taxonomy as a KPI');
  assert(await page.locator('.entry-breadcrumbs').count() === 1, 'Folha visible breadcrumbs missing');

  await page.goto(`${BASE}/pt/internet/best-kenshoo/`, {waitUntil: 'networkidle'});
  assert(await page.locator('main[data-entry-id="internet-best"]').count() === 1, 'BEST Chapter Page stable id missing');
  assert(await page.locator('.evidence').count() === 4, 'BEST Chapter Page did not preserve four workshop parts');
  assert(await page.locator('.fact-strip .fact').count() === 1, 'BEST hero exposes taxonomy as a KPI');

  await context.close();
}

async function runMobile(browser) {
  const context = await browser.newContext({viewport: {width: 390, height: 844}, isMobile: true});
  const page = await context.newPage();
  await blockExternal(page);
  await page.goto(`${BASE}/pt/biografia/`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() >= 30, 'Mobile Full Bio did not initialize disclosure by default');
  assert(await page.locator('#bio-internet-bbs details.reader-disclosure').getAttribute('open') !== null, 'Mobile Minduim/BBS did not start open');
  const melissaPreview = page.locator('#bio-hai-melissa .reader-disclosure__preview');
  assert(await melissaPreview.isVisible(), 'Mobile Melissa rich preview is not visible');
  assert(await melissaPreview.locator('img').isVisible(), 'Mobile Melissa preview cover is not visible');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  assert(overflow <= 2, `Mobile disclosure introduced horizontal overflow: ${overflow}px`);
  assert(await page.getByRole('button', {name: 'Abrir todos'}).isVisible(), 'Mobile Open all control is not visible');
  await context.close();
}

async function runNoJs(browser) {
  const context = await browser.newContext({javaScriptEnabled: false, viewport: {width: 1000, height: 800}});
  const page = await context.newPage();
  await page.goto(`${BASE}/pt/biografia/`, {waitUntil: 'domcontentloaded'});
  assert(await page.locator('details.reader-disclosure').count() === 0, 'No-JS page should retain source HTML rather than depend on disclosure JS');
  assert((await page.locator('#bio-internet-cookieweb').innerText()).includes('qualidade de vida'), 'No-JS Full Bio lost source content');
  await context.close();
}

async function main() {
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, HOST, resolve));
  let browser;
  try {
    browser = await chromium.launch({
      executablePath: CHROME,
      headless: true,
      args: ['--no-sandbox', '--disable-gpu'],
    });
    await runDesktop(browser);
    await runMobile(browser);
    await runNoJs(browser);
    console.log('Reader UX browser smoke test passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
