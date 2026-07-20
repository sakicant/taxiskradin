# -*- coding: utf-8 -*-
"""Quality + coverage audit for one site.

Checks, across every page and language:
  - coverage: which page-ids are missing which languages
  - meta.json validity (parses, has slug/title/description)
  - the WhatsApp rule: prefilled message English everywhere except hr/sr
  - no em dashes anywhere
  - untranslated leftovers: non-English page whose title equals the English one

Usage: python scripts/audit_site.py <site-root> [route-list.md]
"""
import os, json, io, re, sys

ROOT = os.path.abspath(sys.argv[1])
ROUTE_MD = sys.argv[2] if len(sys.argv) > 2 else None
PAGES = os.path.join(ROOT, "src", "pages")

LANGS = ["en", "hr", "de", "pl", "cs", "it", "fr", "nl", "sl", "hu", "sk",
         "es", "sv", "sr", "no", "zh", "ko", "fi", "ja"]

route_slugs = set()
if ROUTE_MD and os.path.isfile(ROUTE_MD):
    for line in io.open(ROUTE_MD, encoding="utf-8"):
        m = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*`(.+?)`', line)
        if m and m.group(1) != "From":
            route_slugs.add(m.group(3))

bad_json, missing, wa_wrong, emdash, untranslated = [], {}, [], [], []
route_missing = {}
hand_missing = {}
en_titles = {}

pids = sorted(d for d in os.listdir(PAGES) if os.path.isdir(os.path.join(PAGES, d)))
for pid in pids:
    pd = os.path.join(PAGES, pid)
    have = set()
    for lang in os.listdir(pd):
        mp = os.path.join(pd, lang, "meta.json")
        cp = os.path.join(pd, lang, "content.html")
        if not (os.path.isfile(mp) and os.path.isfile(cp)):
            continue
        have.add(lang)
        try:
            meta = json.load(io.open(mp, encoding="utf-8"))
        except Exception as e:
            bad_json.append("%s/%s: %s" % (pid, lang, e))
            continue
        for k in ("slug", "title", "description"):
            if k not in meta:
                bad_json.append("%s/%s missing %s" % (pid, lang, k))
        if lang == "en":
            en_titles[pid] = meta.get("title", "")
        html = io.open(cp, encoding="utf-8", errors="ignore").read()
        if "—" in html or "—" in meta.get("title", ""):
            emdash.append("%s/%s" % (pid, lang))
        # WhatsApp rule
        m = re.search(r'wa\.me/[^"\']*text=([^"\'&]*)', html)
        if m:
            txt = m.group(1)
            croatian = ("Pozdrav" in txt) or ("%20bih%20" in txt) or ("Pozdrav" in txt)
            if lang in ("hr", "sr"):
                pass  # Croatian expected
            elif croatian:
                wa_wrong.append("%s/%s" % (pid, lang))
    missing_langs = [l for l in LANGS if l not in have]
    if missing_langs:
        (route_missing if pid in route_slugs else hand_missing)[pid] = missing_langs

# untranslated leftovers (non-en title identical to en title)
for pid in pids:
    pd = os.path.join(PAGES, pid)
    for lang in os.listdir(pd):
        if lang == "en":
            continue
        mp = os.path.join(pd, lang, "meta.json")
        if not os.path.isfile(mp):
            continue
        try:
            t = json.load(io.open(mp, encoding="utf-8")).get("title", "")
        except Exception:
            continue
        if t and t == en_titles.get(pid):
            untranslated.append("%s/%s" % (pid, lang))

print("SITE:", ROOT)
print("page-ids:", len(pids), "| route pages:", len(route_slugs), "| languages expected:", len(LANGS))
print("")
print("invalid/incomplete meta.json:", len(bad_json))
for b in bad_json[:5]: print("   ", b)
print("WhatsApp rule violations (Croatian text on a non-hr/sr page):", len(wa_wrong))
for b in wa_wrong[:5]: print("   ", b)
print("pages containing an em dash:", len(emdash))
for b in emdash[:5]: print("   ", b)
print("untranslated (title identical to English):", len(untranslated))
for b in untranslated[:5]: print("   ", b)
print("")
print("ROUTE pages missing languages:", len(route_missing))
for k in list(route_missing)[:3]: print("   ", k, "->", route_missing[k])
print("HAND-WRITTEN pages missing languages:", len(hand_missing))
tot = 0
for k in sorted(hand_missing):
    tot += len(hand_missing[k])
print("   total missing hand-written translations:", tot)
for k in sorted(hand_missing)[:6]:
    print("   ", k, "missing:", ",".join(hand_missing[k]))
