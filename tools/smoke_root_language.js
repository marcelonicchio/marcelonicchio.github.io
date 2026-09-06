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
  const axisHref = expected === 'pt' ? '/pt/musica/' : '/en/music/';
  assert(await page.locator(`.root-axis[href="${axisHref}"]`).count() === 1, `${locale}: localized Music axis link missing`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, `${locale}: root has horizontal overflow on mobile`);
  const toggleBox = await page.locator('.root-lang-toggle').boundingBox();
  assert(toggleBox && toggleBox.x >= -1 && toggleBox.y >= -1 && toggleBox.x + toggleBox.width <= 391 && toggleBox.y + toggleBox.height <= 845, `${locale}: language toggle escapes mobile viewport`);
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
