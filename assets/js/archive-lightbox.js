(() => {
  const links = [...document.querySelectorAll('a.inline-record')];
  if (!links.length) return;

  const isImage = (href) => {
    try {
      const url = new URL(href, window.location.href);
      return /\.(?:avif|webp|png|jpe?g|gif)$/i.test(url.pathname);
    } catch (_) {
      return false;
    }
  };

  const lightbox = document.createElement('div');
  lightbox.className = 'archive-lightbox';
  lightbox.hidden = true;
  lightbox.setAttribute('aria-hidden', 'true');
  lightbox.innerHTML = `
    <div class="archive-lightbox__panel" role="dialog" aria-modal="true" aria-label="Visualização ampliada / Enlarged view">
      <button class="archive-lightbox__close" type="button" aria-label="Fechar / Close">×</button>
      <img class="archive-lightbox__image" alt="">
      <div class="archive-lightbox__caption"></div>
    </div>`;
  document.body.appendChild(lightbox);

  const image = lightbox.querySelector('.archive-lightbox__image');
  const caption = lightbox.querySelector('.archive-lightbox__caption');
  const closeButton = lightbox.querySelector('.archive-lightbox__close');
  let returnFocus = null;

  const close = () => {
    if (lightbox.hidden) return;
    lightbox.hidden = true;
    lightbox.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('archive-lightbox-open');
    image.removeAttribute('src');
    if (returnFocus) returnFocus.focus({preventScroll: true});
  };

  const open = (link) => {
    returnFocus = link;
    image.src = link.href;
    const thumb = link.querySelector('img');
    image.alt = thumb?.alt || '';
    caption.textContent = link.querySelector('strong')?.textContent?.trim() || thumb?.alt || '';
    lightbox.hidden = false;
    lightbox.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('archive-lightbox-open');
    closeButton.focus({preventScroll: true});
  };

  links.forEach((link) => {
    if (!isImage(link.href)) return;
    const helper = link.querySelector('small');
    if (helper) helper.textContent = document.documentElement.lang?.startsWith('pt') ? 'Clique para ampliar' : 'Click to enlarge';
    link.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      open(link);
    });
  });

  closeButton.addEventListener('click', close);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) close();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') close();
  });
})();
