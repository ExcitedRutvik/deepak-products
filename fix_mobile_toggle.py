#!/usr/bin/env python3
"""
Move the dark/light toggle from inside the mobile menu to the nav bar.

Per page:
  1. Insert #theme-toggle-mob button (lg:hidden) into the nav bar,
     right before #mbtn (the hamburger), so it's always visible on mobile.
  2. Remove the entire #theme-row div from inside #mmenu.
"""

import glob, os, re

BASE_DIR = "/Users/rutvik/Documents/Project Code"

# The button to insert before #mbtn in the nav
MOB_TOGGLE = (
    '<button id="theme-toggle-mob" class="lg:hidden" aria-label="Toggle light / dark theme">'
    '<svg class="t-moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 12.79A9 9 0 1111.21 3a7 7 0 009.79 9.79z"/></svg>'
    '<svg class="t-sun"  width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
    '</button>\n    '
)

# Anchor in the nav to insert before
MBTN_ANCHOR = '<button id="mbtn" class="lg:hidden flex flex-col gap-[5px]"'

html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
ok = skip = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if 'id="theme-row"' not in content:
        print(f"  SKIP (no theme-row): {filename}")
        skip += 1
        continue

    original = content

    # 1. Insert mobile toggle into nav bar before #mbtn (only if not already there)
    if MOB_TOGGLE not in content and MBTN_ANCHOR in content:
        content = content.replace(MBTN_ANCHOR, MOB_TOGGLE + MBTN_ANCHOR, 1)

    # 2. Remove #theme-row from the mobile menu (regex handles whitespace variation)
    content = re.sub(r'\s*<div id="theme-row">.*?</div>', '', content, flags=re.DOTALL)

    if content == original:
        print(f"  no change: {filename}")
        skip += 1
        continue

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  OK: {filename}")
    ok += 1

print(f"\nDone: {ok} updated, {skip} skipped.")
