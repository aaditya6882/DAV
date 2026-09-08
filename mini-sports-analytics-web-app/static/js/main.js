/* =========================================================
   QFIFA — Main JavaScript
   ========================================================= */

(function () {
  'use strict';

  /* ---- Dark Mode ---- */
  const THEME_KEY = 'qfifa-theme';

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    localStorage.setItem('matchiq-theme', theme);
    const btn = document.getElementById('mq-theme-btn');
    if (btn) {
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      btn.innerHTML = theme === 'dark' ? svgSun() : svgMoon();
    }
  }

  function svgMoon() {
    return '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }

  function svgSun() {
    return '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  }

  const savedTheme = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(savedTheme);

  document.addEventListener('DOMContentLoaded', function () {
    // Theme toggle button
    const themeBtn = document.getElementById('mq-theme-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    /* ---- Mobile Nav ---- */
    const navToggle = document.getElementById('mq-nav-toggle');
    const navLinks = document.getElementById('mq-nav-links');
    if (navToggle && navLinks) {
      navToggle.addEventListener('click', function () {
        const isOpen = navLinks.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });

      // Close on link click
      navLinks.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          navLinks.classList.remove('open');
          document.body.style.overflow = '';
        });
      });
    }

    /* ---- Global Search ---- */
    const searchInput = document.getElementById('mq-global-search');
    const searchDropdown = document.getElementById('mq-search-dropdown');
    let searchTimeout;

    if (searchInput && searchDropdown) {
      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        const q = searchInput.value.trim();
        if (q.length < 2) {
          searchDropdown.classList.remove('open');
          return;
        }
        searchTimeout = setTimeout(function () {
          doSearch(q);
        }, 250);
      });

      searchInput.addEventListener('focus', function () {
        if (searchInput.value.trim().length >= 2) {
          searchDropdown.classList.add('open');
        }
      });

      document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
          searchDropdown.classList.remove('open');
        }
      });

      searchInput.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          searchDropdown.classList.remove('open');
          searchInput.blur();
        }
      });
    }

    function doSearch(q) {
      fetch('/api/search?q=' + encodeURIComponent(q))
        .then(function (r) { return r.json(); })
        .then(function (data) {
          renderSearchResults(data);
        })
        .catch(function () {
          searchDropdown.innerHTML = '<div class="mq-search__no-results">Search unavailable.</div>';
          searchDropdown.classList.add('open');
        });
    }

    function renderSearchResults(data) {
      var html = '';
      var hasResults = false;

      if (data.teams && data.teams.length > 0) {
        hasResults = true;
        html += '<div class="mq-search__section-title">Teams</div>';
        data.teams.forEach(function (t) {
          html += '<a href="/teams/' + encodeURIComponent(t.name) + '" class="mq-search__item">' +
            '<span>⚽</span><span>' + escapeHtml(t.name) + '</span></a>';
        });
      }

      if (data.players && data.players.length > 0) {
        hasResults = true;
        html += '<div class="mq-search__section-title">Players</div>';
        data.players.forEach(function (p) {
          html += '<a href="/players/' + encodeURIComponent(p.id) + '" class="mq-search__item">' +
            '<span>👤</span><span>' + escapeHtml(p.name) + '</span>' +
            '<span class="mq-search__item-sub">' + escapeHtml(p.team) + '</span></a>';
        });
      }

      if (data.matches && data.matches.length > 0) {
        hasResults = true;
        html += '<div class="mq-search__section-title">Matches</div>';
        data.matches.forEach(function (m) {
          html += '<a href="/matches/' + m.match_id + '" class="mq-search__item">' +
            '<span>🏟️</span><span>' + escapeHtml(m.label) + ' <strong>' + m.score + '</strong></span>' +
            '<span class="mq-search__item-sub">' + escapeHtml(m.stage) + '</span></a>';
        });
      }

      if (!hasResults) {
        html = '<div class="mq-search__no-results">No results found.</div>';
      }

      searchDropdown.innerHTML = html;
      searchDropdown.classList.add('open');
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    /* ---- Compare mode toggle ---- */
    const modeButtons = document.querySelectorAll('[data-compare-mode]');
    modeButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const mode = btn.getAttribute('data-compare-mode');
        const url = new URL(window.location.href);
        url.searchParams.set('mode', mode);
        window.location.href = url.toString();
      });
    });

    /* ---- Filter/Search forms auto-submit ---- */
    document.querySelectorAll('.mq-auto-submit select').forEach(function (sel) {
      sel.addEventListener('change', function () {
        sel.closest('form').submit();
      });
    });

    /* ---- Tabs ---- */
    document.querySelectorAll('.mq-tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        const target = tab.getAttribute('data-tab');
        if (!target) return;
        const container = tab.closest('[data-tabs]');
        if (!container) return;
        container.querySelectorAll('.mq-tab').forEach(function (t) { t.classList.remove('active'); });
        tab.classList.add('active');
        container.querySelectorAll('[data-tab-content]').forEach(function (panel) {
          panel.classList.toggle('hidden', panel.getAttribute('data-tab-content') !== target);
        });
      });
    });

    /* ---- Did You Know auto-rotate & controls ---- */
    const factsEl = document.querySelectorAll('.mq-fact-item');
    const dotsEl = document.querySelectorAll('.mq-fact-dot');
    const prevBtn = document.getElementById('mq-fact-prev');
    const nextBtn = document.getElementById('mq-fact-next');
    const cardEl = document.getElementById('mq-fact-card');

    if (factsEl.length > 0) {
      let current = 0;
      let timer = null;

      function showFact(index) {
        factsEl.forEach(function (el, i) {
          if (i === index) {
            el.classList.add('active');
          } else {
            el.classList.remove('active');
          }
        });

        dotsEl.forEach(function (dot, i) {
          if (i === index) {
            dot.classList.add('active');
          } else {
            dot.classList.remove('active');
          }
        });

        current = index;
      }

      function nextFact() {
        showFact((current + 1) % factsEl.length);
      }

      function prevFact() {
        showFact((current - 1 + factsEl.length) % factsEl.length);
      }

      function startAutoRotate() {
        if (factsEl.length > 1 && !timer) {
          timer = setInterval(nextFact, 4500);
        }
      }

      function stopAutoRotate() {
        if (timer) {
          clearInterval(timer);
          timer = null;
        }
      }

      // Initial active item setup
      showFact(0);
      startAutoRotate();

      dotsEl.forEach(function (dot) {
        dot.addEventListener('click', function () {
          const idx = parseInt(dot.getAttribute('data-index'), 10);
          if (!isNaN(idx)) {
            showFact(idx);
            stopAutoRotate();
            startAutoRotate();
          }
        });
      });

      if (prevBtn) {
        prevBtn.addEventListener('click', function () {
          prevFact();
          stopAutoRotate();
          startAutoRotate();
        });
      }

      if (nextBtn) {
        nextBtn.addEventListener('click', function () {
          nextFact();
          stopAutoRotate();
          startAutoRotate();
        });
      }

      if (cardEl) {
        cardEl.addEventListener('mouseenter', stopAutoRotate);
        cardEl.addEventListener('mouseleave', startAutoRotate);
      }
    }
  });
})();

