# Phase 3: Homepage Redesign, Widget Rail, and Live AI Headline — Spec (2026-09-03)

**Repository:** `Avulpix0412/theailab-net` (local clone: `~/code`)
**Relationship to Phase 1/2:** Phase 1 (engineering hygiene) and Phase 2 (type/color system, homepage reframe, journey map, dark-mode-ready tokens) are both landed. This spec covers three items raised in a live design-review session, arrived at through iterative mockups (not committed to the repo — see `_mockups/homepage-a4.html`, deleted before implementation): (P3-1, already landed this session) map/schedule differentiation and nav hover-scale; (P3-2, already landed) dark mode; **(P3-3, this spec)** a bolder homepage layout with a persistent widget rail; **(P3-4, this spec)** a live "Today in AI" headline sourced from Hacker News.

**No course content changes.** Everything below restyles or repositions existing content, or adds a self-updating supplementary widget (the AI headline) that is explicitly *not* course content — it is never graded material, never authoritative, and carries no claims about the syllabus.

---

## Part 1 — What Was Explored and Rejected

Documenting the rejected directions matters here because they were seriously prototyped, not just discussed abstractly:

1. **Direction "Editorial Masthead + vertical map"** — a large display headline with the 15-week map rotated vertical and demoted into the sidebar. **Rejected**: compressing the map into a narrow vertical rail lost the "see the whole semester at a glance" property that makes the current horizontal map work — it required scrolling to see all 15 weeks, which defeated the map's purpose.
2. **Direction "map moved to an enlarged sidebar, still horizontal-turned-vertical"** — same rejection reason as above; enlarging the map by relocating it to the rail necessarily made it vertical (the rail is narrow and tall, the map is wide and short), which reintroduces the scrolling problem. **Rejected** for the same reason.
3. **A pure "widen and center the reading column" approach** — resolves the whitespace complaint with the least effort but was judged not bold enough and creates no home for the AI headline. **Rejected** in favor of the widget-rail direction below.

**What was kept:** the horizontal journey map, unchanged in orientation and full fidelity (all 15 nodes clickable and hover-titled, ethics-thread diamonds, "you are here" ring) — this is a hard constraint for any future revision to this homepage. Do not propose relocating or reorienting it again without re-litigating point 1 above.

---

## Part 2 — Homepage Layout (P3-3)

### 2.1 Structure, top to bottom

1. Header (unchanged): site title/tagline, nav.
2. **Nav change:** "Schedule" is removed from the 6-item top nav. The `Schedule` page itself is **not deleted** — it becomes reachable only via the "Full schedule with dates" link under the homepage map (§2.3) and via `core/schedule.html` being linked from wherever else it already is (e.g., if any week page or other content links there, leave those). Nav becomes 5 items: Home, Syllabus, Assignments, Policies, About.
3. Hero (unchanged): dash rule + "Home" `<h1>`.
4. **New: "Today in AI" card**, its own full-width row, right-aligned, sitting between the hero and the two-column area below — deliberately **not** part of either column, so it doesn't read as belonging to the map or the welcome text. See Part 3 for its content/behavior spec.
5. **Two-column area** (new `.home-grid`):
   - **Main column** (`.home-main`, fixed width ~800px): the existing homepage content in its existing order — `home-lead` framing sentence, the journey map card, the welcome paragraph, the Course Details table. Content and copy are unchanged; only the surrounding layout changes.
   - **Rail** (`.home-rail`, max-width ~360px, `position: sticky`): contains one card, **"This Week"** (see §2.4). This is a genuinely new component (not existing content moved), built entirely from data the site already computes (see below) — it adds no new facts.
   - Gap between columns: 3.5rem. Total block max-width ≈ 1200px (800 + 360 + gap), positioned starting at the page's existing `--col-left` offset, with a 2rem right margin before the block's own edge — **not** edge-to-edge, but using substantially more of the viewport than the current ~1064px cap, which is what was leaving the large empty strip on the right at normal desktop widths.
6. Footer (unchanged).

### 2.2 Why this layout and not a sidebar on every element

