"""Feature tests: dark-mode toggle (default dark) and the schedule
current-week highlight.

These check the static scaffolding the runtime script (assets/js/site.js)
depends on. The date arithmetic itself is exercised by hand in a browser.
"""
import datetime as dt
import re
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent


class TestThemeToggleScaffolding:
    def test_site_js_exists(self):
        assert (SITE_ROOT / "assets" / "js" / "site.js").is_file()

    def test_every_page_has_inline_theme_script_in_head(self, parsed_pages):
        failures = []
        for path, _, soup in parsed_pages:
            head = soup.head
            inline = " ".join(
                s.get_text() for s in head.find_all("script") if not s.get("src")
            )
            if 'setAttribute("data-theme"' not in inline or "localStorage" not in inline:
                failures.append(str(path.relative_to(SITE_ROOT)))
        assert not failures, f"Pages missing the inline FOUC theme script: {failures}"

    def test_every_page_loads_site_js(self, parsed_pages):
        failures = []
        for path, _, soup in parsed_pages:
            srcs = [s.get("src", "") for s in soup.find_all("script")]
            if not any(s.endswith("assets/js/site.js") for s in srcs):
                failures.append(str(path.relative_to(SITE_ROOT)))
            for s in srcs:
                if s.endswith("assets/js/site.js"):
                    target = (path.parent / s).resolve()
                    assert target.exists(), f"{path}: {s} does not resolve"
        assert not failures, f"Pages not loading site.js: {failures}"

    def test_toggle_button_present_and_outside_nav(self, parsed_pages):
        failures = []
        for path, _, soup in parsed_pages:
            btn = soup.select_one("button.theme-toggle")
            if not btn:
                failures.append(f"{path.relative_to(SITE_ROOT)}: no .theme-toggle")
                continue
            if btn.find_parent("nav"):
                failures.append(
                    f"{path.relative_to(SITE_ROOT)}: .theme-toggle is inside <nav> "
                    "(breaks nav-identity check)"
                )
            if not btn.get("aria-label"):
                failures.append(f"{path.relative_to(SITE_ROOT)}: toggle has no aria-label")
        assert not failures, "\n".join(failures)

    def test_default_theme_is_dark(self):
        """Bare :root carries the dark palette; light is an explicit override."""
        css = (SITE_ROOT / "css" / "style.css").read_text()
        root = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
        assert "--bg: #16181d" in root, "bare :root is not the dark palette"
        assert ':root[data-theme="light"]' in css, "no explicit light override block"


class TestScheduleWeekData:
    def _week_lis(self):
        from bs4 import BeautifulSoup

        html = (SITE_ROOT / "core" / "schedule.html").read_text()
        soup = BeautifulSoup(html, "lxml")
        return soup.select("li[data-week][data-first]")

    def test_fifteen_weeks_tagged(self):
        lis = self._week_lis()
        assert len(lis) == 15, f"expected 15 tagged week <li>, found {len(lis)}"
        nums = sorted(int(li["data-week"]) for li in lis)
        assert nums == list(range(1, 16))

    def test_first_session_dates_parse_and_are_chronological(self):
        lis = sorted(self._week_lis(), key=lambda li: int(li["data-week"]))
        dates = []
        for li in lis:
            d = dt.date.fromisoformat(li["data-first"])  # raises if malformed
            dates.append(d)
        assert dates == sorted(dates), "data-first dates are not chronological"
        assert dates[0] == dt.date(2026, 8, 27), "Week 1 should start Thu Aug 27, 2026"
        assert all(d.weekday() in (1, 3) for d in dates), (
            "every first session should fall on a Tuesday or Thursday"
        )

    def test_week_li_links_still_point_at_the_right_page(self):
        for li in self._week_lis():
            n = int(li["data-week"])
            href = li.find("a")["href"]
            assert href.endswith(f"week-{n:02d}.html"), (href, n)


class TestUpNextBanner:
    def _index(self):
        from bs4 import BeautifulSoup

        return BeautifulSoup((SITE_ROOT / "index.html").read_text(), "lxml")

    def _assignments_due(self):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup((SITE_ROOT / "core" / "assignments.html").read_text(), "lxml")
        out = {}
        for tr in soup.select("tr[data-assignment][data-due]"):
            out[tr["data-assignment"]] = tr["data-due"]
        return out

    def test_index_has_hidden_up_next_banner(self):
        soup = self._index()
        box = soup.select_one(".up-next")
        assert box is not None, "index.html has no .up-next element"
        assert box.has_attr("hidden"), ".up-next should start hidden (shown by JS)"
        link = box.select_one("a.up-next-body")
        assert link is not None and link.get("href") == "core/assignments.html"

    def test_assignments_data_island_is_valid(self):
        import json

        soup = self._index()
        block = soup.find("script", id="assignments-data")
        assert block is not None, "no #assignments-data JSON island on index.html"
        data = json.loads(block.string)
        assert isinstance(data, list) and data, "assignments data is not a non-empty list"
        for item in data:
            assert {"key", "tag", "name", "due"} <= set(item), item
            dt.date.fromisoformat(item["due"])  # raises on a bad date

    def test_data_island_matches_assignments_page(self):
        import json

        data = json.loads(self._index().find("script", id="assignments-data").string)
        island = {item["key"]: item["due"] for item in data}
        page = self._assignments_due()
        assert island == page, (
            "index.html 'Up next' dates disagree with core/assignments.html "
            f"data-due attributes.\n  island: {island}\n  page:   {page}"
        )

    def test_assignments_page_due_dates_are_iso(self):
        for key, due in self._assignments_due().items():
            dt.date.fromisoformat(due)  # raises if not YYYY-MM-DD
