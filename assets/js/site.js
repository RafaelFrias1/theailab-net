/* IPHS 400 course site — progressive enhancement.
   1. Light/dark theme toggle (dark is the default; choice persists in
      localStorage; an inline <head> script applies it before first paint).
   2. Current-week highlight on the schedule page, from the visitor's local
      date. Each week <li> carries data-week and data-first (ISO date of its
      first session). The highlight moves to a week on the Saturday before its
      first session and moves on at the next week's Saturday. */
(function () {
  "use strict";

  var root = document.documentElement;

  /* ---------- Theme toggle ---------- */
  var toggle = document.querySelector(".theme-toggle");

  function currentTheme() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function setTheme(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("theme", theme);
    } catch (e) {
      /* storage unavailable — the choice just won't persist */
    }
    if (toggle) {
      var toLight = theme === "dark";
      toggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      toggle.setAttribute(
        "aria-label",
        toLight ? "Switch to light theme" : "Switch to dark theme"
      );
      toggle.title = toLight ? "Switch to light theme" : "Switch to dark theme";
    }
  }

  if (toggle) {
    setTheme(currentTheme());
    toggle.addEventListener("click", function () {
      setTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  }

  /* ---------- "Up next" assignment banner (homepage) ---------- */
  var upNext = document.querySelector(".up-next");
  var upNextData = document.getElementById("assignments-data");
  if (upNext && upNextData) {
    renderUpNext(upNext, upNextData);
  }

  function renderUpNext(box, dataEl) {
    var list;
    try {
      list = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }
    if (!Array.isArray(list) || !list.length) return;

    var today = new Date();
    today.setHours(0, 0, 0, 0);

    list.sort(function (a, b) {
      return a.due < b.due ? -1 : a.due > b.due ? 1 : 0;
    });

    var next = null;
    for (var i = 0; i < list.length; i++) {
      var due = parseISODate(list[i].due);
      if (due && due >= today) {
        next = list[i];
        break;
      }
    }
    if (!next) return; // every deadline has passed — leave the banner hidden

    var dueText =
      next.dueText ||
      parseISODate(next.due).toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric"
      });

    var link = box.querySelector(".up-next-body");
    if (!link) return;
    link.textContent = "";
    if (next.tag) {
      var badge = document.createElement("span");
      badge.className = "up-next-tag";
      badge.textContent = next.tag;
      link.appendChild(badge);
    }
    link.appendChild(
      document.createTextNode(
        " " +
          next.name +
          " — due " +
          dueText +
          (next.note ? " (" + next.note + ")" : "")
      )
    );
    box.hidden = false;
  }

  /* ---------- Current-week highlight ---------- */
  var weekItems = document.querySelectorAll(".item-list li[data-week][data-first]");
  if (weekItems.length) {
    highlightCurrentWeek(weekItems);
  }

  function parseISODate(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || "");
    if (!m) return null;
    var d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
    d.setHours(0, 0, 0, 0);
    return d;
  }

  function highlightCurrentWeek(items) {
    var today = new Date();
    today.setHours(0, 0, 0, 0);

    var weeks = [];
    Array.prototype.forEach.call(items, function (li) {
      var first = parseISODate(li.getAttribute("data-first"));
      if (!first) return;
      // Saturday on/before `first`: subtract (weekday + 1) mod 7 days.
      var activates = new Date(first);
      activates.setDate(first.getDate() - ((first.getDay() + 1) % 7));
      weeks.push({ li: li, activates: activates });
    });
    if (!weeks.length) return;

    weeks.sort(function (a, b) {
      return a.activates - b.activates;
    });

    var idx = -1;
    for (var i = 0; i < weeks.length; i++) {
      if (weeks[i].activates <= today) idx = i;
    }
    if (idx === -1) return; // before the first week's window — term not started

    var windowEnd;
    if (idx + 1 < weeks.length) {
      windowEnd = weeks[idx + 1].activates;
    } else {
      windowEnd = new Date(weeks[idx].activates);
      windowEnd.setDate(windowEnd.getDate() + 7);
    }
    if (today >= windowEnd) return; // past the final week's window

    var li = weeks[idx].li;
    li.classList.add("is-current-week");

    var link = li.querySelector("a");
    if (link && !li.querySelector(".week-tag")) {
      var tag = document.createElement("span");
      tag.className = "week-tag";
      tag.textContent = "This week";
      link.appendChild(tag);
    }
  }
})();
