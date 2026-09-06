(() => {
  const KEY = 'mn-root-language';
  const ZENODO_URL = 'https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Nicchio%2C%20Marcelo%22&l=list&p=1&s=10&sort=bestmatch';
  const RESEARCH_ORDER = [
    'https://orcid.org/0009-0002-5626-8973',
    'https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=11881088',
    'https://osf.io/user/b4y7r',
    ZENODO_URL,
    'https://independent.academia.edu/MarceloNicchio',
    'https://cv.hal.science/marcelonicchio',
    'https://www.pubpub.org/user/marcelo-nicchio'
  ];
  const normalize = (value) => String(value || '').toLowerCase().startsWith('pt') ? 'pt' : 'en';
  const absolute = (value) => {
    try { return new URL(value, window.location.href).href; }
    catch (_) { return String(value || ''); }
  };

  function syncResearchPresence() {
    const links = document.querySelector('.root-presence-groups > .root-presence-group:first-child .root-presence-links');
    if (!links) return;

    let zenodo = Array.from(links.querySelectorAll('a.presence-link')).find((link) => absolute(link.getAttribute('href')) === absolute(ZENODO_URL));
    if (!zenodo) {
      zenodo = document.createElement('a');
      zenodo.className = 'presence-link root-zenodo-link';
      zenodo.href = ZENODO_URL;
      zenodo.target = '_blank';
      zenodo.rel = 'noopener noreferrer';
      zenodo.dataset.label = 'Zenodo';
      zenodo.setAttribute('aria-label', 'Zenodo — opens in a new tab');
      zenodo.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M7 7h10L7 17h10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Zenodo</span>';
      links.appendChild(zenodo);
    }

    const current = Array.from(links.querySelectorAll('a.presence-link'));
    RESEARCH_ORDER.forEach((url) => {
      const match = current.find((link) => absolute(link.getAttribute('href')) === absolute(url));
      if (match) links.appendChild(match);
    });
  }

  function applyLanguage(language, persist = true) {
    const lang = normalize(language);
    document.documentElement.dataset.rootLanguage = lang;
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : 'en';

    document.querySelectorAll('[data-root-lang-choice]').forEach((button) => {
      const active = button.dataset.rootLangChoice === lang;
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
      button.classList.toggle('is-active', active);
    });

    const title = document.querySelector(`meta[data-root-title-${lang}]`);
    const description = document.querySelector(`meta[data-root-description-${lang}]`);
    if (title) document.title = title.getAttribute('content') || document.title;
    if (description) {
      const meta = document.querySelector('meta[name="description"]');
      if (meta) meta.setAttribute('content', description.getAttribute('content') || meta.getAttribute('content') || '');
    }

    if (persist) {
      try { localStorage.setItem(KEY, lang); } catch (_) {}
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    syncResearchPresence();

    document.querySelectorAll('[data-root-lang-choice]').forEach((button) => {
      button.addEventListener('click', () => applyLanguage(button.dataset.rootLangChoice));
    });

    let initial = document.documentElement.dataset.rootLanguage || 'en';
    try {
      initial = localStorage.getItem(KEY) || initial;
    } catch (_) {}
    applyLanguage(initial, false);
  });
})();
