# -*- coding: utf-8 -*-
"""Audit built pages for broken internal links.

Usage: python scripts/check_links.py <site-root> [lang ...]
Samples built pages for the given languages (default: the 8 new ones) and
checks that every internal href resolves to a generated index.html.
"""
import os, re, io, sys, random

ROOT = sys.argv[1]
LANGS = sys.argv[2:] or ["es", "sv", "sr", "no", "zh", "ko", "fi", "ja"]
SKIP_EXT = (".xml", ".txt", ".php", ".svg", ".webp", ".css", ".js", ".json", ".ico", ".png", ".jpg")

targets = []
for lang in LANGS:
    d = os.path.join(ROOT, lang)
    if not os.path.isdir(d):
        continue
    for sub in os.listdir(d):
        f = os.path.join(d, sub, "index.html")
        if os.path.isfile(f):
            targets.append(f)

random.seed(1)
sample = random.sample(targets, min(80, len(targets)))
bad = {}
for f in sample:
    s = io.open(f, encoding="utf-8", errors="ignore").read()
    for h in set(re.findall(r'href="(/[^"#?]*)"', s)):
        if h.startswith("/assets") or h.lower().endswith(SKIP_EXT):
            continue
        rel = h.strip("/")
        p = os.path.join(ROOT, "index.html") if rel == "" else os.path.join(ROOT, rel.replace("/", os.sep), "index.html")
        if not os.path.isfile(p):
            bad[h] = bad.get(h, 0) + 1

print("languages checked:", ", ".join(LANGS))
print("built pages sampled:", len(sample), "of", len(targets))
print("BROKEN internal links:", len(bad))
for k, v in sorted(bad.items(), key=lambda x: -x[1])[:12]:
    print("   ", k, "x", v)
