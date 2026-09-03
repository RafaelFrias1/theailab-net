"""Content-source tests: Markdown week outlines must agree with their HTML pages.

Only weeks that ship a `.md` source are checked. The `.html` files are the
source of truth for the rendered site; these tests guard against a `.md`
outline drifting away from (or being a stale copy of another week's) content.
"""
import re
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
WEEKS_DIR = SITE_ROOT / "weeks"

# Distinctive strings that must appear in a given week's HTML *and* its .md,
# and must NOT appear in the other weeks' .md files (catches copy-paste bleed).
WEEK_MARKERS = {
    "week-01": {"must_contain": ["August 27", "Aug 27"], "must_not_contain": ["September 1 & 3", "Sep 1", "Sep 3"]},
    "week-02": {"must_contain": ["September 1", "Sep 1"], "must_not_contain": ["August 27", "Aug 27"]},
}


def _md_files():
    return sorted(WEEKS_DIR.glob("week-*.md"))


class TestMarkdownSourcesMatchHtml:
    def test_each_md_week_agrees_with_its_html(self):
        failures = []
        for md in _md_files():
            stem = md.stem  # e.g. "week-01"
            if stem not in WEEK_MARKERS:
                continue
            html = WEEKS_DIR / f"{stem}.html"
            if not html.exists():
                failures.append(f"{stem}.md has no matching {stem}.html")
                continue
            md_text = md.read_text(encoding="utf-8")
            markers = WEEK_MARKERS[stem]
            if not any(s in md_text for s in markers["must_contain"]):
                failures.append(
                    f"{stem}.md is missing any of {markers['must_contain']}"
                )
            bad = [s for s in markers["must_not_contain"] if s in md_text]
            if bad:
                failures.append(f"{stem}.md unexpectedly contains {bad} (wrong week's content?)")
        assert not failures, "Markdown source mismatches:\n" + "\n".join(failures)

    def test_no_two_md_files_are_near_duplicates(self):
        """No two week .md files may share their INTRODUCTION paragraph verbatim."""
        intros = {}
        for md in _md_files():
            text = md.read_text(encoding="utf-8")
            m = re.search(r"##\s*INTRODUCTION\s*\n(.+?)(?=\n##\s)", text, re.S | re.I)
            intro = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
            if intro and intro in intros.values():
                other = [k for k, v in intros.items() if v == intro][0]
                assert False, f"{md.name} has the same INTRODUCTION as {other}"
            intros[md.name] = intro
