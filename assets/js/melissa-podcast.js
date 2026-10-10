/* Melissa 1.0 audio library.
   Add/remove episodes exclusively in /data/melissa-podcasts.json.
   Scoped to the Melissa vertical entry and its standalone Chapter Pages.
   Audio isn't loaded or played before the visitor chooses it. */
(() => {
  'use strict';
  // Place immediately after Melissa's portrait (including its caption),
  // not after the date. Both pages render the same neutral editorial fragment.
  const vertical = document.querySelector('body.vertical-ai #melissa > figure.melissa-selfportrait');
  const chapter = document.querySelector('main[data-entry-id="hai-melissa"] article.entry-page-body > figure.melissa-selfportrait');
  const anchor = vertical || chapter;
  if (!anchor || document.querySelector('[data-melissa-podcasts]')) return;

  const siteLang = document.documentElement.lang.toLowerCase().startsWith('en') ? 'en' : 'pt';
  const text = {
    pt: {
      heading: 'Ouça os podcasts',
      chooser: 'Escolha o episódio',
      link: 'Ouvir no SoundCloud ↗',
      note: 'Áudio em português',
      unavailable: 'Não foi possível carregar os episódios. Tente atualizar a página.'
    },
    en: {
      heading: 'Listen to the podcasts',
      chooser: 'Choose an episode',
      link: 'Listen on SoundCloud ↗',
      note: 'Currently available in Portuguese',
      unavailable: 'Unable to load the episodes. Please refresh the page.'
    }
  }[siteLang];

  function element(tag, cls, label) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (label) node.textContent = label;
    return node;
  }

  function validSoundCloud(value) {
    try {
      const u = new URL(value);
      return u.protocol === 'https:' &&
        (u.hostname === 'soundcloud.com' || u.hostname === 'www.soundcloud.com') &&
        u.pathname.split('/').filter(Boolean).length >= 2;
    } catch (_) {
      return false;
    }
  }

  function playerUrl(trackUrl) {
    return 'https://w.soundcloud.com/player/?' + new URLSearchParams({
      url: trackUrl,
      color: '#ff625c',
      auto_play: 'false',
      visual: 'false',
      show_artwork: 'true',
      show_comments: 'false',
      show_user: 'true',
      show_reposts: 'false',
      show_teaser: 'false',
      single_active: 'true'
    }).toString();
  }

  async function start() {
    const response = await fetch('/data/melissa-podcasts.json', {cache: 'no-store'});
    if (!response.ok) throw new Error('Melissa podcast manifest unavailable');
    const data = await response.json();
    if (data.entry_id !== 'hai-melissa' || !Array.isArray(data.episodes)) return;
    const tracks = data.episodes.filter(ep =>
      ep && typeof ep.id === 'string' && /^[a-z0-9-]+$/.test(ep.id) &&
      (ep.language === 'pt' || ep.language === 'en') &&
      typeof ep.title === 'string' && ep.title.trim() &&
      typeof ep.soundcloud_url === 'string' && validSoundCloud(ep.soundcloud_url)
    );
    if (!tracks.length || new Set(tracks.map(ep => ep.id)).size !== tracks.length) return;

    const section = element('section', 'research-podcast research-podcast--library');
    section.setAttribute('data-melissa-podcasts', '');
    section.setAttribute('aria-label', text.heading);
    const head = element('div', 'research-podcast__header');
    head.append(element('div', 'research-podcast__eyebrow', text.heading));
    const group = element('div', 'melissa-podcast__choices');
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', text.chooser);
    const buttons = [];

    const players = element('div', 'melissa-podcast__player');
    const title = element('p', 'research-podcast__title');
    const iframe = document.createElement('iframe');
    iframe.setAttribute('data-podcast-player', '');
    iframe.setAttribute('width', '100%');
    iframe.setAttribute('height', '166');
    iframe.setAttribute('loading', 'lazy');
    iframe.setAttribute('scrolling', 'no');
    iframe.setAttribute('allow', 'autoplay; encrypted-media');
    iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
    const outbound = element('a', 'research-podcast__link', text.link);
    outbound.target = '_blank';
    outbound.rel = 'noopener noreferrer';
    players.append(title, iframe, outbound);

    const languageCount = {pt:0, en:0};
    const choose = (episode) => {
      for (const {button, ep} of buttons) {
        button.setAttribute('aria-pressed', String(ep.id === episode.id));
      }
      title.textContent = episode.title;
      outbound.href = episode.soundcloud_url;
      iframe.title = episode.title + ' — SoundCloud';
      // One iframe: replacing src stops playback of the previous episode.
      iframe.src = playerUrl(episode.soundcloud_url);
    };

    for (const ep of tracks) {
      languageCount[ep.language] += 1;
      const flag = ep.language === 'pt' ? '🇧🇷' : '🇺🇸';
      const langLabel = ep.language === 'pt' ? 'Português' : 'English';
      const button = element('button', 'melissa-podcast__choice');
      button.type = 'button';
      button.setAttribute('aria-pressed', 'false');
      button.append(
        element('span', 'melissa-podcast__language', flag + ' ' + langLabel + ' · ' + languageCount[ep.language]),
        element('span', 'melissa-podcast__episode-title', ep.title)
      );
      button.addEventListener('click', () => choose(ep));
      buttons.push({button, ep});
      group.append(button);
    }

    section.append(head, group);
    if (siteLang === 'en' && languageCount.en === 0) {
      section.append(element('p', 'melissa-podcast__note', text.note));
    }
    section.append(players);
    anchor.insertAdjacentElement('afterend', section);

    // Default to the language of the page when available; otherwise the first episode.
    const initial = tracks.find(ep => ep.language === siteLang) || tracks[0];
    choose(initial);
  }

  start().catch((error) => {
    console.warn('Melissa podcast library unavailable:', error);
    // The editorial text remains readable if SoundCloud metadata is unavailable.
  });
})();
