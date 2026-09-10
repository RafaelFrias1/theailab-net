# Phase 2: Design & Experience Revision — Audit, Directions, and Spec (2026-09-03)

**Repository:** `Avulpix0412/theailab-net` (local clone: `~/code`)
**Relationship to Phase 1:** Phase 1 (`docs/tech-spec_website-revision_v1_20260903.md`) covers engineering hygiene (favicon, metadata, accessibility basics, dead-CSS cleanup, table overflow, test coverage) and should land first — this spec assumes Phase 1's markup additions (`id="main"`, `.skip-link`, `.table-wrap`) already exist so Phase 2 doesn't have to re-touch them. **Nothing in this document should be implemented yet.** It is a proposal for review.

**No course content changes.** Every idea below either restyles existing content or restructures *how existing fields are visually presented* (e.g., surfacing the "Ethics thread" line that's already in 3 of 15 week pages as a distinct visual element). Nothing here invents new syllabus text, new deadlines, or new claims about the course.

---

## Part 1 — Visual/UX Audit of the Current Site

### 1.1 What the site currently is

The site is a faithful, hand-ported clone of WordPress's **"Twenty Nineteen"** theme, built (per `README.md`'s own "Content Source and Provenance" section) explicitly **for visual consistency across the instructor's other Kenyon course sites** — this is a stated design goal already on record, not an oversight. Concretely:

