#!/usr/bin/env node
/**
 * Browser regression smoke for discoverable primary navigation on mobile.
 *
 * Mobile must expose an explicit Categories control; no horizontal-swipe discovery is
 * allowed. Desktop keeps the existing always-visible navigation.
 */

const fs = require('fs');
const http = require('http');
const path = require('path');
const { URL } = require('url');

const playwrightPath = process.env.PLAYWRIGHT_CORE_PATH || 'playwright-core';
const { chromium } = require(playwrightPath);

const ROOT = path.resolve(__dirname, '..');
const HOST = '127.0.0.1';
const PORT = Number(process.env.MOBILE_NAV_PORT || 8771);
const BASE = `http://${HOST}:${PORT}`;
const CHROME = process.env.CHROME_PATH || '/usr/bin/google-chrome';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
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

async function assertMobile(browser, pagePath, expectedLanguageLink, expectedLinkCount, expectedToggleLabel) {
  const context = await browser.newContext({viewport: {width: 390, height: 844}});
  const page = await context.newPage();
  await blockExternal(page);
  await page.goto(`${BASE}${pagePath}`, {waitUntil: 'networkidle'});

  const toggle = page.locator('.site-header .nav-toggle');
  const links = page.locator('.site-header .nav-links');

  assert(await toggle.count() === 1, `${pagePath}: mobile Categories control missing`);
  assert(await toggle.isVisible(), `${pagePath}: mobile Categories control is not visible`);
  assert((await toggle.innerText()).trim().toLowerCase().includes(expectedToggleLabel.toLowerCase()), `${pagePath}: Categories control does not use expected label ${expectedToggleLabel}`);
  assert(await toggle.getAttribute('aria-expanded') === 'false', `${pagePath}: categories should start collapsed`);
  assert(await links.isHidden(), `${pagePath}: primary links should start collapsed behind explicit Categories control`);

  const emphasis = await toggle.evaluate((node) => {
    const style = getComputedStyle(node);
    return {
      fontWeight: Number(style.fontWeight),
      borderTopWidth: parseFloat(style.borderTopWidth),
      borderTopStyle: style.borderTopStyle,
      borderTopColor: style.borderTopColor,
      color: style.color,
    };
  });
  assert(emphasis.fontWeight >= 800, `${pagePath}: Categories label is not bold enough (${emphasis.fontWeight})`);
  assert(emphasis.borderTopWidth >= 2, `${pagePath}: Categories border is not emphasized (${emphasis.borderTopWidth}px)`);
  assert(emphasis.borderTopStyle === 'solid', `${pagePath}: Categories border is not solid`);
  assert(emphasis.borderTopColor === 'rgb(255, 255, 255)', `${pagePath}: Categories border is not white (${emphasis.borderTopColor})`);
  assert(emphasis.color === 'rgb(255, 255, 255)', `${pagePath}: Categories text is not white (${emphasis.color})`);

  const initialOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!initialOverflow, `${pagePath}: horizontal overflow exists before opening mobile categories`);

  await toggle.click();
  assert(await toggle.getAttribute('aria-expanded') === 'true', `${pagePath}: Categories control did not enter expanded state`);
  assert(await links.isVisible(), `${pagePath}: primary links did not become visible`);

  const linkCount = await links.locator('a').count();
  assert(linkCount === expectedLinkCount, `${pagePath}: expected ${expectedLinkCount} primary navigation links, found ${linkCount}`);
  assert(await links.getByText(expectedLanguageLink, {exact: true}).count() === 1, `${pagePath}: language switch link missing from opened categories`);

  const panelStyles = await links.locator('a').evaluateAll((nodes) => nodes.map((node) => {
    const style = getComputedStyle(node);
    return {color: style.color, fontWeight: Number(style.fontWeight), opacity: Number(style.opacity)};
  }));
  for (const [index, style] of panelStyles.entries()) {
    assert(style.color === 'rgb(255, 255, 255)', `${pagePath}: nav link ${index + 1} is not white (${style.color})`);
    assert(style.fontWeight >= 600, `${pagePath}: nav link ${index + 1} is not bold enough (${style.fontWeight})`);
    assert(style.opacity === 1, `${pagePath}: nav link ${index + 1} is visually faded (${style.opacity})`);
  }

  const bounds = await links.locator('a').evaluateAll((nodes) => nodes.map((node) => {
    const r = node.getBoundingClientRect();
    return {left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height};
  }));
  for (const [index, box] of bounds.entries()) {
    assert(box.left >= -1 && box.right <= 391, `${pagePath}: nav link ${index + 1} escapes viewport (${box.left}..${box.right})`);
    assert(box.width > 0 && box.height >= 44, `${pagePath}: nav link ${index + 1} is not a usable touch target`);
  }

  const openOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!openOverflow, `${pagePath}: horizontal overflow exists with mobile categories open`);

  await page.keyboard.press('Escape');
  assert(await toggle.getAttribute('aria-expanded') === 'false', `${pagePath}: Escape did not close mobile categories`);
  assert(await links.isHidden(), `${pagePath}: links remained visible after Escape`);

  await context.close();
}

async function assertDesktop(browser) {
  const context = await browser.newContext({viewport: {width: 1365, height: 900}});
  const page = await context.newPage();
  await blockExternal(page);
  await page.goto(`${BASE}/pt/biografia/`, {waitUntil: 'networkidle'});

  const toggle = page.locator('.site-header .nav-toggle');
  const links = page.locator('.site-header .nav-links');
  assert(await toggle.count() === 1, 'Desktop: injected Categories control node missing');
  assert(await toggle.isHidden(), 'Desktop: mobile Categories control must stay hidden');
  assert(await links.isVisible(), 'Desktop: primary navigation must remain always visible');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, 'Desktop: navigation introduced horizontal overflow');

  await context.close();
}

async function main() {
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, HOST, resolve));
  let browser;
  try {
    browser = await chromium.launch({headless: true, executablePath: CHROME, args: ['--no-sandbox']});
    await assertMobile(browser, '/pt/', 'EN', 8, 'Categorias');
    await assertMobile(browser, '/en/', 'PT', 8, 'Categories');
    await assertMobile(browser, '/pt/biografia/', 'EN', 7, 'Categorias');
    await assertDesktop(browser);
    console.log('Mobile navigation discoverability smoke passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
