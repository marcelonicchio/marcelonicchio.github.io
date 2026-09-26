#!/usr/bin/env node
/**
 * Browser smoke for the Spotify Listening Now Home widget.
 *
 * Covers the launch-critical visual states without calling Spotify:
 * playing/paused visibility, long metadata, podcast episode wrapping,
 * missing artwork, official attribution sizing, CTA restraint, responsive
 * overflow, and reduced-motion behavior.
 */

const fs = require('fs');
const http = require('http');
const path = require('path');
const { URL } = require('url');

const playwrightPath = process.env.PLAYWRIGHT_CORE_PATH || 'playwright-core';
const { chromium } = require(playwrightPath);

const ROOT = path.resolve(__dirname, '..');
const HOST = '127.0.0.1';
const PORT = Number(process.env.SPOTIFY_SMOKE_PORT || 8776);
const BASE = `http://${HOST}:${PORT}`;
const CHROME = process.env.CHROME_PATH || '/usr/bin/google-chrome';
const ENDPOINT = 'https://now.marcelonicchio.com/now-playing';
const LOGO = 'https://developer-assets.spotifycdn.com/images/guidelines/design/logo.svg';

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

const baseItem = {
  type: 'track',
  name: 'A Ridiculously Long Song Title Designed to Stress the Listening Now Layout Without Breaking It',
  creators: ['First Artist', 'Second Artist', 'Third Artist', 'Fourth Artist'],
  context_name: 'A Very Long Album Name That Should Still Behave Gracefully',
  duration_ms: 240000,
  explicit: false,
  spotify_url: 'https://open.spotify.com/track/test',
  image: {url: 'https://i.scdn.co/image/test', width: 640, height: 640},
};

async function wireRoutes(page, payload) {
  await page.route('**/*', async (route) => {
    const url = route.request().url();
    const parsed = new URL(url);
    if (parsed.hostname === HOST && Number(parsed.port || 80) === PORT) {
      await route.continue();
      return;
    }
    if (url === ENDPOINT) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload),
      });
      return;
    }
    if (url === LOGO) {
      await route.fulfill({
        status: 200,
        contentType: 'image/svg+xml',
        body: '<svg xmlns="http://www.w3.org/2000/svg" width="140" height="42" viewBox="0 0 140 42"><rect width="140" height="42" fill="#000"/><text x="8" y="28" fill="#1db954" font-size="20">Spotify</text></svg>',
      });
      return;
    }
    if (parsed.hostname === 'i.scdn.co') {
      await route.fulfill({
        status: 200,
        contentType: 'image/svg+xml',
        body: '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640"><rect width="640" height="640" fill="#191414"/></svg>',
      });
      return;
    }
    await route.abort();
  });
}

async function waitForWidget(page) {
  await page.waitForFunction(() => {
    const widget = document.querySelector('[data-now-playing]');
    return widget && !widget.hidden;
  }, {timeout: 5000});
}

async function assertCanonicalRootPlacement(browser) {
  const context = await browser.newContext({viewport: {width: 1440, height: 900}, locale: 'pt-BR'});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item:baseItem});
  await page.goto(`${BASE}/`, {waitUntil:'networkidle'});
  await waitForWidget(page);

  const portrait = page.locator('.root-portrait-panel');
  const actions = page.locator('.root-hero-actions[data-root-lang="pt"]');
  const hero = page.locator('.root-hero');
  const widget = page.locator('[data-now-playing]');
  const bio = page.locator('.root-section.root-biography').first();

  assert(await portrait.isVisible(), 'Root desktop: canonical portrait disappeared');
  assert(await actions.isVisible(), 'Root desktop: vertical shortcut buttons disappeared');

  const [heroBox, widgetBox, bioBox] = await Promise.all([hero.boundingBox(), widget.boundingBox(), bio.boundingBox()]);
  assert(heroBox && widgetBox && bioBox, 'Root desktop: required layout boxes are missing');
  assert(widgetBox.y >= heroBox.y + heroBox.height - 2,
    `Root desktop: Listening Now overlaps/replaces hero (hero bottom=${heroBox.y + heroBox.height}, widget y=${widgetBox.y})`);
  assert(bioBox.y >= widgetBox.y + widgetBox.height - 2,
    `Root desktop: biography starts before Listening Now ends (widget bottom=${widgetBox.y + widgetBox.height}, bio y=${bioBox.y})`);

  await context.close();
}

