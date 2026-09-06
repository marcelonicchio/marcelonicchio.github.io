#!/usr/bin/env node
/** Browser smoke for the canonical bilingual root surface. */
const fs = require('fs');
const http = require('http');
const path = require('path');
const { URL } = require('url');

const playwrightPath = process.env.PLAYWRIGHT_CORE_PATH || 'playwright-core';
const { chromium } = require(playwrightPath);
const ROOT = path.resolve(__dirname, '..');
const HOST = '127.0.0.1';
const PORT = Number(process.env.ROOT_LANGUAGE_PORT || 8775);
const BASE = `http://${HOST}:${PORT}`;
const CHROME = process.env.CHROME_PATH || '/usr/bin/google-chrome';
const MIME = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp'};

function assert(condition, message) { if (!condition) throw new Error(message); }
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
      res.writeHead(404, {'content-type':'text/plain; charset=utf-8'}); res.end('Not found'); return;
    }
    res.writeHead(200, {'content-type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream', 'cache-control':'no-store'});
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
async function assertLanguage(browser, locale, expected) {
  const context = await browser.newContext({locale, viewport:{width:390,height:844}});
  const page = await context.newPage();
  await blockExternal(page);
  await page.goto(`${BASE}/`, {waitUntil:'networkidle'});
  assert(await page.locator('html').getAttribute('data-root-language') === expected, `${locale}: expected root language ${expected}`);
  assert(await page.locator('html').getAttribute('lang') === (expected === 'pt' ? 'pt-BR' : 'en'), `${locale}: html lang mismatch`);
  assert(await page.locator(`[data-root-lang="${expected}"]`).first().isVisible(), `${locale}: expected language panel not visible`);
  const other = expected === 'pt' ? 'en' : 'pt';
  assert(await page.locator(`[data-root-lang="${other}"]`).first().isHidden(), `${locale}: non-selected language remains visible`);
  assert(await page.locator(`[data-root-lang-choice="${expected}"]`).getAttribute('aria-pressed') === 'true', `${locale}: selected language button state wrong`);
  assert(await page.locator('.root-portrait img').isVisible(), `${locale}: portrait missing on mobile`);
  assert(await page.locator(`.root-milestone-grid[data-root-lang="${expected}"] .root-milestone`).count() === 9, `${locale}: expected 9 milestones`);
  assert(await page.locator(`.root-hero-actions[data-root-lang="${expected}"] a`).count() === 5, `${locale}: expected 5 balanced hero shortcuts`);
  assert(await page.getByText(expected === 'pt' ? 'Abrir HUB em português' : 'Open English HUB', {exact:true}).count() === 0, `${locale}: redundant language HUB CTA still present`);
  const axisHref = expected === 'pt' ? '/pt/musica/' : '/en/music/';
  assert(await page.locator(`.root-axis[href="${axisHref}"]`).count() === 1, `${locale}: localized Music axis link missing`);
  assert(await page.locator('a.root-email-link[href="mailto:marcelonicchio@gmail.com"]').count() === 1, `${locale}: canonical e-mail link missing`);
  const order = await page.evaluate(() => {
    const milestones = document.querySelector('.root-milestones');
    const explore = document.querySelector('.root-explore');
    return Boolean(milestones && explore && (milestones.compareDocumentPosition(explore) & Node.DOCUMENT_POSITION_FOLLOWING));
  });
  assert(order, `${locale}: selected milestones must appear before vertical-axis cards`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, `${locale}: root has horizontal overflow on mobile`);
  const toggleBox = await page.locator('.root-lang-toggle').boundingBox();
  assert(toggleBox && toggleBox.x >= -1 && toggleBox.y >= -1 && toggleBox.y <= 20 && toggleBox.x + toggleBox.width <= 391 && toggleBox.y + toggleBox.height <= 845, `${locale}: language toggle is not contained at top of mobile viewport`);
  await context.close();
}
async function assertSwitchPersistence(browser) {
  const context = await browser.newContext({locale:'en-US', viewport:{width:1365,height:900}});
  const page = await context.newPage();
  await blockExternal(page);
  await page.goto(`${BASE}/`, {waitUntil:'networkidle'});
  await page.locator('[data-root-lang-choice="pt"]').click();
  assert(await page.locator('html').getAttribute('data-root-language') === 'pt', 'PT switch did not apply');
  assert(await page.evaluate(() => localStorage.getItem('mn-root-language')) === 'pt', 'PT choice was not persisted');
  await page.reload({waitUntil:'networkidle'});
  assert(await page.locator('html').getAttribute('data-root-language') === 'pt', 'Persisted PT choice did not survive reload');
  assert(await page.locator('.root-milestone-grid[data-root-lang="pt"] .root-milestone').count() === 9, 'PT milestones changed after reload');
  const overlap = await page.evaluate(() => {
    const head = document.querySelector('.root-presence-section .root-section-head[data-root-lang="pt"]');
    const groups = document.querySelector('.root-presence-groups');
    if (!head || !groups) return true;
    const h = head.getBoundingClientRect();
    const g = groups.getBoundingClientRect();
    return g.top < h.bottom - 1;
  });
  assert(!overlap, 'Presence groups overlap the left editorial heading');
  const panelDisplay = await page.locator('.root-presence-section .presence-panel').evaluate((node) => getComputedStyle(node).display);
  assert(panelDisplay === 'block', `Presence panel should be block on root, got ${panelDisplay}`);

  const researchPresence = await page.locator('.root-presence-groups > .root-presence-group:first-child .presence-link').evaluateAll((nodes) => nodes.map((node) => ({
    label: (node.textContent || '').trim(),
    href: node.href,
    rel: node.getAttribute('rel') || ''
  })));
  const expectedResearchLabels = ['ORCID','SSRN','OSF','Zenodo','Academia.edu','HAL','PubPub'];
  assert(researchPresence.map((item) => item.label).join('|') === expectedResearchLabels.join('|'), `Research presence order mismatch: ${researchPresence.map((item) => item.label).join(' | ')}`);
  const zenodo = researchPresence.find((item) => item.label === 'Zenodo');
  assert(zenodo && zenodo.href.startsWith('https://zenodo.org/search?') && zenodo.href.includes('Nicchio'), 'Zenodo author-search link missing from root research presence');
  assert(!zenodo.rel.split(/\s+/).includes('me'), 'Zenodo author-search URL must not be declared rel=me');

  const typography = await page.evaluate(() => {
    const button = document.querySelector('.root-hero-actions[data-root-lang="pt"] .button');
    const strong = document.querySelector('.root-bio-copy strong');
    const strongParent = strong && strong.parentElement;
    const kicker = document.querySelector('.root-milestones .root-section-kicker');
    const year = document.querySelector('.root-milestone-grid[data-root-lang="pt"] .year');
    const axisNo = document.querySelector('.root-axis-grid[data-root-lang="pt"] .root-axis > span');
    if (!button || !strong || !strongParent || !kicker || !year || !axisNo) return null;
    const b = getComputedStyle(button);
    const s = getComputedStyle(strong);
    const p = getComputedStyle(strongParent);
    const k = getComputedStyle(kicker);
    const y = getComputedStyle(year);
    const a = getComputedStyle(axisNo);
    return {
      buttonWeight: Number(b.fontWeight),
      buttonBorder: b.borderTopColor,
      strongWeight: Number(s.fontWeight),
      strongFamily: s.fontFamily,
      parentFamily: p.fontFamily,
      kickerSize: parseFloat(k.fontSize),
      kickerColor: k.color,
      yearSize: parseFloat(y.fontSize),
      axisSize: parseFloat(a.fontSize)
    };
  });
  assert(typography, 'Root hierarchy typography could not be measured');
  assert(typography.buttonWeight >= 700, `Hero shortcut names should be bold, got ${typography.buttonWeight}`);
  assert(typography.buttonBorder === 'rgb(243, 239, 231)', `Hero shortcut border should be site white, got ${typography.buttonBorder}`);
  assert(typography.strongWeight === 700, `Biography emphasis should use readable 700 weight, got ${typography.strongWeight}`);
  assert(typography.strongFamily === typography.parentFamily, 'Biography emphasis must inherit the body typeface');
  assert(typography.kickerSize >= 14, `Section kicker should be at least 14px, got ${typography.kickerSize}`);
  assert(typography.kickerColor === 'rgb(230, 161, 156)', `Section kicker accent changed unexpectedly: ${typography.kickerColor}`);
  assert(typography.yearSize >= 13, `Milestone year should be at least 13px, got ${typography.yearSize}`);
  assert(typography.axisSize >= 13, `Vertical number should be at least 13px, got ${typography.axisSize}`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, 'Desktop root has horizontal overflow');
  await context.close();
}
async function main() {
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, HOST, resolve));
  let browser;
  try {
    browser = await chromium.launch({headless:true, executablePath:CHROME, args:['--no-sandbox']});
    await assertLanguage(browser, 'en-US', 'en');
    await assertLanguage(browser, 'pt-BR', 'pt');
    await assertSwitchPersistence(browser);
    console.log('Canonical root language/mobile smoke passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}
main().catch((error) => { console.error(error.stack || error.message || String(error)); process.exit(1); });
