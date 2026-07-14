# -*- coding: utf-8 -*-
"""Compute route-pages.md rows for the NEW locations (Seget, Čiovo, 11 marinas).

- Towns (Seget, Čiovo): full treatment, every priced non-excluded destination
  over EUR 20, both directions.
- Marinas: long-distance rule. A marina page to destination D is generated iff a
  price exists (>EUR 20) and D is one of: an airport, Šibenik, Skradin, an
  opposite-coast place, or a far same-side city/inland hub. Short same-side local
  hops are dropped. (Marina Trogir -> Split Airport is auto-dropped: no price.)

Prints a full breakdown and writes the new markdown rows to
scratchpad/new-route-rows.md for review. Does NOT modify route-pages.md.
"""
import os, re, json, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = r"C:\Users\sakic\AppData\Local\Temp\claude\C--Users-sakic-taxisibenik-code\cf536c1b-7545-406f-b294-a0de842b092e\scratchpad"

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

# matrix key -> friendly name used in route-pages.md
FRIENDLY = {
    "Šibenik - center": "Šibenik", "Brodarica - Šibenik": "Brodarica", "Skradin - center": "Skradin",
    "Split Airport (SPU)": "Split Airport", "Zadar Airport (ZAD)": "Zadar Airport",
    "Zagreb Airport (ZAG)": "Zagreb Airport", "Dubrovnik Airport (DBV)": "Dubrovnik Airport",
}
friendly = lambda k: FRIENDLY.get(k, k)

# Endpoints that never get route pages (covered by hub/day-trip pages)
EXCLUDED = {
    "Šibenik Bus Station", "Šibenik Ferry Port",
    "D-Resort Hotel Šibenik", "Bellevue Superior Hotel Šibenik", "Amadria Park Hotel Šibenik",
    "Amadria Park Camp", "D-Marin Marina Mandalina Šibenik", "Marina Zaton", "Marina ACI Skradin",
    "NP Krka - Lozovac entrance", "NP Krka - Skradin entrance", "NP Krka - Roški Slap entrance",
    "NP Plitvice Lakes",
    # all new marinas are endpoints-as-origin only, never destinations of each other
    "ACI Marina Trogir", "Marina Trogir (SCT)", "Marina Baotić", "Marina Agana", "Marina Frapa",
    "Marina Kremik", "ACI Marina Vodice", "Marina Tribunj", "Marina Hramina", "Marina Betina",
    "ACI Marina Jezera",
}

# --- coastal classification (matrix keys) ---
AIRPORTS = {"Split Airport (SPU)", "Zadar Airport (ZAD)", "Zagreb Airport (ZAG)", "Dubrovnik Airport (DBV)"}
SIBENIK = "Šibenik - center"
SKRADIN = "Skradin - center"
NORTH = {"Zaton", "Srima", "Vodice", "Tribunj", "Pirovac", "Tisno", "Jezera", "Murter", "Betina"}
NORTH_FAR = {"Zadar", "Novalja"}
SOUTH = {"Zablaće", "Brodarica - Šibenik", "Žaborić", "Grebaštica", "Bilo", "Primošten", "Rogoznica",
         "Trogir", "Seget", "Čiovo"}
SOUTH_FAR = {"Split", "Makarska", "Dubrovnik"}
INLAND_FAR = {"Drniš", "Knin", "Zagreb"}
INLAND_NEAR = {"Bilice", "Tromilja", "Lozovac", "Perković", "Jadrija"}

# new marinas -> coastal side
MARINA_SIDE = {
    "ACI Marina Vodice": "north", "Marina Tribunj": "north", "Marina Hramina": "north",
    "ACI Marina Jezera": "north", "Marina Betina": "north",
    "Marina Kremik": "south", "Marina Frapa": "south", "ACI Marina Trogir": "south",
    "Marina Trogir (SCT)": "south", "Marina Baotić": "south", "Marina Agana": "south",
}
TOWNS = ["Seget", "Čiovo"]

def valid_dest(d):
    return d not in EXCLUDED

def marina_wants(side, d):
    """Long-distance rule: does a marina on `side` get a page to destination d?"""
    if d in AIRPORTS: return True
    if d == SIBENIK or d == SKRADIN: return True
    if d in INLAND_FAR: return True
    if d in INLAND_NEAR: return False
    if side == "north":
        if d in SOUTH or d in SOUTH_FAR: return True      # opposite coast
        if d in NORTH_FAR: return True                     # same-side far major
        if d in NORTH: return False                        # same-side local hop
    else:  # south
        if d in NORTH or d in NORTH_FAR: return True       # opposite coast
        if d in SOUTH_FAR: return True                     # same-side far major
        if d in SOUTH: return False                        # same-side local hop
    return False

def slugify(name):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    s = s.replace('(', '').replace(')', '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

# existing rows (to avoid dupes)
existing = set()
for line in open(os.path.join(ROOT, "docs", "route-pages.md"), encoding="utf-8"):
    m = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*`(.+?)`\s*\|', line)
    if m and m.group(1) != "From":
        existing.add((m.group(1), m.group(2)))

# universe of destination matrix keys
universe = set()
for a, row in PRICES.items():
    universe.add(a); universe.update(row.keys())

rows = []   # (from_friendly, to_friendly, slug, price)
def add_pair(a_key, b_key):
    p = price(a_key, b_key)
    if p is None or p <= 20: return False
    af, bf = friendly(a_key), friendly(b_key)
    if (af, bf) in existing: return False
    slug = "taxi-%s-to-%s" % (slugify(af), slugify(bf))
    rows.append((af, bf, slug, p))
    return True

breakdown = {}

# Towns: full treatment, both directions to every valid priced dest
for town in TOWNS:
    c = 0
    for d in sorted(universe):
        if d == town or not valid_dest(d): continue
        if add_pair(town, d): c += 1
        if add_pair(d, town): c += 1
    breakdown[town] = c

# Marinas: long-distance rule, both directions
for marina, side in MARINA_SIDE.items():
    c = 0
    for d in sorted(universe):
        if not valid_dest(d): continue
        if not marina_wants(side, d): continue
        if add_pair(marina, d): c += 1
        if add_pair(d, marina): c += 1
    breakdown[marina] = c

# Report
print("NEW route rows:", len(rows))
for name in TOWNS + list(MARINA_SIDE):
    print("  %-24s %3d pages (both directions)" % (name, breakdown[name]))

# sample
print("\nSample rows:")
for r in rows[:6] + rows[len(rows)//2: len(rows)//2 + 6]:
    print("  | %s | %s | `%s` | %d |" % r)

# write for review
os.makedirs(SCRATCH, exist_ok=True)
with open(os.path.join(SCRATCH, "new-route-rows.md"), "w", encoding="utf-8") as f:
    f.write("| From | To | EN slug | One-way EUR |\n|---|---|---|---|\n")
    for a, b, s, p in rows:
        f.write("| %s | %s | `%s` | %d |\n" % (a, b, s, p))
print("\nwrote", os.path.join(SCRATCH, "new-route-rows.md"))
