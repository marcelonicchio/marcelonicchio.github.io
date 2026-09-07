(() => {
  const injectStandaloneBiographyEntry = () => {
    const path = window.location.pathname;
    const config = path === '/pt/biografia/'
      ? {
          domain: 'Biografia',
          href: '/pt/biografia/the-more-you-change-the-less-you-feel/',
          body: 'Em 2006, Marcelo Nicchio reuniu registros pessoais em VHS e outras mídias domésticas digitalizadas naquele período e montou <em>The More You Change, The Less You Feel</em>, um vídeo-memorial autobiográfico cobrindo aproximadamente 1980–2006.',
          cta: 'Conhecer a história e assistir →'
        }
      : path === '/en/biography/'
        ? {
            domain: 'Biography',
            href: '/en/biography/the-more-you-change-the-less-you-feel/',
            body: 'In 2006, Marcelo Nicchio assembled personal VHS recordings and other domestic media digitized at the time into <em>The More You Change, The Less You Feel</em>, an autobiographical memorial video spanning approximately 1980–2006.',
            cta: 'Read the story and watch →'
          }
        : null;

    if (!config || document.querySelector('[data-bio-standalone-entry="video-memorial-2006"]')) return;

    const previous = document.getElementById('bio-audiovisual-meia-noite');
    const next = document.getElementById('bio-spirituality-seeker');
    if (!previous || !next || previous.parentNode !== next.parentNode) return;

    const entry = document.createElement('section');
    entry.id = 'bio-video-memorial-2006';
    entry.className = 'chapter bio-entry';
    entry.dataset.bioStandaloneEntry = 'video-memorial-2006';
    entry.dataset.bioDomain = 'context';
    entry.innerHTML = `
      <div class="bio-entry-meta"><span>2006</span><span>${config.domain}</span></div>
      <h2><a class="entry-title-permalink" href="${config.href}"><em>The More You Change, The Less You Feel</em></a></h2>
      <p>${config.body}</p>
      <div class="evidence-links inline-links"><a href="${config.href}">${config.cta}</a></div>
    `;
    next.before(entry);
  };

  injectStandaloneBiographyEntry();

  const MOBILE_QUERY = '(max-width: 820px)';
  const media = window.matchMedia(MOBILE_QUERY);
  const headers = [...document.querySelectorAll('.site-header')];
  if (!headers.length) return;

  const setups = [];

  const close = (setup, { focusToggle = false } = {}) => {
    const { nav, toggle, links } = setup;
    nav.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
    links.hidden = media.matches;
    if (focusToggle) toggle.focus();
  };

  const open = (setup) => {
    const { nav, toggle, links } = setup;
    nav.classList.add('nav-open');
    toggle.setAttribute('aria-expanded', 'true');
    links.hidden = false;
  };

  const syncMode = (setup) => {
    const { nav, toggle, links } = setup;
    if (media.matches) {
      nav.classList.add('mobile-nav-enhanced');
      toggle.hidden = false;
      close(setup);
    } else {
      nav.classList.remove('mobile-nav-enhanced', 'nav-open');
      toggle.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      links.hidden = false;
    }
  };

  headers.forEach((header) => {
    const nav = header.querySelector('.nav');
    const links = nav?.querySelector('.nav-links');
    if (!nav || !links) return;

    if (!links.id) links.id = 'primary-navigation';

    let toggle = nav.querySelector('.nav-toggle');
    if (!toggle) {
      const isPortuguese = document.documentElement.lang.toLowerCase().startsWith('pt');
      const toggleLabel = isPortuguese ? 'Categorias' : 'Categories';
      toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'nav-toggle';
      toggle.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-controls', links.id);
      toggle.setAttribute('aria-label', isPortuguese ? 'Abrir categorias de navegação' : 'Open navigation categories');
      toggle.innerHTML = `<span aria-hidden="true" class="nav-toggle__icon"><i></i><i></i><i></i></span><span>${toggleLabel}</span>`;
      nav.insertBefore(toggle, links);
    }

    const setup = { header, nav, toggle, links };
    setups.push(setup);

    toggle.addEventListener('click', () => {
      if (toggle.getAttribute('aria-expanded') === 'true') close(setup);
      else open(setup);
    });

    links.addEventListener('click', (event) => {
      if (media.matches && event.target.closest('a')) close(setup);
    });

    syncMode(setup);
  });

  const handleModeChange = () => setups.forEach(syncMode);
  if (typeof media.addEventListener === 'function') media.addEventListener('change', handleModeChange);
  else media.addListener(handleModeChange);

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    setups.forEach((setup) => {
      if (setup.toggle.getAttribute('aria-expanded') === 'true') close(setup, { focusToggle: true });
    });
  });

  document.addEventListener('click', (event) => {
    if (!media.matches) return;
    setups.forEach((setup) => {
      if (setup.toggle.getAttribute('aria-expanded') === 'true' && !setup.header.contains(event.target)) close(setup);
    });
  });
})();
