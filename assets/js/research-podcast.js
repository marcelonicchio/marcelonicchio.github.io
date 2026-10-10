/* Research podcast SoundCloud embed: one iframe, two language tabs.
   The renderer supplies data-soundcloud-pt / -en, titles, and default language.
   Missing/invalid track URLs hide the widget instead of showing broken embeds. */
(() => {
  'use strict';
  const labels = { pt: 'Português', en: 'English' };
  function validTrackUrl(value) {
    try {
      const parsed = new URL(value);
      return parsed.protocol === 'https:' &&
        (parsed.hostname === 'soundcloud.com' || parsed.hostname === 'www.soundcloud.com') &&
        parsed.pathname.split('/').filter(Boolean).length >= 2;
    } catch (_error) {
      return false;
    }
  }
  function widgetUrl(trackUrl) {
    const params = new URLSearchParams({
      url: trackUrl, color: '#ff625c', auto_play: 'false',
      visual: 'false', show_artwork: 'true', show_comments: 'false',
      show_user: 'true', single_active: 'true'
    });
    return 'https://w.soundcloud.com/player/?' + params.toString();
  }
  function init(section) {
    const tracks = {
      pt: { url: section.dataset.soundcloudPt, title: section.dataset.soundcloudPtTitle },
      en: { url: section.dataset.soundcloudEn, title: section.dataset.soundcloudEnTitle }
    };
    if (!validTrackUrl(tracks.pt.url) || !validTrackUrl(tracks.en.url)) {
      section.hidden = true;
      return;
    }
    const buttons = Array.from(section.querySelectorAll('[data-podcast-lang]'));
    const iframe = section.querySelector('iframe[data-podcast-player]');
    const heading = section.querySelector('[data-podcast-title]');
    const link = section.querySelector('[data-podcast-link]');
    if (!iframe || buttons.length !== 2 || !heading || !link) return;
    function choose(lang) {
      const selected = tracks[lang];
      if (!selected) return;
      buttons.forEach((button) => {
        const active = button.dataset.podcastLang === lang;
        button.setAttribute('aria-selected', String(active));
        button.tabIndex = active ? 0 : -1;
      });
      heading.textContent = selected.title || 'Podcast — ' + labels[lang];
      link.href = selected.url;
      link.textContent = lang === 'pt' ? 'Ouvir no SoundCloud ↗' : 'Listen on SoundCloud ↗';
      iframe.title = heading.textContent + ' — SoundCloud';
      /* Navigating the only iframe stops the previous language's audio. */
      iframe.src = widgetUrl(selected.url);
    }
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => choose(button.dataset.podcastLang));
      button.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        if (event.key === 'ArrowLeft') next = (index + buttons.length - 1) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        buttons[next].focus();
        choose(buttons[next].dataset.podcastLang);
      });
    });
    section.classList.add('research-podcast--ready');
    choose(section.dataset.defaultLang === 'en' ? 'en' : 'pt');
  }
  document.querySelectorAll('[data-research-podcast]').forEach(init);
})();
