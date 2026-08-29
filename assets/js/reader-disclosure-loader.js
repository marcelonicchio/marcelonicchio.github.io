(() => {
  const params = new URLSearchParams(window.location.search);
  if (params.get('ux') !== 'disclosure') return;

  const supported = new Set([
    '/pt/biografia/', '/en/biography/',
    '/pt/internet/', '/en/internet/',
    '/pt/comunicacao/', '/en/communication/',
    '/pt/audiovisual/', '/en/audiovisual/'
  ]);
  if (!supported.has(window.location.pathname)) return;
  if (window.__mnReaderDisclosureRequested) return;
  window.__mnReaderDisclosureRequested = true;

  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = '/assets/reader-disclosure.css';
  css.dataset.readerDisclosure = 'style';
  document.head.appendChild(css);

  const script = document.createElement('script');
  script.src = '/assets/js/reader-disclosure.js';
  script.defer = true;
  script.dataset.readerDisclosure = 'script';
  document.head.appendChild(script);
})();
