#!/usr/bin/env python3
"""
Normalize inner-page font sizes to match homepage scale.

Changes:
  1. clamp(1.2rem,2.8vw,2.8rem) → clamp(1.8rem,3.5vw,4rem)
       Product detail page h1 (16 pages) — was tiny; now matches homepage energy.

  2. clamp(1.4rem,3.2vw,3.2rem) → clamp(2rem,4vw,4.5rem)
       Content page h1 banners (infrastructure, about, quality, products, etc.)

  3. clamp(1.4rem,2.5vw,2.5rem) → clamp(1.6rem,3vw,3rem)
       Secondary h2 subheadings on content pages.

  4. clamp(1.5rem,3vw,3rem) → clamp(1.8rem,4vw,4rem)
       CTA/bottom section h2 on product detail pages.

Skips index.html (homepage — reference, not changed).
"""

import glob, os

BASE_DIR = "/Users/rutvik/Documents/Project Code"

REPLACEMENTS = [
    # Product detail page h1 — most impactful
    ("font-size:clamp(1.2rem,2.8vw,2.8rem)", "font-size:clamp(1.8rem,3.5vw,4rem)"),
    # Content page banner h1
    ("font-size:clamp(1.4rem,3.2vw,3.2rem)", "font-size:clamp(2rem,4vw,4.5rem)"),
    # Secondary h2 subheadings
    ("font-size:clamp(1.4rem,2.5vw,2.5rem)", "font-size:clamp(1.6rem,3vw,3rem)"),
    # CTA h2 at bottom of product pages
    ("font-size:clamp(1.5rem,3vw,3rem)",     "font-size:clamp(1.8rem,4vw,4rem)"),
]

html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
ok = skip = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename == "index.html":
        print(f"  SKIP (homepage reference): {filename}")
        skip += 1
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    changes = []
    for old, new in REPLACEMENTS:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f"{count}× {old.split('clamp')[1][:20]}…")

    if content == original:
        print(f"  no change: {filename}")
        skip += 1
        continue

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  OK [{len(changes)} rules, {', '.join(changes)}]: {filename}")
    ok += 1

print(f"\nDone: {ok} updated, {skip} skipped, {len(html_files)} total.")
