/* PRO v1 research podcast: one official SoundCloud player with PT/EN switching.
   Render only on the HCI/HAI vertical chapter and standalone chapter page.
   The neutral entry fragment and generated Full Biography remain untouched. */
(() => {
  'use strict';
  const EPISODES = {
    pt: {
      url: 'https://soundcloud.com/marcelonicchio/a-ia-como-maquina-de-hesitar',
      title: 'A IA como "Máquina de Hesitar" (PRO v1)'
    },
    en: {
      url: 'https://soundcloud.com/marcelonicchio/punk-rock-orchestra-one',
      title: 'Punk Rock Orchestra: One Researcher. Many AI Critics. No Easy Answers.'
    }
  };
  const SITE_LANG = document.documentElement.lang.toLowerCase().startsWith('en') ? 'en' : 'pt';
  const CSS_CLASS = 'research-podcast';
  const LABELS = {
    pt: { kicker: 'Ouça o podcast', outbound: 'Ouvir no SoundCloud ↗', pt: 'Português', en: 'English' },
    en: { kicker: 'Listen to the podcast', outbound: 'Listen on SoundCloud ↗', pt: 'Português', en: 'English' }
  };

  function widgetUrl(trackUrl) {
    const params = new URLSearchParams({
      url: trackUrl, color: '#ff625c', auto_play: 'false', visual: 'false',
      show_artwork: 'true', show_comments: 'false', show_user: 'true',
      show_reposts: 'false', show_teaser: 'false', single_active: 'true'
    });
    return 'https://w.soundcloud.com/player/?' + params.toString();
  }

  function make(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function mount(anchor) {
    if (anchor.parentNode.querySelector('[data-research-podcast]')) return;
    const labels = LABELS[SITE_LANG];
    const section = make('section', CSS_CLASS);
    section.setAttribute('data-research-podcast', '');
    section.setAttribute('aria-label', labels.kicker);

    const header = make('div', CSS_CLASS + '__header');
    const kicker = make('div', CSS_CLASS + '__eyebrow', labels.kicker);
    const tabs = make('div', CSS_CLASS + '__tabs');
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', SITE_LANG === 'pt' ? 'Idioma do podcast' : 'Podcast language');
    const controls = {};
    for (const lang of ['pt', 'en']) {
      const button = make('button', '', (lang === 'pt' ? '🇧🇷 ' : '🇺🇸 ') + labels[lang]);
      button.type = 'button';
      button.dataset.podcastLang = lang;
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-selected', 'false');
      tabs.appendChild(button);
      controls[lang] = button;
    }
    header.append(kicker, tabs);

    const title = make('p', CSS_CLASS + '__title');
    title.setAttribute('data-podcast-title', '');
    const frame = document.createElement('iframe');
    frame.setAttribute('data-podcast-player', '');
    frame.setAttribute('width', '100%');
    frame.setAttribute('height', '166');
    frame.setAttribute('scrolling', 'no');
    frame.setAttribute('loading', 'lazy');
    frame.setAttribute('allow', 'autoplay; encrypted-media');
    frame.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
    frame.setAttribute('aria-label', labels.kicker);

    const outbound = make('a', CSS_CLASS + '__link');
    outbound.setAttribute('data-podcast-link', '');
    outbound.target = '_blank';
    outbound.rel = 'noopener noreferrer';
    section.append(header, title, frame, outbound);
    anchor.insertAdjacentElement('afterend', section);

    const buttons = [controls.pt, controls.en];
    function select(lang) {
      const chosen = EPISODES[lang];
      for (const [buttonLang, button] of Object.entries(controls)) {
        const active = buttonLang === lang;
        button.setAttribute('aria-selected', String(active));
        button.tabIndex = active ? 0 : -1;
      }
      title.textContent = chosen.title;
      outbound.href = chosen.url;
      outbound.textContent = labels.outbound;
      frame.title = chosen.title + ' — SoundCloud';
      /* Replacing src of the same iframe terminates the previous track. */
      frame.src = widgetUrl(chosen.url);
    }
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => select(button.dataset.podcastLang));
      button.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        if (event.key === 'ArrowLeft') next = (index + buttons.length - 1) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        buttons[next].focus();
        select(buttons[next].dataset.podcastLang);
      });
    });
    select(SITE_LANG);
  }

  // The year and heading stay first. The audio follows the date, before prose.
  const vertical = document.querySelector('body.vertical-ai #pro1 > p.meta');
  const chapter = document.querySelector('main[data-entry-id="hai-pro1"] article.entry-page-body > p.meta');
  if (vertical) mount(vertical);
  if (chapter) mount(chapter);
})();
