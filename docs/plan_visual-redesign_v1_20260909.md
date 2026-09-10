# Visual Redesign Proposal — theailab-net

**Version:** 1 · **Date:** 2026-09-09 · **Status:** proposal, awaiting direction

## 0. Scope and constraints

**The first step (Phase 1) is a visual-only redesign of the 22-page static
site. It implements NONE of the five features below** — no pipeline diagram, no
colophon page, no dark mode, no search, no current-week highlight, no new
`data-*` attributes, no JavaScript. Phase 1 is CSS plus, at most, mechanical
styling-hook markup edits. Every feature is a separate, later phase (§4).

Nothing in any phase changes course prose, dates, policies, or assignment
content — only presentation and, in later phases, additive non-prose markup and
one new page that documents the build process itself.

**Reference:** al-folio (`https://alshedivat.github.io/al-folio/`, fetched
2026-09-09). Concrete values observed are cited inline as *(al-folio: …)*.
Nothing from al-folio's CSS/JS/assets is copied; the values below are original
and adapted to this site's content and its zero-dependency, hand-authored
architecture.

**Architecture preserved:** no build step, no framework, one stylesheet, every
page a standalone auditable file. The redesign keeps this. The later JS features
add vanilla scripts hand-included per page, the same way the header and footer
are already hand-copied.

---

## 1. Visual design system

### 1.1 Typography

Drop the serif body (`--fh: "Hoefler Text"…`) entirely. Move to a system
sans-serif stack — no web-font download, which matches al-folio's *practical*
result (it renders Roboto) without adding a dependency to a site that
deliberately has none.

| Token | Value |
|---|---|
| `--font-sans` | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Helvetica Neue", sans-serif` |
| `--font-mono` | `ui-monospace, "SF Mono", "Cascadia Code", "Roboto Mono", Menlo, Consolas, monospace` |

*(al-folio: `font-family: Roboto, sans-serif` for body; Roboto Slab is still
loaded but no longer the primary text face. Weights used: 300 / 400 / 500 / 700.)*

**Optional upgrade, not recommended for Phase 1:** self-host Inter or Roboto
Flex as a single `woff2` (~40–100 KB) in `assets/fonts/` and reference it with a
local `@font-face`. Adds a binary asset and a `<link>`/`@font-face` line to
maintain across pages. Defer unless the instructor specifically wants a branded
face.

**Type scale** (down from the current 22px/1.8 serif, which is unusually large):

| Element | Size | Line-height |
|---|---|---|
| body | `1.0625rem` (17px) | `1.65` |
| `.hero h1` | `2.0rem` | `1.15` |
| `h2` | `1.5rem` | `1.25` |
| `h3` | `1.25rem` | `1.3` |
| `h4` | `1.0625rem` | `1.4` |
| `.page-meta`, `small`, footer | `0.875rem` | `1.5` |

Headings: weight 700, `letter-spacing: -0.01em`. Body: weight 400.
*(al-folio container is `max-width: 930px`; headings carry `scroll-margin-top`
for the fixed nav.)*

### 1.2 Color palette

**Recommendation: keep the blue lineage**, deepened for contrast. Rationale:
`favicon.svg` is `#0073aa` and the current `--accent` was flagged in the prior
report as "AA but close to threshold"; a deeper blue fixes the contrast note
and avoids re-cutting the favicon and re-establishing the site's identity color
for no content reason. al-folio's magenta is a theme *default*, not a
requirement — the theme is built to be recolored.

**Light theme** (`:root`)

