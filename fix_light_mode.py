#!/usr/bin/env python3
"""Comprehensive light-mode visibility fix for all 24 HTML pages."""

import os
import re
import glob

BASE_DIR = "/Users/rutvik/Documents/Project Code"

# ── Old :root vars block (exact string from add_theme_toggle.py output) ────
OLD_ROOT_VARS = """    :root {
      --fg-dim: rgba(255,255,255,0.45); --fg-faint: rgba(255,255,255,0.25);
      --border-sub: rgba(255,255,255,0.07); --border-dim: rgba(255,255,255,0.10);
      --border-med: rgba(255,255,255,0.12);
    }
    html[data-theme="light"] {
      --fg-dim: rgba(17,17,17,0.45); --fg-faint: rgba(17,17,17,0.25);
      --border-sub: rgba(0,0,0,0.07); --border-dim: rgba(0,0,0,0.10);
      --border-med: rgba(0,0,0,0.12);
    }"""

NEW_ROOT_VARS = """    :root {
      --fg-dim: rgba(255,255,255,0.45); --fg-faint: rgba(255,255,255,0.25);
      --border-sub: rgba(255,255,255,0.07); --border-dim: rgba(255,255,255,0.10);
      --border-med: rgba(255,255,255,0.12);
      --fg-lo: rgba(255,255,255,0.40); --fg-mid: rgba(255,255,255,0.50);
      --fg-med: rgba(255,255,255,0.60); --fg-hi: rgba(255,255,255,0.70);
      --fg-ghost: rgba(255,255,255,0.22); --fg-faintest: rgba(255,255,255,0.15);
    }
    html[data-theme="light"] {
      --fg-dim: rgba(17,17,17,0.45); --fg-faint: rgba(17,17,17,0.25);
      --border-sub: rgba(0,0,0,0.07); --border-dim: rgba(0,0,0,0.10);
      --border-med: rgba(0,0,0,0.12);
      --fg-lo: rgba(17,17,17,0.40); --fg-mid: rgba(17,17,17,0.50);
      --fg-med: rgba(17,17,17,0.60); --fg-hi: rgba(17,17,17,0.70);
      --fg-ghost: rgba(17,17,17,0.22); --fg-faintest: rgba(17,17,17,0.15);
    }"""

# ── New CSS rules inserted before /* Toggle button */ ──────────────────────
NEW_CSS_RULES = """    /* Additional light-mode overrides */
    html[data-theme="light"] .text-white\\/30 { color: rgba(17,17,17,0.30) !important; }
    html[data-theme="light"] .text-white\\/40 { color: rgba(17,17,17,0.40) !important; }
    html[data-theme="light"] .text-white\\/50 { color: rgba(17,17,17,0.50) !important; }
    html[data-theme="light"] .text-white\\/60 { color: rgba(17,17,17,0.60) !important; }
    html[data-theme="light"] .bg-white\\/15 { background-color: rgba(0,0,0,0.05) !important; }
    html[data-theme="light"] .bg-white\\/50 { background-color: rgba(0,0,0,0.20) !important; }
    html[data-theme="light"] .border-white\\/8 { border-color: rgba(0,0,0,0.08) !important; }
    html[data-theme="light"] .border-white\\/15 { border-color: rgba(0,0,0,0.15) !important; }
    html[data-theme="light"] .bg-black\\/75 { background-color: rgba(0,0,0,0.06) !important; }
    html[data-theme="light"] .bg-black\\/80 { background-color: rgba(0,0,0,0.06) !important; }
    html[data-theme="light"] .cval { color: #111; }
    html[data-theme="light"] #nav img { filter: invert(1); }
    html[data-theme="light"] .nl { color: rgba(0,0,0,0.55) !important; }
    html[data-theme="light"] [style*="color:#fff"] { color: #111 !important; }
    html[data-theme="light"] [style*="fill:rgba(255,255,255"] { fill: rgba(17,17,17,0.40) !important; }
    html[data-theme="light"] .inp,
    html[data-theme="light"] .sinp {
      background: rgba(0,0,0,0.04) !important;
      border-color: rgba(0,0,0,0.15) !important;
      color: #111 !important;
    }
    html[data-theme="light"] .hero-viz-frame { background: #0d0d0d; }
    html[data-theme="light"] .page-banner { border-bottom-color: rgba(0,0,0,0.08); }
    html[data-theme="light"] .diff-card,
    html[data-theme="light"] .sidebar-box { border-color: rgba(0,0,0,0.10); }
    html[data-theme="light"] .spec-row { border-bottom-color: rgba(0,0,0,0.08); }
    html[data-theme="light"] .spec-value { color: rgba(17,17,17,0.58); }
    html[data-theme="light"] .sib-link { border-bottom-color: rgba(0,0,0,0.08); color: rgba(17,17,17,0.55); }
    html[data-theme="light"] .mat-pill { border-color: rgba(0,0,0,0.12); }
    html[data-theme="light"] .hover\\:text-white:hover { color: #111 !important; }
    """

