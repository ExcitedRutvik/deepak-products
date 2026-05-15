# Website Redesign — Design Transfer

## What this project is

The user has an **existing website** (with real content, copy, and images) that needs to be **rebuilt in the visual design language of a different reference website**. The content stays. The look changes.

Two inputs will be provided:

1. **Design reference** — a screenshot (and optionally CSS classes, color tokens, fonts, or style notes) of a website whose *visual language* should be adopted. This is the "how it should look."
2. **Content source** — the existing website that needs to be revamped. Provided as a URL, a screenshot, an HTML export, or pasted content. This is the "what goes on the page" — copy, headings, image positions, sections, structure, information hierarchy.

The job: take the content from #2 and present it in the visual language of #1.

## Workflow

When both inputs are available:

1. **Inventory the content source.** List every section, heading, paragraph, image, CTA, and link from the existing website. This is the content checklist — nothing in it gets dropped, nothing outside it gets added.
2. **Extract the design language from the reference.** Note down the concrete visual tokens:
   - Color palette (exact hex values)
   - Typography (font families, sizes, weights, line heights, letter spacing)
   - Spacing scale and section padding
   - Component patterns (card style, button style, nav style, hero style)
   - Border radii, shadows, gradients, effects
   - Imagery treatment (full-bleed, framed, masked, overlaid)
   - Layout grid and rhythm
   - **Motion and effects** — smooth scroll behavior, scroll-triggered reveals, sticky/pinned sections, hover states, parallax, custom cursors, intro animations, transitions. See the **Motion & Effects** section below for the full catalog and tooling.
   If the user provided CSS classes or tokens, use them verbatim.
3. **Generate** a single `index.html` using Tailwind CSS via CDN. Map each content item from step 1 into the visual patterns from step 2. Inline everything — no external files unless requested.
4. **Screenshot** the rendered page using Puppeteer (`npx puppeteer screenshot index.html --fullpage` or equivalent). Capture distinct sections individually too if the page is long.
5. **Compare on three axes:**
   - **Design fidelity** — does the output match the *reference's* visual language? (spacing, colors, typography, component shapes, rhythm)
   - **Motion fidelity** — do scroll behavior, reveals, hovers, and transitions feel like the reference? (timing, easing, stagger, scrub vs. play-once)
   - **Content fidelity** — does the output preserve every piece of content from the *content source*? (no missing sections, no invented copy, images in roughly the right places)
6. **Fix every mismatch.** Be specific: "hero padding is 48px but reference uses ~96px", "card border-radius is 8px but reference shows 16px", "About section from content source is missing", "headline reveal stagger is 0.05s but reference looks ~0.12s".
7. **Re-screenshot and compare again.** For motion, also re-record or step through the animation manually.
8. **Repeat 5–7** until design is within ~2–3px of the reference everywhere, motion feels right, and every content item from the source is present.

Do NOT stop after one pass. Always do at least 2 comparison rounds. Only stop when the user says so or when both axes are clean.

## Motion & Effects (when the reference is animated)

The design reference may include motion — smooth scrolling, scroll-triggered reveals, sticky/pinned sections, hover effects, parallax, mouse-follow cursors, intro animations, transitions. Treat motion as part of the design language and recreate it with the same fidelity as colors and type. Do not skip animations, and do not invent ones the reference doesn't have.

### Step 1 — Catalog the motion before coding

For each effect on the reference site, write down:
- **Trigger** — page load, scroll position, hover, click, viewport intersection, mouse move
- **Target** — which element(s) animate
- **Properties** — what changes (opacity, transform/translate/scale/rotate, clip-path, color, blur, filter)
- **Timing** — duration in ms/s, easing curve (ease-out-expo, cubic-bezier values, linear, etc.)
- **Stagger** — for groups of elements, the delay between each
- **Scroll mapping** — if scroll-driven: start position, end position, scrub vs. play-once

Common patterns to look for on minimal.gallery / Awwwards-style sites (like ova-investment.com):
- **Smooth scroll** — easing applied to the entire page scroll, not native browser scroll
- **Word/line mask reveal** — headlines split into words or lines, each masked then translated up into view
- **Pinned sticky sections** — a section pins to the viewport while inner content scrolls or transforms
- **Horizontal scroll inside vertical scroll** — common for portfolio strips
- **Image reveal on enter** — clip-path or scale-from-overlay as image enters viewport
- **Sticky index counter** — a number/label stays fixed and updates as sections pass
- **Marquee / infinite ticker** — text or logos translate horizontally on a loop, often scroll-influenced
- **Custom cursor** — a div follows mouse position, scales/morphs on hoverable targets
- **Magnetic buttons / links** — elements pull slightly toward the cursor on near-hover
- **Letter-by-letter or word rotator** — the "future / portfolio / collaboration" pattern (one word in a slot cycles through alternates)
- **Live time/clock** — small UI detail showing local time, updates every second
- **Menu morph** — full-screen overlay menu with staggered link reveal
- **Page transitions** — exit animation on click, enter animation on new route

### Step 2 — Pick the right tools

