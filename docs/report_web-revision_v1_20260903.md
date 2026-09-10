# Website Code Review — IPHS 400 Course Site (theailab-net)

**Report date:** 2026-09-03
**Repository:** `Avulpix0412/theailab-net` (local clone: `~/code`)
**Branch reviewed:** `main` @ `4184aa1` ("Migrate IPHS 400 course site from ai-swe-best-practices"), reviewed **after** Step H.0 (Netlify/GitHub Actions removal) was applied
**Reviewer:** Claude Code, static analysis of the full repository

## 1. Executive Summary

The site is a clean, dependency-free static HTML/CSS course site (22 pages, one shared stylesheet, no build step, no JavaScript) with a genuinely good pytest suite (25 tests, all passing) that checks structural integrity, navigation consistency, and link resolution. That test discipline is the strongest part of this codebase and is worth preserving as the site grows.

This review supersedes `report_web-revision_v1_20260901.md`. The earlier report was written before the site's Netlify/GitHub Actions deploy pipeline was stripped (Step H.0); its two "critical" findings (a wrong-looking GitHub URL and a non-functional Netlify deploy) are now moot — the deploy pipeline no longer exists, and the GitHub URL findings below are re-verified as **not actually errors**. What remains, once the deploy-pipeline noise is removed, is a smaller set of real issues: an all-manual 22-file HTML structure with no templating/include mechanism, a large amount of dead CSS carried over from the WordPress theme this site was visually cloned from, and a handful of accessibility/SEO omissions typical of a hand-authored static site.

| Severity | Count |
|---|---|
| High | 1 |
| Medium | 5 |
| Low | 4 |

## 2. Scope & Methodology

- Read every file in the repository after Step H.0: `index.html`, `404.html`, all 5 `core/*.html` pages, all 15 `weeks/*.html` pages, `css/style.css`, `README.md`, `LICENSE`, `.gitignore`, and the `tests/` suite.
- Ran the pytest suite locally (`pytest tests/ -v`) — **25/25 passed**, post-Netlify-removal.
- Grepped across all pages for GitHub URLs, favicon links, meta description/Open Graph tags, `<img>` tags, `mailto:` links, and `target="_blank"` usage.
- Diffed header/nav/footer markup across sample pages to confirm the boilerplate is hand-duplicated per file, not templated.
- Did not run a browser-based visual QA pass (no rendered screenshots) or an automated accessibility/contrast scanner — findings on contrast and focus states below are derived from reading the CSS rules, not a live audit tool.

## 3. Site Overview

- **Structure:** `index.html` + `404.html` at root, `core/` (syllabus, schedule, assignments, policies, about — 5 pages), `weeks/` (week-01 through week-15 — 15 pages). 22 pages total, verified by `test_e2e_site.py`.
- **Styling:** single `css/style.css` (620 lines), a hand-ported clone of the WordPress "Twenty Nineteen" theme (per the file's own header comment), used to visually match the instructor's other Kenyon course sites.
- **No JS, no build step, no external dependencies** for viewing the site — only the test suite has Python dependencies (`tests/requirements.txt`: pytest, beautifulsoup4, lxml).
- **Local-only now:** as of Step H.0, there is no deploy config, no CI, and no live-site link anywhere in the repo. The README's Local Development instructions (`python3 -m http.server`) are the only way to view the site, which is consistent with the rest of the docs.

## 4. Findings

### 4.1 [HIGH] No templating/include mechanism for 22 pages of duplicated boilerplate

Every page hand-repeats the identical header, nav, and footer markup (confirmed: `week-01.html` and `week-05.html` differ only in the `<h1>` text and `class="active"` position within that block). The nav-consistency tests (`test_all_nav_pages_have_identical_nav_labels`, `test_nav_links_resolve`) exist specifically because this duplication is otherwise unenforced — a future edit to the nav (e.g., adding a page) means editing the same 6-line `<nav>` block in 22 separate files by hand, with only the test suite catching a page that got missed.

This is fine at 22 pages but is a real scaling risk: the course site will grow (more weeks are already templated 1–15, but a real course typically accretes handouts, resource pages, etc.). A missed manual edit is currently caught by tests *after* the fact, not prevented.

**Recommendation:** Not urgent to fix before this is a graded deliverable, but worth a paragraph in any revision plan: either (a) accept the duplication as a deliberate "no build step" tradeoff and lean harder on the test suite as the safety net, or (b) introduce a minimal include mechanism (even a simple Python script that stitches a shared `_header.html`/`_footer.html` into each page at "build" time, writing static output — no client-side JS required) if the page count is expected to keep growing.

### 4.2 [MEDIUM] ~150 lines of dead CSS from the WordPress theme port

`css/style.css` defines rules for `.has-featured-image`, `.featured-media`, `.social-nav`, `.entry-meta`, `.entry-footer`, `.post-nav`, `.share-links`, `.badge`/`.badge-draft`/`.badge-private`/`.badge-placeholder`, `.placeholder-notice`, `.post-preview`, `.columns`, and `.wp-block-*` — none of which appear in any of the 22 HTML pages (verified by grep: zero matches for `has-featured-image` across all `.html` files, and the others are blog/WordPress-post concepts this static course site has no use for). This is leftover styling from the "Twenty Nineteen" theme clone that was never trimmed after the visual-parity pass.

**Recommendation:** Remove the unused rule blocks, or if some are intentionally kept for a near-future page type (e.g., a blog-style news page), say so in a comment — currently there's no way to tell "dead" from "reserved for later" apart.

### 4.3 [MEDIUM] No favicon

No page links a favicon (`grep -rl favicon` across all HTML returns nothing). Every browser tab shows a generic icon. Trivial to add, easy to forget.

**Recommendation:** Add a `favicon.ico`/`favicon.svg` at the root and a `<link rel="icon">` in every page's `<head>` (or better: add it once and have the existing header/footer-consistency tests extended to check for its presence, so it can't silently regress).

