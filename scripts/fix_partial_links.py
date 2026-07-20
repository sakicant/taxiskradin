# -*- coding: utf-8 -*-
"""Make localized partial nav links safe.

The localized partials for the new languages prefix every internal href with
/<lang>. That only works if the target page actually exists in that language.
This rewrites each /<lang>/<slug>/ href to the plain English /<slug>/ whenever
the localized page does not exist yet, so navigation never 404s. When a
translation is later added, re-running this restores the localized link.

Usage: python scripts/fix_partial_links.py <site-root> [lang ...]
"""
import os, re, json, sys, io

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = sys.argv[2:] or ["es", "sv", "sr", "no", "zh", "ko", "fi", "ja"]
PAGES = os.path.join(ROOT, "src", "pages")
PARTIALS = os.path.join(ROOT, "src", "partials")


def slugs_for(lang):
    """Every slug that actually exists for this language."""
    out = set()
    for pid in os.listdir(PAGES):
        mp = os.path.join(PAGES, pid, lang, "meta.json")
        if os.path.isfile(mp):
            try:
                out.add(json.load(io.open(mp, encoding="utf-8")).get("slug", ""))
            except Exception:
                pass
    return out


total_fixed = 0
for lang in LANGS:
    have = slugs_for(lang)
    for name in ("header", "footer", "quote-widget", "related-links"):
        fn = os.path.join(PARTIALS, "%s.%s.html" % (name, lang))
        if not os.path.isfile(fn):
            continue
        s = io.open(fn, encoding="utf-8").read()
        fixed = [0]

        def repl(m):
            path = m.group(1)          # e.g. "about/" or "" for the home link
            slug = path.rstrip("/")    # the home page's slug is "" by convention
            if slug in have:
                return m.group(0)      # localized page exists, keep it
            fixed[0] += 1
            return 'href="/%s"' % path  # fall back to the English page

        new = re.sub(r'href="/%s/([^"]*)"' % re.escape(lang), repl, s)
        if fixed[0]:
            io.open(fn, "w", encoding="utf-8").write(new)
            total_fixed += fixed[0]
            print("  %-22s %s -> %d links pointed at English" % (name + "." + lang, "", fixed[0]))
print("total links made safe:", total_fixed)