| Token | Value | Notes |
|---|---|---|
| `--bg` | `#ffffff` | page |
| `--surface` | `#f5f7f9` | cards, code blocks, table header |
| `--text` | `#1a1d21` | ~15:1 on `--bg` |
| `--text-muted` | `#586069` | ~6.3:1 on `--bg` — passes AA for body text |
| `--border` | `#e3e6e9` | |
| `--accent` | `#005a9c` | links; ~6.4:1 on `--bg` (AA, AAA-large) |
| `--accent-hover` | `#003f6e` | |
| `--accent-fg` | `#ffffff` | text on accent fills |
| `--current-week` | `#fff4d6` / border `#e0b400` | Feature 3 highlight (spec'd now, added with that feature) |

**Dark theme** — *not in Phase 1.* Phase 1 ships the `:root` light tokens only,
named generically (`--bg`, `--text`, `--accent`, …) so the dark set is a pure
addition later. These values are specified now only so the dark-mode phase has
no open design questions. Applied under `@media (prefers-color-scheme: dark)`
and `:root[data-theme="dark"]` when Feature 1 ships.

| Token | Value | Notes |
|---|---|---|
| `--bg` | `#16181d` | *(al-folio: `#1c1c1d`)* |
| `--surface` | `#21242b` | *(al-folio card: `#212529`)* |
| `--text` | `#e6e8eb` | *(al-folio: `#e8e8e8`)* |
| `--text-muted` | `#9aa3ad` | ~7:1 on `--bg` |
| `--border` | `#2e333b` | |
| `--accent` | `#5aa9de` | ~6:1 on `--bg` |
| `--accent-hover` | `#8ac6ec` | |
| `--accent-fg` | `#16181d` | |
| `--current-week` | `#3a3320` / border `#e0b400` | |

**Alternative (noted, not recommended):** a warmer academic hue — deep
burgundy `#8a1c1c` light / `#e0736b` dark, or indigo `#3b3ba6` / `#9aa0ee`.
Either would require a matching favicon recut and reads as a larger identity
break for no functional gain.

### 1.3 Spacing, radius, layout

- **Spacing tokens:** `--space-1: 0.25rem` … `--space-8: 4rem` (×2 steps).
  *(al-folio base unit: `0.25rem`.)*
- **Radius:** `--radius: 6px`, `--radius-lg: 10px`. *(al-folio: `.25 / .375 / .5rem`.)*
- **Container:** replace the signature left-offset column
  (`--col-left: calc(8.33vw + 28px)`, `margin-left` on every block) with a
  **centered** column. `--container: 940px` for wide pages (home, schedule),
  `--measure: 46rem` for prose pages. Horizontal padding `--space-4` (1.25rem),
  `--space-2` on mobile. *(al-folio: centered, `max-width: 930px`.)*
- **Header:** convert to a **slim sticky top bar**, ~56px, `--surface`
  background, 1px `--border` bottom, brand left / nav right, wraps below the
  brand on narrow screens. Body gets `padding-top` to clear it; headings get
  `scroll-margin-top`. *(al-folio: `fixed-top`, `padding-top: 57px`,
  `scroll-margin-top: 66px`.)* Nav stays CSS-only (6 items wrap fine); a
  disclosure/hamburger is a later nicety, not Phase 1.
- **Hero:** keep `section.hero > h1` (tests require it) but **remove the
  `.hero h1::before` gray dash**. Render it as a page-title block: generous
  vertical rhythm, optional muted kicker line above (e.g. the breadcrumb trail
  or "Week 4 · Mini-Project 2" — kicker text derived from existing content, no
  new prose).
- **Components restyled:** tables (`--surface` header, `--border` rules, full
  width, left-aligned, ~0.95rem), blockquotes (accent left border, no italic),
  inline/block code (`--surface`, `--radius`, mono), `ul.item-list` and Quick
  Links → bordered list rows with hover state, footer → centered, muted,
  `0.875rem`.
- **Keep** the two existing breakpoints (1024px, 768px) conceptually; retune
  values for the centered layout. **Keep** `:focus-visible` outlines and the
  `@media print` block (retarget the rules that name `.hero h1::before` and the
  left margin, which no longer exist).

### 1.4 What this costs in the stylesheet

`css/style.css` is currently ~444 lines with a test guard at `< 450`
(`test_unit_css.py::test_stylesheet_shrank_below_450_lines`, docstring: "Guard
against the WordPress blog machinery creeping back in"). The Phase 1 redesign
(light tokens + component styles, no diagram, no dark set) will land at roughly
**500–650 lines**; later feature phases add more. This one guard must be relaxed
— raise the cap to `800` and reword the docstring to name the real risk
(blog-machinery class names, not raw line count). Single-line change; **it is
the only test change in Phase 1**.

`test_unit_css.py::test_no_dead_class_selectors` requires every class selector
in the stylesheet to appear in at least one HTML file. **Every new class must be
introduced in markup and CSS together.** Runtime-only classes (later phases) go
on the explicit `ALLOW` list.

---

## 2. The five features

Legend — **Complexity**: S (hours), M (1–2 days), L (multi-day).
**Risk**: chance of breaking content, tests, or the no-dependency architecture.
**None of these is part of Phase 1.** Phase assignments below refer to §4's order.

### Feature 4 — Homepage pipeline diagram · Phase 2 · Complexity M · Risk Low

**Where it fits.** `index.html`, `.page-content`, immediately before
`<h2>Course Details</h2>`. The existing intro `<p>` (the "four mini-projects
that stack on each other" paragraph) stays **verbatim** — see the tension note
below — with the diagram added directly above it as the primary visual element.

**What it depends on.** Nothing technical. The four stages and their
week/mini-project mapping already exist verbatim in `core/schedule.html`
section headings and `core/assignments.html` `<h2>`s:

1. **Development environment** — Weeks 1–2 · Mini-Project 1
2. **Agent configuration & Skills** — Weeks 3–5 · Mini-Project 2
3. **Agent harness & hooks** — Weeks 6–9 · Mini-Project 3
4. **Spec-driven SDLC capstone** — Weeks 10–13 · Mini-Project 4
   → **Final research project** — Weeks 14–15

**Implementation.** A horizontal flow of five nodes joined by arrows. Pure
HTML + CSS for the nodes (flex row → vertical stack under 768px); inline
`<svg>` only for the connecting arrows, or CSS triangles. Each node links to
its `core/schedule.html` section or `core/assignments.html` anchor. Colors via
`currentColor` / tokens so it themes automatically. No JS. New classes
(`.pipeline`, `.pipeline-stage`, …) styled and used together.

**Tension to resolve.** The original brief says "replacing the current plain
paragraph description," but a later hard constraint says written text must not
change. **Recommendation:** keep the paragraph's text intact, place the diagram
above it, and optionally de-emphasize the paragraph visually (smaller, muted).
If the instructor confirms the paragraph itself may be cut or trimmed, that is a
one-line follow-up.

**Test impact.** `.page-content` min-text check still satisfied (paragraph
stays). Inline SVG must pass strict `html5lib` (`test_html_valid.py`) — keep it
well-formed and namespaced. Any node linking off-site (it won't) would need
`rel="noopener noreferrer"`.

### Feature 5 — "How this site was built" / AI changelog page · Phase 3 · Complexity M · Risk Low–Med

**Where it fits.** A **new standalone page**, `core/colophon.html`, linked from
the **footer** (not the primary nav — see test impact). Same skeleton and
`<head>` furniture as every other page.

**What it depends on.** Source material that already exists: the git commits,
the two `docs/` revision reports, and this redesign. Real, documented episodes
to cover honestly:

- The site began as a WordPress "Twenty Nineteen" theme port; Netlify/CI was
  later stripped to make it a standalone local static site (`9bd5b5a`).
- `weeks/week-01.md` contained Week 2's content; resolved by deleting the
  Markdown sources and making the HTML the single source of truth.
- Week 14/15 titles disagreed across `<title>`, `<h1>`, breadcrumb, and the
  schedule link; reconciled.
- A phantom font name (`"NonBreakingSpaceOverride"`) and a duplicate color
  token (`--primary` vs `--accent`) were carried over from the theme and removed.
- ~230 lines of dead WordPress blog CSS removed; a stray `docs/r` file deleted.
- Which prompts mattered: the audit-then-tiered-tasks structure
  (report → 24 numbered tasks → High/Medium/Low commits), and the
  test-suite-as-gate discipline.
- This visual redesign and what had to be corrected during it.

**Content principle.** Written to inform, not to market — concrete about what
was automated, what broke, and what a human had to catch. This page's prose is
*about the build process*, so it is new content but not "course material" and
does not violate the no-content-change constraint. It is inherently a living
document; note that it will be updated as work continues.

**Test impact (the one unavoidable multi-line test change):**

- `test_e2e_site.py::test_exact_total_page_count` — `22` → `23`.
- `test_e2e_site.py::TestCoreDirectoryContents` — add `colophon.html` to
  `EXPECTED_CORE_FILES`.
- Reachability BFS already covers footer links, so a footer link makes the page
  reachable — **no nav change, so `EXPECTED_NAV_LABELS` and the
  byte-identical-nav test stay untouched.** This is why the footer, not the nav,
  is the right home for it.
- The new page must carry all required furniture: unique 50–200-char meta
  description, title with the `– IPHS 400: Frontiers in AI` suffix, skip link
  first, `header.site-header`, `footer.site-footer` with source+license links,
  `section.hero > h1`, `.page-content` ≥ 20 chars.
- Footer changes on **all 22 existing pages** (add the colophon link) — a
  mechanical edit, the same shape as the prior revision's footer-links task.

### Feature 1 — Dark mode · Phase 4 · Complexity S (+S) · Risk Low

**Step 4a (zero JS).** Add the dark palette under
`@media (prefers-color-scheme: dark)`. The site then follows the OS setting
automatically with no script. Pure CSS, building on the Phase 1 token names.

**Step 4b (manual toggle).** Adds:

- `:root[data-theme="dark"]` / `:root[data-theme="light"]` overrides so an
  explicit choice wins over the media query.
- A **blocking inline `<script>` in `<head>` on all 22 pages** that reads
  `localStorage.theme` and sets `data-theme` before first paint (prevents a
  white flash). ~8 lines, hand-copied like the rest of the `<head>`.
- A toggle control in the header — **placed outside `nav.main-nav`** so
  `test_integration_links.py::test_nav_html_identical_across_content_pages`
  (which normalizes and compares the nav subtree) stays green. ~30 lines of
  vanilla JS in `assets/js/theme.js`, hand-included per page.
- Helper classes `.only-light` / `.only-dark` on the `ALLOW` list.

*(al-folio structure, for reference: `<button id="light-toggle">` with three
`<i>` icons (`#light-toggle-system/dark/light`); cycles system → light → dark;
`localStorage.setItem("theme", …)`; `html[data-theme]` +
`html[data-theme-setting]`; listens to
`matchMedia("(prefers-color-scheme: dark)")` `change`.)*

**Depends on:** the Phase 1 token names. **Risk:** low — the FOUC script is the
only subtlety; needs to be identical across 22 files.

### Feature 3 — Auto-highlighted current week · Phase 5 · Complexity S+S · Risk Low–Med

**Step 5a — machine-readable dates (additive markup, no visible change).** The
schedule's dates currently live only as prose ("Tuesday & Thursday,
September 15 & 17"). Add attributes:

- On `core/schedule.html`, wrap each week `<li>` (or add to it)
  `data-week="N" data-start="2026-MM-DD" data-end="2026-MM-DD"`.
- Optionally mirror onto each `weeks/week-NN.html` (`data-week-start/-end` on
  `<main>`).
- A small Python test (existing `pytest` style) asserts all 15 parse, are
  chronological, and match between schedule and week pages.

**Care required:** the 15 date ranges must be transcribed correctly against the
2026 calendar (Week 1 = Thursday only; Week 7 = Tuesday only, per October
Break). The prior revision already verified these dates against the real
calendar, so this is transcription, not research — but it is 15 rows to get
right, hence Risk Low–Med.

**Step 5b — script.** ~20 lines of vanilla JS on `core/schedule.html`: read
`new Date()` client-side, find the `<li>` whose `data-start`…`data-end`
(or the week containing "now") matches, add `.is-current-week`. CSS for
`.is-current-week` (using the `--current-week` tokens spec'd in §1.2) — left
accent bar, subtle background, a "This week" chip. Degrades to nothing with JS
off. Before the semester starts / after it ends, highlight nothing (or the
first / last week — instructor's call).

**Depends on:** step 5a's `data-*` dates. **Independent of** search and dark mode.

### Feature 2 — Client-side search · Phase 6 · Complexity M–L · Risk Med

This is the only feature with a real dependency and maintenance footprint, and
the reason it goes last.

**Where it fits.** A search control in the header (outside `nav.main-nav`, same
as the theme toggle) and a modal overlay opened by click or **Ctrl/Cmd+K**.
Markup + a `<script>` include on all 22 pages.

**Two approaches:**

| | **A. Lightweight (recommended first)** | **B. Full-text (Lunr.js)** |
|---|---|---|
| Index | Page titles + `h2`/`h3` headings only, ~5 KB JSON | Full body text, ~50–150 KB JSON |
| Index generation | ~30-line Python script (`tools/build_search_index.py`), run manually, output committed | Same script, larger output |
| Runtime dep | None (plain substring/fuzzy match in ~40 lines JS) | Lunr.js ~29 KB, **vendored** in `assets/js/` (no CDN, per the standalone-site rule) |
| Staleness | Low stakes — headings change rarely | Higher — every prose edit should trigger a rebuild; a test can assert the index is fresh |
| Value on a 22-page site | Covers the real navigation need | Marginal extra recall for the cost |

*(al-folio itself uses a build-time-generated static command-palette index
(`ninja-keys`), **not** Lunr full-text — even the reference doesn't do true
prose search out of the box.)*

**Recommendation:** ship **A** first. It delivers the Ctrl+K jump-to-page
experience with zero runtime dependency and a trivial index. Treat **B** as a
documented drop-in upgrade if the instructor wants full-text later.

**Depends on:** the index-generation script (a new, if tiny, build step — the
first crack in "no build step," worth calling out honestly in the colophon).
**Test impact:** new test asserting the index file exists and lists all 22
pages; a freshness check if approach B is taken.

---

## 3. What needs restructuring vs what doesn't

### No restructuring — pure CSS + additive markup

- **Phase 1 — the visual redesign (§1):** palette (light only), typography,
  spacing, centered layout, sticky nav bar, hero, tables, cards, footer. Styles
  target existing elements and existing classes (`.site-header`,
  `.content-wrapper`, `.page-content`, `.hero`, `.item-list`, …). Markup barely
  moves.
- *(Later phases, also no restructuring:)* system-preference dark mode
  (CSS only); the homepage pipeline diagram (additive markup on `index.html`);
  `data-*` date attributes (additive on schedule + week pages);
  `core/colophon.html` (one new standalone file).

### Touches shared chrome in all 22 files (mechanical, unavoidable — same as the prior revision's skip-link / footer-links tasks)

*(All later phases — Phase 1 does not touch shared chrome beyond CSS-level
restyling of existing markup.)*

- Footer gains the colophon link (Phase 3).
- `<head>` gains the FOUC inline script (Phase 4).
- Header gains the toggle control (Phase 4) and the search control (Phase 6).
- Pages gain `<script src="assets/js/…">` includes (Phases 4–6), with the
  correct `../` prefix per directory depth.

There is no include mechanism, so these are hand-edits across 22 files. The
existing tests (`test_integration_links.py` nav-identity,
`test_unit_html_structure.py`) catch most drift; a per-page grep during
implementation catches the rest.

### Would require real restructuring — explicitly out of scope

- **A templating / build system** to stop hand-copying the header, nav, footer,
  and (soon) script tags. This is the honest structural weakness and it grows
  with every shared-chrome change. But introducing Jekyll/11ty/a generator
  contradicts the "auditable in one sitting, no build step" principle the site
  was deliberately rebuilt around (`9bd5b5a`). **Recommendation:** stay
  hand-authored for now; revisit only if shared-chrome churn becomes painful.
  Note the tradeoff in the colophon.
- **A Node/browser test toolchain** for the JS features. The current suite is
  Python/BeautifulSoup with no browser. Keep it that way; test the JS features
  structurally (controls exist, `data-theme` contract, index file shape) rather
  than behaviorally. Accept that "does search actually rank well" is verified by
  hand.

---

## 4. Suggested implementation order

**Phase 1 is the whole of the first step. It contains no feature work.** Each
later phase is its own review and its own commit(s), added only after the
previous one is merged.

### Phase 1 — Visual redesign ONLY *(the first step; one PR, optionally 2–3 tiered commits like the prior revision)*

Scope: `css/style.css` and nothing else of substance.

1. Rewrite `css/style.css`: `:root` **light** token set (typography, color,
   spacing, radius), centered container layout, slim sticky nav bar, restyled
   hero (drop the `::before` dash), tables, blockquotes, code, list rows,
   footer. Retarget the `@media print` rules that name now-deleted selectors.
   Keep `:focus-visible` and the print block.
2. Only if strictly needed for the layout: add one wrapper class in the 22
   files' markup. Prefer styling the existing `.content-wrapper` /
   `.page-content` / `.hero` so markup does not move at all.
3. Update `test_unit_css.py` line-count guard (450 → 800, reword docstring).
   **This is the only test change in Phase 1.**

**Explicitly NOT in Phase 1:** no pipeline diagram, no colophon page, no dark
palette / `prefers-color-scheme` block, no `data-*` attributes, no JavaScript,
no new files under `assets/`, no page-count or nav test changes.

**Why this is the whole first step:** it is the highest-visibility, lowest-risk
change, stays almost entirely within the existing test suite, adds no
dependency and no build step, and establishes the token system every later
phase reads from. Ship and review it in isolation.

### Phase 2 — Homepage pipeline diagram (Feature 4)

`index.html` markup + CSS only. Still no JS. Small, contained, visible payoff.
**Why next:** no dependencies, no shared-chrome edits, no test-suite changes
beyond keeping the inline SVG valid.

### Phase 3 — Colophon page (Feature 5)

`core/colophon.html` + footer link on all 22 pages. Test edits: page count
22 → 23, add to `EXPECTED_CORE_FILES`. **Why here:** no JS, no dependency; it is
the first shared-chrome edit (footer) and the first test-set change, best done
before the JS phases pile more onto the footer/header.

### Phase 4 — Dark mode (Feature 1)

4a: `@media (prefers-color-scheme: dark)` palette — CSS only, system-driven.
4b: `data-theme` overrides, `<head>` FOUC script ×22, header toggle control ×22
(outside `nav.main-nav`), `assets/js/theme.js`, structural test.
**Why here:** smallest JS feature; establishes the per-page `<script>` include
and out-of-nav control pattern that Phase 6 reuses.

### Phase 5 — Current-week highlight (Feature 3)

5a: `data-week` / `data-start` / `data-end` on `core/schedule.html` (+ mirror on
week pages) + a date-validation test.
5b: `assets/js/schedule.js` (~20 lines) + `.is-current-week` CSS.
**Why here:** tiny; self-contained to one page; no new dependency.

### Phase 6 — Client-side search (Feature 2), approach A

`tools/build_search_index.py`, `assets/search-index.json`, header control ×22,
modal + Ctrl/Cmd+K in `assets/js/search.js`, `<script>` includes ×22, index
test. **Why last:** the only feature that introduces a build step and the only
candidate for a vendored runtime dependency; everything else should be stable
first. Approach B (Lunr full-text) is a later optional upgrade on top.

---

## 5. Open decisions for the instructor

1. **Accent color** — proceed with deepened blue `#005a9c` / `#5aa9de`
   (recommended), or pick the burgundy/indigo alternative (adds a favicon recut)?
2. **Homepage intro paragraph** — keep it verbatim above the diagram
   (recommended), or is trimming/cutting that specific paragraph acceptable
   (the diagram would then carry the description)?
3. **Search** — confirm approach A (lightweight, no dependency) as the first
   target, with Lunr as a documented future upgrade?
4. **Current-week highlight out of term** — highlight nothing before/after the
   semester, or clamp to Week 1 / Week 15?
5. **Colophon in nav?** — recommended in the footer only (keeps the nav tests
   untouched); confirm that's acceptable rather than a 7th primary-nav item.

---

## 6. Verification

### Phase 1 (the first step)

- `cd tests && pip install -r requirements.txt && cd .. && python3 -m pytest tests/ -v`
  — green, with only the line-count guard edited.
- `python3 -m http.server 8080` and walk every page type (index, a core page, a
  week page, 404) at desktop and <768px widths — layout, type, nav bar, hero,
  tables, links, focus rings.
- Print preview: nav and skip-link hidden, content readable, link URLs expanded.
- Confirm no course prose, dates, or table content changed (`git diff` is
  `css/style.css` plus at most a wrapper class in the HTML).

### Later phases (when each is implemented)

- Pipeline diagram: nodes link correctly, stack on mobile, valid inline SVG.
- Colophon: reachable from the footer, passes all structure tests, page count
  test updated.
- Dark mode: OS appearance toggle (4a); control toggle + reload for persistence
  and no white flash (4b).
- Current-week: override `Date` in the console to a mid-semester day; correct
  week lights up; nothing lights up out of term (or the agreed clamp).
- Search: Ctrl/Cmd+K opens the modal; queries resolve to the right pages;
  `assets/search-index.json` lists all pages.
- `git grep -n 'assets/js'` — every page has the expected includes at the
  correct relative depth.
