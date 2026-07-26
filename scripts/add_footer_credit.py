# -*- coding: utf-8 -*-
"""Add a 'Website created by antoniodigital.com' credit to every footer partial.

Inserts one <p> right after the copyright line (the one with id="year") in each
footer.<lang>.html, translated per language. Idempotent: skips a file that
already links to antoniodigital.com.

Usage: python scripts/add_footer_credit.py <partials-dir> [--write]
"""
import os, io, sys

PDIR = sys.argv[1]
WRITE = "--write" in sys.argv

PHRASE = {
    "en": "Website created by",
    "hr": "Izrada web stranice",
    "de": "Website erstellt von",
    "pl": "Wykonanie strony",
    "cs": "Tvorba webu",
    "it": "Sito web creato da",
    "fr": "Site web créé par",
    "nl": "Website gemaakt door",
    "sl": "Izdelava spletne strani",
    "hu": "A weboldalt készítette",
    "sk": "Tvorba webu",
    "es": "Sitio web creado por",
    "sv": "Webbplats skapad av",
    "sr": "Izrada sajta",
    "no": "Nettsted laget av",
    "zh": "网站制作",
    "ko": "웹사이트 제작",
    "fi": "Verkkosivun toteutus",
    "ja": "ウェブサイト制作",
}
LINK = '<a href="https://antoniodigital.com" target="_blank" rel="noopener">Antonio Digital</a>'

done, skipped, problems = 0, 0, []
for fn in sorted(os.listdir(PDIR)):
    if not (fn == "footer.html" or (fn.startswith("footer.") and fn.endswith(".html"))):
        continue
    lang = "en" if fn == "footer.html" else fn.split(".")[1]
    if lang not in PHRASE:
        problems.append(fn + " (no phrase for lang)")
        continue
    path = os.path.join(PDIR, fn)
    html = io.open(path, encoding="utf-8", errors="ignore").read()
    if "antoniodigital.com" in html:
        skipped += 1
        continue
    lines = html.split("\n")
    out, inserted = [], False
    for line in lines:
        out.append(line)
        if not inserted and 'id="year"' in line:
            indent = line[:len(line) - len(line.lstrip())]
            out.append('%s<p class="footer-credit">%s %s</p>' % (indent, PHRASE[lang], LINK))
            inserted = True
    if not inserted:
        problems.append(fn + ' (no id="year" anchor)')
        continue
    if WRITE:
        io.open(path, "w", encoding="utf-8").write("\n".join(out))
    done += 1

print("footers updated:", done, "| already had link:", skipped)
if problems:
    print("PROBLEMS:", problems)
if not WRITE:
    print("(dry run - nothing written. re-run with --write)")
