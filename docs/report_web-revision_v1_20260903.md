# theailab-net Website Review

**Date:** 2026-09-03
**Version:** v1
**Scope:** Full repository as it stands after the Netlify/CI strip — 22 static HTML pages, one shared stylesheet (`css/style.css`), a pytest suite (`tests/`), plus repo hygiene (`.gitignore`, tracked non-site files, partial Markdown sources).
**Reviewer:** Claude Code (automated codebase audit)
**Test status at review:** 25 / 25 passing.

---

## Summary

This is a small, disciplined static site: no build step, no JavaScript, one
stylesheet, a consistent page skeleton (header → nav → hero → `main` →
footer), and a genuinely useful pytest suite that already guards the failure
modes most common in hand-edited multi-page HTML (broken links, drifted nav,
orphaned pages, leftover template branding, stub text). Content is thorough and
internally date-consistent — every session date across `schedule.html` and the
15 week pages lands on the weekday it claims for the real 2026 calendar
(spot-checked: Aug 27 = Thursday, Sep 1 = Tuesday, Sep 3 = Thursday, Oct 6 =
Tuesday, Dec 11 = Friday).

The prior deploy-time critical finding (a catch-all `netlify.toml` redirect to
`/404.html`) is **resolved**: `netlify.toml` and `.github/workflows/` have been
removed and the site is now a standalone local static site. That shifts the
weight of this review onto four areas the test suite does not cover:

1. **Repo hygiene** — several non-site files are tracked or left untracked in
   the working tree; the Markdown week sources are partial and one is wrong.
2. **Accessibility affordances** beyond what semantic HTML gives for free.
3. **SEO / social / discoverability metadata** — absent site-wide.
4. **Dead CSS** — roughly 40% of the stylesheet targets classes no page uses.

None of the site's *prose* is wrong. The findings below are omissions,
inconsistencies, and cruft — not errors in what's written — with two
exceptions noted under High (2.1, 2.2).

Findings are ordered by severity.

---

## 1. Critical

Nothing in the current tree rises to critical. The former critical finding (the
Netlify catch-all redirect) no longer applies now that hosting config has been
removed.

---

## 2. High

### 2.1 `weeks/week-01.md` contains Week 2's content

`weeks/week-01.html` is correct: it describes a single Thursday session on
**August 27** ("Week 1 has no Tuesday class"). But `weeks/week-01.md` — the
Markdown source that a regeneration step would read — describes **Tuesday &
Thursday, September 1 & 3**, "Shell Fundamentals," the Zitron readings, and the
DataCamp Git courses. That is Week 2's material, and it is nearly identical to
`weeks/week-02.md`.

Anyone who rebuilds `week-01.html` from its `.md` (the pattern the recent commit
history shows — "rebuild page body from week-02.md outline") will silently
overwrite the correct Week 1 page with Week 2 content. Fix the source file to
match the real Week 1 outline, or delete it (see 3.3).

### 2.2 Schedule link text disagrees with the week pages' own titles

`core/schedule.html` links to two week pages with titles that don't match the
destination page's `<title>` / `<h1>`:

| Schedule link text | Actual page `<title>` / `<h1>` |
|---|---|
| Week 14: Final Project Work Session **and Poster Development** | Week 14: Final Project Work Session |
| Week 15: Final Project **Poster** Presentations | Week 15: Final Project Presentations |

The tests only check that the *href* resolves, not that link text matches the
target, so this passes CI. Pick the canonical phrasing for each week and make
the schedule link, the `<title>`, the `<h1>`, and the breadcrumb agree.

### 2.3 No `<meta name="description">` on any of the 22 pages

Every page — home, 404, 5 core, 15 weeks — lacks a meta description. This drives
search-result snippets and is the fallback for link unfurls. Each page already
has distinct, well-written opening prose to summarize; this is a one-line
per-page addition.

### 2.4 No favicon

No `<link rel="icon">` anywhere and no icon file in the repo. All 22 pages show
a generic browser icon in tabs and bookmarks. A single `favicon.svg` or
`favicon.ico` at the root plus one `<link>` in the shared `<head>` fixes it.

### 2.5 No `aria-current` on the active nav item

