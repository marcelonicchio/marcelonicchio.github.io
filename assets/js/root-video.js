(() => {
  const section = document.querySelector('[data-root-video]');
  if (!section) return;

  const frame = section.querySelector('[data-root-video-frame]');
  const videoId = section.getAttribute('data-youtube-id');
  if (!frame || !videoId) return;

  const loadPlayer = () => {
    if (frame.dataset.loaded === 'true') return;
    frame.dataset.loaded = 'true';

    const lang = document.documentElement.dataset.rootLanguage === 'pt' ? 'pt' : 'en';
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(videoId)}?autoplay=1&rel=0`;
    iframe.title = lang === 'pt'
      ? 'The More You Change, The Less You Feel — vídeo de Marcelo Nicchio'
      : 'The More You Change, The Less You Feel — video by Marcelo Nicchio';
    iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.allowFullscreen = true;

    frame.replaceChildren(iframe);
    iframe.focus();
  };

  section.querySelectorAll('[data-root-video-play]').forEach((button) => {
    button.addEventListener('click', loadPlayer);
  });
})();
