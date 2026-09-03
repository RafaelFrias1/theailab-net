"""Unit tests for css/style.css: no dead class selectors.

Every class targeted by the stylesheet must be used by at least one HTML page,
except for an explicit allow-list of state/utility classes that are applied at
runtime or reserved deliberately.
"""
import re
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
CSS = SITE_ROOT / "css" / "style.css"

# Classes that legitimately appear only in CSS.
ALLOW = {
    "skip-link",     # present in HTML, but also has :focus state selectors
    "active",        # runtime state on the current nav link
    "no-featured-image",  # header modifier, always present
    "footer-links",  # added by the footer-links task; harmless if a page lacks it
    "page-meta",     # "Last updated" row; only on syllabus/schedule
}


def _css_classes():
    text = CSS.read_text()
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)  # strip comments
    return set(re.findall(r"\.([a-zA-Z][\w-]*)", text))


def _html_class_tokens():
    tokens = set()
    for f in SITE_ROOT.rglob("*.html"):
        if ".venv" in f.parts:
            continue
        for m in re.finditer(r'class="([^"]+)"', f.read_text(encoding="utf-8")):
            tokens.update(m.group(1).split())
    return tokens


def test_no_dead_class_selectors():
    used = _html_class_tokens()
    dead = sorted(c for c in _css_classes() if c not in used and c not in ALLOW)
    assert not dead, f"Dead class selectors in style.css: {dead}"


def test_no_phantom_font_or_duplicate_blue_token():
    text = CSS.read_text()
    assert "NonBreakingSpaceOverride" not in text, "phantom font name still present"
    assert "--primary" not in text, "duplicate blue token --primary still present"


def test_has_focus_visible_and_print_rules():
    text = CSS.read_text()
    assert ":focus-visible" in text, "no :focus-visible styling"
    assert "@media print" in text, "no print stylesheet"


def test_stylesheet_shrank_below_450_lines():
    """Guard against the WordPress blog machinery creeping back in."""
    n = len(CSS.read_text().splitlines())
    assert n < 450, f"style.css is {n} lines; expected the trimmed sheet"