The current page is marked only with `class="active"` (a CSS hook). Sighted
users get an underline; screen-reader users get nothing. Add
`aria-current="page"` alongside `class="active"` on every page's active link
(22 one-attribute edits, or one template change if the pages are regenerated).

### 2.6 Inconsistent internal-link conventions across `core/`

Within `core/`, the six pages disagree on how they link to each other:

- `syllabus.html` and `schedule.html` use `../core/syllabus.html`,
  `../core/schedule.html` — up to root and back down into the same directory
  they already live in.
- `assignments.html`, `policies.html`, `about.html` use bare
  `syllabus.html`, `schedule.html`.

Both forms resolve (the link-integrity tests confirm it), so this is not a bug —
but it signals the pages were not emitted from one template, and it will
confuse the next editor. There's a matching cosmetic drift in attribute order:
some pages write `<a href="..." class="active">`, others `<a class="active"
href="...">`. Normalize to bare sibling-relative links and one attribute order.

---

## 3. Medium

### 3.1 No skip-to-content link, and `<main>` has no `id`

Every page repeats the same branding + 6-link nav before `<main
class="content-wrapper">`. There is no
`<a class="skip-link" href="#main-content">Skip to content</a>` as the first
focusable element, and `<main>` carries no `id` for such a link (or any
deep-link) to target. Keyboard and screen-reader users tab through the full nav
on every one of 22 page loads. Standard fix: add the skip link to the shared
header, give `<main>` `id="main-content"`, and add a few lines of CSS to hide
the link until focused.

### 3.2 `<nav>` has no accessible name

`<nav class="main-nav">` has no `aria-label` (e.g. `aria-label="Primary"`).
With only one nav per page this is minor, but it's a cheap WCAG best practice
and future-proofs against adding a second nav (e.g. a weeks sub-nav).

### 3.3 Markdown week sources are partial and inconsistently tracked

`weeks/` contains `week-01.md` and `week-02.md` but no `.md` for weeks 3–15,
plus a **zero-byte** `week-template.md`. So the "regenerate HTML from Markdown"
workflow the commit history implies only exists for 2 of 15 weeks, and the
template that would seed the rest is empty. Either commit a complete, correct
set of `.md` sources (and a real template), or remove the two partial ones and
the empty template so the `.html` files are unambiguously the source of truth.

### 3.4 Non-site files are committed to the repo

`git ls-files` tracks:

- **`.DS_Store`** — macOS Finder metadata, no business in any repo. Not listed
  in `.gitignore`.
- **`2026-09-01-161322-1-analyze-this-website-code-base-and-critique-it.txt`** —
  a saved Claude Code session transcript (ANSI art banner and all), not site
  content.

Remove both from version control (`git rm --cached`) and add `.DS_Store` to
`.gitignore`.

### 3.5 Untracked files sitting in the working tree

`git status` is not clean on a fresh checkout:

- **`notes/subscription-zai-glm-coder.md`** — a referral-program note for an
  unrelated tool (Z.AI / GLM). Tracked in git already, but unrelated to the
  site; consider moving it out of this repo entirely.
- **`docs/r`** — a byte-for-byte executable copy of
  `docs/manual_mp1-setup-redesign-course-website_v1_20260901.md` with a
  stray name. Almost certainly an accidental `cp`/redirect artifact. Delete it.

### 3.6 `.gitignore` is a full Python-application template

The committed `.gitignore` is the generic GitHub Python template — Django,
Flask, Scrapy, PyBuilder, Jupyter, pipenv/poetry/pdm/pixi, Streamlit secrets,
marimo, and more — for a repo whose only Python is `tests/`. It's harmless (it
over-ignores, never under-ignores) but misleads a reader about what this project
is. A trimmed version — `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`,
`.DS_Store` — is functionally equivalent for this repo and self-documenting.

### 3.7 Table headers lack `scope` attributes

Every data table (Course Details, Assignments & Weights, Grading Scale, the
MP3/4 rubric, Required Accounts, …) omits `scope="col"` / `scope="row"` on its
`<th>` cells. This is WCAG 1.3.1 (Info and Relationships): without it a screen
reader can't reliably associate a data cell with its header. Several tables also
have a header *row* (`<th>` in the first `<tr>`) and a header *column* (`<th>`
as the first cell of each row) — those need `scope="col"` and `scope="row"`
respectively.

