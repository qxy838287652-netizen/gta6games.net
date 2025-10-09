/**
 * News Navigation: Previous/Next links generator
 * Keeps an ordered list of news by date (desc). On each news page, renders prev/next.
 */
(function(){
  const NEWS_ORDER = [
    // 2025-10
    "gta6-community-mod-showcase.html",         // 2025-10-09 (Community)
    "gta6-roleplay-server-vicecity.html",       // 2025-10-09 (Community)
    "gta6-speedrun-record-broken.html",         // 2025-10-08 (Community)
    "gta6-photo-contest-winners.html",          // 2025-10-07 (Community)
    "gta6-modded-car-meet.html",                // 2025-10-06 (Community)
    "gta6-official-site-update.html",           // 2025-10-09
    "gta6-cross-progression-and-cloud-saves.html", // 2025-10-08
    "gta6-photo-mode-and-social-sharing.html",  // 2025-10-07
    "gta6-dynamic-weather-and-events.html",     // 2025-10-06
    "gta6-pc-features-and-mod-policy.html",     // 2025-10-05
    // 2025-09
    "gta6-preorders-and-editions.html",         // 2025-09-24
    "gta6-trailer-2-october-rumor.html",        // 2025-09-23
    "gta6-soundtrack-ai-radio.html",            // 2025-09-22
    "gta6-performance-targets.html",            // 2025-09-21
    "gta6-ai-npc-system.html",                  // 2025-09-20
    "gta6-map-size-expansion.html",             // 2025-09-19
    "gta6-further-delay-2026.html",             // 2025-09-18
    "gta6-largest-launch.html",                 // 2025-09-17
    "gta6-advanced-destruction.html",           // 2025-09-16
    "gta6-delay-2026.html",                     // 2025-09-15
    "gta6-dual-protagonists.html",              // 2025-09-14
    "gta6-online-100players.html",              // 2025-09-13
    "gta6-vice-city-return.html",               // 2025-09-12
    "gta6-graphics-leak.html",                  // 2025-09-11
    "gta6-preorder-bonus.html"                  // 2025-09-10
  ];

  function getCurrentSlug() {
    try {
      const href = window.location.href.split('#')[0].split('?')[0];
      const slug = href.substring(href.lastIndexOf('/') + 1);
      return slug || '';
    } catch { return ''; }
  }

  function renderNav() {
    const slug = getCurrentSlug();
    const idx = NEWS_ORDER.indexOf(slug);
    if (idx === -1) return;

    const prevSlug = NEWS_ORDER[idx - 1] || null; // newer
    const nextSlug = NEWS_ORDER[idx + 1] || null; // older
    const wrapper = document.createElement('div');
    wrapper.className = 'flex items-center justify-between px-8 py-6 border-t border-gray-100 bg-gray-50';

    const link = (href, label) => {
      const a = document.createElement('a');
      a.className = 'inline-flex items-center text-primary hover:text-primary/80';
      a.href = href;
      a.innerHTML = label;
      return a;
    };

    const left = document.createElement('div');
    const right = document.createElement('div');

    if (prevSlug) {
      left.appendChild(link(`./${prevSlug}`, '<i class="fa fa-arrow-left mr-2"></i> Previous'));
    } else {
      const span = document.createElement('span');
      span.className = 'text-apple-gray';
      span.textContent = 'No newer post';
      left.appendChild(span);
    }

    if (nextSlug) {
      right.appendChild(link(`./${nextSlug}`, 'Next <i class="fa fa-arrow-right ml-2"></i>'));
    } else {
      const span = document.createElement('span');
      span.className = 'text-apple-gray';
      span.textContent = 'No older post';
      right.appendChild(span);
    }

    wrapper.appendChild(left);
    wrapper.appendChild(right);

    // Append to end of article
    const article = document.querySelector('article');
    if (article) {
      article.appendChild(wrapper);
    }
  }

  window.initializeNewsNavigation = renderNav;
})();