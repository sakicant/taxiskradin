# -*- coding: utf-8 -*-
import json, urllib.request, os

# Town/city/airport centre coordinates (lat, lon). OSRM snaps to the nearest road,
# so approximate town-centre points are fine.
COORDS = {
 'Šibenik':(43.7350,15.8890), 'Skradin':(43.8190,15.9230), 'Vodice':(43.7597,15.7783),
 'Tribunj':(43.7560,15.7480), 'Srima':(43.7450,15.8050), 'Zaton':(43.7920,15.8280),
 'Bilice':(43.7550,15.9050), 'Zablaće':(43.7050,15.8610), 'Jadrija':(43.7160,15.8470),
 'Brodarica':(43.6870,15.9080), 'Žaborić':(43.6650,15.9250), 'Grebaštica':(43.6350,15.9350),
 'Bilo':(43.6100,15.9250), 'Primošten':(43.5860,15.9280), 'Rogoznica':(43.5280,15.9670),
 'Tromilja':(43.7850,15.9650), 'Perković':(43.6900,16.0400), 'Lozovac':(43.8050,15.9700),
 'Drniš':(43.8600,16.1550), 'Knin':(44.0410,16.1990), 'Pirovac':(43.8200,15.6800),
 'Tisno':(43.7970,15.6440), 'Jezera':(43.7770,15.6420), 'Murter':(43.8220,15.5920),
 'Betina':(43.8190,15.6060), 'Trogir':(43.5150,16.2510), 'Split':(43.5080,16.4400),
 'Split Airport':(43.5390,16.2980), 'Zadar':(44.1190,15.2310), 'Zadar Airport':(44.1080,15.3470),
 'Dubrovnik':(42.6410,18.1080), 'Dubrovnik Airport':(42.5610,18.2680),
 'Zagreb':(45.8150,15.9820), 'Zagreb Airport':(45.7430,16.0690),
 'Makarska':(43.2970,17.0180), 'Novalja':(44.5560,14.8850),
}
names = list(COORDS.keys())
coord_str = ";".join("%f,%f" % (COORDS[n][1], COORDS[n][0]) for n in names)  # lon,lat
url = ("https://router.project-osrm.org/table/v1/driving/%s?annotations=distance,duration" % coord_str)
print("requesting OSRM table for %d endpoints..." % len(names))
req = urllib.request.Request(url, headers={"User-Agent": "taxisibenik-build/1.0"})
data = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
assert data.get("code") == "Ok", data
dist = data["distances"]   # metres [i][j]
dur = data["durations"]    # seconds [i][j]

out = {}
missing = 0
for i, a in enumerate(names):
    for j, b in enumerate(names):
        if i == j: continue
        dm = dist[i][j]; ds = dur[i][j]
        if dm is None or ds is None:
            missing += 1; continue
        out["%s|%s" % (a, b)] = {"km": round(dm / 1000), "sec": round(ds)}
os.makedirs("docs", exist_ok=True)
json.dump(out, open("docs/route-distances.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("saved docs/route-distances.json with %d directed pairs (missing: %d)" % (len(out), missing))
# sanity spot checks
for a, b in [("Šibenik","Split"),("Šibenik","Split Airport"),("Šibenik","Zadar"),
             ("Vodice","Split Airport"),("Knin","Split Airport"),("Šibenik","Dubrovnik"),
             ("Šibenik","Zagreb"),("Šibenik","Trogir"),("Šibenik","Primošten")]:
    r = out.get("%s|%s" % (a, b))
    print("  %-26s %3d km  %4d min" % (a+" -> "+b, r["km"], round(r["sec"]/60)))
