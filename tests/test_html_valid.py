"""HTML5 validity checks using the pure-Python html5lib parser.

This is not the full W3C Nu validator, but html5lib is a spec-compliant parser:
in strict mode it raises on parse errors (misnested/unclosed tags, stray
characters, bogus attributes), which catches the structural mistakes most
likely in hand-edited multi-page HTML. We also assert no duplicate ids.
"""
from pathlib import Path

import html5lib
import pytest

SITE_ROOT = Path(__file__).parent.parent


def _rel(p):
    return str(p.relative_to(SITE_ROOT))


def _pages():
    return sorted(
        f for f in SITE_ROOT.rglob("*.html") if ".venv" not in f.parts
    )


@pytest.mark.parametrize("page", _pages(), ids=_rel)
def test_page_parses_without_html5_errors(page):
    parser = html5lib.HTMLParser(strict=True)
    try:
        parser.parse(page.read_text(encoding="utf-8"))
    except html5lib.html5parser.ParseError as exc:
        pytest.fail(f"{_rel(page)}: HTML5 parse error: {exc}")


@pytest.mark.parametrize("page", _pages(), ids=_rel)
def test_page_has_no_duplicate_ids(page):
    parser = html5lib.HTMLParser(namespaceHTMLElements=False)
    tree = parser.parse(page.read_text(encoding="utf-8"))
    ids = [el.get("id") for el in tree.iter() if el.get("id")]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"{_rel(page)}: duplicate id(s): {sorted(dupes)}"