TOGGLE_ANCHOR = "/* Toggle button */"

# ── Inline rgba substitutions for remaining unconverted values ─────────────
INLINE_REPLACEMENTS_2 = [
    # 0.72 / 0.7 / 0.70 → --fg-hi
    ('color:rgba(255,255,255,0.72)',  'color:var(--fg-hi)'),
    ('color:rgba(255,255,255,0.70)',  'color:var(--fg-hi)'),
    ('color:rgba(255,255,255,0.7)',   'color:var(--fg-hi)'),
    ('color: rgba(255,255,255,0.7)',  'color:var(--fg-hi)'),
    # 0.6 / 0.60 / 0.58 → --fg-med
    ('color:rgba(255,255,255,0.60)',  'color:var(--fg-med)'),
    ('color:rgba(255,255,255,0.6)',   'color:var(--fg-med)'),
    ('color: rgba(255,255,255,0.6)',  'color:var(--fg-med)'),
    ('color:rgba(255,255,255,0.58)',  'color:var(--fg-med)'),
    # 0.5 / 0.50 → --fg-mid
    ('color:rgba(255,255,255,0.50)',  'color:var(--fg-mid)'),
    ('color:rgba(255,255,255,0.5)',   'color:var(--fg-mid)'),
    ('color: rgba(255,255,255,0.5)',  'color:var(--fg-mid)'),
    # 0.42 / 0.40 / 0.4 / 0.38 → --fg-lo
    ('color:rgba(255,255,255,0.42)',  'color:var(--fg-lo)'),
    ('color:rgba(255,255,255,0.40)',  'color:var(--fg-lo)'),
    ('color:rgba(255,255,255,0.4)',   'color:var(--fg-lo)'),
    ('color: rgba(255,255,255,0.4)',  'color:var(--fg-lo)'),
    ('color:rgba(255,255,255,0.38)',  'color:var(--fg-lo)'),
    ('color: rgba(255,255,255,0.38)', 'color:var(--fg-lo)'),
    # 0.22 / 0.2 → --fg-ghost
    ('color:rgba(255,255,255,0.22)',  'color:var(--fg-ghost)'),
    ('color: rgba(255,255,255,0.22)', 'color:var(--fg-ghost)'),
    ('color:rgba(255,255,255,0.2)',   'color:var(--fg-ghost)'),
    ('color: rgba(255,255,255,0.2)',  'color:var(--fg-ghost)'),
    # 0.15 → --fg-faintest
    ('color:rgba(255,255,255,0.15)',  'color:var(--fg-faintest)'),
    ('color: rgba(255,255,255,0.15)', 'color:var(--fg-faintest)'),
]

# ── Process ────────────────────────────────────────────────────────────────

html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
ok = skip = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already processed
    if '--fg-lo' in content:
        print(f"  SKIP (already done): {filename}")
        skip += 1
        continue

    changes = []

    # 1. Extend :root + html[data-theme="light"] var blocks
    if OLD_ROOT_VARS in content:
        content = content.replace(OLD_ROOT_VARS, NEW_ROOT_VARS, 1)
        changes.append('CSS vars extended')
    else:
        print(f"  WARN: old :root block not found in {filename}")

    # 2. Insert new CSS rules before /* Toggle button */
    toggle_idx = content.find(TOGGLE_ANCHOR)
    if toggle_idx != -1:
        content = content[:toggle_idx] + NEW_CSS_RULES + content[toggle_idx:]
        changes.append('new CSS rules')
    else:
        print(f"  WARN: toggle anchor not found in {filename}")

    # 3. Inline rgba substitutions (skip lines that already use var(--)
    lines = content.split('\n')
    new_lines = []
    n_inline = 0
    for line in lines:
        if 'var(--' not in line:
            for old, new in INLINE_REPLACEMENTS_2:
                if old in line:
                    line = line.replace(old, new)
                    n_inline += 1
        new_lines.append(line)
    content = '\n'.join(new_lines)
    if n_inline:
        changes.append(f'{n_inline} inline color vars')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK [{', '.join(changes)}]: {filename}")
    ok += 1

print(f"\nDone: {ok} updated, {skip} skipped, {len(html_files)} total.")
