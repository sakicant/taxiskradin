# -*- coding: utf-8 -*-
"""Generate localized (non-English) route pages for taxiskradin.hr.

Data-driven: loops every language present in route_loc.TR and every route in
docs/route-pages-skradin.md, and writes src/pages/<en-slug>/<lang>/{meta.json,
content.html} using the shared engine in route_loc.py. English pages are made
separately by gen_routes_skradin.py. Run after that, before build.py.
"""
import os, re, json, hashlib, sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import route_loc as R

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "src", "pages")

src = open(os.path.join(ROOT, "script.js"), encoding="utf-8").read()
i = src.index("const PRICES = {"); j = src.index("{", i); d = 0
for k in range(j, len(src)):
    if src[k] == "{": d += 1
    elif src[k] == "}":
        d -= 1
        if d == 0: end = k + 1; break
PRICES = json.loads(src[j:end])

def price(a, b):
    if a in PRICES and PRICES[a].get(b) is not None: return PRICES[a][b]
    if b in PRICES and PRICES[b].get(a) is not None: return PRICES[b][a]
    return None

DIST = json.load(open(os.path.join(ROOT, "docs", "route-distances.json"), encoding="utf-8"))
def fmt_time(sec):
    m = int(round(sec / 60 / 5.0) * 5)
    if m >= 90:
        h, mm = m // 60, m % 60
        return "%d h" % h if mm == 0 else "%d h %d min" % (h, mm)
    return "%d min" % m

MAPK = {'Šibenik':'Šibenik - center','Brodarica':'Brodarica - Šibenik','Skradin':'Skradin - center',
        'Split Airport':'Split Airport (SPU)','Zadar Airport':'Zadar Airport (ZAD)',
        'Zagreb Airport':'Zagreb Airport (ZAG)','Dubrovnik Airport':'Dubrovnik Airport (DBV)',
        'Roški Slap':'NP Krka - Roški Slap entrance'}
key = lambda n: MAPK.get(n, n)

BIG_CITIES = {'Split','Zadar','Dubrovnik','Zagreb','Trogir'}
AIRPORT_CITY = {'Split Airport':'Split','Zadar Airport':'Zadar','Zagreb Airport':'Zagreb','Dubrovnik Airport':'Dubrovnik'}
MARINAS = {'ACI Marina Trogir','Marina Trogir (SCT)','Marina Baotić','Marina Agana','Marina Pakoštane','D-Marin Dalmacija','Marina Frapa',
           'Marina Kremik','ACI Marina Vodice','Marina Tribunj','Marina Hramina','Marina Betina','ACI Marina Jezera'}

PROVIDER = {
    "@type": "LocalBusiness", "name": "Taxi Antonio",
    "telephone": "+385994471013", "email": "info@taxiskradin.hr",
    "address": {"@type": "PostalAddress", "addressLocality": "Skradin", "addressCountry": "HR"},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "142"},
}
TI_HERO = "43a5bc1770e0096ff5068047a68"
TI_REVIEWS = "8affc48775310964b636fcaecfe"

def vhash(slug, n):
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n

rows = []
for line in open(os.path.join(ROOT, "docs", "route-pages-skradin.md"), encoding="utf-8"):
    m = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*`(.+?)`\s*\|\s*(.+?)\s*\|', line)
    if not m: continue
    frm, to, slug, doc = m.groups()
    if frm == "From": continue
    rows.append((frm, to, slug))
slug_of = {(f, t): s for f, t, s in rows}

def bkey(name): return quote(key(name))

def route_type(frm, to):
    if to in AIRPORT_CITY: return "to_airport"
    if frm in AIRPORT_CITY: return "from_airport"
    if frm in MARINAS or to in MARINAS: return "marina"
    if frm in BIG_CITIES or to in BIG_CITIES: return "city"
    return "local"

def hero_for(frm, to, slug, typ):
    if typ in ("to_airport", "from_airport"):
        desk = "skradin-hero-airport.webp" if vhash(slug, 2) == 0 else "skradin-hero-airport-2.webp"
        return desk, "skradin-hero-airport-mobile.webp"
    if frm == "Roški Slap" or to == "Roški Slap":
        return "skradin-hero-roski.webp", "skradin-hero-roski-mobile.webp"
    return "skradin-hero-city.webp", "skradin-hero-city-mobile.webp"

LANGS = [l for l in R.TR]

def build_lang(lang, frm, to, en_slug):
    p = price(key(frm), key(to))
    rp = p * 2
    typ = route_type(frm, to)
    frm_loc, to_loc = R.name_for(lang, frm), R.name_for(lang, to)
    rel = "%s - %s" % (frm_loc, to_loc)
    loc_slug = R.slug_for(lang, en_slug)
    herod, herom = hero_for(frm, to, en_slug, typ)
    hero_html = ('<picture>\n'
        '        <source media="(max-width: 768px)" srcset="/assets/img/%s">\n'
        '        <img src="/assets/img/%s" alt="%s" loading="eager">\n'
        '      </picture>') % (herom, herod, R.TR[lang]["hero_alt"].format(rel=rel))

    rev = slug_of.get((to, frm))
    if rev:
        revlink = '<a href="/%s/%s/">%s - %s</a>' % (lang, R.slug_for(lang, rev), to_loc, frm_loc)
    elif frm == "Skradin" and to == "Šibenik":
        revlink = '<a href="https://taxisibenik.hr/%s/%s/">%s - %s</a>' % (
            lang, R.slug_for(lang, "taxi-sibenik-to-skradin"), to_loc, frm_loc)
    else:
        revlink = "%s - %s" % (to_loc, frm_loc)

    book_link = "/%s/%s/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (
        lang, R.TR[lang]["book_slug"], bkey(frm), bkey(to), p)

    dd = DIST.get("%s|%s" % (frm, to))
    ctx = {
        "frm": frm, "to": to, "rel": rel, "rel_from": frm_loc, "rel_to": to_loc,
        "city": AIRPORT_CITY.get(frm) or AIRPORT_CITY.get(to) or "",
        "p": p, "rp": rp, "typ": typ, "v": vhash(en_slug, 2),
        "dd": bool(dd), "km": dd["km"] if dd else None, "t": fmt_time(dd["sec"]) if dd else None,
        "hero_html": hero_html, "book_link": book_link, "revlink_html": revlink,
        "slug": loc_slug, "page_url": "https://taxiskradin.hr/%s/%s/" % (lang, loc_slug),
        "provider": PROVIDER, "og_image": "https://taxiskradin.hr/assets/img/%s" % herod,
        "ti_hero": TI_HERO, "ti_reviews": TI_REVIEWS,
    }
    content, meta = R.build_page(lang, ctx)
    outdir = os.path.join(PAGES, en_slug, lang)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = 0; skipped_noprice = 0
for lang in LANGS:
    for frm, to, en_slug in rows:
        if price(key(frm), key(to)) is None:
            skipped_noprice += 1; continue
        if en_slug == "taxi-sibenik-to-split-airport":
            continue
        build_lang(lang, frm, to, en_slug)
        made += 1
print("generated skradin localized:", made, "langs:", LANGS)
print("skipped (no matrix price):", skipped_noprice // max(1, len(LANGS)))