### 3.8 External links have no `rel` and open in the same tab

The ~5 outbound links on `week-02.html` (YouTube, danluu, DataCamp) and similar
links elsewhere carry no `rel="noopener noreferrer"` and no `target`. Opening
course-external content in the same tab is a defensible choice, but if any are
switched to `target="_blank"` later, `rel="noopener"` must come with them.
Adding `rel="noopener noreferrer"` now is harmless and forward-safe.

### 3.9 No `robots.txt` or `sitemap.xml`

Neither exists at the site root. Both are one-file, zero-maintenance additions:
a sitemap improves crawlability and lets you exclude `404.html`; `robots.txt`
lets you suppress indexing entirely if the site is meant to stay low-visibility
until an official launch.

---

## 4. Low / Polish

### 4.1 Roughly 40% of `css/style.css` is dead

The stylesheet is a port "measured from programminghumanity.wordpress.com" and
carries the source theme's blog machinery, none of which any page uses. Verified
zero usages across all 22 pages for:

`.has-featured-image`, `.featured-media` (+ `::after` duotone),
`.social-nav`, `.entry-meta`, `.entry-footer`, `.post-nav`, `.share-links`,
`.post-preview`, `.other-blog-pages`, `.wp-block-image`, `.wp-block-separator`,
`.badge` / `.badge-draft` / `.badge-private` / `.badge-placeholder`,
`.placeholder-notice`, `.columns`, `.page-meta`.

That's ~230 of ~620 lines. The blog-index and featured-image blocks in
particular pull in `mix-blend-mode`, `object-fit`, and a 100vh hero that will
never render. Delete the unused rules (the test `test_no_placeholder_notice`
even asserts `.placeholder-notice` is never used — so its CSS is guaranteed
dead). Keep `.page-meta` only if you wire up 4.2.

### 4.2 The syllabus promises a "last updated" indicator the pages don't show

`syllabus.html` tells readers the schedule "may be updated during the semester"
and that the GitHub repo is "the authoritative version." No page shows a
last-updated date or links to its history, so a reader can't tell current from
stale content from the page itself. The stylesheet already defines a
`.page-meta` class ("repo addition — quiet") that was evidently designed for
exactly this and never wired up. Add
`<p class="page-meta">Last updated: 2026-09-03</p>` to `syllabus.html` and
`schedule.html` (or all pages), or drop the unused class.

### 4.3 The GitHub repo URL is `<code>`, not a link

In `syllabus.html` and `about.html`, `https://github.com/jon-chun/theailab-net`
is marked up as `<code>` text. Readers must copy-paste it. Make it an `<a>`.

### 4.4 Footer is plain text with no links

Every page's footer is just `IPHS 400: Frontiers in AI · Kenyon College`. For a
public academic site whose repo is MIT-licensed and publicly documented, a
footer link to the repo and/or the `LICENSE` is a small standard courtesy.

### 4.5 No print stylesheet

A syllabus is among the most-printed pages of any course site. There is no
`@media print` block, so printing includes the nav, the hero, and the
decorative `.hero h1::before` underline, and keeps the narrow `--mw: 640px`
column instead of using the page width. A short print block (hide
`.site-header nav`, `.hero::before`, `.breadcrumbs`; widen `.content-wrapper`)
is worth the ~15 lines.

### 4.6 Font stack begins with a non-existent font

`--fh` and `--fb` both start with `"NonBreakingSpaceOverride"` — a Twenty
Nineteen hack carried over verbatim. It resolves to nothing and falls through to
the real fallbacks, so it's harmless, but it's confusing cruft; drop it.

### 4.7 Two near-identical blue tokens

