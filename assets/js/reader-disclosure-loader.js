(() => {
  const params = new URLSearchParams(window.location.search);
  const pagePath = window.location.pathname;

  const defaultSupported = new Set([
    '/pt/biografia/', '/en/biography/',
    '/pt/internet/', '/en/internet/',
    '/pt/ia-hai/', '/en/ai-hai/'
  ]);
  const pilotSupported = new Set([
    ...defaultSupported,
    '/pt/comunicacao/', '/en/communication/',
    '/pt/audiovisual/', '/en/audiovisual/'
  ]);

  const requestedPilot = params.get('ux') === 'disclosure';
  if (!defaultSupported.has(pagePath) && !(requestedPilot && pilotSupported.has(pagePath))) return;
  if (window.__mnReaderDisclosureRequested) return;
  window.__mnReaderDisclosureRequested = true;

  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = '/assets/reader-disclosure.css?v=20260901-reader6';
  css.dataset.readerDisclosure = 'style';
  document.head.appendChild(css);

  const script = document.createElement('script');
  script.src = '/assets/js/reader-disclosure.js?v=20260901-reader6';
  script.defer = true;
  script.dataset.readerDisclosure = 'script';
  document.head.appendChild(script);
})();
