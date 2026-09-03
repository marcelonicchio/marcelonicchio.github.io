(() => {
  const isPortuguese = document.documentElement.lang?.startsWith('pt');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobileViewport = window.matchMedia('(max-width: 580px)');

  const isImage = (href) => {
    try {
      const url = new URL(href, window.location.href);
      return /\.(?:avif|webp|png|jpe?g|gif)$/i.test(url.pathname);
    } catch (_) {
      return false;
    }
  };

  const galleries = [...document.querySelectorAll('[data-gallery]')];
  galleries.forEach((gallery) => {
    const strip = gallery.querySelector('[data-gallery-strip]');
    const prev = gallery.querySelector('[data-gallery-prev]');
    const next = gallery.querySelector('[data-gallery-next]');
    if (!strip || !prev || !next) return;

    const updateControls = () => {
      const overflow = strip.scrollWidth > strip.clientWidth + 2;
      const showArrows = overflow && !mobileViewport.matches;
      prev.hidden = !showArrows;
      next.hidden = !showArrows;
      if (!showArrows) return;
      prev.disabled = strip.scrollLeft <= 2;
      next.disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 2;
    };

    const scrollByPage = (direction) => {
      strip.scrollBy({
        left: direction * Math.max(strip.clientWidth * 0.78, 220),
        behavior: reducedMotion.matches ? 'auto' : 'smooth'
      });
    };

    prev.addEventListener('click', () => scrollByPage(-1));
    next.addEventListener('click', () => scrollByPage(1));
    strip.addEventListener('scroll', updateControls, {passive: true});
    window.addEventListener('resize', updateControls);
    mobileViewport.addEventListener?.('change', updateControls);
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(updateControls);
      observer.observe(strip);
      gallery.__mnGalleryResizeObserver = observer;
    }
    requestAnimationFrame(updateControls);
  });

  const links = [...document.querySelectorAll('a.inline-record, a.record-gallery__item')].filter((link) => isImage(link.href));
  if (!links.length) return;

  // The hidden lightbox image exists from initial page load. Seed it with a
  // valid intrinsic ratio from the first thumbnail, then update that ratio for
  // each opened item. This keeps every runtime image dimensionally explicit.
  const initialThumb = links[0].querySelector('img');
  const initialWidth = Number(initialThumb?.getAttribute('width')) || 1;
  const initialHeight = Number(initialThumb?.getAttribute('height')) || 1;

  const lightbox = document.createElement('div');
  lightbox.className = 'archive-lightbox';
  lightbox.hidden = true;
  lightbox.setAttribute('aria-hidden', 'true');
  lightbox.innerHTML = `
    <div class="archive-lightbox__panel" role="dialog" aria-modal="true" aria-label="${isPortuguese ? 'Visualização ampliada' : 'Enlarged view'}">
      <button class="archive-lightbox__close" type="button" aria-label="${isPortuguese ? 'Fechar' : 'Close'}">×</button>
      <button class="archive-lightbox__nav archive-lightbox__nav--prev" type="button" aria-label="${isPortuguese ? 'Imagem anterior' : 'Previous image'}" hidden>‹</button>
      <img class="archive-lightbox__image" alt="" width="${initialWidth}" height="${initialHeight}">
      <button class="archive-lightbox__nav archive-lightbox__nav--next" type="button" aria-label="${isPortuguese ? 'Próxima imagem' : 'Next image'}" hidden>›</button>
      <div class="archive-lightbox__meta">
        <div class="archive-lightbox__caption"></div>
        <div class="archive-lightbox__counter" aria-live="polite"></div>
      </div>
    </div>`;
  document.body.appendChild(lightbox);

  const image = lightbox.querySelector('.archive-lightbox__image');
  const caption = lightbox.querySelector('.archive-lightbox__caption');
  const counter = lightbox.querySelector('.archive-lightbox__counter');
  const closeButton = lightbox.querySelector('.archive-lightbox__close');
  const prevButton = lightbox.querySelector('.archive-lightbox__nav--prev');
  const nextButton = lightbox.querySelector('.archive-lightbox__nav--next');
  let returnFocus = null;
  let activeItems = [];
  let activeIndex = 0;

  const getCaption = (link) => {
    const thumb = link.querySelector('img');
    return link.dataset.caption?.trim() || link.querySelector('strong')?.textContent?.trim() || thumb?.alt || '';
  };

  const render = () => {
    const link = activeItems[activeIndex];
    if (!link) return;
    const thumb = link.querySelector('img');
    const thumbWidth = Number(thumb?.getAttribute('width')) || thumb?.naturalWidth || 1;
    const thumbHeight = Number(thumb?.getAttribute('height')) || thumb?.naturalHeight || 1;
    image.width = thumbWidth;
    image.height = thumbHeight;
    image.src = link.href;
    image.alt = thumb?.alt || '';
    caption.textContent = getCaption(link);
    const multiple = activeItems.length > 1;
    counter.textContent = multiple ? `${activeIndex + 1} / ${activeItems.length}` : '';
    prevButton.hidden = !multiple;
    nextButton.hidden = !multiple;
    prevButton.disabled = !multiple || activeIndex === 0;
    nextButton.disabled = !multiple || activeIndex === activeItems.length - 1;
  };

  const close = () => {
    if (lightbox.hidden) return;
    lightbox.hidden = true;
    lightbox.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('archive-lightbox-open');
    image.removeAttribute('src');
    activeItems = [];
    activeIndex = 0;
    if (returnFocus) returnFocus.focus({preventScroll: true});
  };

  const open = (link) => {
    returnFocus = link;
    const gallery = link.closest('[data-gallery]');
    if (gallery && link.classList.contains('record-gallery__item')) {
      activeItems = [...gallery.querySelectorAll('a.record-gallery__item')].filter((item) => isImage(item.href));
      activeIndex = Math.max(0, activeItems.indexOf(link));
    } else {
      activeItems = [link];
      activeIndex = 0;
    }
    render();
    lightbox.hidden = false;
    lightbox.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('archive-lightbox-open');
    closeButton.focus({preventScroll: true});
  };

  const navigate = (delta) => {
    const nextIndex = activeIndex + delta;
    if (nextIndex < 0 || nextIndex >= activeItems.length) return;
    activeIndex = nextIndex;
    render();
  };

  links.forEach((link) => {
    if (link.classList.contains('inline-record')) {
      const helper = link.querySelector('small');
      if (helper) helper.textContent = isPortuguese ? 'Clique para ampliar' : 'Click to enlarge';
    }
    link.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      open(link);
    });
  });

  closeButton.addEventListener('click', close);
  prevButton.addEventListener('click', () => navigate(-1));
  nextButton.addEventListener('click', () => navigate(1));
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) close();
  });

  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) return;
    if (event.key === 'Escape') {
      close();
      return;
    }
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      navigate(-1);
      return;
    }
    if (event.key === 'ArrowRight') {
      event.preventDefault();
      navigate(1);
      return;
    }
    if (event.key === 'Home' && activeItems.length > 1) {
      event.preventDefault();
      activeIndex = 0;
      render();
      return;
    }
    if (event.key === 'End' && activeItems.length > 1) {
      event.preventDefault();
      activeIndex = activeItems.length - 1;
      render();
      return;
    }
    if (event.key === 'Tab') {
      const focusable = [closeButton, prevButton, nextButton].filter((button) => !button.hidden && !button.disabled);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
})();