### 4.4 [MEDIUM] No meta description or Open Graph tags

No page has a `<meta name="description">` or `og:*` tags. For a course site that students and prospective students may link to or that gets indexed, this means search engines and any link-preview card (Slack, email, etc.) show nothing useful.

**Recommendation:** Add a per-page `<meta name="description">` at minimum; Open Graph tags are a nice-to-have if the site is ever going to be shared as a link outside class.

### 4.5 [MEDIUM] No accessibility "skip to content" link

Every page repeats the same 6-item nav before reaching page content, with no skip link for keyboard/screen-reader users to jump past it. This is a standard, cheap accessibility fix that's currently entirely absent (`grep -rl skip` returns nothing).

**Recommendation:** Add a visually-hidden-until-focused `<a href="#main" class="skip-link">Skip to content</a>` as the first element in `<body>`, and `id="main"` on the `<main class="content-wrapper">` element (already present, just needs the id).

### 4.6 [MEDIUM] Wide tables have no horizontal-scroll wrapper on mobile

`css/style.css`'s `.page-content table` rules (`width: 100%`) don't include an `overflow-x: auto` wrapper `<div>`, and none of the pages wrap their `<table>` elements in one. The syllabus page's tables (up to 3 columns of prose, e.g. the assignments-and-weights table) risk clipping or forcing horizontal page scroll on narrow phone screens, where the mobile breakpoint at 768px only reduces font size, not table layout strategy.

**Recommendation:** Wrap `<table>` elements in a `<div style="overflow-x:auto">` (or a `.table-wrap` class) at the two or three pages that actually use tables (syllabus, and any future policy/schedule tables), and add a general rule in the CSS.

### 4.7 [LOW] GitHub URL in content is correct but easy to misjudge on re-review

`core/syllabus.html` and `core/about.html` both reference `https://github.com/jon-chun/theailab-net` as the canonical "Course Site." This is **not an error** — it correctly points to the instructor's upstream repo, distinct from a given student's personal fork (e.g. `Avulpix0412/theailab-net`). Flagging this explicitly because the previous review (Sept 1) treated a related URL as a "critical" bug; on closer reading it is intentional (course materials live at the instructor's canonical repo regardless of whose fork a given student is viewing the site from). No action needed — noted here only so a future reviewer doesn't re-flag it without checking.

### 4.8 [LOW] Test suite doesn't cover the new omissions above

The 25 existing tests check DOCTYPE, title suffix, CSS link resolution, header/footer/hero presence, nav consistency, internal link resolution, and no-leftover-branding/placeholder text — all solid. They do not check for favicon presence, meta description presence, or any accessibility markers (skip link, heading order). If 4.3–4.5 above are fixed, extending the test suite to assert their presence would keep them from silently regressing later, consistent with this repo's existing test-first discipline.

### 4.9 [LOW] No `robots.txt` or `sitemap.xml`

Now that the site is explicitly local-only (post Step H.0), this is lower priority than it would be for a publicly deployed site — but worth a one-line note in the tech-spec in case a future step re-adds public hosting, since these are typically forgotten until someone asks "why isn't this indexed."

### 4.10 [LOW] `.gitignore` correctly excludes `.venv` — no action needed

Verified with `git check-ignore -v .venv` — the virtual environment created in Part F of the setup manual will not be accidentally committed. Listed here only as a confirmed non-issue, since a leaked/committed venv is a common mistake worth explicitly ruling out.

## 5. What Changed Since the Sept 1 Report

- **Netlify/GitHub Actions removed** (Step H.0): `netlify.toml` and `.github/workflows/deploy-netlify.yml` deleted; README's "Live site" placeholder and "Deployment" section removed and replaced with local-only instructions. This resolves both "critical" findings from the previous report outright — they no longer apply to a repo with no deploy pipeline.
- The GitHub-URL finding from the previous report was re-examined here (4.7) and reclassified as **not a bug**.
- All other findings in this report (dead CSS, missing favicon/meta/skip-link, table overflow, templating) are newly surfaced by this pass and were not called out in the Sept 1 report, which focused heavily on the (now-removed) deploy pipeline.

## 6. Suggested Priority for Next Steps

1. Favicon, meta description, skip link — all small, independent, low-risk fixes (4.3, 4.4, 4.5).
2. Dead CSS removal (4.2) — safe, mechanical, shrinks the file a reviewer has to read.
3. Table overflow wrapper (4.6) — small CSS/markup change.
4. Templating/include mechanism (4.1) — the only finding that's a real design decision, not a quick fix; worth discussing rather than defaulting into.
5. Test coverage extension (4.8) — natural follow-on once 4.3–4.5 land.
