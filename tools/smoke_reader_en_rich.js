#!/usr/bin/env node
/** Browser regression coverage for English rich Reader summaries. */
const fs = require('fs');
const http = require('http');
const path = require('path');
const {URL} = require('url');

const playwrightPath = process.env.PLAYWRIGHT_CORE_PATH || 'playwright-core';
const {chromium} = require(playwrightPath);
const ROOT = path.resolve(__dirname, '..');
const HOST = '127.0.0.1';
const PORT = Number(process.env.READER_EN_RICH_PORT || 8766);
const BASE = `http://${HOST}:${PORT}`;
const CHROME = process.env.CHROME_PATH || '/usr/bin/google-chrome';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'
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
    res.writeHead(200, {
      'content-type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'cache-control': 'no-store'
    });
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

async function checkPreview(page, spec) {
  const section = page.locator(spec.selector);
  const preview = section.locator('.reader-disclosure__preview');
  assert(await preview.count() === 1, `${spec.name}: English rich preview missing`);
  assert(await preview.locator('.reader-disclosure__preview-paragraph').count() === spec.paragraphs,
    `${spec.name}: English preview paragraph count incorrect`);
  assert((await preview.innerText()).includes(spec.phrase), `${spec.name}: English preview lost expected copy: ${spec.phrase}`);
  assert(await preview.locator('img').getAttribute('src') === spec.image, `${spec.name}: English preview image incorrect`);
  const badges = await section.locator('.reader-disclosure__badge').allInnerTexts();
  spec.badges.forEach((label) => assert(badges.includes(label), `${spec.name}: English indicator missing: ${label}`));
  if (spec.permalink) {
    const titleLink = section.locator('h2 a.entry-title-permalink');
    assert(await titleLink.count() === 1, `${spec.name}: standalone title permalink missing`);
    assert(await titleLink.getAttribute('href') === spec.permalink, `${spec.name}: standalone title permalink incorrect`);
  }
  const details = section.locator('details.reader-disclosure');
  assert(await details.getAttribute('open') === null, `${spec.name}: English rich entry should start collapsed`);
  await details.locator(':scope > summary').click();
  assert(await details.getAttribute('open') !== null, `${spec.name}: English rich entry did not expand`);
  assert(await preview.isHidden(), `${spec.name}: English rich preview remained visible after expansion`);
  await details.locator(':scope > summary').click();
}

async function main() {
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, HOST, resolve));
  let browser;
  try {
    browser = await chromium.launch({executablePath: CHROME, headless: true, args: ['--no-sandbox', '--disable-gpu']});
    const context = await browser.newContext({viewport: {width: 1365, height: 900}});
    const page = await context.newPage();
    await blockExternal(page);
    await page.goto(`${BASE}/en/biography/`, {waitUntil: 'networkidle'});

    const specs = [
      {
        name: 'Mirantte News', selector: '#bio-internet-mirantte', paragraphs: 4,
        phrase: 'organic traffic', image: '/assets/media/galleries/mirantte-news/mirantte-news-02-480.webp',
        badges: ['34 photos', '1 business card'], permalink: '/en/internet/mirantte-news/'
      },
      {
        name: 'CookieWEB', selector: '#bio-internet-cookieweb', paragraphs: 4,
        phrase: 'more than 22 accounts', image: '/assets/media/galleries/cookieweb/cookieweb-19-480.webp',
        badges: ['20 photos', '3 GAP certificates', '1 contemporary source'], permalink: '/en/internet/cookieweb/'
      },
      {
        name: 'Meia-Noite e Uns', selector: '#bio-audiovisual-meia-noite', paragraphs: 3,
        phrase: '00:01', image: '/assets/media/galleries/meia-noite-e-uns/meia-noite-e-uns-01-480.webp',
        badges: ['22 photos', '4 videos'], permalink: '/en/communication/meia-noite-e-uns/'
      },
      {
        name: 'Melissa 1.0', selector: '#bio-hai-melissa', paragraphs: 4,
        phrase: '63 hours and 518 prompts', image: '/assets/media/thread/melissa1_0_selfportrait300kb.jpg',
        badges: ['2 images', '1 download link', '4 DOI documents', '1 repository link']
      }
    ];

    for (const spec of specs) await checkPreview(page, spec);

    const melissaTopics = await page.locator('#bio-hai-melissa .reader-disclosure__topic').allInnerTexts();
    ['AI', 'HAI', 'HCI', 'Prompt Engineering', 'Melissa 1.0'].forEach((label) =>
      assert(melissaTopics.includes(label), `Melissa 1.0: English topic missing: ${label}`));

    for (const spec of specs.filter((item) => item.permalink)) {
      await page.goto(`${BASE}${spec.permalink}`, {waitUntil: 'networkidle'});
      assert(await page.locator('main[data-entry-id]').count() === 1, `${spec.name}: standalone page did not render`);
      assert((await page.locator('meta[name="robots"]').getAttribute('content')) === 'noindex,follow',
        `${spec.name}: standalone pilot unexpectedly changed robots`);
      await page.goto(`${BASE}/en/biography/`, {waitUntil: 'networkidle'});
    }

    await context.close();
    console.log('English rich Reader summary smoke test passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
