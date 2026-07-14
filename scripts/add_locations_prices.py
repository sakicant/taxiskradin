# -*- coding: utf-8 -*-
"""Add new locations (2 towns + 11 marinas) to the PRICES matrix in script.js.
Each new location gets a COMPLETE, bidirectionally-resolved row copied from an
existing anchor (with an optional offset), so every lookup resolves directly
without depending on sparse reverse entries. Marina Kremik = midpoint of
Rogoznica and Primošten. Rewrites the PRICES block with matching formatting so
the diff is additions-only."""
import re, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "script.js")
text = open(path, encoding="utf-8").read()

# Extract PRICES object
anchor_kw = "const PRICES = "
ki = text.index(anchor_kw)
obj_start = text.index("{", ki)
d = 0
for k in range(obj_start, len(text)):
    if text[k] == "{": d += 1
    elif text[k] == "}":
        d -= 1
        if d == 0:
            obj_end = k
            break
P = json.loads(text[obj_start:obj_end + 1])

# Universe of all locations (top-level keys + all destinations), in encounter order
universe = []
seen = set()
for a, row in P.items():
    if a not in seen:
        seen.add(a); universe.append(a)
    for b in row:
        if b not in seen:
            seen.add(b); universe.append(b)

def resolve(a, b):
    if a in P and P[a].get(b) is not None:
        return P[a][b]
    if b in P and P[b].get(a) is not None:
        return P[b][a]
    return None

def round5(x):
    return int(round(x / 5.0) * 5)

def mirror_row(anchor, offset):
    row = {}
    for X in universe:
        if X == anchor:
            continue
        v = resolve(anchor, X)
        if v is None:
            continue
        row[X] = v + offset
    return row

def midpoint_row(a1, a2):
    row = {}
    for X in universe:
        if X in (a1, a2):
            continue
        v1 = resolve(a1, X); v2 = resolve(a2, X)
        if v1 is None or v2 is None:
            continue
        row[X] = round5((v1 + v2) / 2.0)
    return row

# (new key, anchor, offset)  -- offset applied to a copy of anchor's resolved prices
MIRRORS = [
    ("Seget", "Trogir", 0),
    ("Čiovo", "Trogir", 15),
    ("ACI Marina Trogir", "Trogir", 15),
    ("Marina Trogir (SCT)", "Trogir", 15),
    ("Marina Baotić", "Trogir", 0),
    ("Marina Agana", "Trogir", 0),
    ("Marina Frapa", "Rogoznica", 0),
    ("ACI Marina Vodice", "Vodice", 0),
    ("Marina Tribunj", "Tribunj", 0),
    ("Marina Hramina", "Murter", 0),
    ("Marina Betina", "Betina", 0),
    ("ACI Marina Jezera", "Jezera", 0),
]

new_rows = {}
for key, anchor, off in MIRRORS:
    new_rows[key] = mirror_row(anchor, off)
new_rows["Marina Kremik"] = midpoint_row("Rogoznica", "Primošten")

# Guard: no key collisions with existing
for k in new_rows:
    assert k not in P, "collision: " + k

# Merge (existing order preserved, new appended)
merged = dict(P)
merged.update(new_rows)

# Serialize with the file's 4-space / 6-space indentation
def ser_val(v):
    return "null" if v is None else str(v)

def ser(prices):
    tops = []
    for k, row in prices.items():
        lines = ['    %s: {' % json.dumps(k, ensure_ascii=False)]
        items = list(row.items())
        for i, (dk, dv) in enumerate(items):
            comma = ',' if i < len(items) - 1 else ''
            lines.append('      %s: %s%s' % (json.dumps(dk, ensure_ascii=False), ser_val(dv), comma))
        lines.append('    }')
        tops.append('\n'.join(lines))
    return '{\n' + ',\n'.join(tops) + '\n  }'

new_text = text[:obj_start] + ser(merged) + text[obj_end + 1:]

# Sanity: re-extract and json.loads to confirm validity
ci = new_text.index(anchor_kw)
os2 = new_text.index("{", ci)
d = 0
for k in range(os2, len(new_text)):
    if new_text[k] == "{": d += 1
    elif new_text[k] == "}":
        d -= 1
        if d == 0:
            oe2 = k; break
P2 = json.loads(new_text[os2:oe2 + 1])
assert len(P2) == len(P) + 13, (len(P2), len(P))

open(path, "w", encoding="utf-8").write(new_text)

# Report
print("existing locations:", len(P), "-> new total:", len(P2))
for key, anchor, off in MIRRORS:
    print("  %-24s = %-10s +%-3d  (%d dests)" % (key, anchor, off, len(new_rows[key])))
print("  %-24s = midpoint(Rogoznica,Primošten)  (%d dests)" % ("Marina Kremik", len(new_rows["Marina Kremik"])))
print()
print("Seget -> Split Airport (SPU):", new_rows["Seget"].get("Split Airport (SPU)"))
print("Čiovo -> Split Airport (SPU):", new_rows["Čiovo"].get("Split Airport (SPU)"))
print("Marina Hramina -> Split Airport (SPU):", new_rows["Marina Hramina"].get("Split Airport (SPU)"))
print("Marina Kremik -> Šibenik - center:", new_rows["Marina Kremik"].get("Šibenik - center"),
      "(Rogoznica 65, Primošten 50 -> 58 -> 60)")
print("Marina Frapa -> Zadar:", new_rows["Marina Frapa"].get("Zadar"))
