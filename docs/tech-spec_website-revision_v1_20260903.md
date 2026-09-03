# Tech Spec: Website Revision v1

**Date:** 2026-09-03
**Repo:** `theailab-net` (IPHS 400 course site)
**Scope:** Revisions to the standalone static site *after* the Netlify/CI strip. `netlify.toml` and `.github/workflows/` are already removed; the site is served locally only (`python3 -m http.server`). No page's prose content changes except where a task explicitly fixes an error in it (Tasks 1–2).
**Input:** `docs/report_web-revision_v1_20260903.md`, re-scoped and re-ranked as standalone implementation tasks.
**Audience:** A student working through Mini-Project #1 with an AI coding agent. Each task is self-contained: read the description and justification, then follow the numbered steps. Do tasks in order within a tier; do tiers High → Medium → Low.

**Conventions:**
- File paths are relative to the repo root.
- **"All pages"** = `index.html`, `404.html`, `core/*.html` (5), `weeks/week-01.html` … `week-15.html` (15) — **22 files total**.
- **"Content pages"** = all pages *except* `404.html` (21 files) — the set the nav-consistency and reachability tests use.
- The shared `<head>` block, header, nav, and footer are duplicated by hand in all 22 files. "Apply to the shared header" means make the identical edit in every file. Keep the pages byte-for-byte consistent outside the page-specific bits (`<title>`, `<meta name="description">`, hero `<h1>`, breadcrumb, `class="active"` position, `.page-content`).
- After **every** task: run `pytest tests/ -v` — all tests must stay green. If a task adds behaviour that "done" depends on, add or extend a test **in the same task**; do not defer test-writing.
- Serve locally to eyeball changes: `python3 -m http.server 8080` then open `http://localhost:8080/`.
- Commit after each task (or each coherent tier) with a message naming the task.

---

## Task List Overview

