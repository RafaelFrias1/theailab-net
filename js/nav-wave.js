/* Dock-style nav magnification (P3-2). As the cursor sweeps across the main
   nav, each link scales up based on horizontal distance from the cursor —
   nearest link largest, tapering to normal size by RADIUS px away — like
   macOS Dock icons or piano keys lighting up in sequence. Purely a visual
   affordance; layout and click targets are unaffected. */
(function () {
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var nav = document.querySelector(".main-nav ul");
    var links = nav ? nav.querySelectorAll(":scope > li > a") : [];
    if (!nav || !links.length) return;

    var MAX_SCALE = 1.18;
    var RADIUS = 110; // px — links farther than this stay at scale 1

    function update(mouseX) {
      for (var i = 0; i < links.length; i++) {
        var rect = links[i].getBoundingClientRect();
        var center = rect.left + rect.width / 2;
        var dist = Math.abs(mouseX - center);
        var t = Math.max(0, 1 - dist / RADIUS);
        var scale = 1 + (MAX_SCALE - 1) * t;
        links[i].style.transform = t > 0 ? "scale(" + scale.toFixed(3) + ")" : "";
      }
    }

    function reset() {
      for (var i = 0; i < links.length; i++) links[i].style.transform = "";
    }

    nav.addEventListener("mousemove", function (e) {
      update(e.clientX);
    });
    nav.addEventListener("mouseleave", reset);
  });
})();
