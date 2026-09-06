(() => {
  const KEY = 'mn-root-language';
  const normalize = (value) => String(value || '').toLowerCase().startsWith('pt') ? 'pt' : 'en';

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
