"""Content-consistency tests: a page's hero <h1> must agree with its <title>
and, where present, the final breadcrumb segment.

The `weeks/*.html` files are the hand-maintained source of truth for the site
(there are no Markdown sources). These checks guard against the title / hero /
breadcrumb drifting apart when a page is edited.
"""
from pathlib import Path
from bs4 import BeautifulSoup

SITE_ROOT = Path(__file__).parent.parent


def _rel(p):
    return str(p.relative_to(SITE_ROOT))


class TestHeroTitleBreadcrumbAgree:
    def test_h1_matches_title_and_breadcrumb(self, parsed_pages):
        failures = []
        for path, _, soup in parsed_pages:
            h1 = soup.select_one("section.hero h1")
            if not h1:
                continue
            h1_text = h1.get_text(strip=True)
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            if not title.startswith(h1_text):
                failures.append(f"{_rel(path)}: <title> does not start with h1 '{h1_text}'")
            crumb = soup.select_one(".breadcrumbs span")
            if crumb and crumb.get_text(strip=True) != h1_text:
                failures.append(
                    f"{_rel(path)}: breadcrumb '{crumb.get_text(strip=True)}' != h1 '{h1_text}'"
                )
        assert not failures, "Hero/title/breadcrumb mismatches:\n" + "\n".join(failures)


class TestLastUpdatedIndicator:
    def test_syllabus_and_schedule_show_last_updated(self):
        import re as _re
        for name in ("core/syllabus.html", "core/schedule.html"):
            soup = BeautifulSoup((SITE_ROOT / name).read_text(), "lxml")
            meta = soup.select_one(".page-meta")
            assert meta, f"{name}: no .page-meta element"
            assert _re.search(r"Last updated:\s*\d{4}-\d{2}-\d{2}", meta.get_text()), (
                f"{name}: .page-meta has no ISO date"
            )


class TestNoMarkdownSources:
    def test_weeks_dir_has_no_stale_markdown(self):
        """weeks/ holds only .html files — the HTML is canonical, no partial
        Markdown outlines that could be regenerated over correct pages."""
        stray = sorted(p.name for p in (SITE_ROOT / "weeks").glob("*.md"))
        assert not stray, f"Unexpected Markdown in weeks/: {stray}"
