(() => {
  if (window.__mnReaderDisclosureLoaded) return;
  window.__mnReaderDisclosureLoaded = true;

  const isPortuguese = document.documentElement.lang?.startsWith('pt');
  const pagePath = window.location.pathname;
  const repoPathByUrl = {
    '/pt/biografia/': 'pt/biografia/index.html',
    '/en/biography/': 'en/biography/index.html',
    '/pt/internet/': 'pt/internet/index.html',
    '/en/internet/': 'en/internet/index.html',
    '/pt/comunicacao/': 'pt/comunicacao/index.html',
    '/en/communication/': 'en/communication/index.html',
    '/pt/audiovisual/': 'pt/audiovisual/index.html',
    '/en/audiovisual/': 'en/audiovisual/index.html'
  };
  const repoPath = repoPathByUrl[pagePath];
  if (!repoPath) return;

  const labels = isPortuguese ? {
    mode: 'Leitura compacta',
    openAll: 'Abrir todos',
    closeAll: 'Recolher todos',
    open: 'Clique para expandir',
    close: 'Clique para recolher',
    closeBottom: 'Clique para recolher',
    page: 'Página própria',
    pageLink: 'Abrir página própria ↗',
    related: 'Relacionado',
    photoOne: '1 foto',
    photoMany: (n) => `${n} fotos`,
    imageOne: '1 imagem',
    imageMany: (n) => `${n} imagens`,
    videoOne: '1 vídeo',
    videoMany: (n) => `${n} vídeos`,
    docOne: '1 documento',
    docMany: (n) => `${n} documentos`
  } : {
    mode: 'Compact reading',
    openAll: 'Open all',
    closeAll: 'Collapse all',
    open: 'Click to expand',
    close: 'Click to collapse',
    closeBottom: 'Click to collapse',
    page: 'Standalone page',
    pageLink: 'Open standalone page ↗',
    related: 'Related',
    photoOne: '1 photo',
    photoMany: (n) => `${n} photos`,
    imageOne: '1 image',
    imageMany: (n) => `${n} images`,
    videoOne: '1 video',
    videoMany: (n) => `${n} videos`,
    docOne: '1 document',
    docMany: (n) => `${n} documents`
  };

  const cleanText = (value) => String(value || '').replace(/\s+/g, ' ').trim();
  const language = isPortuguese ? 'pt' : 'en';

  const excerptFor = (section) => {
    const directParagraph = [...section.children].find((node) => node.tagName === 'P');
    const paragraph = directParagraph || section.querySelector('p');
    if (!paragraph) return '';
    const text = cleanText(paragraph.textContent);
    if (text.length <= 240) return text;
    const firstSentence = text.match(/^.{80,240}?[.!?](?:\s|$)/);
    if (firstSentence) return cleanText(firstSentence[0]);
    const clipped = text.slice(0, 237);
    const lastSpace = clipped.lastIndexOf(' ');
    return `${clipped.slice(0, lastSpace > 170 ? lastSpace : 237).trim()}…`;
  };

  const uniqueVideoLinks = (section) => {
    const urls = new Set();
    section.querySelectorAll('iframe[src], video, a[href]').forEach((node) => {
      if (node.tagName === 'VIDEO') {
        urls.add(`local-video:${urls.size}`);
        return;
      }
      const raw = node.getAttribute(node.tagName === 'IFRAME' ? 'src' : 'href') || '';
      if (/youtube\.com|youtu\.be|vimeo\.com/i.test(raw)) urls.add(raw);
    });
    return urls.size;
  };

  const contentBadgesFor = (section) => {
    const galleryPhotos = section.querySelectorAll('.record-gallery__item').length;
    const documents = section.querySelectorAll('.inline-record').length;
    const videos = uniqueVideoLinks(section);
    const totalImages = section.querySelectorAll('img').length;
    const nonGalleryNonDocumentImages = Math.max(0, totalImages - galleryPhotos - documents);
    const badges = [];

    if (galleryPhotos) badges.push(galleryPhotos === 1 ? labels.photoOne : labels.photoMany(galleryPhotos));
    else if (nonGalleryNonDocumentImages) badges.push(nonGalleryNonDocumentImages === 1 ? labels.imageOne : labels.imageMany(nonGalleryNonDocumentImages));
    if (videos) badges.push(videos === 1 ? labels.videoOne : labels.videoMany(videos));
    if (documents) badges.push(documents === 1 ? labels.docOne : labels.docMany(documents));
    return badges;
  };

  const loadData = async () => {
    try {
      const [entryResponse, tagResponse] = await Promise.all([
        fetch('/data/entries.json', {cache: 'no-store'}),
        fetch('/data/tags.json', {cache: 'no-store'})
      ]);
      if (!entryResponse.ok || !tagResponse.ok) throw new Error('registry fetch failed');
      const [entryData, tagData] = await Promise.all([entryResponse.json(), tagResponse.json()]);
      return {entryData, tagData};
    } catch (error) {
      console.warn('Reader disclosure metadata unavailable; using structural fallback.', error);
      return {entryData: {entries: []}, tagData: {tags: []}};
    }
  };

  const run = async () => {
    const {entryData, tagData} = await loadData();
    const tags = new Map((tagData.tags || []).map((tag) => [tag.id, tag.label || {}]));
    const directEntries = [];
    const landmarks = [];

    (entryData.entries || []).forEach((entry) => {
      if (entry.kind === 'landmark-set') {
        (entry.landmarks?.[language] || []).forEach((landmark) => {
          if (landmark.path === repoPath) landmarks.push({entry, landmark});
        });
        return;
      }
      (entry.reader_targets?.[language] || []).forEach((target) => {
        if (target.path === repoPath) directEntries.push({entry, target});
      });
    });

    const fullBio = pagePath === '/pt/biografia/' || pagePath === '/en/biography/';
    const selector = fullBio ? 'section.chapter.bio-entry' : 'article.article-body > section.chapter';
    const chapters = [...document.querySelectorAll(selector)];
    if (!chapters.length) return;

    const metadataFor = (section) => {
      const hit = directEntries.find(({target}) => {
        try { return section.matches(target.selector); } catch (_) { return false; }
      });
      return hit?.entry || null;
    };

    const relatedFor = (section) => landmarks
      .filter(({landmark}) => {
        try { return section.matches(landmark.selector); } catch (_) { return false; }
      })
      .map(({entry}) => entry);

    document.documentElement.classList.add('reader-disclosure-active');
    const detailsForSection = new Map();

    chapters.forEach((section) => {
      const heading = [...section.children].find((node) => node.tagName === 'H2');
      if (!heading) return;
      const meta = [...section.children].find((node) => node.classList?.contains('bio-entry-meta')) || null;
      const entry = metadataFor(section);
      const related = relatedFor(section);
      const summaryText = entry?.summary?.[language] || excerptFor(section);
      const readerPreview = entry?.reader_preview?.[language] || null;
      const contentBadges = contentBadgesFor(section);
      const topicIds = entry?.topic_ids || [];
      const presentationState = entry?.reader_presentation?.state || 'normal';

      if (entry) section.dataset.entryId = entry.id;
      section.dataset.readerPresentation = presentationState;

      const details = document.createElement('details');
      details.className = `reader-disclosure reader-disclosure--${presentationState}`;
      if (presentationState === 'default-open') details.open = true;
      const summary = document.createElement('summary');
      summary.className = 'reader-disclosure__summary';

      if (meta) summary.appendChild(meta);
      summary.appendChild(heading);

      if (readerPreview?.paragraphs?.length) {
        const preview = document.createElement('span');
        preview.className = 'reader-disclosure__preview';

        if (readerPreview.image) {
          const media = document.createElement('span');
          media.className = 'reader-disclosure__preview-media';
          const image = document.createElement('img');
          image.src = readerPreview.image;
          image.alt = readerPreview.alt || '';
          image.loading = 'lazy';
          image.decoding = 'async';
          media.appendChild(image);
          preview.appendChild(media);
        }

        const copy = document.createElement('span');
        copy.className = 'reader-disclosure__preview-copy';
        readerPreview.paragraphs.forEach((text) => {
          const paragraph = document.createElement('span');
          paragraph.className = 'reader-disclosure__preview-paragraph';
          paragraph.textContent = text;
          copy.appendChild(paragraph);
        });
        preview.appendChild(copy);
        summary.appendChild(preview);
      } else if (summaryText) {
        const excerpt = document.createElement('p');
        excerpt.className = 'reader-disclosure__excerpt';
        excerpt.textContent = summaryText;
        summary.appendChild(excerpt);
      }

      if (topicIds.length) {
        const row = document.createElement('div');
        row.className = 'reader-disclosure__topics';
        topicIds.forEach((id) => {
          const label = tags.get(id)?.[language];
          if (!label) return;
          const chip = document.createElement('span');
          chip.className = 'reader-disclosure__topic';
          chip.textContent = label;
          row.appendChild(chip);
        });
        if (row.children.length) summary.appendChild(row);
      }

      const badges = [...contentBadges];
      if (entry?.chapter_page?.status === 'pilot') badges.push(labels.page);
      if (badges.length) {
        const row = document.createElement('div');
        row.className = 'reader-disclosure__badges';
        badges.forEach((text) => {
          const badge = document.createElement('span');
          badge.className = 'reader-disclosure__badge';
          badge.textContent = text;
          row.appendChild(badge);
        });
        summary.appendChild(row);
      }

      if (related.length) {
        const row = document.createElement('div');
        row.className = 'reader-disclosure__related';
        related.forEach((relatedEntry) => {
          const chip = document.createElement('span');
          chip.textContent = `${labels.related}: ${relatedEntry.title?.[language] || relatedEntry.id}`;
          row.appendChild(chip);
        });
        summary.appendChild(row);
      }

      const toggle = document.createElement('span');
      toggle.className = 'reader-disclosure__toggle';
      toggle.innerHTML = `<span class="reader-disclosure__toggle-open">${labels.open} ↓</span><span class="reader-disclosure__toggle-close">${labels.close} ↑</span>`;
      summary.appendChild(toggle);

      const body = document.createElement('div');
      body.className = 'reader-disclosure__body';
      while (section.firstChild) body.appendChild(section.firstChild);

      if (entry?.chapter_page?.status === 'pilot') {
        const rawPath = entry.chapter_page?.[`${language}_path`];
        if (rawPath) {
          const pageLink = document.createElement('p');
          pageLink.className = 'reader-disclosure__page-link';
          const anchor = document.createElement('a');
          anchor.href = `/${rawPath.replace(/index\.html$/, '')}`;
          anchor.textContent = labels.pageLink;
          pageLink.appendChild(anchor);
          body.insertBefore(pageLink, body.firstChild);
        }
      }

      const collapseRow = document.createElement('div');
      collapseRow.className = 'reader-disclosure__collapse-row';
      const collapseButton = document.createElement('button');
      collapseButton.type = 'button';
      collapseButton.className = 'reader-disclosure__collapse-button';
      collapseButton.textContent = `${labels.closeBottom} ↑`;
      collapseButton.addEventListener('click', () => {
        details.open = false;
        requestAnimationFrame(() => {
          summary.focus({preventScroll: true});
          section.scrollIntoView({block: 'start'});
        });
      });
      collapseRow.appendChild(collapseButton);
      body.appendChild(collapseRow);

      details.append(summary, body);
      section.appendChild(details);
      section.classList.add('reader-disclosure-chapter');
      detailsForSection.set(section, details);
    });

    const activeDetails = [...detailsForSection.values()];
    if (!activeDetails.length) return;

    const controls = document.createElement('div');
    controls.className = 'reader-disclosure-controls';
    controls.setAttribute('role', 'group');
    controls.setAttribute('aria-label', labels.mode);
    const controlLabel = document.createElement('span');
    controlLabel.className = 'reader-disclosure-controls__label';
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

    openAll.addEventListener('click', () => activeDetails.forEach((details) => { details.open = true; }));
    closeAll.addEventListener('click', () => activeDetails.forEach((details) => { details.open = false; }));

    const openContainingChapter = (target, scroll = false) => {
      if (!(target instanceof Element)) return false;
      const section = target.closest('section.chapter');
      if (!section) return false;
      const details = detailsForSection.get(section);
      if (!details) return false;
      details.open = true;
      if (scroll) requestAnimationFrame(() => section.scrollIntoView({block: 'start'}));
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
  };

  run();
})();
