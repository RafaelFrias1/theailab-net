# Phase 1: Engineering Polish — Tech Spec (2026-09-03)

**Source:** synthesized from `docs/report_web-revision_v1_20260903.md`
**Repository:** `Avulpix0412/theailab-net` (local clone: `~/code`)
**Scope:** targeted fixes and additions to the existing 22-page static site. No content rewrite, no restructuring of pages/nav, no redesign. The Netlify/GitHub Actions/wrong-URL findings from the prior report are resolved or moot and are not included here (see report §4.7, §4.10 and §5 for why).

**Relationship to Phase 2:** this document covers engineering correctness and hygiene only (accessibility basics, metadata, dead-code cleanup, test coverage). Visual identity, homepage framing, and the course-map/week-structure exploration are deliberately deferred to `docs/design-spec_phase2_website-revision_v1_20260903.md`, so the two can be reviewed independently.

Tasks are grouped by criticality. Within Part I, work top to bottom; each task should get a test that captures "done" before moving to the next.

---

## HIGH

*(none — this pass surfaced no findings that block the site from being correct/usable as-is; see the templating item under LOW for the one architectural finding, deliberately not ranked higher because it requires a design decision, not a quick fix)*

---

## MEDIUM

### M1 — Add a favicon

**Description:** No page links a favicon; browser tabs show a generic icon.

**Justification:** Report §4.3. Trivial to add, currently entirely absent across all 22 pages, and easy to forget once other work starts — best done early and enforced by a test so it can't silently regress.

**Steps:**
1. Add a simple favicon file (e.g. `favicon.svg` or `favicon.ico`) at the repo root — a plain initials/monogram mark is sufficient, doesn't need to be elaborate.
2. Add `<link rel="icon" href="favicon.svg">` (adjusting the relative path — `favicon.svg` at root, `../favicon.svg` from `core/` and `weeks/`) to the `<head>` of all 22 pages.
3. Add a test to `tests/test_unit_html_structure.py` asserting every page's `<head>` contains a `<link rel="icon">` tag.

### M2 — Add per-page meta description

**Description:** No page has a `<meta name="description">`.

**Justification:** Report §4.4. Affects search indexing and link-preview cards (Slack, email, etc.) if the site is ever shared as a link outside class.

**Steps:**
1. Write a one-to-two-sentence description for each of the 22 pages (e.g. index: "Course website for IPHS 400: Frontiers in AI at Kenyon College."; each week page: a short summary of that week's topic, reusable from the page's existing intro paragraph).
2. Add `<meta name="description" content="...">` to each page's `<head>`.
3. Add a test asserting every page has a non-empty `<meta name="description">`.

### M3 — Add a "skip to content" link for accessibility

**Description:** No skip-navigation link exists; keyboard/screen-reader users must tab through the full 6-item nav on every page before reaching content.

**Justification:** Report §4.5. Standard, low-cost accessibility fix; currently entirely absent.

**Steps:**
1. Add `id="main"` to the existing `<main class="content-wrapper">` element (currently has no id) on all 22 pages.
2. Add a visually-hidden-until-focused `<a href="#main" class="skip-link">Skip to content</a>` as the first child of `<body>` on all 22 pages.
3. Add CSS for `.skip-link`: absolutely positioned off-screen by default, moved on-screen with visible styling on `:focus`.
4. Add a test asserting every page has a `.skip-link` as the first element inside `<body>` and that `<main>` has `id="main"`.

### M4 — Wrap tables for horizontal overflow on mobile

