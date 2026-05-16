#!/usr/bin/env python3
"""
Light mode v3 — final CSS rule gaps:
  - .prod-img border (product detail pages)
  - .prod-label border-top (product detail pages)
  - .inp/.sinp ::placeholder (contact form, sidebar enquiry)
  - .sib-link:hover color
  - .fac-card border (infrastructure.html)
  - .lb-nav / .lb-dot (infrastructure lightbox)
  - .val-pill border (infrastructure.html)
  - .eq-item border-top / .proc-card border / .eq-panel-inner border (quality.html)
"""

import glob
import os

BASE_DIR = "/Users/rutvik/Documents/Project Code"

TOGGLE_ANCHOR = "/* Toggle button */"

NEW_CSS = """    html[data-theme="light"] .prod-img { border-color: rgba(0,0,0,0.10); }
    html[data-theme="light"] .prod-label { border-top-color: rgba(0,0,0,0.08); }
    html[data-theme="light"] .inp::placeholder,
    html[data-theme="light"] .sinp::placeholder { color: rgba(0,0,0,0.40) !important; }
    html[data-theme="light"] .sib-link:hover { color: #111; }
    html[data-theme="light"] .fac-card { border-color: rgba(0,0,0,0.10); }
    html[data-theme="light"] .lb-nav { background: rgba(0,0,0,0.06) !important; border-color: rgba(0,0,0,0.12) !important; color: #111 !important; }
    html[data-theme="light"] .lb-dot { background: rgba(0,0,0,0.22) !important; }
    html[data-theme="light"] .val-pill { border-color: rgba(0,0,0,0.12); }
    html[data-theme="light"] .eq-item { border-top-color: rgba(0,0,0,0.10); }
    html[data-theme="light"] .proc-card { border-color: rgba(0,0,0,0.10); }
    html[data-theme="light"] .eq-panel-inner { border-color: rgba(0,0,0,0.10); background: #f0f0f0; }
    """

html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
ok = skip = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'sinp::placeholder' in content and 'data-theme' in content and 'rgba(0,0,0,0.40)' in content:
        print(f"  SKIP (already done): {filename}")
        skip += 1
        continue

    if TOGGLE_ANCHOR not in content:
        print(f"  WARN: anchor not found in {filename}")
        continue

    content = content.replace(TOGGLE_ANCHOR, NEW_CSS + TOGGLE_ANCHOR, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK: {filename}")
    ok += 1

print(f"\nDone: {ok} updated, {skip} skipped, {len(html_files)} total.")