async function assertCanonicalMobilePlacement(browser) {
  const context = await browser.newContext({viewport: {width: 390, height: 844}, locale: 'pt-BR'});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item:baseItem});
  await page.goto(`${BASE}/`, {waitUntil:'networkidle'});
  await waitForWidget(page);

  const portrait = page.locator('.root-portrait-panel');
  const actions = page.locator('.root-hero-actions[data-root-lang="pt"]');
  const hero = page.locator('.root-hero');
  const widget = page.locator('[data-now-playing]');
  const bio = page.locator('.root-section.root-biography').first();

  assert(await portrait.isVisible(), 'Root mobile: canonical portrait disappeared');
  assert(await actions.isVisible(), 'Root mobile: vertical shortcut buttons disappeared');

  const [heroBox, widgetBox, bioBox] = await Promise.all([hero.boundingBox(), widget.boundingBox(), bio.boundingBox()]);
  assert(heroBox && widgetBox && bioBox, 'Root mobile: required layout boxes are missing');
  assert(widgetBox.y >= heroBox.y + heroBox.height - 2,
    'Root mobile: Listening Now must begin only after title/photo/buttons hero is complete');
  assert(bioBox.y >= widgetBox.y + widgetBox.height - 2,
    'Root mobile: Listening Now must remain before biography section');

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, 'Root mobile: Listening Now introduces horizontal overflow');
  await context.close();
}

async function assertDesktopPlaying(browser) {
  const context = await browser.newContext({viewport: {width: 1365, height: 900}});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item:baseItem});
  await page.goto(`${BASE}/pt/`, {waitUntil:'networkidle'});
  await waitForWidget(page);

  const widget = page.locator('[data-now-playing]');
  const card = widget.locator('.now-playing-card');
  const logo = widget.locator('.spotify-logo-field img');
  const action = widget.locator('.now-playing-action:visible');
  const title = widget.locator('.now-playing-title');

  assert(await logo.count() === 1, 'Desktop: official Spotify full-logo image missing');
  const logoBox = await logo.boundingBox();
  assert(logoBox && logoBox.width >= 69.5, `Desktop: Spotify logo below 70px minimum (${logoBox?.width})`);
  assert(await logo.getAttribute('src') === LOGO, 'Desktop: Spotify logo does not use official developer asset');
  assert(await title.getAttribute('title') === baseItem.name, 'Desktop: truncated title does not expose full metadata');

  const actionStyle = await action.evaluate((node) => {
    const style = getComputedStyle(node);
    return {fontSize: parseFloat(style.fontSize), fontWeight: Number(style.fontWeight)};
  });
  assert(actionStyle.fontSize <= 10.5, `Desktop: Spotify CTA is too large (${actionStyle.fontSize}px)`);
  assert(actionStyle.fontWeight <= 600, `Desktop: Spotify CTA is too bold (${actionStyle.fontWeight})`);

  const cardBox = await card.boundingBox();
  assert(cardBox && cardBox.x >= 0 && cardBox.x + cardBox.width <= 1366,
    `Desktop: Spotify card escapes viewport (x=${cardBox?.x}, width=${cardBox?.width})`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, 'Desktop: Spotify widget introduces horizontal overflow');
  await context.close();
}

async function assertPausedHidden(browser) {
  const context = await browser.newContext({viewport: {width: 390, height: 844}});
  const page = await context.newPage();
  await wireRoutes(page, {status:'paused', is_playing:false, item:baseItem});
  await page.goto(`${BASE}/pt/`, {waitUntil:'networkidle'});
  await page.waitForTimeout(250);
  const widget = page.locator('[data-now-playing]');
  assert(await widget.isHidden(), 'Paused state must remain hidden on Home');
  await context.close();
}