| # | Task | Criticality |
|---|---|---|
| 1 | Fix `weeks/week-01.md` (holds Week 2's content) | High |
| 2 | Reconcile schedule link text with week-page titles (Weeks 14 & 15) | High |
| 3 | Add per-page `<meta name="description">` | High |
| 4 | Add a favicon | High |
| 5 | Add `aria-current="page"` to the active nav link | High |
| 6 | Add a skip-to-content link + `id="main-content"` on `<main>` | High |
| 7 | Normalize internal-link style and attribute order across `core/` | High |
| 8 | Add `aria-label` to `<nav>` | Medium |
| 9 | Add `scope` attributes to all table headers | Medium |
| 10 | Add `rel="noopener noreferrer"` to external links | Medium |
| 11 | Resolve the partial Markdown week sources + empty template | Medium |
| 12 | Untrack non-site files (`.DS_Store`, session transcript); delete `docs/r` | Medium |
| 13 | Trim `.gitignore` to match the actual project | Medium |
| 14 | Add `robots.txt` and `sitemap.xml` | Medium |
| 15 | Add Open Graph / Twitter Card + canonical metadata | Medium |
| 16 | Remove dead CSS from `css/style.css` | Low |
| 17 | Add a "Last updated" indicator using the existing `.page-meta` class | Low |
| 18 | Make the GitHub repo URL a real link (currently `<code>`) | Low |
| 19 | Add footer links (repo, license) | Low |
| 20 | Add a print stylesheet | Low |
| 21 | Collapse duplicate blue tokens and drop the phantom font name | Low |
| 22 | Add `:focus-visible` styling | Low |
| 23 | Add a `Course` JSON-LD block | Low |
| 24 | Add an HTML-validity check to the local workflow | Low |

---

## High Criticality

### Task 1 — Fix `weeks/week-01.md` (it currently holds Week 2's content)

**Description:** `weeks/week-01.md` describes "Tuesday & Thursday, September 1 & 3", shell fundamentals, the Zitron readings, and DataCamp Git courses — that is Week 2's material, nearly identical to `weeks/week-02.md`. `weeks/week-01.html` is correct (single Thursday session, August 27). Bring the source file into agreement with the real Week 1.

**Justification:** The commit history shows week HTML bodies being rebuilt from their `.md` outlines. As it stands, regenerating `week-01.html` from `week-01.md` would silently overwrite the correct page with Week 2 content. This is a latent data-loss bug, not a style nit.

**Steps:**
1. Open `weeks/week-01.html` and `weeks/week-01.md` side by side.
2. Rewrite `weeks/week-01.md` so its outline matches `week-01.html`: a single **Thursday, August 27** session; "Week 1 has no Tuesday class"; course introduction / 2026 AI landscape; account + tool setup (Claude Code, GitHub, WSL2); secrets hygiene from day one; "Lightning Presentation sign-ups open Tuesday, September 1." Match the heading style already used in `weeks/week-02.md` (`## INTRODUCTION`, `## THURSDAY (Aug 27, 2026)`, `### READINGS`, `### CODING`, etc.).
3. Do **not** change `week-01.html` — it is the correct artifact and the tests already validate it.
4. If you conclude the `.md` files are not actually a maintained source (see Task 11), you may instead delete `week-01.md` and `week-02.md` here and handle both in Task 11. Pick one path; do not leave `week-01.md` containing Week 2 content.
5. Run `pytest tests/ -v` (no test change expected — `.md` files are not covered).

---

### Task 2 — Reconcile schedule link text with week-page titles (Weeks 14 & 15)

**Description:** `core/schedule.html` links to two weeks with text that disagrees with the destination page's `<title>` and `<h1>`:

| `schedule.html` link text | `week-XX.html` `<title>` / `<h1>` |
|---|---|
| Week 14: Final Project Work Session **and Poster Development** | Week 14: Final Project Work Session |
| Week 15: Final Project **Poster** Presentations | Week 15: Final Project Presentations |

**Justification:** A visitor clicking "…and Poster Development" lands on a page titled "…Work Session" and reasonably wonders if they followed the wrong link. The tests only check that the href resolves, so this passes CI. Consistency between link text, `<title>`, `<h1>`, and breadcrumb is a basic wayfinding guarantee.

**Steps:**
1. Decide the canonical title for each week. Recommended (matches the fuller schedule phrasing):
   - Week 14: **Final Project Work Session and Poster Development**
   - Week 15: **Final Project Poster Presentations**
2. In `weeks/week-14.html`: update `<title>`, the hero `<h1>`, and the breadcrumb trailing `<span>` to the canonical Week 14 title. Keep the `– IPHS 400: Frontiers in AI` suffix on `<title>`.
3. In `weeks/week-15.html`: same for the canonical Week 15 title.
4. Grep the repo for any other reference to these weeks' titles (`grep -rn "Week 1[45]" --include=*.html`) and confirm `schedule.html`, the prev/next links on `week-13`/`week-14`, and the breadcrumbs all now agree.
5. Add a test to `tests/test_integration_links.py` (new class `TestScheduleLinkTextMatchesTarget`): for each week link in `schedule.html`, load the target page and assert the link's visible text equals the target's hero `<h1>` text. Run `pytest tests/ -v`.

---

### Task 3 — Add per-page `<meta name="description">`

**Description:** None of the 22 pages has a meta description. Add one per page, written from that page's own content.

**Justification:** Controls the search-result snippet and is the fallback for link unfurls in Slack/email — the two ways this course site will actually be shared. Every page already has distinct opening prose to summarize.

**Steps:**
1. For each of the 22 HTML files, write one sentence, **110–160 characters**, describing the page. Examples: `index.html` → "IPHS 400: Frontiers in AI at Kenyon College — a hands-on course in AI software engineering, built around four stacking mini-projects and a research capstone." A week page → "Week 3 of IPHS 400: anatomy of an AI coding agent, prompt vs. context engineering, and an ethics thread on labor, deskilling, and accountability."
2. Insert `<meta name="description" content="..."/>` in the `<head>`, on its own line immediately after the viewport `<meta>` and before `<title>`. Keep the self-closing `/>` style the existing tags use.
3. Add a test to `tests/test_unit_html_structure.py` (`TestMetaDescription`): every page has exactly one `meta[name="description"]` whose `content` is 50–200 chars and is not a duplicate of another page's.
4. Run `pytest tests/ -v`.

---

### Task 4 — Add a favicon

**Description:** No `<link rel="icon">` and no icon file exist. All 22 tabs/bookmarks show a generic glyph.

**Justification:** One asset + one shared `<link>` tag; immediately visible in the tab bar, history, and bookmarks.

**Steps:**
1. Create `favicon.svg` at the repo root — a simple mark (e.g. a monogram "AI" or "400" on `#0073aa`, or a lab-flask glyph). Keep it under ~2 KB. SVG so no raster tooling is needed.
2. Optionally also add `favicon.ico` (32×32) for older browsers.
3. In the shared `<head>` of all 22 pages, after the stylesheet `<link>`, add:
   - root pages: `<link rel="icon" href="favicon.svg" type="image/svg+xml"/>`
   - `core/` and `weeks/` pages: `href="../favicon.svg"`
4. Add a test to `tests/test_unit_html_structure.py`: every page has a `link[rel="icon"]` whose `href` resolves to an existing file (resolve relative to the page's directory, mirroring the existing `test_all_pages_link_to_resolvable_style_css`).
5. Update `tests/test_e2e_site.py` if it asserts an exact root file set (it currently does not — `TestPageCount` counts only `*.html` — so `favicon.svg` is fine, but re-run to confirm).
6. Run `pytest tests/ -v` and load the site to check the tab icon.

---

### Task 5 — Add `aria-current="page"` to the active nav link

**Description:** The current page's nav link carries only `class="active"` (a CSS hook). Add `aria-current="page"` on the same element.

**Justification:** Sighted users get an underline; screen-reader users currently get no indication of which page they're on. `aria-current="page"` is the standard, single-attribute fix and is WCAG-aligned.

**Steps:**
1. In each of the 22 pages, find the nav `<a>` that has `class="active"` and add `aria-current="page"` to it. (`404.html` has no active link — skip it there.)
2. While you're in each file, note the attribute-order inconsistency for Task 7; don't fix it here unless doing both tasks in one pass.
3. Add a test to `tests/test_integration_links.py` (`TestActiveNav`): on every content page, exactly one `nav.main-nav a` has `class` containing `active`, and that same element has `aria-current="page"`; no other nav link has `aria-current`.
4. Run `pytest tests/ -v`.

---

### Task 6 — Add a skip-to-content link and `id="main-content"` on `<main>`

**Description:** Every page repeats branding + a 6-link nav before `<main>`. There is no skip link, and `<main>` has no `id` to target.

**Justification:** Keyboard and screen-reader users must traverse the full nav on all 22 page loads. A visually-hidden-until-focused skip link is the standard remedy and pays off site-wide because the chrome is shared.

**Steps:**
1. In all 22 pages, change `<main class="content-wrapper">` to `<main id="main-content" class="content-wrapper">`.
2. In all 22 pages, add as the **first** child of `<body>`, before `<header>`:
   `<a class="skip-link" href="#main-content">Skip to content</a>`
3. In `css/style.css`, add:
   ```css
   .skip-link {
     position: absolute;
     left: -9999px;
     top: 0;
     background: var(--bg);
     color: var(--accent);
     padding: 0.5rem 1rem;
     z-index: 100;
   }
   .skip-link:focus {
     left: 0;
   }
   ```
4. Add a test to `tests/test_unit_html_structure.py`: every page has `a.skip-link[href="#main-content"]` as the first focusable element, and a `main#main-content` exists.
5. Manually verify: load a page, press Tab once — the skip link should appear; press Enter — focus jumps past the nav.
6. Run `pytest tests/ -v`.

---

### Task 7 — Normalize internal-link style and attribute order across `core/`

**Description:** `core/syllabus.html` and `core/schedule.html` link to sibling core pages as `../core/x.html`; `assignments.html`, `policies.html`, `about.html` use bare `x.html`. Separately, some pages write `<a href="…" class="active">` and others `<a class="active" href="…">`.

**Justification:** Both link forms resolve, so this is not a bug — but it proves the pages weren't emitted from one template and it will trip the next editor. One convention makes future edits mechanical.

**Steps:**
1. **Link style:** In every `core/*.html` file, rewrite sibling links to the bare form: `../core/syllabus.html` → `syllabus.html`, etc. Links from `core/` up to root stay `../index.html`; links from `core/` into `weeks/` stay `../weeks/week-XX.html`.
2. **Attribute order:** Standardize every nav `<a>` to `<a href="…" class="active" aria-current="page">` (href first). Apply across all 22 pages so the nav block is byte-identical except for which link is active.
3. Re-run the existing `test_all_internal_links_resolve` and `test_nav_links_resolve` — they must still pass.
4. Optionally add a test asserting the `<nav class="main-nav">` inner HTML (with the active markers stripped) is identical across all content pages — this locks the nav against future drift.
5. Run `pytest tests/ -v`.

---

## Medium Criticality

### Task 8 — Add `aria-label` to `<nav>`

**Description:** `<nav class="main-nav">` has no accessible name.

**Justification:** Cheap WCAG best practice; disambiguates if a second nav (e.g. a weeks sub-nav) is ever added.

**Steps:**
1. In all 22 pages, change `<nav class="main-nav">` to `<nav class="main-nav" aria-label="Primary">`.
2. Extend the Task 5/7 nav test (or add one) asserting `nav.main-nav[aria-label]` on every page.
3. Run `pytest tests/ -v`.

---

### Task 9 — Add `scope` attributes to all table headers

**Description:** Every `<th>` in every data table omits `scope`. Several tables have both a header row and a header column.

**Justification:** WCAG 1.3.1 (Info and Relationships). Without `scope`, a screen reader can't reliably associate a cell with its header, which matters for the grading, weights, and schedule tables students will actually read with AT.

**Steps:**
1. For each `<table>` in `core/*.html` and `index.html`:
   - `<th>` cells in the first `<tr>` that label columns → `scope="col"`.
   - `<th>` cells that are the first cell of a row and label that row (e.g. "Instructor", "Schedule", "A", "B") → `scope="row"`.
2. Watch the mixed tables: `syllabus.html` "Course Details" has row headers; "Summary of Assignments and Weights" has a column-header row plus a `<th>Total</th>` row-header in the last row.
3. Add a test to `tests/test_unit_html_structure.py`: every `<th>` in the site has a `scope` attribute of `col` or `row`.
4. Run `pytest tests/ -v`.

---

### Task 10 — Add `rel="noopener noreferrer"` to external links

**Description:** Outbound links (YouTube, danluu, DataCamp on `week-02.html`, and any similar links elsewhere) carry no `rel`.

**Justification:** Harmless now (no `target="_blank"`), but forward-safe: if any link is later switched to open in a new tab, `rel="noopener"` must accompany it or the new tab can script `window.opener`. Adding it now removes a future footgun.

**Steps:**
1. Grep for external links: `grep -rn 'href="https\?://' --include=*.html`.
2. For each `<a>` whose href is `http(s)://` and not a `kenyon.edu` / `github.com/jon-chun` internal reference, add `rel="noopener noreferrer"`. Leave `target` alone (same-tab is fine).
3. Add a test to `tests/test_integration_links.py`: every `<a>` with an `http(s)` href has `rel` containing `noopener`.
4. Run `pytest tests/ -v`.

---

### Task 11 — Resolve the partial Markdown week sources and empty template

**Description:** `weeks/` has `week-01.md` and `week-02.md` only (not 03–15), plus a zero-byte `week-template.md`.

**Justification:** A "regenerate HTML from Markdown" workflow that covers 2 of 15 weeks, seeded by an empty template, is a trap: it looks like a source of truth but isn't. Make the `.html` files unambiguously canonical, or make the `.md` set complete and correct.

**Steps (pick ONE path):**
- **Path A — HTML is canonical (recommended, least work):**
  1. `git rm weeks/week-01.md weeks/week-02.md weeks/week-template.md`.
  2. Add a short `weeks/README.md` (or a note in the top-level README) stating the `week-*.html` files are hand-maintained and are the source of truth.
- **Path B — Markdown is canonical:**
  1. Write `weeks/week-template.md` with the real skeleton (INTRODUCTION / per-day sections / READINGS / CODING / PRESENTATIONS), matching `week-02.md`'s structure.
  2. Create `week-03.md` … `week-15.md` by reverse-engineering each existing `week-XX.html` body.
  3. Fix `week-01.md` per Task 1.
  4. Document the regeneration command/step in the README.
2. Run `pytest tests/ -v` (unaffected — `.md` files aren't tested — but confirm the `*.html` count is still exactly 22).

---

### Task 12 — Untrack non-site files; delete `docs/r`

**Description:** `git ls-files` tracks `.DS_Store` and `2026-09-01-161322-1-analyze-this-website-code-base-and-critique-it.txt` (a saved Claude Code session transcript). The working tree also has `docs/r`, a stray executable byte-for-byte copy of `docs/manual_mp1-setup-redesign-course-website_v1_20260901.md`.

**Justification:** `.DS_Store` is OS cruft that never belongs in a repo; the transcript is not site content; `docs/r` is an accidental `cp` artifact. Removing them makes `git status` clean and the repo legible.

**Steps:**
1. `git rm --cached .DS_Store`
2. `git rm --cached "2026-09-01-161322-1-analyze-this-website-code-base-and-critique-it.txt"` — then decide: delete the file, or move it under a git-ignored `scratch/` dir if you want to keep it locally.
3. `rm docs/r` (verify first: `diff docs/r docs/manual_mp1-setup-redesign-course-website_v1_20260901.md` should report no differences).
4. `git rm --cached notes/subscription-zai-glm-coder.md` and move it out of the repo, or keep it only if the instructor wants it here — it's unrelated to the site.
5. Add `.DS_Store` to `.gitignore` (folded into Task 13).
6. `git status` should now be clean apart from your intended changes. Run `pytest tests/ -v`.

---

### Task 13 — Trim `.gitignore` to match the actual project

**Description:** The committed `.gitignore` is the full GitHub Python-application template (Django, Flask, Scrapy, Jupyter, poetry/pdm/pixi, Streamlit, marimo, …) for a repo whose only Python is `tests/`.

**Justification:** It over-ignores harmlessly but misrepresents the project to any reader. A short, purpose-built ignore file is self-documenting.

**Steps:**
1. Replace `.gitignore` with:
   ```gitignore
   # Python test tooling
   __pycache__/
   *.py[cod]
   .pytest_cache/
   .venv/
   venv/

   # OS / editor cruft
   .DS_Store
   *.swp
   .idea/
   .vscode/
   ```
2. Confirm nothing currently ignored-and-wanted becomes tracked: `git status --ignored` before and after.
3. Run `pytest tests/ -v`.

---

### Task 14 — Add `robots.txt` and `sitemap.xml`

**Description:** Neither file exists at the site root.

**Justification:** One-file, zero-maintenance each. `sitemap.xml` aids crawlability and lets you exclude `404.html`; `robots.txt` lets you suppress indexing entirely if the site should stay low-visibility until an official launch.

**Steps:**
1. Decide the canonical base URL with the instructor (e.g. `https://theailab.net/` or a GitHub Pages URL). If there is no public URL yet, still add the files with a placeholder and a `TODO` **outside** the HTML pages (the stub-text test only scans `*.html`).
2. Create `robots.txt`:
   ```
   User-agent: *
   Allow: /
   Sitemap: https://EXAMPLE/sitemap.xml
   ```
   (Use `Disallow: /` instead if the site should not be indexed yet.)
3. Create `sitemap.xml` listing the 21 content pages (not `404.html`), each as a `<url><loc>` entry. Generate it from the file list rather than hand-typing.
4. Add a test to `tests/test_e2e_site.py`: both files exist; `sitemap.xml` parses as XML and contains exactly the 21 content-page paths; `404.html` is absent from it.
5. Run `pytest tests/ -v`.

---

### Task 15 — Add Open Graph / Twitter Card + canonical metadata

**Description:** No `og:*`, `twitter:card`, or `<link rel="canonical">` anywhere.

**Justification:** Course links shared in Slack/email currently unfurl as a bare URL. OG tags give a title + description preview. Canonical URLs prevent duplicate-content ambiguity if the site is ever mirrored.

**Steps:**
1. Requires a canonical base URL (see Task 14 step 1).
2. In the shared `<head>` of all 22 pages, after `<title>` and the meta description, add:
   ```html
   <link rel="canonical" href="BASE/PAGE_PATH"/>
   <meta property="og:type" content="website"/>
   <meta property="og:site_name" content="IPHS 400: Frontiers in AI"/>
   <meta property="og:title" content="PAGE TITLE"/>
   <meta property="og:description" content="SAME AS META DESCRIPTION"/>
   <meta property="og:url" content="BASE/PAGE_PATH"/>
   <meta name="twitter:card" content="summary"/>
   ```
   `PAGE_PATH` is the page's path from the site root (`/`, `/core/syllabus.html`, `/weeks/week-03.html`, …).
3. If you made a favicon/OG image, add `<meta property="og:image" content="BASE/og-image.png"/>` (1200×630).
4. Add a test: every content page has `og:title`, `og:description`, `og:url`, and a `canonical` link, and `og:description` equals the page's `meta[name=description]` content.
5. Run `pytest tests/ -v`.

---

## Low Criticality

### Task 16 — Remove dead CSS from `css/style.css`

**Description:** ~230 of ~620 lines target classes no page uses (WordPress-theme carryover).

**Justification:** Roughly 40% of the stylesheet is unreachable. It carries `mix-blend-mode`, `object-fit`, a 100vh hero, and blog-index machinery that will never render, and makes the file hard to reason about.

**Steps:**
1. Confirm each candidate is unused: for each class, `grep -rn "CLASSNAME" --include=*.html .` returns nothing. Candidates:
   `.site-header.has-featured-image`, `.featured-media` (+ `::after`), `.social-nav`, `.entry-meta`, `.entry-footer`, `.post-nav`, `.share-links`, `.post-preview`, `.other-blog-pages`, `.wp-block-image`, `.wp-block-separator`, `.badge*`, `.placeholder-notice`, `.columns`, `.page-meta`.
2. Keep `.page-meta` **only if** doing Task 17; otherwise remove it too.
3. Delete the confirmed-dead rule blocks. Also simplify `.site-header` selectors that only existed to contrast with `.has-featured-image` (e.g. `.site-header.no-featured-image .main-nav li a` can become `.site-header .main-nav li a` once the featured variant is gone) — but do this conservatively and diff the rendered pages before/after.
4. Add a test to `tests/` (`test_unit_css.py`, new file): parse `css/style.css` for class selectors and assert each appears in at least one HTML file. Allow an explicit ignore-list (e.g. `.skip-link` states, `.page-meta` if kept). This prevents dead CSS from creeping back.
5. Load every page type (home, core, week, 404) locally and compare against a pre-change screenshot. Run `pytest tests/ -v`.

---

### Task 17 — Add a "Last updated" indicator using the existing `.page-meta` class

**Description:** `syllabus.html` tells readers the schedule "may be updated during the semester" and that GitHub is "the authoritative version," but no page shows when it last changed. `css/style.css` already defines an unused `.page-meta` class evidently meant for this.

**Justification:** Closes the gap between what the syllabus promises and what the page delivers, and puts the already-designed CSS hook to use.

**Steps:**
1. In `core/syllabus.html` and `core/schedule.html`, add directly after the `.breadcrumbs` div:
   `<p class="page-meta">Last updated: 2026-09-03</p>`
   (extend to all content pages if you prefer site-wide consistency).
2. Decide whether the date is maintained by hand or by a tiny script/hook that stamps the file's last git-commit date. If by hand, add a line to the README's contribution notes reminding editors to bump it.
3. Add a test asserting `syllabus.html` and `schedule.html` each contain a `.page-meta` element matching `Last updated: \d{4}-\d{2}-\d{2}`.
4. Run `pytest tests/ -v`.

---

### Task 18 — Make the GitHub repo URL a real link

**Description:** In `syllabus.html` and `about.html`, `https://github.com/jon-chun/theailab-net` is marked up as `<code>` text.

**Justification:** Readers currently copy-paste it. One `<a>` wrap fixes it.

**Steps:**
1. In both files, change `<code>https://github.com/jon-chun/theailab-net</code>` to
   `<a href="https://github.com/jon-chun/theailab-net" rel="noopener noreferrer"><code>github.com/jon-chun/theailab-net</code></a>`
   (keeping `<code>` inside the link preserves the monospace styling).
2. Run the link-integrity test — external links aren't checked for resolution, so this is safe — and `pytest tests/ -v`.

---

### Task 19 — Add footer links (repo, license)

**Description:** Every footer is plain text: `IPHS 400: Frontiers in AI · Kenyon College`.

**Justification:** For a public, MIT-licensed academic site, a footer link to the repo and license is a small standard courtesy and improves discoverability.

**Steps:**
1. In the shared footer of all 22 pages, add after the existing `<p>`:
   `<p class="footer-links"><a href="BASE_OR_RELATIVE/LICENSE">License</a> · <a href="https://github.com/jon-chun/theailab-net" rel="noopener noreferrer">Source</a></p>`
   Use a root-relative or correctly-`../`-prefixed path for `LICENSE` depending on page depth, or just link the GitHub `LICENSE` URL to avoid serving a bare file.
2. Add minimal CSS if needed (`.footer-links { margin-top: 0.5rem; }`) — the footer already has an `a` colour rule.
3. Update the footer-text test if it asserts exact footer HTML (it currently only checks the course string is *present* via `get_text()`, so adding a second `<p>` is fine). Run `pytest tests/ -v`.

---

### Task 20 — Add a print stylesheet

**Description:** No `@media print` block. Printing any page includes the nav, hero, and the decorative `.hero h1::before` rule, and keeps the narrow 640px column.

**Justification:** The syllabus is among the most-printed pages of any course site (advising, financial aid, students without a laptop in class).

**Steps:**
1. Append to `css/style.css`:
   ```css
   @media print {
     .skip-link,
     .site-header .main-nav,
     .breadcrumbs,
     .site-footer { display: none; }
     .hero h1::before { display: none; }
     body { font-size: 12pt; color: #000; background: #fff; }
     .content-wrapper,
     .hero { margin-left: 0; max-width: none; }
     a { color: #000; text-decoration: underline; }
     .page-content a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 0.85em; }
   }
   ```
2. Print-preview `syllabus.html`, `schedule.html`, and a week page in the browser; adjust.
3. No test needed (visual). Run `pytest tests/ -v` to confirm nothing regressed.

---

### Task 21 — Collapse duplicate blue tokens and drop the phantom font name

**Description:** `--accent: #0073aa` and `--primary: #0073a8` differ by one hex digit; the header comment cites a third value. `--fh` and `--fb` both begin with `"NonBreakingSpaceOverride"`, a Twenty Nineteen hack that resolves to nothing.

**Justification:** Cruft that misleads anyone tuning the palette or the type stack.

**Steps:**
1. Decide the one canonical blue (recommend `#0073aa`, the link colour). Replace all `--primary` uses with `--accent` (most `--primary` uses are in dead CSS removed by Task 16 anyway), then delete the `--primary` declaration. Update the top-of-file comment to match reality.
2. Remove `"NonBreakingSpaceOverride", ` from the start of both `--fh` and `--fb`.
3. Load every page type and confirm no visual change. Run `pytest tests/ -v`.

---

### Task 22 — Add `:focus-visible` styling

**Description:** Links rely on the browser default focus ring, even though hover/active states are customized.

**Justification:** Keeps keyboard navigation legible and consistent with the site's visual language.

**Steps:**
1. In `css/style.css`, add:
   ```css
   a:focus-visible,
   .main-nav li a:focus-visible {
     outline: 2px solid var(--accent);
     outline-offset: 2px;
     text-decoration: underline;
   }
   ```
2. Tab through a page and confirm every interactive element shows a clear ring.
3. Run `pytest tests/ -v`.

---

### Task 23 — Add a `Course` JSON-LD block

**Description:** No structured data anywhere.

**Justification:** Low cost; helps search engines and any course-aggregator tooling understand the page, and models the "professional public artifact" practice the syllabus asks of students.

**Steps:**
1. In `index.html` (or `core/syllabus.html`), add before `</head>`:
   ```html
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "Course",
     "name": "IPHS 400: Frontiers in AI",
     "description": "SAME AS PAGE META DESCRIPTION",
     "provider": { "@type": "CollegeOrUniversity", "name": "Kenyon College" },
     "url": "BASE/",
     "inLanguage": "en"
   }
   </script>
   ```
2. Validate the JSON with a linter and against schema.org's validator.
3. Add a test asserting the block exists on the chosen page and parses as valid JSON.
4. Run `pytest tests/ -v`.

---

### Task 24 — Add an HTML-validity check to the local workflow

**Description:** The pytest suite parses leniently (`lxml`) and checks this site's invariants, but nothing validates HTML5 — unclosed tags, duplicate `id`s, invalid attribute values would pass.

**Justification:** Rounds out the existing discipline for the price of one dependency and one command.

**Steps:**
1. Add `html5validator` (or `htmlhint`) to `tests/requirements.txt`.
2. Add `tests/test_html_valid.py`: for each of the 22 pages, run the validator and assert zero errors. Or, if you prefer keeping it out of pytest, add a `Makefile` target `validate:` and document it in the README's "Running the Tests" section.
3. Fix whatever the validator flags — expect at least: the blank line between `<!DOCTYPE html>` and `<html>` (cosmetic, validator may tolerate), any stray unclosed tags, and confirm no duplicate `id`s once Task 6 adds `id="main-content"`.
4. Run the full suite.

---

## Cross-cutting notes

- **Tasks that touch the shared `<head>`/header/footer (3, 4, 5, 6, 7, 8, 15, 19, 23)** are best batched into as few passes over the 22 files as possible. Consider doing Tasks 3–8 as one editing pass per file, then one test-writing pass.
- **Tasks 14, 15, 23** all need the canonical public base URL. If it isn't decided yet, do Tasks 3–13 and 16–22 first and revisit these three once the instructor confirms where the site will live.
- **Task 16 (dead CSS)** should come after Tasks 6, 17, 20, 22 add their new rules, so you delete and add in a coherent final CSS pass rather than fighting merge noise.
- Every task above keeps `pytest tests/ -v` green and adds coverage where "done" is otherwise unobservable. If any existing test needs to *change* (not just gain a sibling), call that out explicitly in the task's commit message.

---

*Generated by Claude Code as part of Mini-Project 1, from `docs/report_web-revision_v1_20260903.md`. Re-verify any step that names a specific file, line, or class before acting — the tree changes as tasks land.*
