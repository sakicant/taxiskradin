# -*- coding: utf-8 -*-
"""Enforce the WhatsApp rule on hand-written pages.

Owner rule: the prefilled wa.me message must be ENGLISH in every language
except hr and sr (which stay Croatian). Route pages already follow this via
route_loc.py; some older hand-written translations still carry Croatian text.

For each offending page we copy the wa.me URLs from the English version of the
same page, which is by definition the correct English message.

Usage: python scripts/fix_wa_language.py <site-root>
"""
import os, re, io, sys

ROOT = os.path.abspath(sys.argv[1])
PAGES = os.path.join(ROOT, "src", "pages")
KEEP_CROATIAN = ("hr", "sr")

WA_RE = re.compile(r'https://wa\.me/[^"\']+')
# Markers that the prefilled text is Croatian rather than English.
CRO = ("Pozdrav", "%20bih%20", "rezervirati", "Moji%20podaci")

fixed = []
for pid in sorted(os.listdir(PAGES)):
    pd = os.path.join(PAGES, pid)
    en = os.path.join(pd, "en", "content.html")
    if not os.path.isfile(en):
        continue
    en_html = io.open(en, encoding="utf-8", errors="ignore").read()
    en_urls = WA_RE.findall(en_html)
    if not en_urls:
        continue
    en_url = en_urls[0]
    for lang in os.listdir(pd):
        if lang in KEEP_CROATIAN or lang == "en":
            continue
        cp = os.path.join(pd, lang, "content.html")
        if not os.path.isfile(cp):
            continue
        html = io.open(cp, encoding="utf-8", errors="ignore").read()
        urls = WA_RE.findall(html)
        if not urls:
            continue
        if not any(any(c in u for c in CRO) for u in urls):
            continue  # already English
        new = WA_RE.sub(lambda m: en_url, html)
        io.open(cp, "w", encoding="utf-8").write(new)
        fixed.append("%s/%s" % (pid, lang))

print("WhatsApp messages switched to English:", len(fixed))
for f in fixed[:20]:
    print("   ", f)