async function assertMobileEpisode(browser) {
  const episode = {
    ...baseItem,
    type:'episode',
    name:'A Very Long Podcast Episode Title That Needs Two Lines to Remain Useful on Narrow Screens',
    creators:['Podcast Publisher With A Long Name'],
    context_name:'The Long Form Conversation Show',
    spotify_url:'https://open.spotify.com/episode/test',
  };
  const context = await browser.newContext({viewport: {width: 390, height: 844}});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item:episode});
  await page.goto(`${BASE}/pt/`, {waitUntil:'networkidle'});
  await waitForWidget(page);

  const widget = page.locator('[data-now-playing]');
  assert(await widget.getAttribute('data-item-type') === 'episode', 'Episode state is not exposed to CSS');
  const titleMetrics = await widget.locator('.now-playing-title').evaluate((node) => {
    const style = getComputedStyle(node);
    return {height: node.getBoundingClientRect().height, lineHeight: parseFloat(style.lineHeight)};
  });
  assert(titleMetrics.height > titleMetrics.lineHeight * 1.2, 'Episode title did not expand beyond one line');
  assert(titleMetrics.height <= titleMetrics.lineHeight * 2.25, 'Episode title exceeds intended two-line treatment');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  assert(!overflow, 'Mobile episode widget introduces horizontal overflow');
  await context.close();
}

async function assertMissingArtwork(browser) {
  const item = {...baseItem, image:null, name:'No Artwork Track'};
  const context = await browser.newContext({viewport: {width: 390, height: 844}});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item});
  await page.goto(`${BASE}/pt/`, {waitUntil:'networkidle'});
  await waitForWidget(page);

  const widget = page.locator('[data-now-playing]');
  assert(!(await widget.evaluate((node) => node.classList.contains('has-now-playing-art'))), 'Missing artwork should not retain artwork layout');
  const artworkState = await widget.locator('[data-now-playing-art]').evaluate((node) => ({
    hidden: node.hidden,
    display: getComputedStyle(node).display,
    hasSrc: node.hasAttribute('src'),
  }));
  assert(artworkState.hidden, `Missing artwork image should keep hidden=true (${JSON.stringify(artworkState)})`);
  assert(artworkState.display === 'none', `Missing artwork image should render display:none (${JSON.stringify(artworkState)})`);
  assert(!artworkState.hasSrc, `Missing artwork image should not retain src (${JSON.stringify(artworkState)})`);
  const geometry = await widget.evaluate((node) => {
    const card = node.querySelector('.now-playing-card').getBoundingClientRect();
    const copy = node.querySelector('.now-playing-copy').getBoundingClientRect();
    return {gap: copy.left - card.left};
  });
  assert(geometry.gap < 24, `Missing artwork leaves a dead first column (${geometry.gap}px)`);
  await context.close();
}

async function assertReducedMotion(browser) {
  const context = await browser.newContext({viewport:{width:390,height:844}, reducedMotion:'reduce'});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item:baseItem});
  await page.goto(`${BASE}/pt/`, {waitUntil:'networkidle'});
  await waitForWidget(page);
  const animation = await page.locator('.now-playing-pulse').evaluate((node) => getComputedStyle(node).animationName);
  assert(animation === 'none', `Reduced motion should disable pulse animation (got ${animation})`);
  await context.close();
}

async function assertEnglish(browser) {
  const context = await browser.newContext({viewport:{width:1365,height:900}});
  const page = await context.newPage();
  await wireRoutes(page, {status:'playing', is_playing:true, item:baseItem});
  await page.goto(`${BASE}/en/`, {waitUntil:'networkidle'});
  await waitForWidget(page);
  const kickerCopy = await page.locator('.now-playing-kicker').evaluate((node) => node.textContent.trim());
  const actionCopy = await page.locator('.now-playing-action').evaluate((node) => node.textContent.trim());
  assert(kickerCopy === 'Listening now', `EN kicker copy regressed (${kickerCopy})`);
  assert(actionCopy.includes('Listen on Spotify'), `EN Spotify CTA copy regressed (${actionCopy})`);
  await context.close();
}

async function main() {
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, HOST, resolve));
  let browser;
  try {
    browser = await chromium.launch({headless:true, executablePath:CHROME, args:['--no-sandbox']});
    await assertCanonicalRootPlacement(browser);
    await assertCanonicalMobilePlacement(browser);
    await assertDesktopPlaying(browser);
    await assertPausedHidden(browser);
    await assertMobileEpisode(browser);
    await assertMissingArtwork(browser);
    await assertReducedMotion(browser);
    await assertEnglish(browser);
    console.log('Spotify Listening Now browser smoke passed: branding, responsive states, edge metadata, pause hiding and reduced motion.');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
