// "You are here" indicator for the homepage's 15-week journey map.
// Scoped to index.html only — the map only exists there. Uses the shared
// window.CourseCalendar (js/course-calendar.js) for date logic; the
// "This Week" rail card that used to be populated from here is now handled
// sitewide by js/this-week-card.js. See
// docs/design-spec_phase3_website-revision_v1_20260903.md (Part 2.3-2.4).

(function () {
  function nodeCenter(node) {
    return node.tagName === "rect"
      ? {
          x: parseFloat(node.getAttribute("x")) + parseFloat(node.getAttribute("width")) / 2,
          y: parseFloat(node.getAttribute("y")) + parseFloat(node.getAttribute("height")) / 2
        }
      : { x: parseFloat(node.getAttribute("cx")), y: parseFloat(node.getAttribute("cy")) };
  }

  function init() {
    var svg = document.getElementById("journey-map");
    var marker = document.getElementById("here-marker");
    var CC = window.CourseCalendar;
    if (!svg || !marker || !CC) return;

    var todayStr = CC.today();
    var wk = CC.currentWeekNumber(todayStr);
    if (!wk) return; // semester hasn't started yet

    var brk = CC.activeBreak(todayStr);
    marker.style.display = "";

    if (brk) {
      var nextWk = wk + 1 <= 15 ? wk + 1 : null;
      if (nextWk) {
        var nextNode = svg.querySelector('[data-week="' + nextWk + '"]');
        var c = nodeCenter(nextNode);
        marker.innerHTML =
          '<circle class="here-ring next" cx="' + c.x + '" cy="' + c.y + '" r="13"></circle>';
      }
    } else {
      var node = svg.querySelector('[data-week="' + wk + '"]');
      if (!node) return;
      var center = nodeCenter(node);
      var isEthicsWeek = CC.ETHICS_WEEKS.indexOf(wk) !== -1;
      var labelY = isEthicsWeek ? center.y + 34 : center.y - 24;
      marker.innerHTML =
        '<circle class="here-ring" cx="' + center.x + '" cy="' + center.y + '" r="13"></circle>' +
        '<text fill="var(--accent)" font-family="Quicksand" font-size="11" font-weight="700" ' +
        'x="' + center.x + '" y="' + labelY + '" text-anchor="middle">You are here</text>';
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
