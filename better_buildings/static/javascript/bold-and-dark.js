(function() {
  "use strict"; // Start of use strict

  function initParallax() {

    if (!('requestAnimationFrame' in window)) return;
    if (/Mobile|Android/.test(navigator.userAgent)) return;

    var parallaxItems = document.querySelectorAll('[data-bss-parallax]');

    if (!parallaxItems.length) return;

    var defaultSpeed = 0.5;
    var visible = [];
    var scheduled;

    window.addEventListener('scroll', scroll);
    window.addEventListener('resize', scroll);

    scroll();

    function scroll() {

      visible.length = 0;

      for (var i = 0; i < parallaxItems.length; i++) {
        var rect = parallaxItems[i].getBoundingClientRect();
        var speed = parseFloat(parallaxItems[i].getAttribute('data-bss-parallax-speed'), 10) || defaultSpeed;

        if (rect.bottom > 0 && rect.top < window.innerHeight) {
          visible.push({
            speed: speed,
            node: parallaxItems[i]
          });
        }

      }

      cancelAnimationFrame(scheduled);

      if (visible.length) {
        scheduled = requestAnimationFrame(update);
      }

    }

    function update() {

      for (var i = 0; i < visible.length; i++) {
        var node = visible[i].node;
        var speed = visible[i].speed;

        node.style.transform = 'translate3d(0, ' + (-window.scrollY * speed) + 'px, 0)';
      }

    }
  }

  initParallax();
})(); // End of use strict

(function() {

  // JavaScript snippet handling Dark/Light mode switching

  const getStoredTheme = () => localStorage.getItem('theme');
  const setStoredTheme = theme => localStorage.setItem('theme', theme);
  const forcedTheme = document.documentElement.getAttribute('data-bss-forced-theme');

  const getPreferredTheme = () => {

      if (forcedTheme) return forcedTheme;

      const storedTheme = getStoredTheme();
      if (storedTheme) {
          return storedTheme;
      }

      const pageTheme = document.documentElement.getAttribute('data-bs-theme');

      if (pageTheme) {
          return pageTheme;
      }

      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  const setTheme = theme => {
      if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          document.documentElement.setAttribute('data-bs-theme', 'dark');
      } else {
          document.documentElement.setAttribute('data-bs-theme', theme);
      }
  }

  setTheme(getPreferredTheme());

  const showActiveTheme = (theme, focus = false) => {
      const themeSwitchers = [].slice.call(document.querySelectorAll('.theme-switcher'));

      if (!themeSwitchers.length) return;

      document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
          element.classList.remove('active');
          element.setAttribute('aria-pressed', 'false');
      });

      for (const themeSwitcher of themeSwitchers) {

          const btnToActivate = themeSwitcher.querySelector('[data-bs-theme-value="' + theme + '"]');

          if (btnToActivate) {
              btnToActivate.classList.add('active');
              btnToActivate.setAttribute('aria-pressed', 'true');
          }
      }
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      const storedTheme = getStoredTheme();
      if (storedTheme !== 'light' && storedTheme !== 'dark') {
          setTheme(getPreferredTheme());
      }
  });

  window.addEventListener('DOMContentLoaded', () => {
      showActiveTheme(getPreferredTheme());

      document.querySelectorAll('[data-bs-theme-value]')
          .forEach(toggle => {
              toggle.addEventListener('click', (e) => {
                  e.preventDefault();
                  const theme = toggle.getAttribute('data-bs-theme-value');
                  setStoredTheme(theme);
                  setTheme(theme);
                  showActiveTheme(theme);
              })
          })
  });
})();