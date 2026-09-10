/* Dark mode (P3-1): wires the nav's toggle/lock buttons to window.__theme
   (defined in js/theme-init.js) and re-checks for override expiry while the
   tab stays open. Loaded near the end of <body> on every page. */
(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var T = window.__theme;
    var toggleBtn = document.getElementById("theme-toggle");
    var lockBtn = document.getElementById("theme-lock");
    if (!T || !toggleBtn || !lockBtn) return;

    function currentTheme() {
      return document.documentElement.getAttribute("data-theme") || T.autoTheme(new Date());
    }

    function updateUI() {
      var theme = currentTheme();
      var pref = T.load();

      toggleBtn.classList.toggle("is-dark", theme === "dark");
      toggleBtn.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
      );
      toggleBtn.title = theme === "dark" ? "Dark mode — click for light" : "Light mode — click for dark";

      if (pref) {
        lockBtn.hidden = false;
        lockBtn.classList.toggle("is-locked", !!pref.locked);
        lockBtn.setAttribute("aria-pressed", pref.locked ? "true" : "false");
        lockBtn.title = pref.locked
          ? "Locked to this theme — click to unlock"
          : "Manual override (reverts to auto later) — click to lock";
      } else {
        lockBtn.hidden = true;
      }
    }

    toggleBtn.addEventListener("click", function () {
      var newTheme = currentTheme() === "dark" ? "light" : "dark";
      var pref = T.load();

      if (pref && pref.locked) {
        T.save({ theme: newTheme, locked: true });
      } else {
        var expiresAt = T.nextTwoBoundaries(new Date())[1];
        T.save({ theme: newTheme, locked: false, expiresAt: expiresAt });
      }

      T.apply(newTheme);
      updateUI();
    });

    lockBtn.addEventListener("click", function () {
      var pref = T.load();
      if (!pref) return;

      if (pref.locked) {
        var expiresAt = T.nextTwoBoundaries(new Date())[1];
        T.save({ theme: pref.theme, locked: false, expiresAt: expiresAt });
      } else {
        T.save({ theme: pref.theme, locked: true });
      }

      updateUI();
    });

    updateUI();

    setInterval(function () {
      var resolved = T.resolve();
      if (resolved !== currentTheme()) T.apply(resolved);
      updateUI();
    }, 60000);
  });
})();
