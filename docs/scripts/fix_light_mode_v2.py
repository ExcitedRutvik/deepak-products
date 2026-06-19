#!/usr/bin/env python3
"""
Light mode v2 fixes:
  1. Logo: brightness(0) instead of invert(1) — kills purple tint from green gradient
  2. Text colors: all --fg-* light-mode vars bumped ~25% darker for legibility
  3. Direct color overrides (nl, nav-dd-link, flink, spec-value, sib-link) darkened
  4. index.html: CNC canvas line widths ×1.5 in light mode via lm() helper
  5. index.html: canvas opacity 1.0 in light mode (was 0.78)
"""

import glob
import os

BASE_DIR = "/Users/rutvik/Documents/Project Code"

# ─────────────────────────────────────────────────────────────────────────────
# ALL-PAGE replacements (simple str.replace, all 24 files)
# ─────────────────────────────────────────────────────────────────────────────

ALL_PAGE_REPLACEMENTS = [

    # 1. Fix logo filter: invert(1) inverts green → purple; brightness(0) → all black
    (
        'html[data-theme="light"] #nav img { filter: invert(1); }',
        'html[data-theme="light"] #nav img { filter: brightness(0); }',
    ),

    # 2. Darker CSS vars — line 1 of the light-mode var block
    (
        '--fg-dim: rgba(17,17,17,0.45); --fg-faint: rgba(17,17,17,0.25);',
        '--fg-dim: rgba(17,17,17,0.62); --fg-faint: rgba(17,17,17,0.42);',
    ),

    # 3. Darker CSS vars — line 2 of the light-mode var block
    (
        '--fg-lo: rgba(17,17,17,0.40); --fg-mid: rgba(17,17,17,0.50);',
        '--fg-lo: rgba(17,17,17,0.58); --fg-mid: rgba(17,17,17,0.68);',
    ),

    # 4. Darker CSS vars — line 3 of the light-mode var block
    (
        '--fg-med: rgba(17,17,17,0.60); --fg-hi: rgba(17,17,17,0.70);',
        '--fg-med: rgba(17,17,17,0.78); --fg-hi: rgba(17,17,17,0.88);',
    ),

    # 5. Darker CSS vars — line 4 of the light-mode var block
    (
        '--fg-ghost: rgba(17,17,17,0.22); --fg-faintest: rgba(17,17,17,0.15);',
        '--fg-ghost: rgba(17,17,17,0.38); --fg-faintest: rgba(17,17,17,0.28);',
    ),

    # 6. Darker nav links (original rule from add_theme_toggle.py — no !important)
    (
        'html[data-theme="light"] .nl { color: rgba(0,0,0,0.55); }',
        'html[data-theme="light"] .nl { color: rgba(0,0,0,0.72); }',
    ),

    # 7. Darker nav links (rule from fix_light_mode.py — with !important)
    (
        'html[data-theme="light"] .nl { color: rgba(0,0,0,0.55) !important; }',
        'html[data-theme="light"] .nl { color: rgba(0,0,0,0.72) !important; }',
    ),

    # 8. Darker dropdown links
    (
        'html[data-theme="light"] .nav-dd-link { color: rgba(0,0,0,0.42); }',
        'html[data-theme="light"] .nav-dd-link { color: rgba(0,0,0,0.62); }',
    ),

    # 9. Darker footer links
    (
        'html[data-theme="light"] .flink { color: rgba(0,0,0,0.45); }',
        'html[data-theme="light"] .flink { color: rgba(0,0,0,0.62); }',
    ),

    # 10. Darker text-white/70 override
    (
        'html[data-theme="light"] .text-white\\/70 { color: rgba(17,17,17,0.7) !important; }',
        'html[data-theme="light"] .text-white\\/70 { color: rgba(17,17,17,0.88) !important; }',
    ),

    # 11. Darker Tailwind opacity class overrides
    (
        'html[data-theme="light"] .text-white\\/30 { color: rgba(17,17,17,0.30) !important; }',
        'html[data-theme="light"] .text-white\\/30 { color: rgba(17,17,17,0.48) !important; }',
    ),
    (
        'html[data-theme="light"] .text-white\\/40 { color: rgba(17,17,17,0.40) !important; }',
        'html[data-theme="light"] .text-white\\/40 { color: rgba(17,17,17,0.58) !important; }',
    ),
    (
        'html[data-theme="light"] .text-white\\/50 { color: rgba(17,17,17,0.50) !important; }',
        'html[data-theme="light"] .text-white\\/50 { color: rgba(17,17,17,0.68) !important; }',
    ),
    (
        'html[data-theme="light"] .text-white\\/60 { color: rgba(17,17,17,0.60) !important; }',
        'html[data-theme="light"] .text-white\\/60 { color: rgba(17,17,17,0.78) !important; }',
    ),

    # 12. Darker spec value and sib-link text
    (
        'html[data-theme="light"] .spec-value { color: rgba(17,17,17,0.58); }',
        'html[data-theme="light"] .spec-value { color: rgba(17,17,17,0.72); }',
    ),
    (
        'color: rgba(17,17,17,0.55); }',
        'color: rgba(17,17,17,0.70); }',
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# index.html-only changes
# ─────────────────────────────────────────────────────────────────────────────

INDEX_REPLACEMENTS = [
    # Add lm() helper right after ctx is created
    (
        'const ctx = canvas.getContext(\'2d\');',
        'const ctx = canvas.getContext(\'2d\');\n    function lm(w){return document.documentElement.getAttribute(\'data-theme\')==\'light\'?w*1.5:w;}',
    ),
    # Bump all lineWidth=1 to lm(1)
    (   'ctx.lineWidth=1; ctx.strokeRect',  'ctx.lineWidth=lm(1); ctx.strokeRect' ),
    (   'ctx.lineWidth=1;\n',               'ctx.lineWidth=lm(1);\n' ),
    (   'ctx.lineWidth=1;ctx.setLineDash',  'ctx.lineWidth=lm(1);ctx.setLineDash' ),
    (   'ctx.setLineDash([3,3]); ctx.lineWidth=1;', 'ctx.setLineDash([3,3]); ctx.lineWidth=lm(1);' ),
    (   'ctx.setLineDash([2,5]); ctx.strokeStyle=\'rgba(74,171,61,0.22)\'; ctx.lineWidth=1;',
        'ctx.setLineDash([2,5]); ctx.strokeStyle=\'rgba(74,171,61,0.22)\'; ctx.lineWidth=lm(1);' ),
    (   'ctx.strokeStyle=\'rgba(74,171,61,0.5)\';ctx.lineWidth=1;',
        'ctx.strokeStyle=\'rgba(74,171,61,0.5)\';ctx.lineWidth=lm(1);' ),
    (   'ctx.strokeStyle=\'rgba(74,171,61,0.85)\';ctx.lineWidth=1.5;',
        'ctx.strokeStyle=\'rgba(74,171,61,0.85)\';ctx.lineWidth=lm(1.5);' ),
    (   'ctx.strokeStyle=\'rgba(74,171,61,0.75)\';ctx.lineWidth=1.2;',
        'ctx.strokeStyle=\'rgba(74,171,61,0.75)\';ctx.lineWidth=lm(1.2);' ),
    (   'ctx.strokeStyle=\'rgba(74,171,61,0.6)\';ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(head3',
        'ctx.strokeStyle=\'rgba(74,171,61,0.6)\';ctx.lineWidth=lm(1.2);ctx.beginPath();ctx.moveTo(head3' ),
    (   'ctx.strokeStyle=\'rgba(255,255,255,0.10)\';ctx.lineWidth=1;ctx.strokeRect',
        'ctx.strokeStyle=\'rgba(255,255,255,0.10)\';ctx.lineWidth=lm(1);ctx.strokeRect' ),
    (   'ctx.strokeStyle=\'rgba(255,255,255,0.08)\';ctx.lineWidth=1;',
        'ctx.strokeStyle=\'rgba(255,255,255,0.08)\';ctx.lineWidth=lm(1);' ),
    # spark lineWidth stays thin (sparks are tiny) — already handled by ctx.lineWidth=1; on its own line
    # canvas opacity 1.0 in light mode
    (
        'html[data-theme="light"] .hero-viz-frame { background: #0d0d0d; }',
        'html[data-theme="light"] .hero-viz-frame { background: #0d0d0d; }\n    html[data-theme="light"] #cnc-canvas { opacity: 1; }',
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Process files
# ─────────────────────────────────────────────────────────────────────────────

html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
ok = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already processed
    if 'rgba(17,17,17,0.62)' in content:
        print(f"  SKIP (already done): {filename}")
        continue

    changes = []

    for old, new in ALL_PAGE_REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            changes.append(old[:40].strip())
        # else: silently skip (some rules may not be present on all pages)

    if filename == 'index.html':
        for old, new in INDEX_REPLACEMENTS:
            if old in content:
                content = content.replace(old, new)
                changes.append('canvas:' + old[:30].strip())

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK [{len(changes)} changes]: {filename}")
    ok += 1

print(f"\nDone: {ok}/{len(html_files)} files updated.")
