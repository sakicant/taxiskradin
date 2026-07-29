# -*- coding: utf-8 -*-
"""Generate skradin's 301 redirect block for .htaccess from the list of old
taxiskradin.hr WordPress URLs that now 404 (exported from Search Console to
scripts/redirects-source-skradin.txt).

Each old URL is mapped to its closest current page:
  - old localized booking slugs (/de/buchen/, ...) -> /<lang>/book/ (query kept)
  - old hubs / airport / city-to-city / krka / winery -> the current hub
  - old policy / terms / about -> the current localized slug (from meta.json)
  - old route pages (taxi-... ) -> the relevant hub (airport vs city transfers),
    since the new route slugs differ and the hub is the safe, relevant target
  - old blog posts -> the language home
  - WordPress plugin/admin junk (wp-*, feeds, author archives, *) -> skipped

Run: python scripts/gen_redirects.py         (writes the block into .htaccess)
     python scripts/gen_redirects.py --dry    (print report only)
"""
import os, io, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scripts", "redirects-source-skradin.txt")
HTACCESS = os.path.join(ROOT, ".htaccess")
DRY = "--dry" in sys.argv

LANGS = ["de", "hr", "pl", "cs", "it", "fr", "nl", "sl", "hu", "sk",
         "es", "sv", "sr", "no", "zh", "ko", "fi", "ja"]

# Old localized /book/ slugs seen in the 404 list.
BOOKING_SLUGS = {"rezervace", "buchen", "reservar", "reservation", "rezervacija",
                 "foglalas", "prenota", "rezerwacja", "boka", "varaa", "yoyaku",
                 "yeyak", "boeken", "bestill", "rezervacia", "yuding"}

HUBS = {
    "airport": "skradin-airport-transfers",
    "city": "skradin-transfers",
    "krka": "krka-national-park-transfers",
    "winery": "skradin-winery-transfers",
    "aci": "aci-marina-skradin-transfers",
}


def slug_of(page_id, lang):
    p = os.path.join(ROOT, "src", "pages", page_id, lang, "meta.json")
    if not os.path.isfile(p):
        p = os.path.join(ROOT, "src", "pages", page_id, "en", "meta.json")
    return json.load(io.open(p, encoding="utf-8"))["slug"]


def is_junk(rest, full):
    bad = ["wp-", "cgi-bin", "edd-api", "wc-api", "jetpack", "kinsta",
           "ao_noptirocket", "ao_speedup", "removed_item", "trustindex.io"]
    if any(b in full for b in bad):
        return True
    if "/author/" in full or rest.startswith("author/"):
        return True
    if rest.endswith("/feed") or "/feed/" in full or "*" in full:
        return True
    return False


def target(lang, rest):
    """Return the current path (with leading slash) for an old <lang>/<rest>."""
    pref = "" if lang == "en" else "/" + lang
    first = rest.split("/")[0]

    # Booking pages
    if first in BOOKING_SLUGS or first == "book":
        return pref + "/book/"

    # Policy / terms / about (match by old slug keywords)
    if first in ("privacy-policy", "datenschutz", "polityka-prywatnosci") or "prywatnosc" in first or "privatnost" in first:
        return pref + "/" + slug_of("privacy-policy", lang) + "/"
    if first in ("terms-and-conditions", "agb") or "warunki" in first or "uvjeti" in first:
        return pref + "/" + slug_of("terms-and-conditions", lang) + "/"
    if first in ("about", "o-meni", "ueber-mich", "o-mnie") or first.startswith("about"):
        return pref + "/" + slug_of("about", lang) + "/"

    # Hubs by keyword
    if "krka" in rest:
        return pref + "/" + HUBS["krka"] + "/"
    if "winer" in rest or "vinar" in rest or "wein" in rest or "winnic" in rest:
        return pref + "/" + HUBS["winery"] + "/"
    if "aci-marina" in rest or "aci_marina" in rest:
        return pref + "/" + HUBS["aci"] + "/"

    airport_kw = ["flughafen", "lotnisk", "zracn", "airport", "aeroport", "letalis",
                  "letist", "repuloter", "transfer-z-lotniska", "transfery-lotniskowe",
                  "prijevoz-od-zracne", "flughafentransfers"]
    city_kw = ["staedte-transfers", "stadt-zu-stadt", "przejazdy-miedzymiastowe",
               "city-to-city", "przesyly", "miedzymiastowe", "stadt"]

    # Standalone hub landing pages (not point-to-point routes). Airport is
    # checked first so "airport-transfers-from-skradin" lands on the airport hub.
    if any(k in rest for k in airport_kw) and "taxi" not in rest and "taks" not in rest:
        return pref + "/" + HUBS["airport"] + "/"
    if ("transfers-from-skradin" in rest or any(k in rest for k in city_kw)) and "taxi" not in rest and "taks" not in rest:
        return pref + "/" + HUBS["city"] + "/"

    # Point-to-point route pages -> the relevant hub (new route slugs differ)
    if rest.startswith(("taxi-", "taksowka-", "taksi-", "taxi")):
        if any(k in rest for k in airport_kw):
            return pref + "/" + HUBS["airport"] + "/"
        return pref + "/" + HUBS["city"] + "/"

    # Old blog posts / anything else content-ish -> language home
    return pref + "/" if pref else "/"


def main():
    paths = [l.strip() for l in io.open(SRC, encoding="utf-8") if l.strip()]
    rules, report, skipped = [], [], []
    seen = set()
    for p in sorted(paths):
        rest_full = p.strip("/")
        parts = rest_full.split("/")
        if parts and parts[0] in LANGS:
            lang, rest = parts[0], "/".join(parts[1:])
        else:
            lang, rest = "en", rest_full
        if is_junk(rest, p) or rest == "":
            skipped.append(p)
            continue
        tgt = target(lang, rest)
        pattern = "^" + p.lstrip("/").rstrip("/") + "/?$"
        if pattern in seen:
            continue
        seen.add(pattern)
        # Don't emit a no-op (old == new)
        if ("/" + p.strip("/") + "/") == tgt:
            continue
        rules.append("  RewriteRule %s %s [R=301,L]" % (pattern, tgt))
        report.append("%-55s -> %s" % (p, tgt))

    print("=== MAPPING REPORT (%d redirects, %d skipped as junk) ===" % (len(rules), len(skipped)))
    for r in report:
        print(r)
    print("\n=== SKIPPED (left to 404 - not real pages) ===")
    for s in skipped:
        print("  ", s)

    block = ("\n  # ===== BEGIN old-WordPress 301 redirects (scripts/gen_redirects.py) =====\n"
             "  # taxiskradin.hr was its own WordPress site; these are its old URLs\n"
             "  # (from a Search Console 404 export) mapped to the current pages.\n"
             + "\n".join(rules) +
             "\n  # ===== END old-WordPress 301 redirects =====\n")

    if DRY:
        print("\n(dry run - .htaccess not modified)")
        return

    ht = io.open(HTACCESS, encoding="utf-8").read()
    # Remove any previous generated block, then insert before the closing </IfModule>.
    ht = re.sub(r"\n  # ===== BEGIN old-WordPress 301 redirects.*?# ===== END old-WordPress 301 redirects =====\n",
                "\n", ht, flags=re.S)
    idx = ht.rindex("</IfModule>")
    ht = ht[:idx] + block + ht[idx:]
    io.open(HTACCESS, "w", encoding="utf-8", newline="\n").write(ht)
    print("\nInserted %d redirects into .htaccess" % len(rules))


if __name__ == "__main__":
    main()
