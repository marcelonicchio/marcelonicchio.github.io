(() => {
  const section = document.querySelector('[data-root-video]');
  if (!section) return;

  const frame = section.querySelector('[data-root-video-frame]');
  const videoId = section.getAttribute('data-youtube-id');
  if (!frame || !videoId) return;

  if (window.location.pathname === '/') {
    const actions = section.querySelector('.root-video-actions');
    if (actions && !actions.querySelector('[data-root-video-story-link]')) {
      const storyPt = document.createElement('a');
      storyPt.href = '/pt/biografia/the-more-you-change-the-less-you-feel/';
      storyPt.dataset.rootLang = 'pt';
      storyPt.dataset.rootVideoStoryLink = '';
      storyPt.textContent = 'Conhecer a história deste vídeo →';

      const storyEn = document.createElement('a');
      storyEn.href = '/en/biography/the-more-you-change-the-less-you-feel/';
      storyEn.dataset.rootLang = 'en';
      storyEn.dataset.rootVideoStoryLink = '';
      storyEn.textContent = 'About this video →';

      actions.prepend(storyEn);
      actions.prepend(storyPt);
    }
  }

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