`--accent: #0073aa` (used for links) and `--primary: #0073a8` (hero tint, and
only referenced by now-dead featured-image CSS) differ by one hex digit and the
header comment describes a third value (`#0073a8` "primary #0073a8"). Collapse
to one token. Both current text colors clear WCAG AA on white (`--text-lt`
#767676 ≈ 4.5:1; `--accent` #0073aa ≈ 4.5:1) — fine, but `--accent` is close
enough to the threshold that any future lightening should be contrast-checked.

### 4.8 No focus-visible styling

Links rely on the browser default focus ring. Given the site already customizes
underline thickness and offset for `:hover` and `.active`, an explicit
`:focus-visible` treatment (matching or stronger than hover) would keep keyboard
navigation legible and consistent with the visual language.

### 4.9 `<head>` metadata gaps beyond description

No `<link rel="canonical">`, no Open Graph / Twitter Card tags, no theme-color,
no JSON-LD. For a course site meant to be shared in Slack/email, OG tags
(`og:title`, `og:description`, `og:type`, `og:url`) are the highest-value of
these; a `Course` JSON-LD block on the home or syllabus page is a nice-to-have
that models the "professional public artifact" practice the syllabus asks of
students.

### 4.10 No HTML-validity check anywhere

The pytest suite parses with `lxml`'s lenient parser and checks this site's
specific invariants well, but nothing checks HTML5 validity — unclosed tags,
duplicate `id`s, invalid attribute values would pass. A single
`html5validator`/`htmlhint` invocation (in a `Makefile`, a pre-commit hook, or a
test) would round out the existing discipline. The `<!DOCTYPE html>` followed by
a blank line then `<html>` in every file is valid but unusual — a validator or
formatter pass would normalize it.

---

## 5. What's already good (preserve, don't regress)

- **The pytest suite is strong for its scope.** Doctype, title suffix, CSS
  resolution, header/footer/hero presence, no leftover branding, no stub text,
  all internal links resolve, nav identical and correct across all 22 pages,
  schedule links all 15 weeks, exact page-count and exact file-set assertions,
  and full BFS reachability from `index.html`. This is more rigorous than most
  static sites of this size, and it already catches the most common class of
  hand-edited-HTML bug.
- **Date consistency.** Every session date, the October Break window,
  Thanksgiving recess, and the exam period are internally correct against the
  real 2026 calendar.
- **Content quality.** Syllabus, policies, and assignments are unusually
  complete — clear grading breakdowns, an explicit non-punitive AI-use policy,
  secrets-hygiene baked into course content, and a deliberate non-AI-maximalist
  carve-out for the final poster prose.
- **Architecture matches its stated goals.** No build, no JS, one stylesheet,
  custom-property theming, sensible responsive breakpoints (1024px / 768px).
  The whole site is auditable in one sitting.
- **The Netlify/CI strip was clean.** `netlify.toml` and `.github/workflows/`
  are gone, the README's deployment section is replaced with local-serving
  instructions, and no page content changed. The former catch-all-404 redirect
  risk is fully retired.

---

## 6. Suggested priority order

1. **Fix `weeks/week-01.md` (2.1) and the schedule/title mismatches (2.2)** —
   these are the only findings where something is actually *wrong* rather than
   merely absent.
2. **Repo hygiene batch (3.3–3.6):** untrack `.DS_Store` and the session
   transcript, delete `docs/r`, decide the fate of the partial `.md` sources
   and empty template, trim `.gitignore`. All low-risk, makes `git status`
   clean, one commit.
3. **Accessibility batch (2.5, 3.1, 3.2, 3.7):** `aria-current` on active nav,
   skip link + `id="main-content"` on `<main>`, `aria-label` on `<nav>`,
   `scope` on table headers. One shared-template change replicated across
   pages.
4. **Metadata batch (2.3, 2.4, 3.9, 4.9):** per-page meta description, a
   favicon, `robots.txt`/`sitemap.xml`, canonical + OG tags. Batchable,
   low-risk.
5. **Normalize `core/` link style and attribute order (2.6).**
6. **CSS cleanup (4.1)** and the remaining Section 4 polish, prioritizing 4.2
   (last-updated indicator) since the syllabus text explicitly promises it and
   the CSS hook is already sitting unused.

---

*Generated by Claude Code as part of Mini-Project 1. Every finding above was
checked against the working tree at review time; re-verify any that name a
specific file or line before acting, since the tree changes as tasks land.*
