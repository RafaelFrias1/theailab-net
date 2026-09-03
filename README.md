# IPHS 400: Frontiers in AI

**Kenyon College — Integrated Program for Humane Studies (IPHS) — Fall 2026**

Course website for IPHS 400, a hands-on study of AI software engineering (AI-SWE):
configuring, extending, and orchestrating AI coding agents through a professional
software development lifecycle. This repository contains the site's source and
its test suite; course submissions, quizzes, and grades are handled separately
on Moodle.

- **Instructor:** Jon Chun
- **Schedule:** Tu/Th, 2:40–4:00 PM · Timberlake #5 (Evans Conference Room)

## Repository Structure

```
.
├── index.html              # Home page
├── 404.html                 # Not-found page
├── core/                    # Syllabus, schedule, assignments, policies, about
│   ├── syllabus.html
│   ├── schedule.html
│   ├── assignments.html
│   ├── policies.html
│   └── about.html
├── weeks/                   # One page per week, week-01.html … week-15.html (hand-maintained; the HTML is the source of truth)
├── css/
│   └── style.css            # Single shared stylesheet, no build step
├── tests/                   # pytest suite validating the site
│   ├── conftest.py
│   ├── test_unit_html_structure.py
│   ├── test_integration_links.py
│   ├── test_content_sources.py
│   ├── test_e2e_site.py
│   └── requirements.txt
└── docs/                    # Project reports, tech-specs, and manuals
```

The site is static HTML/CSS with no build step or JS framework. Every page
shares one stylesheet and a common header/nav/hero/footer skeleton.

## Running the Site Locally

This is a standalone static site — no build step, no deploy pipeline, no
external hosting configuration. Serve the repository root with Python's
built-in HTTP server and open the printed URL in your browser:

```bash
python3 -m http.server 8080
# then open http://localhost:8080/
```

Stop the server with `Ctrl+C` when you're done. No install step is required to
view the site — only the test suite has dependencies.

## Running the Tests

The test suite (pytest + BeautifulSoup/lxml) validates structural and content
integrity of every page:

- `test_unit_html_structure.py` — every page has a DOCTYPE, title, stylesheet
  link, header, footer, and hero `<h1>`; no leftover template branding; no
  placeholder or stub content
- `test_integration_links.py` — every internal link resolves; navigation is
  identical across all pages; the schedule links to all 15 week pages
- `test_e2e_site.py` — required files/directories exist; exact page count;
  every page is reachable from `index.html` (no orphaned pages)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tests/requirements.txt
pytest tests/ -v
```

Run a single test file or test:

```bash
pytest tests/test_unit_html_structure.py -v
pytest tests/test_integration_links.py::TestNavConsistency::test_nav_links_resolve -v
```

## Content Source and Provenance

All course content (syllabus text, schedule, assignments, policies) is
sourced from the official Fall 2026 syllabus. The page layout, navigation
pattern, and stylesheet are adapted from a prior Kenyon course site
([`programminghumanity-org`](https://github.com/jon-chun)) for visual
consistency across Jon Chun's Kenyon course sites; no course content from
that site is reused here.

## License

See [LICENSE](LICENSE).