**Description:** `.page-content table` has no `overflow-x: auto` wrapper; wide tables (e.g. the syllabus's assignments-and-weights table) risk clipping or forcing page-wide horizontal scroll on narrow screens.

**Justification:** Report §4.6. The mobile breakpoint at 768px only reduces font size, not table layout strategy.

**Steps:**
1. Wrap every `<table>` element in the pages that use tables (currently: `core/syllabus.html` — course details, assignments/weights, grading scale tables) in a `<div class="table-wrap">`.
2. Add `.table-wrap { overflow-x: auto; }` to `css/style.css`.
3. Add a test asserting every `<table>` in the site has an ancestor `.table-wrap` element.

### M5 — Remove dead CSS from the WordPress theme port

**Description:** `css/style.css` carries ~150 lines of rules (`.has-featured-image`, `.featured-media`, `.social-nav`, `.entry-meta`, `.entry-footer`, `.post-nav`, `.share-links`, `.badge*`, `.placeholder-notice`, `.post-preview`, `.columns`, `.wp-block-*`) that match zero elements across all 22 pages.

**Justification:** Report §4.2. Leftover from the "Twenty Nineteen" WordPress theme clone; adds maintenance burden and reader confusion (can't tell "dead" from "reserved for later").

**Steps:**
1. Grep each class name above against all `.html` files to reconfirm zero usage (already verified in the report, but reconfirm since this task runs after M1–M4 may have touched files).
2. Delete the confirmed-unused rule blocks from `css/style.css`.
3. Run the full pytest suite (a CSS-only change should not break any HTML-structure test, but confirm) and manually reload a couple of pages locally to confirm no visual regression.

### M6 — Extend the test suite to cover M1–M3

**Description:** The existing 25 tests don't check favicon, meta description, or accessibility markers.

**Justification:** Report §4.8. Once M1–M3 land, extending the test suite (already begun inline in each task above) keeps this repo's existing test-first discipline intact and prevents silent regression.

**Steps:**
1. Confirm the three tests added in M1, M2, and M3 are present and passing (this task is mostly a checkpoint, not new work, if M1–M3 were implemented as specified).
2. Run the full suite once more (`pytest tests/ -v`) and confirm the total test count increased from 25 to 28+ and all pass.

---

## LOW

### L1 — Discuss (don't yet implement) a templating/include mechanism

**Description:** All 22 pages hand-duplicate identical header/nav/footer markup. A nav change today means editing the same block in 22 files by hand; only the test suite catches a missed page, after the fact.

**Justification:** Report §4.1. This is a real scaling risk, but it's a design decision (accept the duplication + lean on tests, vs. introduce a build step), not a quick fix — explicitly not ranked HIGH for that reason.

**Steps (discussion only, no code change expected from this task):**
1. Decide: does the site's page count grow meaningfully beyond the current 22 pages this semester? If not, the duplication + existing nav-consistency tests are an acceptable tradeoff for a genuinely zero-build-step site.
2. If growth is expected, scope a minimal include mechanism as a separate follow-up spec (e.g. a small Python script run manually before `git commit` that stitches shared `_header.html`/`_footer.html` fragments into static output — no client-side JS, no server-side includes, keeps the "no build step at view time" property).
3. Record the decision (even "we're keeping the duplication, revisit if page count exceeds ~35") somewhere durable — e.g. a short note added to `README.md`'s Repository Structure section — so a future reviewer doesn't re-flag this without knowing it was already considered.

### L2 — Add `robots.txt` / `sitemap.xml` (deferred)

**Description:** No `robots.txt` or `sitemap.xml` exist.

**Justification:** Report §4.9. Deliberately deprioritized: the site is explicitly local-only as of Step H.0 (no deploy pipeline), so this has no effect until/unless the site is publicly hosted again.

**Steps:**
1. No action needed now. If a future step re-adds public hosting, revisit this task before that hosting goes live — add a one-line reminder in that future spec rather than doing the work now.

---

## Explicitly out of scope for this spec

- The GitHub-URL "finding" from the Sept 1 report (report §4.7) — re-verified as correct, not a bug. No task.
- Netlify/CI config — already removed in Step H.0, before this report was written. No task.
- `.gitignore` venv coverage (report §4.10) — verified correct, no action needed.
