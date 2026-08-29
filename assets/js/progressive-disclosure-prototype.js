(() => {
  if (window.__mnDisclosurePrototypeLoaded) return;
  window.__mnDisclosurePrototypeLoaded = true;

  const isPortuguese = document.documentElement.lang?.startsWith('pt');
  const path = window.location.pathname;
  const fullBio = path === '/pt/biografia/' || path === '/en/biography/';
  const internet = path === '/pt/internet/' || path === '/en/internet/';
  if (!fullBio && !internet) return;

  const labels = isPortuguese ? {
    mode: 'Modo compacto experimental',
    openAll: 'Abrir todos',
    closeAll: 'Recolher todos',
    open: 'Expandir capítulo',
    close: 'Recolher capítulo',
    photoOne: '1 foto',
    photoMany: (n) => `${n} fotos`,
    imageOne: '1 imagem',
    imageMany: (n) => `${n} imagens`,
    videoOne: '1 vídeo',
    videoMany: (n) => `${n} vídeos`,
    docOne: '1 documento',
    docMany: (n) => `${n} documentos`
  } : {
    mode: 'Experimental compact mode',
    openAll: 'Open all',
    closeAll: 'Collapse all',
    open: 'Expand chapter',
    close: 'Collapse chapter',
    photoOne: '1 photo',
    photoMany: (n) => `${n} photos`,
    imageOne: '1 image',
    imageMany: (n) => `${n} images`,
    videoOne: '1 video',
    videoMany: (n) => `${n} videos`,
    docOne: '1 document',
    docMany: (n) => `${n} documents`
  };

  const selector = fullBio
    ? 'section.chapter.bio-entry'
    : 'article.article-body > section.chapter';
  const chapters = [...document.querySelectorAll(selector)];
  if (!chapters.length) return;

  document.documentElement.classList.add('ux-disclosure-prototype');

  const cleanText = (value) => value.replace(/\s+/g, ' ').trim();

  const excerptFor = (section) => {
    const directParagraph = [...section.children].find((node) => node.tagName === 'P');
    const paragraph = directParagraph || section.querySelector('p');
    if (!paragraph) return '';
    const text = cleanText(paragraph.textContent || '');
    if (text.length <= 230) return text;

    const firstSentence = text.match(/^.{80,230}?[.!?](?:\s|$)/);
    if (firstSentence) return cleanText(firstSentence[0]);

    const clipped = text.slice(0, 227);
    const lastSpace = clipped.lastIndexOf(' ');
    return `${clipped.slice(0, lastSpace > 160 ? lastSpace : 227).trim()}…`;
  };

  const uniqueVideoLinks = (section) => {
    const urls = new Set();
    section.querySelectorAll('iframe[src], video, a[href]').forEach((node) => {
      if (node.tagName === 'VIDEO') {
        urls.add(`video:${urls.size}`);
        return;
      }
      const raw = node.getAttribute(node.tagName === 'IFRAME' ? 'src' : 'href') || '';
      if (/youtube\.com|youtu\.be|vimeo\.com/i.test(raw)) urls.add(raw);
    });
    return urls.size;
  };

  const badgesFor = (section) => {
    const galleryPhotos = section.querySelectorAll('.record-gallery__item').length;
    const documents = section.querySelectorAll('.inline-record').length;
    const videos = uniqueVideoLinks(section);
    const totalImages = section.querySelectorAll('img').length;
    const nonGalleryNonDocumentImages = Math.max(0, totalImages - galleryPhotos - documents);
    const badges = [];

    if (galleryPhotos) badges.push(galleryPhotos === 1 ? labels.photoOne : labels.photoMany(galleryPhotos));
    else if (nonGalleryNonDocumentImages) {
      badges.push(nonGalleryNonDocumentImages === 1 ? labels.imageOne : labels.imageMany(nonGalleryNonDocumentImages));
    }
    if (videos) badges.push(videos === 1 ? labels.videoOne : labels.videoMany(videos));
    if (documents) badges.push(documents === 1 ? labels.docOne : labels.docMany(documents));
    return badges;
  };

  const detailsForSection = new Map();

  chapters.forEach((section) => {
    const heading = [...section.children].find((node) => node.tagName === 'H2');
    if (!heading) return;

    const meta = [...section.children].find((node) => node.classList?.contains('bio-entry-meta')) || null;
    const excerpt = excerptFor(section);
    const badges = badgesFor(section);

    const details = document.createElement('details');
    details.className = 'ux-disclosure';

    const summary = document.createElement('summary');
    summary.className = 'ux-disclosure__summary';

    if (meta) summary.appendChild(meta);
    summary.appendChild(heading);

    if (excerpt) {
      const excerptNode = document.createElement('p');
      excerptNode.className = 'ux-disclosure__excerpt';
      excerptNode.textContent = excerpt;
      summary.appendChild(excerptNode);
    }

    if (badges.length) {
      const badgeRow = document.createElement('div');
      badgeRow.className = 'ux-disclosure__badges';
      badges.forEach((text) => {
        const badge = document.createElement('span');
        badge.className = 'ux-disclosure__badge';
        badge.textContent = text;
        badgeRow.appendChild(badge);
      });
      summary.appendChild(badgeRow);
    }

    const toggle = document.createElement('span');
    toggle.className = 'ux-disclosure__toggle';
    toggle.innerHTML = `<span class="ux-disclosure__toggle-open">${labels.open} ↓</span><span class="ux-disclosure__toggle-close">${labels.close} ↑</span>`;
    summary.appendChild(toggle);

    const body = document.createElement('div');
    body.className = 'ux-disclosure__body';
    while (section.firstChild) body.appendChild(section.firstChild);

    details.appendChild(summary);
    details.appendChild(body);
    section.appendChild(details);
    section.classList.add('ux-disclosure-chapter');
    detailsForSection.set(section, details);
  });

  const activeDetails = [...detailsForSection.values()];
  if (!activeDetails.length) return;

  const controls = document.createElement('div');
  controls.className = 'ux-disclosure-controls';
  controls.setAttribute('role', 'group');
  controls.setAttribute('aria-label', labels.mode);

  const controlLabel = document.createElement('span');
  controlLabel.className = 'ux-disclosure-controls__label';
  controlLabel.textContent = labels.mode;

  const openAll = document.createElement('button');
  openAll.type = 'button';
  openAll.textContent = labels.openAll;

  const closeAll = document.createElement('button');
  closeAll.type = 'button';
  closeAll.textContent = labels.closeAll;

  controls.append(controlLabel, openAll, closeAll);

  if (fullBio) {
    const intro = document.querySelector('.bio-chronology-intro');
    if (intro) intro.insertAdjacentElement('afterend', controls);
    else chapters[0].insertAdjacentElement('beforebegin', controls);
  } else {
    chapters[0].insertAdjacentElement('beforebegin', controls);
  }

  openAll.addEventListener('click', () => {
    activeDetails.forEach((details) => { details.open = true; });
  });

  closeAll.addEventListener('click', () => {
    activeDetails.forEach((details) => { details.open = false; });
  });

  const openContainingChapter = (target, scroll = false) => {
    if (!(target instanceof Element)) return false;
    const section = target.closest('section.chapter');
    if (!section) return false;
    const details = detailsForSection.get(section);
    if (!details) return false;
    details.open = true;
    if (scroll) {
      requestAnimationFrame(() => section.scrollIntoView({block: 'start'}));
    }
    return true;
  };

  const handleHash = (scroll = false) => {
    if (!window.location.hash) return;
    let id = window.location.hash.slice(1);
    try { id = decodeURIComponent(id); } catch (_) {}
    const target = document.getElementById(id);
    if (target) openContainingChapter(target, scroll);
  };

  document.addEventListener('click', (event) => {
    const link = event.target.closest?.('a[href^="#"]');
    if (!link) return;
    const href = link.getAttribute('href');
    if (!href || href === '#') return;
    let id = href.slice(1);
    try { id = decodeURIComponent(id); } catch (_) {}
    const target = document.getElementById(id);
    if (target) openContainingChapter(target, false);
  });

  window.addEventListener('hashchange', () => handleHash(true));
  handleHash(false);

  let printState = null;
  window.addEventListener('beforeprint', () => {
    printState = activeDetails.map((details) => details.open);
    activeDetails.forEach((details) => { details.open = true; });
  });
  window.addEventListener('afterprint', () => {
    if (!printState) return;
    activeDetails.forEach((details, index) => { details.open = Boolean(printState[index]); });
    printState = null;
  });
})();
