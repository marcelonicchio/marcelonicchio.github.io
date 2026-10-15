#!/usr/bin/env node
/**
 * Browser-level regression smoke test for Reader Page disclosure + pilot Chapter Pages.
 *
 * Full Biography uses compact disclosure by default. Internet & Performance
 * is fully open native HTML without Reader controls. IA/HAI uses selective
 * disclosure for registered entries. Culture & Audiovisual also remains
 * a continuous-reading page and never initializes disclosure.
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
  assert(await page.locator('details.reader-disclosure').count() >= 28, 'Normal Full Bio URL did not initialize disclosure');
  assert((await page.locator('html').getAttribute('class') || '').includes('reader-disclosure-active'), 'Normal Full Bio root did not receive Reader UX class');
  assert((await page.locator('#bio-internet-cookieweb').innerText()).includes('qualidade de vida'), 'Full Bio lost autobiographical text');
  assert((await page.getByText('Clique para expandir', {exact: false}).count()) > 0, 'Permanent Portuguese CTA missing');

  // Type 1 / always-open entries remain plain open HTML; dense entries can still be featured disclosures.
  const bbsBio = page.locator('#bio-internet-bbs');
  assert(await bbsBio.getAttribute('data-reader-presentation') === 'always-open', 'Minduim/BBS always-open presentation state missing');
  assert(await bbsBio.locator('details.reader-disclosure').count() === 0, 'Minduim/BBS must not be wrapped in disclosure');
  assert(await bbsBio.locator('.reader-disclosure__toggle').count() === 0, 'Minduim/BBS must not expose a top toggle');
  assert(await bbsBio.locator('.reader-disclosure__collapse-button').count() === 0, 'Minduim/BBS must not expose a bottom collapse action');
  const folhaBioOpen = page.locator('#bio-communication-folha');
  assert(await folhaBioOpen.getAttribute('data-reader-presentation') === 'always-open', 'Folhateen always-open presentation state missing');
  assert(await folhaBioOpen.locator('details.reader-disclosure').count() === 0, 'Folhateen must not be wrapped in disclosure');
  assert(await folhaBioOpen.locator('.reader-disclosure__toggle').count() === 0, 'Folhateen must not expose a top toggle');
  assert(await folhaBioOpen.locator('.reader-disclosure__collapse-button').count() === 0, 'Folhateen must not expose a bottom collapse action');
  const spiritualityBio = page.locator('#bio-spirituality-seeker');
  assert(await spiritualityBio.getAttribute('data-reader-presentation') === 'always-open', 'Spirituality biography-only always-open state missing');
  assert(await spiritualityBio.locator('details.reader-disclosure').count() === 0, 'Spirituality must not be wrapped in disclosure');
  assert(await spiritualityBio.locator('.reader-disclosure__toggle').count() === 0, 'Spirituality must not expose a top toggle');
  assert(await spiritualityBio.locator('.reader-disclosure__collapse-button').count() === 0, 'Spirituality must not expose a bottom collapse action');
  assert(await spiritualityBio.locator('h2 > a.entry-title-permalink').getAttribute('href') === '/pt/biografia/espiritualidade-o-buscador/', 'Spirituality standalone permalink missing from Full Bio heading');
  const spiritualityTopics = await spiritualityBio.locator('.reader-disclosure__topic').allInnerTexts();
  ['Meditação', 'Vipassana', 'Budismo', 'Osho', 'Mindfulness'].forEach((label) => assert(spiritualityTopics.includes(label), `Spirituality topic missing: ${label}`));
  assert(!spiritualityTopics.includes('Buddhismo'), 'Legacy Buddhismo topic must not reappear');
  assert(!/buddhista/i.test(await spiritualityBio.innerText()), 'Legacy Portuguese buddhista spelling must not reappear');
  assert(await spiritualityBio.locator('img[src="/assets/media/thread/vipassana03.jpg"]').count() === 1, 'Spirituality cropped Vipassana reconstruction missing from always-open body');
  assert((await page.locator('#bio-internet-mirantte details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Mirantte is not featured in Full Bio');
  assert((await page.locator('#bio-internet-cookieweb details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'CookieWEB is not featured in Full Bio');
  assert((await page.locator('#bio-audiovisual-meia-noite details.reader-disclosure').getAttribute('class')).includes('reader-disclosure--featured'), 'Meia-Noite is not featured in Full Bio');

  // Featured visual treatment exists only while collapsed.
  const featuredStateProbe = page.locator('#bio-internet-mirantte details.reader-disclosure');
  const featuredClosedStyle = await featuredStateProbe.evaluate((el) => ({backgroundImage: getComputedStyle(el).backgroundImage, boxShadow: getComputedStyle(el).boxShadow}));
  assert(featuredClosedStyle.backgroundImage !== 'none', 'Featured entry lost collapsed highlight background');
  assert(featuredClosedStyle.boxShadow !== 'none', 'Featured entry lost collapsed highlight shadow');
  await page.locator('#bio-internet-mirantte details.reader-disclosure > summary').click();
  await page.waitForTimeout(250);
  const featuredOpenStyle = await featuredStateProbe.evaluate((el) => ({backgroundImage: getComputedStyle(el).backgroundImage, boxShadow: getComputedStyle(el).boxShadow}));
  assert(featuredOpenStyle.backgroundImage === 'none', `Featured highlight background remained after expansion: ${featuredOpenStyle.backgroundImage}`);
  assert(featuredOpenStyle.boxShadow === 'none', `Featured highlight shadow remained after expansion: ${featuredOpenStyle.boxShadow}`);
  await page.locator('#bio-internet-mirantte details.reader-disclosure > summary').click();
  await page.waitForTimeout(250);
  const featuredReclosedStyle = await featuredStateProbe.evaluate((el) => ({backgroundImage: getComputedStyle(el).backgroundImage, boxShadow: getComputedStyle(el).boxShadow}));
  assert(featuredReclosedStyle.backgroundImage !== 'none', 'Featured highlight did not return after collapse');
  assert(featuredReclosedStyle.boxShadow !== 'none', 'Featured highlight shadow did not return after collapse');

  // Full Biography rich summaries are path-scoped: dense entries can be compact here without changing thematic vertical UX.
  const mirantteBioPreview = page.locator('#bio-internet-mirantte .reader-disclosure__preview');
  assert(await mirantteBioPreview.count() === 1, 'Mirantte Full Bio rich preview missing');
  assert(await mirantteBioPreview.locator('.reader-disclosure__preview-paragraph').count() === 4, 'Mirantte Full Bio preview paragraph count incorrect');
  assert((await mirantteBioPreview.innerText()).includes('tráfego orgânico'), 'Mirantte Full Bio preview lost acquisition problem');
  assert(await mirantteBioPreview.locator('img').getAttribute('src') === '/assets/media/galleries/mirantte-news/mirantte-news-02-480.webp', 'Mirantte Full Bio preview image incorrect');
  const mirantteIndicators = await page.locator('#bio-internet-mirantte .reader-disclosure__badge').allInnerTexts();
  ['34 fotos'].forEach((label) => assert(mirantteIndicators.includes(label), `Mirantte indicator missing: ${label}`));

  const cookieBioPreviewRich = page.locator('#bio-internet-cookieweb .reader-disclosure__preview');
  assert(await cookieBioPreviewRich.count() === 1, 'CookieWEB Full Bio rich preview missing');
  assert(await cookieBioPreviewRich.locator('.reader-disclosure__preview-paragraph').count() === 4, 'CookieWEB Full Bio preview paragraph count incorrect');
  assert((await cookieBioPreviewRich.innerText()).includes('mais de 22 contas simultâneas'), 'CookieWEB Full Bio preview lost operating scale');
  assert(await cookieBioPreviewRich.locator('img').getAttribute('src') === '/assets/media/galleries/cookieweb/cookieweb-19-480.webp', 'CookieWEB Full Bio preview image incorrect');
  const cookieIndicators = await page.locator('#bio-internet-cookieweb .reader-disclosure__badge').allInnerTexts();
  ['20 fotos', '3 certificados GAP', '1 registro contemporâneo'].forEach((label) => assert(cookieIndicators.includes(label), `CookieWEB indicator missing: ${label}`));

  const meiaBioPreview = page.locator('#bio-audiovisual-meia-noite .reader-disclosure__preview');
  assert(await meiaBioPreview.count() === 1, 'Meia-Noite Full Bio rich preview missing');
  assert(await meiaBioPreview.locator('.reader-disclosure__preview-paragraph').count() === 3, 'Meia-Noite Full Bio preview paragraph count incorrect');
  assert((await meiaBioPreview.innerText()).includes('00:01'), 'Meia-Noite Full Bio preview lost title rationale');
  assert(await meiaBioPreview.locator('img').getAttribute('src') === '/assets/media/galleries/meia-noite-e-uns/meia-noite-e-uns-01-480.webp', 'Meia-Noite Full Bio preview image incorrect');
  const meiaIndicators = await page.locator('#bio-audiovisual-meia-noite .reader-disclosure__badge').allInnerTexts();
  ['22 fotos', '4 vídeos'].forEach((label) => assert(meiaIndicators.includes(label), `Meia-Noite indicator missing: ${label}`));

  const bestBioPreview = page.locator('#bio-internet-best .reader-disclosure__preview');
  assert(await bestBioPreview.count() === 1, 'BEST Full Bio rich preview missing');
  assert(await bestBioPreview.locator('.reader-disclosure__preview-paragraph').count() === 3, 'BEST Full Bio preview paragraph count incorrect');
  assert((await bestBioPreview.innerText()).includes('Segmentação Avançada em Search e Social'), 'BEST Full Bio preview lost workshop context');
  assert(await bestBioPreview.locator('img').getAttribute('src') === '/assets/media/thread/best-kenshoo-workshop.webp', 'BEST Full Bio preview image incorrect');
  const bestBioIndicators = await page.locator('#bio-internet-best .reader-disclosure__badge').allInnerTexts();
  ['4 vídeos', '11 registros visuais'].forEach((label) => assert(bestBioIndicators.includes(label), `BEST Full Bio indicator missing: ${label}`));
  const bestBioTopics = await page.locator('#bio-internet-best .reader-disclosure__topic').allInnerTexts();
  ['Performance', 'Search Marketing', 'Social Ads', 'Kenshoo', 'E-commerce'].forEach((label) => assert(bestBioTopics.includes(label), `BEST Full Bio topic missing: ${label}`));

  // Rich collapsed-summary pilot: Melissa is useful before expansion and returns to the full entry when opened.
  const melissaBio = page.locator('#bio-hai-melissa');
  const melissaPreview = melissaBio.locator('.reader-disclosure__preview');
  assert(await melissaPreview.count() === 1, 'Melissa rich collapsed preview missing');
  assert((await melissaPreview.innerText()).includes('63 horas e 518 prompts'), 'Melissa collapsed preview lost core case metrics');
  assert((await melissaPreview.innerText()).includes('Melissa Framework'), 'Melissa collapsed preview lost framework outcome');
  assert(await melissaPreview.locator('.reader-disclosure__preview-paragraph').count() === 4, 'Melissa collapsed preview should contain four concise editorial paragraphs');
  assert(await melissaPreview.locator('strong').count() >= 8, 'Melissa collapsed preview lost editorial emphasis');
  const melissaTopics = await melissaBio.locator('.reader-disclosure__topic').allInnerTexts();
  const melissaTopicBackground = await melissaBio.locator('.reader-disclosure__topic').first().evaluate((el) => getComputedStyle(el).backgroundColor);
  assert(melissaTopicBackground !== 'rgba(0, 0, 0, 0)', 'Melissa topic chips lost their neutral background surface');
  ['AI', 'HAI', 'HCI', 'Prompt Engineering', 'Melissa 1.0'].forEach((label) => assert(melissaTopics.includes(label), `Melissa topic missing: ${label}`));
  const melissaIndicators = await melissaBio.locator('.reader-disclosure__badge').allInnerTexts();
  ['2 imagens', '1 link para download', '4 documentos com DOI', '1 link para repositório'].forEach((label) => assert(melissaIndicators.includes(label), `Melissa indicator missing: ${label}`));
  const melissaPreviewStyle = await melissaPreview.locator('.reader-disclosure__preview-paragraph').first().evaluate((el) => ({fontSize: getComputedStyle(el).fontSize, color: getComputedStyle(el).color}));
  assert(parseFloat(melissaPreviewStyle.fontSize) >= 16.5, `Melissa preview font is still too small: ${melissaPreviewStyle.fontSize}`);
  assert(melissaPreviewStyle.color !== 'rgb(170, 167, 159)', 'Melissa preview is still using muted gray text');
  assert(await melissaPreview.locator('img').getAttribute('src') === '/assets/media/thread/melissa1_0_selfportrait300kb.jpg', 'Melissa collapsed preview cover image incorrect');
  assert(await melissaBio.locator('details.reader-disclosure').getAttribute('open') === null, 'Melissa preview should start collapsed');
  await melissaBio.locator('details.reader-disclosure > summary').click();
  assert(await melissaBio.locator('details.reader-disclosure').getAttribute('open') !== null, 'Melissa summary click did not open full entry');
  assert(await melissaPreview.isHidden(), 'Melissa compact preview remained visible after expansion');
  assert((await melissaBio.locator('.reader-disclosure__body').innerText()).includes('O que aconteceu depois não foi planejado.'), 'Melissa full body was not preserved after expansion');
  await melissaBio.locator('details.reader-disclosure > summary').click();

  // Biography-only Chapter Page stays fully readable and carries the same controlled topics.
  await page.goto(`${BASE}/pt/biografia/espiritualidade-o-buscador/`, {waitUntil: 'networkidle'});
  assert(await page.locator('h1').innerText() === 'Espiritualidade — “O Buscador”', 'Spirituality standalone H1 incorrect');
  assert(await page.locator('meta[name="robots"]').getAttribute('content') === 'index,follow', 'Spirituality standalone robots incorrect');
  const standaloneSpiritualityTopics = await page.locator('.entry-topic').allInnerTexts();
  ['Meditação', 'Vipassana', 'Budismo', 'Osho', 'Mindfulness'].forEach((label) => assert(standaloneSpiritualityTopics.includes(label), `Standalone spirituality topic missing: ${label}`));
  assert(!standaloneSpiritualityTopics.includes('Buddhismo'), 'Legacy standalone Buddhismo topic must not reappear');
  assert(!/buddhista/i.test(await page.locator('article.entry-page-body').innerText()), 'Standalone Portuguese buddhista spelling must not reappear');
  assert((await page.locator('article.entry-page-body').innerText()).includes('Dhanadhammo'), 'Spirituality standalone page lost Dhanadhammo');
  assert(await page.locator('img[src="/assets/media/thread/vipassana03.jpg"]').count() === 1, 'Spirituality standalone page lost cropped reconstruction');
  assert(await page.locator('details.reader-disclosure').count() === 0, 'Standalone spirituality page must not initialize Reader disclosure');

  await page.goto(`${BASE}/en/biography/spirituality-the-seeker/`, {waitUntil: 'networkidle'});
  const seekerEnglishText = await page.locator('article.entry-page-body').innerText();
  assert(/\bBuddhism\b/.test(seekerEnglishText), 'English Seeker page lost conventional Buddhism spelling');
  assert(/\bBuddhist\b/.test(seekerEnglishText), 'English Seeker page lost conventional Buddhist spelling');
  assert(!/\bBudism\b|\bBudist\b|\bBuddhismo\b|\bbuddhista\b/i.test(seekerEnglishText), 'English Seeker page contains a non-conventional Buddhism/Buddhist spelling');

  // IA/HAI preserves continuous reading: Melissa is the oldest/final chapter and stays fully open.
  await page.goto(`${BASE}/pt/ia-hai/`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() === 0, 'IA/HAI should preserve a fully open continuous-reading surface');
  assert(await page.locator('.reader-disclosure-controls').count() === 0, 'IA/HAI should not show global disclosure controls');
  assert(await page.locator('#pro2 details.reader-disclosure').count() === 0, 'PRO v2 was unexpectedly collapsed');
  assert(await page.locator('#pro1 details.reader-disclosure').count() === 0, 'PRO v1 was unexpectedly collapsed');
  const melissaHai = page.locator('#melissa');
  assert(await melissaHai.getAttribute('data-reader-presentation') === 'always-open', 'Melissa IA/HAI path-scoped always-open state missing');
  assert(await melissaHai.locator('details.reader-disclosure').count() === 0, 'Melissa IA/HAI must not be wrapped in disclosure');
  assert(await melissaHai.locator('.reader-disclosure__preview').count() === 0, 'Melissa IA/HAI must not render a compact preview');
  assert((await melissaHai.innerText()).includes('O que aconteceu depois não foi planejado.'), 'Melissa IA/HAI full body is not visible');
  assert((await melissaHai.innerText()).includes('Melissa Framework'), 'Melissa IA/HAI lost framework content');

  await page.goto(`${BASE}/en/ai-hai/`, {waitUntil: 'networkidle'});
  const melissaHaiEn = page.locator('#melissa');
  assert(await melissaHaiEn.getAttribute('data-reader-presentation') === 'always-open', 'Melissa EN AI/HAI path-scoped always-open state missing');
  assert(await melissaHaiEn.locator('details.reader-disclosure').count() === 0, 'Melissa EN AI/HAI must not be wrapped in disclosure');
  assert(await melissaHaiEn.locator('.reader-disclosure__preview').count() === 0, 'Melissa EN AI/HAI must not render a compact preview');
  assert((await melissaHaiEn.innerText()).includes('What happened afterward was not planned.'), 'Melissa EN AI/HAI full body is not visible');

  // Full Biography: deep-link opening + registry-backed metadata without query flag.
  await page.goto(`${BASE}/pt/biografia/#bio-internet-cookieweb`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() >= 28, 'Full Bio produced too few disclosures');
  const cookieBio = page.locator('#bio-internet-cookieweb');
  assert(await cookieBio.locator('details.reader-disclosure').getAttribute('open') !== null, 'CookieWEB deep link did not auto-open');
  assert(await cookieBio.locator('.reader-disclosure__preview').count() === 1, 'CookieWEB rich summary was not used on Full Bio deep link');
  assert(await cookieBio.locator('.reader-disclosure__topic').count() >= 4, 'CookieWEB topic chips missing');
  assert((await cookieBio.innerText()).includes('qualidade de vida'), 'Disclosure transformation lost CookieWEB body text');
  assert(await cookieBio.locator('.reader-disclosure__collapse-button').count() === 1, 'Bottom collapse action missing from CookieWEB');
  await cookieBio.locator('.reader-disclosure__collapse-button').click();
  assert(await cookieBio.locator('details.reader-disclosure').getAttribute('open') === null, 'Bottom collapse action did not close CookieWEB');

  // Internet stress set: normal URL + large galleries, composite landmark, video count and Chapter Page link.
  // Internet & Performance is a native, continuous-reading editorial vertical.
  // No details, Reader toolbar or bottom collapse buttons; the full HTML stays readable.
  await page.goto(`${BASE}/pt/internet/`, {waitUntil: 'networkidle'});
  const internetChapters = page.locator('article.article-body > section.chapter.internet-entry');
  assert(await internetChapters.count() >= 11, 'Internet must preserve its full collection of chapters');
  assert(await page.locator('details.reader-disclosure').count() === 0, 'Internet must not wrap chapters in collapsible details');
  assert(await page.locator('.reader-disclosure-controls').count() === 0, 'Internet must not show the legacy reading toolbar');
  assert(await page.locator('.reader-disclosure__collapse-button, .reader-disclosure__toggle').count() === 0, 'Internet must not expose collapse buttons');
  assert(!((await page.locator('html').getAttribute('class') || '').includes('reader-disclosure-active')), 'Internet must not initialize the disclosure Reader');
  for (const label of ['Controles de leitura', 'Abrir todos', 'Recolher todos', 'Clique para recolher']) {
    assert(await page.getByText(label, {exact: true}).count() === 0, `Internet still displays legacy Reader text: ${label}`);
  }

  const bbs = page.locator('#bbs');
  assert(await bbs.locator(':scope > .phase-year').innerText() === '1992–1996', 'BBS date lost its original location');
  assert(await bbs.locator(':scope > h2').innerText() === 'Cultura BBS', 'BBS heading changed');

  const mirantte = page.locator('#mirantte');
  assert(await mirantte.locator(':scope > .phase-year').innerText() === '2004–2008', 'Mirantte date changed');
  assert(await mirantte.locator(':scope > h2 .entry-title-permalink').getAttribute('href') === '/pt/internet/mirantte-news/', 'Mirantte standalone page link missing');
  assert(await mirantte.locator('.record-gallery__item').count() === 34, 'Mirantte gallery items were lost');
  assert(await mirantte.isVisible(), 'Mirantte chapter became hidden');
  // The editorial header uses the upper half of the original gallery photos 1 and 2.
  const mirantteFeature = mirantte.locator('.mirantte-feature');
  const mirantteTiles = mirantteFeature.locator('a.mirantte-feature__link');
  assert(await mirantteTiles.count() === 2, 'Mirantte lead must contain exactly two stacked images');
  assert(await mirantteTiles.nth(0).getAttribute('data-gallery-preview') === 'mirantte-news', 'Mirantte photo 1 is not linked to the gallery');
  assert(await mirantteTiles.nth(1).getAttribute('data-gallery-preview') === 'mirantte-news', 'Mirantte photo 2 is not linked to the gallery');
  const leadBeforeCopy = await mirantte.evaluate((section) => {
    const heading = section.querySelector(':scope > h2');
    const imagePair = section.querySelector(':scope > .mirantte-feature');
    return heading && imagePair && heading.nextElementSibling === imagePair;
  });
  assert(leadBeforeCopy, 'Mirantte cropped pair is not directly below its heading');
  const imageStyle = await mirantteTiles.nth(0).locator('img').evaluate((img) => ({
    fit: getComputedStyle(img).objectFit,
    position: getComputedStyle(img).objectPosition,
    cropRatio: getComputedStyle(img.parentElement).aspectRatio
  }));
  assert(imageStyle.fit === 'cover' && (imageStyle.position.endsWith('0%') || imageStyle.position.includes('top')), `Mirantte highlight needs top crop: ${JSON.stringify(imageStyle)}`);
  assert(imageStyle.cropRatio === '3 / 2', 'Mirantte highlight must use the rectangular crop');
  assert(await mirantte.locator('a[href="/assets/archive/mirantte-news-card.webp"]').count() === 0, 'Mirantte obsolete business card still visible');

  await mirantteTiles.nth(0).click();
  assert(await page.locator('.archive-lightbox:not([hidden]) .archive-lightbox__counter').innerText() === '1 / 34', 'Cropped photo 1 should open at gallery position 1/34');
  await page.keyboard.press('Escape');
  await mirantteTiles.nth(1).click();
  assert(await page.locator('.archive-lightbox:not([hidden]) .archive-lightbox__counter').innerText() === '2 / 34', 'Cropped photo 2 should open at gallery position 2/34');
  await page.keyboard.press('Escape');

  const cookieweb = page.locator('#cookieweb');
  assert(await cookieweb.locator(':scope > .phase-year').innerText() === '2010–2012', 'CookieWEB date changed');
  assert(await cookieweb.locator(':scope > h2').innerText() === 'Agência CookieWEB - Search em Escala', 'CookieWEB heading changed');
  assert(await cookieweb.locator('.record-gallery__item').count() === 20, 'CookieWEB gallery items were lost');
  assert(await cookieweb.isVisible(), 'CookieWEB chapter became hidden');

  const best = page.locator('#best');
  assert(await best.locator(':scope > h2 .entry-title-permalink').getAttribute('href') === '/pt/internet/best-kenshoo/', 'BEST Chapter Page link missing');
  assert(await best.locator('.video-pill').count() === 4, 'BEST video collection was lost');

  // English has the identical non-collapsible policy and full open content.
  await page.goto(`${BASE}/en/internet/`, {waitUntil: 'networkidle'});
  assert(await page.locator('article.article-body > section.chapter.internet-entry').count() >= 11, 'English Internet chapters missing');
  assert(await page.locator('details.reader-disclosure, .reader-disclosure-controls, .reader-disclosure__collapse-button, .reader-disclosure__toggle').count() === 0, 'English Internet still has disclosure UI');
  assert(!((await page.locator('html').getAttribute('class') || '').includes('reader-disclosure-active')), 'English Internet initialized disclosure');
  for (const label of ['Reading controls', 'Open all', 'Collapse all', 'Click to collapse']) {
    assert(await page.getByText(label, {exact: true}).count() === 0, `English Internet still displays Reader text: ${label}`);
  }
  assert(await page.locator('#cookieweb > .phase-year').innerText() === '2010–2012', 'English CookieWEB date changed');
  assert(await page.locator('#cookieweb > h2').innerText() === 'CookieWEB Agency - Search at Scale', 'English CookieWEB heading changed');
  assert(await page.locator('#mirantte .record-gallery__item').count() === 34, 'English Mirantte gallery was lost');
  assert(await page.locator('#mirantte .mirantte-feature__link').count() === 2, 'English Mirantte lead pair missing');
  assert(await page.locator('#mirantte a[href="/assets/archive/mirantte-news-card.webp"]').count() === 0, 'English Mirantte card remains');

  // Culture & Audiovisual is intentionally continuous reading: normal and legacy query-flag URLs remain fully open.
  await page.goto(`${BASE}/pt/comunicacao/`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() === 0, 'Culture & Audiovisual must not initialize disclosure');
  assert(!((await page.locator('html').getAttribute('class') || '').includes('reader-disclosure-active')), 'Culture & Audiovisual unexpectedly received Reader UX class');
  assert(await page.locator('#folha').isVisible(), 'Folhateen disappeared from open Culture & Audiovisual page');
  assert(await page.locator('#meia-noite').isVisible(), 'Meia-Noite disappeared from open Culture & Audiovisual page');
  await page.goto(`${BASE}/pt/comunicacao/?ux=disclosure`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() === 0, 'Legacy disclosure query must not collapse Culture & Audiovisual');

  // EN core page consumes the same registry with language-specific labels/copy by default.
  await page.goto(`${BASE}/en/biography/#bio-communication-folha`, {waitUntil: 'networkidle'});
  assert(await page.getByRole('button', {name: 'Open all'}).count() === 1, 'English disclosure controls not localized');
  assert((await page.getByText('Click to expand', {exact: false}).count()) > 0, 'Permanent English CTA missing');
  const folhaEn = page.locator('#bio-communication-folha');
  assert(await folhaEn.getAttribute('data-reader-presentation') === 'always-open', 'English Folha always-open state missing');
  assert(await folhaEn.locator('details.reader-disclosure').count() === 0, 'English Folha must not be wrapped in disclosure');
  assert((await folhaEn.innerText()).includes('Folhateen'), 'English Folha content disappeared');

  // Chapter Pages: browser-readable, indexing policy, canonical, exact preserved structures.
  await page.goto(`${BASE}/pt/comunicacao/folhateen-orfaos-do-rock/`, {waitUntil: 'networkidle'});
  assert(await page.locator('main[data-entry-id="communication-folha"]').count() === 1, 'Folha Chapter Page stable id missing');
  assert(await page.locator('meta[name="robots"]').getAttribute('content') === 'index,follow', 'Folha Chapter Page robots incorrect');
  assert((await page.locator('link[rel="canonical"]').getAttribute('href')).endsWith('/pt/comunicacao/folhateen-orfaos-do-rock/'), 'Folha canonical incorrect');
  assert(await page.locator('.fact-strip .fact').count() === 1, 'Folha hero exposes taxonomy as a KPI');
  assert(await page.locator('.entry-breadcrumbs').count() === 1, 'Folha visible breadcrumbs missing');

  // Generated standalone Chapter Page inherits Mirantte features from the neutral PT/EN fragment.
  await page.goto(`${BASE}/pt/internet/mirantte-news/`, {waitUntil: 'networkidle'});
  assert(await page.locator('.entry-page-body > .mirantte-feature .mirantte-feature__link').count() === 2, 'Mirantte standalone feature missing');
  assert(await page.locator('.record-gallery[data-gallery="mirantte-news"] .record-gallery__item').count() === 34, 'Mirantte standalone gallery lost images');
  assert(await page.locator('a[href="/assets/archive/mirantte-news-card.webp"]').count() === 0, 'Mirantte standalone card remains');
  await page.locator('.mirantte-feature__link').nth(1).click();
  assert(await page.locator('.archive-lightbox:not([hidden]) .archive-lightbox__counter').innerText() === '2 / 34', 'Standalone cropped Mirantte image does not expand into gallery');
  await page.keyboard.press('Escape');
  await page.goto(`${BASE}/en/internet/mirantte-news/`, {waitUntil: 'networkidle'});
  assert(await page.locator('.mirantte-feature__link').count() === 2, 'English standalone Mirantte feature missing');
  assert(await page.locator('a[href="/assets/archive/mirantte-news-card.webp"]').count() === 0, 'English standalone Mirantte card remains');

  await page.goto(`${BASE}/pt/internet/best-kenshoo/`, {waitUntil: 'networkidle'});
  assert(await page.locator('main[data-entry-id="internet-best"]').count() === 1, 'BEST Chapter Page stable id missing');
  const bestWorkshopVideoLibrary = page.locator('.video-library').filter({has: page.locator('#best-workshop-video-title')});
  assert(await bestWorkshopVideoLibrary.count() === 1, 'BEST Chapter Page audiovisual library missing');
  assert(await bestWorkshopVideoLibrary.locator('.video-pill').count() === 4, 'BEST Chapter Page did not preserve four workshop video parts');
  assert(await page.locator('.fact-strip .fact').count() === 1, 'BEST hero exposes taxonomy as a KPI');

  await context.close();
}

async function runMobile(browser) {
  const context = await browser.newContext({viewport: {width: 390, height: 844}, isMobile: true});
  const page = await context.newPage();
  await blockExternal(page);
  await page.goto(`${BASE}/pt/biografia/`, {waitUntil: 'networkidle'});
  assert(await page.locator('details.reader-disclosure').count() >= 28, 'Mobile Full Bio did not initialize disclosure by default');
  assert(await page.locator('#bio-internet-bbs details.reader-disclosure').count() === 0, 'Mobile Minduim/BBS must not become disclosure');
  assert(await page.locator('#bio-internet-bbs').getAttribute('data-reader-presentation') === 'always-open', 'Mobile Minduim/BBS always-open state missing');
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
