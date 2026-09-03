"""Integration tests: internal links resolve, nav is consistent, schedule links all weeks."""
import pytest
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import unquote

SITE_ROOT = Path(__file__).parent.parent

EXPECTED_NAV_LABELS = {"Home", "Syllabus", "Schedule", "Assignments", "Policies", "About"}


def _rel(path):
    return str(path.relative_to(SITE_ROOT))


def _resolve_href(href, page_path):
    """Resolve a relative href to an absolute Path, or None for external/anchor/mailto links."""
    if not href or href.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
        return None
    href = href.split("#")[0]
    if not href:
        return None
    href = unquote(href)
    return (page_path.parent / href).resolve()


def _collect_broken_links(page_path, soup, selector="a"):
    broken = []
    for tag in soup.select(selector):
        href = tag.get("href", "")
        target = _resolve_href(href, page_path)
        if target is not None and not target.exists():
            broken.append(href)
    return broken


class TestAllInternalLinks:
    def test_all_internal_links_resolve(self, site_root, parsed_pages):
        """Every internal <a href> across all pages must resolve to an existing file."""
        broken = []
        for path, _, soup in parsed_pages:
            for bad in _collect_broken_links(path, soup):
                broken.append(f"{_rel(path)} -> {bad}")
        assert not broken, f"{len(broken)} broken internal links. First 15: {broken[:15]}"


class TestExternalLinkRel:
    def test_external_anchors_have_noopener(self, parsed_pages):
        """Every <a> with an http(s) href must carry rel="noopener"."""
        failures = []
        for path, _, soup in parsed_pages:
            for a in soup.find_all("a", href=True):
                if a["href"].startswith(("http://", "https://")):
                    rel = " ".join(a.get("rel", []))
                    if "noopener" not in rel:
                        failures.append(f"{_rel(path)} -> {a['href']}")
        assert not failures, f"External links without rel=noopener: {failures[:15]}"


class TestNavConsistency:
    def test_all_nav_pages_have_identical_nav_labels(self, site_root, nav_pages):
        """Every page (except 404.html) must have the exact same set of nav link labels."""
        failures = []
        for f in nav_pages:
            soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
            nav = soup.select_one("nav.main-nav")
            if not nav:
                failures.append(f"{_rel(f)}: missing nav.main-nav")
                continue
            labels = {a.get_text(strip=True) for a in nav.find_all("a")}
            if labels != EXPECTED_NAV_LABELS:
                failures.append(f"{_rel(f)}: {sorted(labels)}")
        assert not failures, f"Pages with inconsistent nav labels: {failures[:15]}"

    def test_nav_links_resolve(self, site_root, nav_pages):
        """Nav links on every non-404 page must resolve to existing files."""
        broken = []
        for f in nav_pages:
            soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
            nav = soup.select_one("nav.main-nav")
            if not nav:
                continue
            for link in _collect_broken_links(f, nav, "a"):
                broken.append(f"{_rel(f)} -> {link}")
        assert not broken, f"Broken nav links: {broken[:15]}"


class TestNavMarkupIdentical:
    def test_nav_html_identical_across_content_pages(self, site_root, nav_pages):
        """With the active markers and depth-prefix stripped, the primary nav
        markup must be byte-identical across every content page."""
        norm = {}
        for f in nav_pages:
            soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
            nav = soup.select_one("nav.main-nav")
            html = str(nav)
            html = html.replace(' class="active"', "").replace(' aria-current="page"', "")
            html = html.replace("../", "").replace('href="core/', 'href="')
            norm[_rel(f)] = html
        for f in nav_pages:
            soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
            nav = soup.select_one("nav.main-nav")
            assert nav and nav.get("aria-label"), f"{_rel(f)}: nav missing aria-label"
        distinct = set(norm.values())
        assert len(distinct) == 1, (
            "Nav markup differs across pages:\n"
            + "\n".join(f"{k}: {v}" for k, v in norm.items())
        )


class TestActiveNav:
    def test_exactly_one_active_link_with_aria_current(self, site_root, nav_pages):
        """On every content page, exactly one nav link is class="active", that
        link also carries aria-current="page", and no other nav link does."""
        failures = []
        for f in nav_pages:
            soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
            nav = soup.select_one("nav.main-nav")
            links = nav.find_all("a") if nav else []
            active = [a for a in links if "active" in (a.get("class") or [])]
            aria = [a for a in links if a.get("aria-current") == "page"]
            if len(active) != 1:
                failures.append(f"{_rel(f)}: {len(active)} active links")
            elif active != aria:
                failures.append(f"{_rel(f)}: active link and aria-current link differ")
        assert not failures, f"Active-nav issues: {failures[:15]}"


class TestScheduleLinkTextMatchesTarget:
    def test_week_link_text_equals_target_hero_h1(self, site_root):
        """Each week link in schedule.html must have visible text equal to the
        target week page's hero <h1>."""
        schedule = site_root / "core" / "schedule.html"
        soup = BeautifulSoup(schedule.read_text(encoding="utf-8"), "lxml")
        failures = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "week-" not in href or not href.endswith(".html"):
                continue
            target = (schedule.parent / href).resolve()
            if not target.exists():
                failures.append(f"{href}: target missing")
                continue
            tsoup = BeautifulSoup(target.read_text(encoding="utf-8"), "lxml")
            h1 = tsoup.select_one("section.hero h1")
            h1_text = h1.get_text(strip=True) if h1 else ""
            link_text = a.get_text(strip=True)
            if link_text != h1_text:
                failures.append(f"{href}: link text '{link_text}' != hero h1 '{h1_text}'")
        assert not failures, "Schedule link/title mismatches:\n" + "\n".join(failures)


class TestScheduleLinksAllWeeks:
    def test_schedule_links_to_all_15_weeks(self, site_root):
        """core/schedule.html must link to weeks/week-01.html through weeks/week-15.html."""
        schedule = site_root / "core" / "schedule.html"
        soup = BeautifulSoup(schedule.read_text(encoding="utf-8"), "lxml")
        hrefs = {a.get("href", "") for a in soup.find_all("a")}
        missing = []
        for n in range(1, 16):
            expected = f"../weeks/week-{n:02d}.html"
            alt = f"weeks/week-{n:02d}.html"
            if expected not in hrefs and alt not in hrefs and not any(
                h.endswith(f"week-{n:02d}.html") for h in hrefs
            ):
                missing.append(f"week-{n:02d}.html")
        assert not missing, f"core/schedule.html missing links to: {missing}"
