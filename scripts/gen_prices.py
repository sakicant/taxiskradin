"""Extract the PRICES matrix from script.js into admin/prices-data.js.

The price matrix in script.js is the single source of truth for fares. The
admin offers form loads the generated file to pre-fill the "Normal price"
field from the matrix, so the owner only types the discounted offer price.

Run `python scripts/gen_prices.py` whenever the PRICES matrix in script.js
changes.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_prices(js):
    marker = "const PRICES = {"
    start = js.index(marker) + len(marker) - 1  # position of the opening brace
    depth = 0
    for i in range(start, len(js)):
        c = js[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(js[start:i + 1])
    raise ValueError("Could not find a balanced PRICES object in script.js")


def main():
    with open(os.path.join(ROOT, "script.js"), "r", encoding="utf-8") as f:
        prices = extract_prices(f.read())

    # Union of every location that appears as an origin or a destination.
    locations = set(prices.keys())
    for dests in prices.values():
        locations.update(dests.keys())
    locations = sorted(locations)

    payload = (
        "// AUTO-GENERATED from script.js by scripts/gen_prices.py. Do not edit by hand.\n"
        "window.TX_PRICES = " + json.dumps(prices, ensure_ascii=False, indent=1) + ";\n"
        "window.TX_LOCATIONS = " + json.dumps(locations, ensure_ascii=False, indent=1) + ";\n"
        "// Look up a one-way fare, falling back to the reverse direction.\n"
        "window.txPrice = function (from, to) {\n"
        "  var P = window.TX_PRICES || {};\n"
        "  if (P[from] && P[from][to] != null) return P[from][to];\n"
        "  if (P[to] && P[to][from] != null) return P[to][from];\n"
        "  return null;\n"
        "};\n"
    )
    out = os.path.join(ROOT, "admin", "prices-data.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"wrote {os.path.relpath(out, ROOT)} ({len(prices)} origins, {len(locations)} locations)")


if __name__ == "__main__":
    main()