- **Typography:** serif reading text (`"Hoefler Text", Garamond, "Times New Roman"`, 22px/1.8 line-height) for body copy; bold sans-serif system font stack for headings and UI chrome (nav, meta, labels). This pairing is genuinely good — a comfortable, readable serif for long-form prose with a crisp sans for structure — and is the single strongest asset already in place.
- **Color:** one accent blue (`#0073aa` / `#0073a8`, functionally identical — two CSS variables carrying the same color, likely a leftover from the theme port), used for links and active nav state. Everything else is black/white/gray. No secondary or tertiary color anywhere.
- **Layout:** a narrow reading column (640px content measure) offset from the left edge by a viewport-relative gutter (`--col-left: calc(8.33vw + 28px)`), which is a distinctive, slightly asymmetric layout choice — most course sites center content; this one deliberately doesn't. That asymmetry is one of the few genuinely distinctive-looking decisions already in the CSS.
- **Page furniture:** every page repeats the same header (site title + tagline + 6-item nav), a "hero" band with a dash-underline above the page's `<h1>`, breadcrumbs, and an identical one-line footer. No images anywhere in the site (confirmed in the Phase 1 audit — zero `<img>` tags across all 22 pages).
- **Week pages** already share an implicit four-part structure, even though it isn't visually distinguished:
  1. A date/session line (`<strong>Tuesday & Thursday, ...</strong>`)
  2. A "Part of [Mini-Project N — Name]" line linking the week to its project arc
  3. One or two sentences of session content/topic
  4. On exactly 3 of 15 weeks (3, 8, 12 — confirmed against `core/syllabus.html`'s "We take that up explicitly in Weeks 3, 8, and 12"), a bolded **"Ethics thread:"** line — a one-sentence discussion prompt that already functions as a reflection cue, just not styled as one.
- **Homepage** is minimal: a two-sentence welcome paragraph, a course-details table, and a quick-links list. It does not frame the course intellectually beyond restating the syllabus's opening paragraph — there's no visual sense of the 15-week arc, the four-mini-project structure, or the ethics thread running through it, even though all of that exists in the content already (schedule.html groups weeks by mini-project; syllabus.html names the ethics weeks).
- **Dead CSS** (flagged in Phase 1, §4.2 of the engineering report): ~150 lines for WordPress blog/post concepts (`.post-preview`, `.entry-meta`, `.badge-*`, `.share-links`, featured-image duotone hero) that match nothing on this site. This matters for Phase 2 specifically because it means the current visual system is partly aspirational/unused scaffolding, not a fully realized design — there's headroom to build into, not just around.

### 1.2 Where it currently reads as generic rather than distinctive

- The accent blue (`#0073aa`) is a stock WordPress-theme blue, not a color anyone would associate with *this* course, IPHS, or Kenyon.
- Every page's hero is identical in structure to every other page's hero — nothing marks a week page as different in kind from a policy page, even though "Week 3" and "Policies" are very different content types (a session in a 15-week narrative vs. a static reference document).
- The homepage doesn't visually differentiate itself as an entry point — it's laid out exactly like every interior page (same hero, same content-wrapper), just with a shorter intro paragraph.
- Nothing on the site visually signals "this is a course about AI coding agents" — the visual language is entirely borrowed from a humanities-blog theme with no connection to the subject matter. That's not necessarily wrong (see Direction A below), but it is a missed opportunity if the goal is *recognizable as this specific course*.

### 1.3 Conventions to preserve (do not touch in Phase 2)

These are working well and any Phase 2 direction should build on them, not replace them:

1. **The serif/sans pairing** (`--fh` for body, `--fb` for headings/UI) — genuinely good editorial typography already in place.
2. **The narrow reading column** (`--mw: 640px`) — appropriate for dense syllabus/policy prose; don't widen it just to "fill space."
3. **The asymmetric left-gutter layout** (`--col-left`) — already a distinctive, non-generic layout decision worth keeping and possibly reinforcing rather than discarding for a centered/boxed layout.
4. **Breadcrumbs and consistent header/nav/footer** — necessary wayfinding across 22 pages; Phase 2 should restyle, not remove.
5. **No images / no JS** — keeps the site fast and simple; any Phase 2 direction should stay within static HTML/CSS wherever possible. (Revised in Part 3b: the user later approved one narrow, explicit JS exception for a current-week indicator — see P2-5 — but this remains the default constraint everywhere else.)
6. **The existing per-page test suite's structural guarantees** (DOCTYPE, title suffix, nav consistency, etc.) — Phase 2 changes must not break these; new visual elements need new tests of their own (see §4 below), not a weakening of existing ones.

---

## Part 2 — Three Design Directions

### Direction A: "Editorial Journal"

Lean fully into the serif/print heritage already in the CSS. Treat the site as a scholarly publication: refine the type scale, replace the generic WordPress blue with a deliberate ink/accent color (e.g., a deep oxblood, forest, or midnight — something that reads as chosen, not defaulted), add small-caps section labels, style the "Ethics thread" line as a pull-quote/marginal note (a common academic-journal device), and give week pages numbered like journal entries/issues ("No. 03" rather than just "Week 3").

- **Strengths:** Lowest implementation risk — mostly CSS token changes plus light semantic wrapping (e.g., `<aside class="ethics-thread">`), no new layout primitives. Directly satisfies "academically appropriate," "editorial and intellectually serious," and "avoid unnecessary complexity." Reinforces rather than fights the site's existing typographic strengths.
- **Weaknesses:** On its own, does the least to satisfy the "distinctive... immediately recognizable as a considered student project" and "subtle computational/AI visual language" goals — a journal aesthetic is tasteful but not obviously *this course*. Doesn't by itself deliver the 15-week visual map.

### Direction B: "Computational Notebook"

Introduce a restrained monospace type layer for *meta information only* (dates, week numbers, mini-project tags, breadcrumb separators) — evoking terminal output, commit metadata, and lab-notebook annotation — while keeping the serif body prose untouched. Muted, desaturated accent colors evocative of syntax highlighting (not neon), used sparingly for the mini-project "tags" on week pages and schedule groupings.

- **Strengths:** Directly ties the visual language to the course's actual subject matter (coding agents, CLI tools, harness engineering) in a way Direction A doesn't. Satisfies "subtle computational/AI visual language" most directly.
- **Weaknesses:** Highest risk of tipping into the "generic AI startup" or "hacker aesthetic" cliché the user explicitly wants to avoid if not applied with real restraint — monospace + dark accents is an overused shorthand for "tech." Requires the most editorial judgment to get right, and is the hardest direction to specify precisely in advance (a lot rides on execution, not just the plan). Does the least, alone, for the homepage-framing and course-map goals.

### Direction C: "Course-as-System"

Center the homepage on a compact, diagrammatic 15-week map (a horizontal or vertical timeline grouped into the four mini-project arcs plus the Final Project, with the 3 ethics-thread weeks marked), treating the course's own structure as the thing being designed — fitting for a course about designing systems. Week pages get a small persistent "position in arc" indicator (e.g., "MP2 · Week 4 of 5"). Lower emphasis on prose-heavy homepage framing, higher emphasis on the course structure being immediately legible at a glance.

- **Strengths:** Most directly satisfies "redesigned homepage with clear intellectual framing" and "visual 15-week course map" — these are named, specific user goals this direction is built around. Most likely single element to make the site memorable/distinctive.
- **Weaknesses:** Requires a genuinely new component (the map/timeline) that doesn't exist in any form today — highest design and implementation effort of the three, and the one most likely to need iteration to avoid looking like a marketing-site "roadmap" graphic if not kept typographically restrained. Says little on its own about the visual-identity/color/type-system goals (1) or the computational-language goal (5).

### Tradeoff summary

| | Effort | Distinctiveness | Risk of cliché | Satisfies homepage/map goals | Satisfies visual-identity goal |
|---|---|---|---|---|---|
| A. Editorial Journal | Low | Medium | Low | Weak | Strong |
| B. Computational Notebook | Medium | Medium-High | **High** if overdone | Weak | Medium |
| C. Course-as-System | High | High | Medium | Strong | Weak |

No single direction alone satisfies all seven of the user's stated interests (§Part 3). All three are compatible with each other in principle — they operate on different layers (type/color system, meta-info styling, homepage/structural components) rather than contradicting each other.

---

## Part 3 — Recommendation

**Recommended: Direction A as the foundation (type system, color, page furniture), with Direction C's course-map contributed only to the homepage and schedule page (not as a repeating element on all 22 pages), and Direction B's monospace/meta-label treatment applied narrowly to date lines, mini-project tags, and breadcrumb separators only — never to body prose or full headings.**

This is a synthesis, not a fourth direction — it's Direction A doing the load-bearing work (lowest risk, reinforces existing strengths, satisfies "editorial/serious" and "avoid unnecessary complexity" most directly) with two small, deliberately scoped borrowings from B and C to hit the specific goals A alone can't:

| User's stated interest (Part 3 of the request) | Addressed by |
|---|---|
| 1. Stronger visual identity & typography system | Direction A (refined type scale, deliberate accent color) |
| 2. Redesigned homepage, clear intellectual framing | Direction A (rewritten-in-tone-only framing using existing course-description language) + Direction C (map) |
| 3. Visual 15-week course map | Direction C, scoped to homepage + schedule only |
| 4. Question/Read/Discuss/Reflect-style week structure | Derived from existing fields already in week pages (date, MP-arc line, topic sentence, Ethics thread) — visual restyling only, per §4 below |
| 5. Subtle computational visual language, no cliché | Direction B, narrowly scoped to meta-labels only |
| 6. Optional dark mode / small interactions | Deferred — see §4, task P2-8 (explicitly optional, last priority) |
| 7. Transparent "About this site" human–AI note | New content block on `about.html`, drawing only from existing `core/policies.html` Generative AI Use Policy language — no new policy invented |

**Why not a pure single direction:** Pure A leaves three of the user's seven named interests (map, computational language, week-structure) unaddressed. Pure C or B alone under-serves the "academically serious, not startup-landing-page" requirement that's stated as the primary goal, and pure B carries real cliché risk on its own. Scoping C and B narrowly (map only on 2 of 22 pages; monospace only on meta text) keeps total implementation effort closer to A's low-risk profile than to a full C or B build-out, while still hitting all seven named interests.

---

## Part 3b — Finalized Decisions (after user design review, 2026-09-03)

Following review of live typography/color previews and a homepage mockup (screenshots, not committed to the repo), the user finalized the following specifics on top of the Part 3 recommendation. These supersede any general placeholders in Part 4 below where they conflict.

**Typography (Direction A, made concrete):**
- Headings / display text: **Fraunces** (a soft, characterful display serif), replacing the current `--fh` (Hoefler Text/Garamond) for headings only.
- Body prose: keep **Newsreader** (a book-style serif close in spirit to the current Hoefler Text/Garamond stack) — this preserves the "preserve" list's serif/sans pairing rather than abandoning it.
- Navigation / UI / labels: **Quicksand** (rounded sans), set to **bold weight** (the user specifically asked for a bolder nav than the current `.main-nav li a` weight).
- Both are Google Fonts — this is the one deliberate exception to a fully system-font stack; loaded via a single `<link>` to `fonts.googleapis.com`, no additional build tooling.

**Color tokens (replacing the current `--accent`/`--accent-dk` WordPress blue):**

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#faf7f2` | page background (warm off-white) |
| `--text` | `#2a2622` | body text (warm near-black) |
| `--text-lt` | `#8a8378` | secondary text |
| `--accent` | `#c2703f` | links, active nav, "here" markers — a muted warm terracotta, chosen as a deliberate alternative to the old WordPress blue and loosely inspired by (not copied from) Claude's own orange/gray pairing per the user's reference |
| `--border` | `#e8e2d8` | rules, table borders, card borders |

**Secondary "kusumi-iro" palette** (低饱和度・中高明度・灰调, i.e. Japanese dusty/muted pastel — explicitly *not* bright candy-macaron colors), used only as small-area markers for the five course-arc segments (never as large background washes):

| Segment | Name | Hex |
|---|---|---|
| MP1 — Dev Environment | 桜鼠 dusty rose | `#c3a89f` |
| MP2 — Agent Config | 鶯 moss | `#a3ac93` |
| MP3 — Harness & Hooks | 芥子 mustard | `#c4ab77` |
| MP4 — SDLC Capstone | 藤鼠 dusty violet | `#a49cb0` |
| Final Project | 水鼠 dusty teal | `#9bb0b5` |

Target range for this secondary palette: saturation ~28–35%, lightness ~60–68% — muted by graying the hue, not by mixing toward white, which is what keeps it reading as "considered/editorial" rather than "pastel/candy."

**Homepage layout (finalized order, top to bottom):**
1. Header: site title/tagline, bold Quicksand nav.
2. One-line intellectual framing sentence (existing course-description language, per P2-4).
3. **The 15-week journey map, immediately below the framing line** — the user was explicit this should lead the page, not be buried after prose.
4. A trimmed welcome paragraph (shorter than today's, since the map now carries some of that structural information).
5. Course Details table.
6. **No "Quick Links" section** — the user flagged this as pure duplication of the top nav (same 5 links) that added page length with no added value. It is removed, not relocated. (This revises P2-4 below, which had originally proposed keeping the quick-links list lower on the page.)

**Journey map component — clickable, not decorative (revises P2-5):**
- Each of the 15 week markers (and the Final Project marker) is a real link (`<a href="weeks/week-NN.html">` wrapping the visual node), not a static illustration. Clicking navigates like any other site link.
- Rendered as an inline SVG (geometric path + circular/square nodes in the five palette colors above), grouped by the same five arcs as `core/schedule.html`. No character, mascot, or illustrative artwork — nodes and a connecting line only, per the "restrained" direction the user chose over a literal game-map illustration.
- The 3 ethics-thread weeks (3, 8, 12) get a small diamond marker in the accent orange, distinct from the circular week nodes.

**"You are here" current-week indicator — approved JS exception:**
The user requested a feature that reads the current date and highlights the current week on the map. This cannot be done in CSS/HTML alone, so **this is a deliberate, scoped exception** to the site's otherwise-JS-free constraint (see Part 5). Specification:
- A small vanilla JS snippet (no framework, no external library) on `index.html` only.
- A hardcoded array of each week's actual first-session date (already extracted from `weeks/week-01.html` through `week-15.html` — see table below), used to compute the current week as "the highest-numbered week whose start date is on or before today."
- **Recess-awareness:** a second hardcoded list of recess date ranges (from the Kenyon College 2026–27 academic calendar the user supplied) suppresses the "current week" claim during breaks and instead shows "On break (Break Name) — next: Week N", with a dashed (not pulsing) ring on the *upcoming* week's node:

  | Recess | Dates |
  |---|---|
  | October Break | 2026-10-08 to 2026-10-09 |
  | Thanksgiving Recess | 2026-11-21 to 2026-11-29 |

  | Week | First session date | Week | First session date |
  |---|---|---|---|
  | 1 | 2026-08-27 | 9 | 2026-10-20 |
  | 2 | 2026-09-01 | 10 | 2026-10-27 |
  | 3 | 2026-09-08 | 11 | 2026-11-03 |
  | 4 | 2026-09-15 | 12 | 2026-11-10 |
  | 5 | 2026-09-22 | 13 | 2026-11-17 |
  | 6 | 2026-09-29 | 14 | 2026-12-01 |
  | 7 | 2026-10-06 | 15 | 2026-12-08 |
  | 8 | 2026-10-13 | | |

- On a non-recess day, the current week's node gets a pulsing solid accent-color ring plus a text label ("You are here — Week N").
- Verified in a throwaway mockup (not committed) against both a normal day (2026-09-03 → correctly resolved to Week 2) and simulated recess dates (2026-10-08 → October Break, next Week 8; 2026-11-25 → Thanksgiving Recess, next Week 14) — both matched the official calendar.

---

## Part 4 — Phase 2 Spec: Tasks, Acceptance Criteria, and QA

Ordered for implementation. Each task lists what "done" means and how it would be tested/verified — following this repo's existing test-first convention from Phase 1. **Do not implement any of this without separate sign-off** — this table is what gets reviewed, not executed, in this pass.

### P2-1 — Establish the type scale and color tokens

**Task:** Replace `--fh`/`--fb` font stacks with Fraunces (headings/display) + Newsreader (body) + Quicksand (nav/UI, bold weight), loaded via one Google Fonts `<link>`. Replace `--accent`/`--accent-dk`/`--primary` with the finalized token set from Part 3b (`--bg`, `--text`, `--text-lt`, `--accent`, `--border`), plus the five-color kusumi-iro secondary palette as new tokens (`--mp1` through `--mp4`, `--final`). Audit whether `--mww: 1168px` is used anywhere (a stray unused token was already flagged in Phase 1's dead-CSS finding — a new design pass shouldn't reintroduce the same problem).

**Acceptance criteria:** New tokens defined once in `:root` with the exact hex values from Part 3b; every existing use of the old blue is migrated (no hardcoded hex colors left outside `:root`); nav links render in Quicksand bold; a manual side-by-side screenshot of 3 representative pages (home, a week page, policies) at both desktop and mobile widths shows a single coherent palette matching the approved preview.

**QA:** Run the full Phase 1 + Phase 2 test suite; visually diff before/after screenshots (per Part I.2 of the setup manual's browser-check step) rather than relying on tests alone — color/type changes are exactly the kind of thing automated tests can't catch.

### P2-2 — Restyle the "Ethics thread" line as a distinct visual element

**Task:** Wrap the existing "Ethics thread:" text (present verbatim in weeks 3, 8, 12 only — do not add it to other weeks, that would be inventing content) in a semantic `<aside class="ethics-thread">` and style it distinctly (e.g., a left-border accent, the small-caps label treatment from P2-1) rather than a plain bolded inline sentence.

**Acceptance criteria:** Exactly the 3 pages that currently contain "Ethics thread:" get the new markup/style; the other 12 week pages are unchanged; no new ethics-thread text is added anywhere.

**QA:** A test asserting the count of `.ethics-thread` elements across the site equals exactly 3, and that each matches a week page already known to contain that phrase (regression-proofs against someone accidentally adding or removing one later).

### P2-3 — Introduce restrained meta-label styling (Direction B, scoped)

**Task:** Apply the monospace/meta treatment *only* to: the date line at the top of each week page, the "Part of [Mini-Project N]" line, and breadcrumb separators. Explicitly do not apply it to body prose, headings, or the Ethics thread text (which should read as prose, not code).

**Acceptance criteria:** A visual spot-check confirms monospace styling appears only in the three specified locations across a sample of week pages; body paragraphs are unaffected.

**QA:** Manual review is the primary check here (this is a taste/restraint judgment, not something a structural test can verify) — the reviewer should be able to point to any monospace text on the page and say which of the three approved categories it belongs to.

### P2-4 — Homepage reframe

**Task:** Rewrite the homepage's *visual presentation* (not its factual content) per the finalized order in Part 3b: header → one-line intellectual framing sentence (already present in the syllabus/about content, e.g. "AI software engineering... coordinating autonomous coding agents through a professional software development lifecycle") → the course-map component (P2-5), placed immediately below the framing line, not lower on the page → a trimmed welcome paragraph → Course Details table. **The Quick Links section is removed, not relocated** — it duplicated the top nav's 5 links with no added value.

**Acceptance criteria:** No new claims about the course appear anywhere on the homepage that aren't already present verbatim (or a light paraphrase) in `index.html`, `core/about.html`, or `core/syllabus.html`; the course-details table still exists; the map appears before the welcome paragraph, not after; no Quick Links list remains anywhere on the page.

**QA:** Diff the homepage's text content against existing pages to confirm no fabricated claims; run existing `test_unit_html_structure.py` checks (hero/h1 presence, etc.) to confirm the page still passes structural tests after reordering; add a test asserting the homepage's `.page-content` has no list of links duplicating the nav.

### P2-5 — 15-week course map component (homepage only) + current-week indicator

**Task:** Build the journey map as an inline SVG (not a CSS flex/grid grid of link cards — revised from the original plan now that the map is a real illustrated path, not a table-like layout) grouped by the four Mini-Project arcs + Final Project, using the exact five-arc coloring and ethics-thread diamond markers specified in Part 3b. Each week node is a real `<a href="weeks/week-NN.html">`-wrapped SVG element — clicking it navigates to that week's page. Reuse this component on the homepage only (not `core/schedule.html`, which keeps its existing grouped-list structure per Phase 1/Phase 2 scope — a second map placement is not in scope for this pass).

Additionally implement the "you are here" current-week indicator specified in Part 3b: a small vanilla-JS snippet, scoped to `index.html` only, using the hardcoded week-start-date and recess-date tables from Part 3b.

**Acceptance criteria:**
- The map's five arc groupings and colors match Part 3b's table exactly; all 15 week links plus the Final Project link resolve.
- The map is legible and doesn't require horizontal scroll at any tested breakpoint (desktop, tablet, mobile).
- On a non-recess day, exactly one node shows the pulsing "here" ring, matching the week whose start date is the latest one on or before today.
- On a recess day (per the two ranges in Part 3b), no node shows a pulsing ring; the next upcoming week's node shows a dashed ring instead, and the text label reads "On break (Recess Name) — next: Week N".
- Before the semester start date (2026-08-27), no marker is shown at all (no false "Week 1" claim).

**QA:** Extend `test_integration_links.py`-style checks to include the 15 links inside the new map component; manual responsive check at 375px, 768px, 1024px+ widths in Chrome; confirm no layout overflow. For the JS date logic specifically, automated pytest can't exercise browser JS — instead, manually verify via the browser console (`currentWeekNumber('2026-10-08')`, etc., as done in the mockup review) against at least: a normal mid-semester day, both recess ranges, and a day before 2026-08-27; a code-review pass should also confirm the hardcoded date tables match the live `weeks/week-NN.html` date lines and the official Kenyon academic calendar, since this data will silently go stale if either source changes and this file isn't updated to match.

### P2-6 — Week-page structural labels (Question/Read/Discuss/Reflect-derived)

**Task:** Where content already supports it, add small visual field labels above existing content rather than restructuring or rewriting the content itself: a "Session" label above the date line, a label above the "Part of [MP]" line (e.g., framed as the week's place in the arc), and reuse the Ethics-thread aside from P2-2 as the "Discuss" analog on the 3 weeks that have it. **Do not add "Question" or "Reflect" labels to weeks that have no corresponding existing content** — inventing a discussion question for the 12 weeks without an Ethics thread would violate the "no content rewrite" constraint.

**Acceptance criteria:** No week page gains new prose; only label/wrapper markup is added around existing text; the 12 non-ethics-thread weeks look visually consistent with each other (same label set) and distinct from the 3 ethics-thread weeks (extra "Discuss" element), without looking incomplete or broken for lacking it.

**QA:** Visual review across all 15 week pages side-by-side to confirm the partial-structure (12 weeks with 3 labels, 3 weeks with 4) doesn't read as an error; a test asserting every week page has at least the three baseline labels present.

### P2-7 — "About this site" / human–AI collaboration note

**Task:** Add a new section to `core/about.html` (not a new page — keep the nav at 6 items) titled something like "About This Site" or "A Note on How This Site Was Built," drawing only from language already present in `core/policies.html`'s Generative AI Use Policy (the course is explicitly "about configuring and directing generative AI coding agents... transparency and demonstrated understanding" are already the course's own stated values) plus a factual, first-person note that this site itself was built using the course's own toolchain (Claude Code) as a demonstration of the material, if that framing is accurate to how the student actually built it.

**Acceptance criteria:** No new policy claims are invented — this section either quotes/paraphrases `core/policies.html` or states a factual claim about how the site was built (verifiable, e.g. against git history); it's additive to `about.html`, not a new nav item.

**QA:** Manual read-through to confirm nothing here contradicts or duplicates `core/policies.html` in a way that could create two sources of truth for the AI-use policy — this section should point to Policies for the authoritative statement, not restate it independently.

### P2-8 — Dark mode (optional, lowest priority, implement only if time allows)

**Task:** If pursued, define a `prefers-color-scheme: dark` media query swapping the token values from P2-1 (not a separate stylesheet, not a JS toggle — CSS-only, matching the "avoid unnecessary complexity" constraint). Explicitly marked optional per the user's own framing ("only if this materially improves the experience").

**Acceptance criteria:** If implemented, all text remains readable (contrast-checked) in both modes; if not implemented, this task is simply dropped with no site behavior change — its absence is not a defect.

**QA:** If implemented, manual check in both OS-level light and dark mode in Chrome; contrast-ratio spot check (WCAG AA, 4.5:1 for body text) for both palettes.

---

## Part 5 — What This Spec Deliberately Does Not Do

- Does not touch any factual course content (dates, weights, policies, learning outcomes) anywhere.
- Does not add a build step or an external framework/library. **One narrow exception to "no JavaScript":** the "you are here" current-week indicator (P2-5) requires a small vanilla-JS snippet on `index.html`, since reading today's date is impossible in CSS/HTML alone — this was raised and explicitly approved by the user during design review (Part 3b) as worth breaking the otherwise-static-only constraint for. It is scoped to one page, has no dependencies, and every other task remains static HTML + CSS.
- Does not change the 22-page site structure, URLs, or navigation item count.
- Does not implement anything — this document is for review. Implementation should be scoped into its own follow-up (a Phase 2 execution pass, analogous to Part I of the setup manual) only after the professor/reviewer has approved a direction.