The rail holds exactly one card. Early iterations tried stacking the "Today in AI" card in the rail alongside the "This Week" card, which was rejected for two reasons surfaced during review: (a) it made the map/text asymmetry worse, since the rail's total height still didn't come close to matching the main column, and (b) once the two-column grid was widened to close the horizontal whitespace gap, two flat, wide, short cards stacked in the rail read as "crowded but shallow" rather than well-proportioned. Detaching "Today in AI" into its own row above the grid, and leaving the rail with one well-proportioned card, resolved both.

### 2.3 The journey map's "you are here" indicator moves onto the map itself

Currently (Phase 2), the pulsing ring is drawn on the correct map node, and a plain text line ("You are here — Week N") sits below the whole map card, generic and disconnected from the ring spatially. This is revised:

- The ring stays exactly as it is (pulsing, `journey-pulse` keyframe, unchanged CSS).
- A short text label, just **"You are here"** (no week number — the rail's "This Week" card already states the week number prominently, so repeating it here is redundant), is drawn as SVG text positioned near the ring: **above** the node by default.
- **Ethics-thread collision rule:** for the three ethics-thread weeks (3, 8, 12), the diamond marker sits close to the node. If the current week is one of these three, the "you are here" label flips to sit **below** the node instead of above, so it never competes with the diamond for the same space. This is a `data-week` conditional in `journey-map.js` (it already knows the current week number and already has the ethics-week list available from the existing `WEEK_START_DATES`/ethics-thread convention — cross-reference against `[3, 8, 12]`).
- The old below-the-card text line and its `#here-label` div are removed; the "This Week" rail card (§2.4) is the one canonical place for the week number/title, and the map's own label is purely spatial ("you're looking at this dot").

### 2.4 Ethics-thread diamond spacing fix (bundled into this pass)

Verified against a mockup: the pulsing ring's peak radius (17px, per the existing `journey-pulse` keyframe) comes close enough to the ethics-thread diamonds (previously offset only ~19.5px from their node center) to visually overlap at full pulse. **Fix:** increase each ethics-thread diamond's offset from its node center from ~19.5px to ~27px (recentering the diamond further along the same direction from the node, same visual relationship, just more clearance). Apply to all three diamonds in `index.html`'s inline SVG.

**Also discovered, unrelated, note-only:** the third diamond's coordinates (`rotate(45 616.5 46.5)`) sit above week **11**'s node (616, 67), not week **12**'s node (674, 78), which is what the design spec and content (weeks 3, 8, 12) call for. This is a pre-existing placement bug from Phase 2, not something this session introduced. **Fix it while touching this SVG** — move the third diamond to sit near week 12's node instead (674, 78 minus ~27px along the same up-and-slightly-right direction used for the others).

### 2.5 "This Week" rail card

Replaces the removed below-map text line's information, presented as a proper card:

```
Week 2 of 15
Shell Fundamentals and Dotfiles
[▬▬░░░░░░░░░░░░░]   (thin progress bar, filled = week/15)
Go to this week →
```

- "Week N of 15" — display-serif, prominent (largest text in the card).
- The week's real title — reused verbatim from the same `<title>` text already embedded in that week's map node (added in an earlier pass this session for hover tooltips) — **do not hardcode a second copy of week titles**; read it from the DOM (`document.querySelector('[data-week="'+wk+'"] title').textContent`, stripping the "Week N: " prefix) so there is exactly one source of truth for week titles on the page.
- Progress bar: width = `(currentWeek / 15) * 100%`, fill color `var(--mp1)` (arbitrary single accent for the bar; it does not need to match the current week's own arc color — keep it simple).
- "Go to this week →" links to `weeks/week-NN.html` for the current week.
- **On a recess day:** mirror the existing on-break behavior — show "On break (Recess Name)" and "Go to this week" points at the next upcoming week instead. **Before the semester start:** hide the card entirely (same rule as the existing "no marker before 2026-08-27" behavior).
- No icon, no decorative graphic — an earlier iteration added a small circular progress-ring icon next to the text and it was rejected as redundant with the progress bar beneath it. Text + one progress bar only.

---

## Part 3 — "Today in AI" Live Headline (P3-4)

### 3.1 Data source

**Hacker News via the Algolia Search API** (`https://hn.algolia.com/api/v1/search_by_date`) — fully public, no API key, no CORS issues, free, and thematically appropriate for a course about AI coding agents. Confirmed feasible and already the established pattern for this site's one other JS data computation (the current-week logic), extended to a second narrowly-scoped client-side fetch.

**Query approach:**
1. Compute `todayStartEpoch` (local midnight, seconds).
2. Fetch `search_by_date?tags=story&numericFilters=created_at_i>{todayStartEpoch}&hitsPerPage=50`.
3. Client-side filter the returned hits to those whose `title` matches a small AI-relevance keyword list (case-insensitive substring match): `ai`, `llm`, `gpt`, `openai`, `anthropic`, `claude`, `gemini`, `machine learning`, `neural`, `agent`. (Tune this list during implementation if it's too noisy or too narrow — it's a heuristic, not a precise classifier.)
4. Sort the filtered hits by `points` descending; take the top one.
5. If no hit survives filtering, or the fetch fails (network error, non-200, timeout), **the card does not render** — no error state, no placeholder text, just absent. This is supplementary, not core content; failing invisibly is correct.

### 3.2 Caching

Cache the winning story (title, url, points, objectID, fetchedAt) in `localStorage` under a single key. On page load, use the cached value if it's less than 1 hour old; otherwise refetch. This keeps the API call to roughly once per hour per visitor regardless of how many pages they navigate, consistent with the site's "as little JS/network activity as reasonably possible" ethos.

### 3.3 Card content and behavior

```
TODAY IN AI
"New open-weight model claims to match GPT-5 on
reasoning benchmarks at 1/10th the inference cost"
via Hacker News, 812 points →
The field doesn't pause for a syllabus — here's today's
version of it, next to where you are in the course.
```

- **"TODAY IN AI"** — small uppercase eyebrow label, accent color.
- **Headline** — the HN story's title, quoted, display-serif, the card's largest text.
- **"via Hacker News, N points →"** — `N` is the story's real live point count (not decorative — it's the same number used to select this story as "biggest," so showing it lets the reader judge how much traction the story has). **This line links to the story's original external URL** (the HN item's own `url` field — the article/repo/paper being discussed — not the Hacker News comments page itself. If a story has no external `url` (a text-only "Ask HN" post, which the tag/keyword filter should mostly exclude anyway), skip it as a candidate in step 4 above.
- **Italic caption** — static copy, not per-story generated: "The field doesn't pause for a syllabus — here's today's version of it, next to where you are in the course." Do not describe the UI mechanism in this line (an earlier draft said "this rail stays in view as you scroll and appears on every page," which was rejected as too literal/mechanical) — the line's job is to connect *today's news* to *the student's place in the syllabus*, nothing about how the widget is implemented.

### 3.4 Where it appears

- **Homepage:** its own detached row, right-aligned, between the hero and the two-column grid (§2.1).
- **All 21 interior pages** (core pages + week pages): the same card, in a sticky right rail alongside the page's main content column — this is the "widget rail" that was the original, lower-effort direction (Direction A from the initial brainstorm) applied everywhere the homepage doesn't need its bespoke treatment. No "This Week" card, no map — just "Today in AI," since those are homepage-specific. This gives every page on the site the same live-AI-news touchpoint without duplicating homepage-specific components.
- **Dark mode:** verified in a mockup — the card's `background: var(--surface)` and text tokens are already theme-aware from the Phase 3 dark-mode token work; no new dark-specific styling needed.

---

## Part 4 — Tasks

### P3-3a — Homepage layout restructure
Implement §2.1's structure in `index.html` and `css/style.css`: detach the news-card row, introduce `.home-grid`/`.home-main`/`.home-rail`, remove "Schedule" from nav (`index.html` and all other 21 pages' nav — this is a sitewide nav-consistency change, so the existing `test_nav_links_resolve`/nav-consistency tests need updating to expect 5 items, not 6), enlarge `.map-schedule-link` per §2.1 point 2 styling already prototyped (15px bold accent).