Default stack for an `index.html` build that needs serious motion:

```html
<!-- Smooth scroll -->
<link rel="stylesheet" href="https://unpkg.com/lenis@1.3.23/dist/lenis.css">
<script src="https://unpkg.com/lenis@1.3.23/dist/lenis.min.js"></script>

<!-- GSAP + ScrollTrigger + SplitText (free as of 2024) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/SplitText.min.js"></script>
```

Tool selection by effect:
- **Smooth scroll** → Lenis (sync with GSAP ticker so ScrollTrigger reads Lenis-driven scroll, not native)
- **Scroll-driven animations / pinning / scrubs** → GSAP ScrollTrigger
- **Headline word/line reveals** → GSAP SplitText (or manual `<span>` wrapping if avoiding the plugin)
- **Simple hover / micro-interactions** → CSS transitions, only reach for GSAP if the reference shows complex multi-property choreography
- **Custom cursor / magnetic links / mouse-follow** → vanilla JS with `requestAnimationFrame` and lerp toward target position
- **Marquee / infinite ticker** → CSS `@keyframes` with `transform: translateX` for simple cases; GSAP for scroll-influenced direction
- **Word rotator (cycling words in a slot)** → GSAP timeline with repeat, or a CSS-only solution if the timing is uniform
- **Reveal on enter** → IntersectionObserver + CSS class toggle for lightweight cases; ScrollTrigger for anything coupled to scroll progress
- **Page transitions in a single-page build** → GSAP timelines triggered on anchor click, not full route changes

### Step 3 — Standard Lenis + ScrollTrigger wiring

```js
const lenis = new Lenis({ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)) });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

Match Lenis's `duration` and `easing` to the feel of the reference site — if the reference scrolls long and floaty, raise `duration`; if it's snappy, lower it.

### Step 4 — Match motion fidelity, not just visual fidelity

When comparing the rendered build to the reference, also check:
- Does scroll feel as smooth/heavy/snappy as the reference?
- Do reveal animations trigger at roughly the same scroll position?
- Is the easing curve right? (linear vs. ease-out-expo vs. ease-in-out vs. custom cubic-bezier are visibly different)
- Do staggers feel even-paced? Tight or loose?
- Do hover effects respond at the same speed?
- Are pinned sections pinning for the same scroll distance?

Record motion mismatches with the same specificity as visual ones: "headline reveal duration is 0.6s but reference feels closer to 1.2s with ease-out-expo", "stagger between cards is 0.05s but reference looks ~0.12s".

### Step 5 — Performance and accessibility

- Animate `transform` and `opacity` only where possible — avoid animating `width`, `height`, `top`, `left`
- `will-change: transform` on heavy animated elements, but don't blanket-apply
- Honor `prefers-reduced-motion` — wrap motion init in a check and fall back to instant transitions
- Lenis has a known iOS Safari overscroll quirk; use the `autoToggle` option or disable on touch devices if the reference doesn't have smooth scroll on mobile (most don't — check)

## Technical Defaults

- Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`)
- If the reference uses custom fonts, load them via Google Fonts or the user-provided source
- If content-source images aren't directly accessible, use `https://placehold.co/` placeholders sized to match the original, and note clearly which images need to be swapped in by the user
- Use `.avif` or `.webp` for images when possible; fall back to `.jpg`
- Mobile-first responsive design
- Single `index.html` file unless the user requests otherwise; if the JS becomes large, allow a single `script.js` and `style.css` companion

## Rules

- **Content is sacred.** Do not drop sections, rewrite copy, or invent new content. If something exists on the source site, it goes on the new one. If it's not on the source, it doesn't appear.
- **Design is borrowed wholesale.** Match the reference's visual language exactly — colors, type, spacing, component shapes. Do not "improve" the reference design or mix in your own taste.
- **Motion is part of the design.** If the reference has smooth scroll, scroll-triggered reveals, hover effects, sticky sections, custom cursors, etc., recreate them. Do not deliver a static version of an animated reference. Conversely, do not invent animations the reference doesn't have.
- **Information architecture is preserved.** Section order, heading hierarchy, and the relationship between elements (e.g., image-left/text-right vs. stacked) follow the content source unless the reference's layout patterns require an obvious adaptation. When in doubt, ask.
- **No feature creep.** Don't add a testimonials section, a newsletter signup, or a footer link group that wasn't in the content source — even if the reference has one.
- **Verbatim tokens.** If the user gives CSS classes, hex codes, or font names, use them exactly as provided.
- **Specific feedback during comparison.** Don't say "spacing looks off" — say "the gap between hero and feature grid is 32px but the reference shows ~80px."
- Keep code clean but inline Tailwind classes are fine. Don't over-abstract.

## When inputs are missing or ambiguous

- If the user provides only the design reference, ask for the content source.
- If the user provides only the content source, ask for the design reference.
- If the design reference is a screenshot of just one section (e.g., only a hero), ask whether other sections should follow the same visual language by extension or whether more references are coming.
- If a content-source section has no clear analog in the reference's visual vocabulary, propose an adaptation and confirm before building it.