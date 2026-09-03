(() => {
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
      toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'nav-toggle';
      toggle.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-controls', links.id);
      toggle.setAttribute('aria-label', document.documentElement.lang.toLowerCase().startsWith('pt') ? 'Abrir menu principal' : 'Open main menu');
      toggle.innerHTML = '<span aria-hidden="true" class="nav-toggle__icon"><i></i><i></i><i></i></span><span>Menu</span>';
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