**Acceptance criteria:** nav has exactly 5 items on all 22 pages (Schedule removed); `core/schedule.html` still exists and is reachable from the homepage map link; no other page links to Schedule via nav; existing nav-consistency tests updated and passing; homepage's two-column block visibly uses more of the viewport width at 1440px than the current ~1064px cap.

### P3-3b — "You are here" onto the map + diamond spacing + week-11/12 bug fix
Update `journey-map.js` and `index.html`'s inline SVG per §2.3 and §2.4.

**Acceptance criteria:** the below-map `#here-label` text line and its div are removed; a "You are here" SVG text label appears near the current week's ring, above by default, below for weeks 3/8/12; all three ethics diamonds are re-offset to ~27px from their node; the third diamond now sits near week 12's node, not week 11's; manual verification (as in Phase 2's original spec) against a normal day, a recess day, and specifically a day that falls in week 3, 8, or 12 to confirm the label-flip rule.

### P3-3c — "This Week" rail card
New component per §2.5, reusing `journey-map.js`'s already-computed current-week/recess logic (extend it — don't duplicate the date tables) and reading week titles from the existing `<title>` SVG elements.

**Acceptance criteria:** card shows the correct week number, the correct title (matches the map node's own tooltip text, verified for at least 3 sample weeks), a progress bar proportional to week/15, and a working link to that week's page; recess and pre-semester states match the rules already established for the map's own indicator; no hardcoded second copy of week titles anywhere in this card's code.

### P3-4a — "Today in AI" fetch + cache
New `js/today-in-ai.js`, loaded on all 22 pages, implementing §3.1–3.2.

**Acceptance criteria:** a manual test with dev tools open confirms exactly one network request per hour of active browsing regardless of page-to-page navigation (cache working); confirm in the browser console that a failed/offline fetch results in the card simply not appearing, no console error surfaced to a normal user, no broken layout; spot-check the keyword filter against a day's real HN front page to confirm it's not wildly over- or under-inclusive (a judgment call, not a hard test).

### P3-4b — "Today in AI" card markup + placement
Per §3.3–3.4: homepage detached row; sticky rail on all 21 interior pages.

**Acceptance criteria:** card renders identically in light and dark mode (manual check, both themes); the "via Hacker News, N points" link opens the story's original external URL, not an HN URL; the caption text matches §3.3 exactly (not the earlier, rejected "stays in view as you scroll" wording); test suite extended to assert the card's container element and script tag are present on all 22 pages (the card's *content* can't be asserted by static tests since it's runtime-fetched — only structure/script presence).

---

## Part 5 — What This Spec Deliberately Does Not Do

- Does not change any course content, dates, or policies.
- Does not touch the map's orientation, size relative to the page, or its fundamental horizontal-timeline design — that direction was explicitly tried and rejected (Part 1).
- Does not add the map itself to any page but the homepage (interior pages have no room for it and no "you are here" ring context) — but see Part 6, the "This Week" card *is* sitewide.
- Does not invent a second AI-news source or a fallback news source if Hacker News is unreachable — the card simply doesn't render that session (§3.1 step 5).
- Does not add user accounts, server-side rendering, or a build step — the news fetch is a client-side, unauthenticated, cached `fetch()` call, consistent with the site's static-HTML/no-backend constraint.

---

## Part 6 — Post-Implementation Revision (2026-09-03, same day)

Corrections made after the first implementation pass and several rounds of live review:

1. **"This Week" card is sitewide, not homepage-only.** §3.4 and Part 5 above originally scoped it to the homepage only, on the assumption that it depended on the map's DOM for week titles. This was an assumption made while writing this spec, not something confirmed with the user — and it was wrong. The user's intent was for both rail cards ("Today in AI" and "This Week") to appear on all 22 pages. Fixed by extracting the week-date/title/recess data that `journey-map.js` depended on into a shared `js/course-calendar.js` (`window.CourseCalendar`), so both `journey-map.js` (homepage map ring/label only, now) and a new sitewide `js/this-week-card.js` (populates `#here-card` everywhere) read from one source of truth instead of the map's tooltip text. Interior pages' `.page-rail` now stacks both cards.
2. **Homepage layout bug: doubled left offset.** The implementation gave `.home-grid`/`.news-row` their own `margin-left: var(--col-left)`, not realizing `.content-wrapper` (their ancestor) already applies that offset to `.page-content`. The duplicate offset, combined with `.home-grid` being a normal-flow block child that shrink-fits to its container rather than a flex root, squeezed the whole two-column area down to `.content-wrapper`'s old 704px cap — visually this showed up as the rail collapsing to ~148px (wrapping "Week 2 of 15" into a vertical sliver) and the detached "Today in AI" row rendering left-aligned above the main column instead of right-aligned above the rail. Fixed by widening `.content-wrapper` itself for the homepage (new `.is-home` modifier, `max-width: calc(800px + 360px + 3.5rem + 2rem)`) and removing the redundant margins from `.home-grid`/`.news-row`, which restored the exact 800/360 column split approved in the mockup.
3. **Rail squeeze at common laptop widths (1150-1400px).** The fix for #2 above widened `.content-wrapper.is-home`'s cap but left `.home-main` fixed at `800px` (`flex: 0 0 auto`) and `.home-rail` flexible (`flex: 1 1 auto`). Below roughly 1470px viewport width — i.e. most laptop screens, not just narrow ones — the rigid main column absorbed none of the narrowing, so the rail took the entire squeeze well before the 1100px stacking breakpoint. Fixed by swapping which side is fixed: `.home-rail` is `flex: 0 0 360px` (always 360px until it stacks), `.home-main` flexes between 480px and 800px instead.
4. **Homepage/interior-page rail inconsistency.** Once both pages could be compared side by side, the homepage's detached "Today in AI" row (approved in Part 1/2 as a deliberate "belongs to neither column" treatment) read as inconsistent with every interior page, where "Today in AI" and "This Week" stack together in one rail column starting at the top of the content. The user reversed this decision after seeing it in context: the detached row is gone, and `#today-in-ai-card` now sits inside `.home-rail` above `#here-card`, identical to every other page. `js/today-in-ai.js` was simplified to the single `#today-in-ai-card` pattern (the old `#today-in-ai-row` branch is gone, since nothing uses it anymore).
5. **Interior-page rail proportions unified with the homepage.** After #4, the interior pages' original, narrower split (`704px` main / `320px` max rail) looked cramped next to the homepage's `800`/`360`. Unified `.content-wrapper.has-rail`/`.page-main`/`.page-rail` to the exact same fixed-rail/flexing-main pattern as the homepage (same numbers as #3), sitewide.
6. **Wrong HN endpoint picked near-zero-point stories.** §3.1 originally specified `search_by_date` (chronological order). Live testing surfaced a 2-point story as "today's biggest AI news" — the endpoint only samples stories from the last few minutes of the query window, never the actual top story of the day. Switched to the `search` endpoint (sorted by relevance/points/comments) with `hitsPerPage=100`; verified against the real API that this correctly surfaces 1000+ point stories when they exist. Also, per feedback, the "via Hacker News, N points" line — which linked to the story's external URL — read as an unrelated commercial site with no visible tie to Hacker News; simplified to plain, unlinked "via Hacker News" text, dropping both the points count and the link.

Lesson for future specs on this site: when a mockup is a standalone HTML file (not wired into the real page template), double-check how its CSS assumptions (margins, containing-block widths) map onto the *actual* nested structure (`.content-wrapper` > `.page-content` > ...) before writing acceptance criteria — a mockup with no ancestor offsets can hide a doubled-offset bug that only appears once the CSS lands in the real template. And when a spec's acceptance criteria reference a live third-party API, verify against the *actual* API response during implementation, not just during initial feasibility research — an endpoint that's technically correct (keyless, CORS-friendly, well-documented) can still return the wrong *shape* of data (chronological instead of popularity-sorted) in a way that only shows up once real results are on screen.
