# -*- coding: utf-8 -*-
"""Generate the HUNGARIAN variant of every route page. Mirrors gen_routes.py.
Place names kept nominative via "a <A> - <B> útvonalon". Run after gen_routes.py."""
import os, re, json, hashlib
from urllib.parse import quote

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
        'Zagreb Airport':'Zagreb Airport (ZAG)','Dubrovnik Airport':'Dubrovnik Airport (DBV)'}
key = lambda n: MAPK.get(n, n)
BIG_CITIES = {'Split','Zadar','Dubrovnik','Zagreb','Trogir'}
AIRPORT_CITY = {'Split Airport':'Split','Zadar Airport':'Zadar','Zagreb Airport':'Zagreb','Dubrovnik Airport':'Dubrovnik'}
MARINAS = {'ACI Marina Trogir','Marina Trogir (SCT)','Marina Baotić','Marina Agana','Marina Frapa',
           'Marina Kremik','ACI Marina Vodice','Marina Tribunj','Marina Hramina','Marina Betina','ACI Marina Jezera'}
HU_NAME = {'Split Airport':'Split repülőtér','Zadar Airport':'Zadar repülőtér',
           'Zagreb Airport':'Zagreb repülőtér','Dubrovnik Airport':'Dubrovnik repülőtér'}
hu = lambda n: HU_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'repter-split','zadar-airport':'repter-zadar',
                'zagreb-airport':'repter-zagreb','dubrovnik-airport':'repter-dubrovnik'}
def hu_slug(en_slug):
    s = en_slug.replace('-to-', '-')
    for a, b in AIRPORT_SLUG.items():
        s = s.replace(a, b)
    return s

PROVIDER = {"@type": "LocalBusiness", "name": "Taxi Antonio", "telephone": "+385994471013",
    "email": "info@taxisibenik.hr",
    "address": {"@type": "PostalAddress", "addressLocality": "Šibenik", "addressCountry": "HR"},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "142"}}

def vhash(slug, n): return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n

rows = []
for line in open(os.path.join(ROOT, "docs", "route-pages.md"), encoding="utf-8"):
    m = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*`(.+?)`\s*\|\s*(.+?)\s*\|', line)
    if not m: continue
    frm, to, slug, doc = m.groups()
    if frm == "From": continue
    rows.append((frm, to, slug))
slug_of = {(f, t): s for f, t, s in rows}

def bkey(name): return quote(key(name))
def book_link(frm, to, price):
    return "/hu/foglalas/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

def route_type(frm, to):
    if to in AIRPORT_CITY: return "to_airport"
    if frm in AIRPORT_CITY: return "from_airport"
    if frm in MARINAS or to in MARINAS: return "marina"
    if frm in BIG_CITIES or to in BIG_CITIES: return "city"
    return "local"

def faq_html(items):
    return "\n".join('          <div class="faq-item">\n            <h4>%s</h4>\n            <p>%s</p>\n          </div>' % (q, a) for q, a in items)

def build(frm, to, slug):
    p = price(key(frm), key(to)); rp = p * 2
    typ = route_type(frm, to)
    hfr, hto = hu(frm), hu(to)
    rel = "%s - %s" % (hfr, hto)
    huslug = hu_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/hu/%s/">%s - %s</a>' % (hu_slug(rev), hto, hfr)) if rev else ("%s - %s" % (hto, hfr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fix ár, egy irány</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Távolság</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Menetidő</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Oda-vissza</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fix ár, egy irány</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Oda-vissza</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Max. 4</div><div class="rf-label">Utasok</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Privát, háztól házig</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Az Ön privát taxija és transzfere: %s" % rel
        tagline = "Privát taxi és transzfer fix áron, %s, egyenesen az indulásokhoz." % rel
        intro = ("A %s repülőtérről indul? A %s útvonalra privát taxit és transzfert kínálok fix áron. "
                 "Antonio vagyok, helyi sofőr Šibenikből: felveszem Önt a címén, és egyenesen az indulási terminálhoz viszem egy kényelmes Škoda Superbben. "
                 "Az ár fix, &euro;%d a teljes járműért, max. 4 utas, előre megbeszélve, taxióra nélkül és meglepetések nélkül. "
                 "A felvételt a járata időpontjához igazítom, hogy elegendő idővel érkezzen a becsekkoláshoz. "
                 "A fenti árajánlat-űrlap már ki van töltve erre az útvonalra, így látja az árat, és néhány kattintással foglalhat." % (city, rel, p))
        whys = [("Fix ár &euro;%d" % p, "Egy ár a teljes járműért, max. 4 utas, előre megbeszélve. Útdíj, üzemanyag és csomag beleértve, taxióra nélkül."),
                ("A járatához igazítva", "Adja meg az indulási időt, és visszafelé számolok, hogy időben a terminálon legyen a becsekkoláshoz."),
                ("Az ajtótól a terminálig", "Felvétel a címén, és letétel egyenesen az indulási terminál bejáratánál."),
                ("Bármikor", "A kora reggeli és késő esti járatok sem gondot. 0-24 vezetek előre megbeszélt áron.")]
        faqs = [("Mennyibe kerül egy taxi a %s útvonalon?" % rel,
                 "Fix &euro;%d járművenként, egy irány, max. 4 utas. Az ár járművenként, nem személyenként értendő, és tartalmazza az útdíjat, üzemanyagot és csomagot. Az oda-vissza út &euro;%d." % (p, rp)),
                ("Mikor induljak a járatomra?",
                 "Általában körülbelül 3 órával a nemzetközi és 2 órával a belföldi járat előtt. Adja meg a járat idejét, és megerősítem a pontos felvételt."),
                ("Elvisz egészen az indulási terminálig?",
                 "Igen. Egyenesen az indulási terminálhoz viszem, és segítek a csomaggal. Nincs séta a parkolóból, nincs shuttle busz."),
                ("Mennyivel korábban foglaljak?",
                 "Legalább 2 órával korábban, hogy megerősítsem a járművet és a felvételt, korábbi járatoknál és főszezonban pedig hamarabb. Gyors útért hívjon vagy írjon WhatsApp-on.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Az Ön reptéri felvétele és transzfere: %s" % rel
        tagline = "Privát reptéri felvétel és transzfer fix áron, %s, járatkövetéssel." % rel
        intro = ("Éppen most landolt a %s repülőtéren? A %s útvonalra szóló privát transzfer leveszi a stresszt az érkezésről. "
                 "A megérkezési csarnokban névtáblával várom, segítek a csomaggal, és egyenesen a célhoz viszem egy kényelmes Škoda Superbben, "
                 "fix áron, &euro;%d a teljes járműért, max. 4 utas. A járatát valós időben követem, így ott vagyok, akár korábban, akár később landol. "
                 "Nincs taxisor, nincs közös transzfer és nincs felár. A fenti űrlap már ki van töltve erre az útvonalra." % (city, rel, p))
        whys = [("Fogadás névtáblával", "A megérkezési csarnokban névtáblával várom, és segítek a csomagokkal, hogy egyenesen a járműhöz menjen."),
                ("Járatkövetés", "A járatát valós időben követem, és alkalmazkodom a korai leszálláshoz vagy késéshez, ingyenes várakozással."),
                ("Fix ár &euro;%d" % p, "Egy ár a teljes járműért, max. 4 utas, előre megbeszélve. Útdíj, üzemanyag és csomag beleértve, taxióra nélkül."),
                ("Egyenesen az ajtajához", "Nincs sor és nincs átszállás. Egyenesen a címére viszem.")]
        faqs = [("Hol fogad engem?",
                 "A megérkezési csarnokban, közvetlenül a csomagfelvétel után, névtáblával. Segítek a csomaggal, és a járműhöz kísérem."),
                ("Mi van, ha a járatom késik?",
                 "Semmi gond. A járatát valós időben követem, és a felvételt a tényleges leszálláshoz igazítom, a várakozásért felár nélkül."),
                ("Mennyibe kerül a transzfer a %s útvonalon?" % rel,
                 "Fix &euro;%d járművenként max. 4 utasra, egy irány, útdíj és csomag beleértve. Az oda-vissza út &euro;%d." % (p, rp)),
                ("Mennyivel korábban foglaljak?",
                 "Legalább 2 órával korábban, hogy a járatához igazítsam. Aznapi felvételhez hirtelen változás után hívjon vagy írjon WhatsApp-on.")]
    elif typ == "marina":
        heading = "Privát marina transzfer: %s" % rel
        tagline = "Privát taxi és transzfer fix áron, %s, a hajója időzítéséhez igazítva." % rel
        intro = ("A %s útvonalon utazik? Privát, fix áras taxit és transzfert kínálok marinavendégeknek, a hajójához és az utazási terveihez igazítva. "
                 "Bőséges hely a csomagnak, kényelmes Škoda Superb az egész úton, fix &euro;%d a teljes járműért, max. 4 utas, előre megbeszélve. "
                 "Akár a jachtjához érkezik, akár arról indul tovább, taxióra és sorban állás nélkül, egyetlen helyi sofőrrel, akit közvetlenül foglal. "
                 "Ez hosszú távú privát transzfer, nem rövid helyi út, és a fenti árajánlat már erre az útvonalra van beállítva." % (rel, p))
        whys = [("Fix &euro;%d ár" % p, "Egy ár a teljes járműért, max. 4 utas, előre megbeszélve. Útdíj, üzemanyag és csomag beleértve, taxióra nélkül."),
                ("A hajójához igazítva", "Adja meg a charter, becsekkolás vagy indulás idejét, és ahhoz igazítom a felvételt, hogy egy lassabb szakasz se siettesse."),
                ("Hely a csomagjának", "Bőröndök, ellátmány és hajóstáskák is elférnek a kényelmes Škoda Superbben, be- és kirakodási segítséggel."),
                ("Egyetlen helyi sofőr", "Mindent közvetlenül velem intéz, a foglalástól az érkezésig, telefonon, WhatsApp-on vagy e-mailben. Nincs call center.")]
        faqs = [("Mennyibe kerül a transzfer a %s útvonalon?" % rel,
                 "Fix &euro;%d járművenként max. 4 utasra, egy irány, útdíjjal, üzemanyaggal és csomaggal. Az oda-vissza út &euro;%d." % (p, rp)),
                ("Fel tud venni közvetlenül a marinánál?",
                 "Igen. A marina bejáratánál vagy a recepciónál várom, és segítek a csomaggal, hogy a pontonról egyenesen a járműhöz jusson."),
                ("Hozzá tudja igazítani a transzfert a hajómhoz?",
                 "Igen. Küldje el a charter, becsekkolás vagy indulás idejét a foglaláskor, és ahhoz igazítom a felvételt."),
                ("Mennyivel korábban foglaljak?",
                 "Legalább 2 órával korábban, hogy megerősítsem a járművet és a felvétel idejét. Gyors útért hívjon vagy írjon WhatsApp-on.")]
    elif typ == "city":
        heading = "Privát transzfer: %s" % rel
        tagline = "Privát taxi és transzfer fix áron, %s, háztól házig." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Megbízható transzferre van szüksége a %s útvonalon? Privát taxit és transzfert kínálok fix áron, háztól házig, egy kényelmes Škoda Superbben. "
                     "Felveszem Önt a pontos címén, és egyenesen a célhoz viszem, nem kívánt megállók és útitársak nélkül. "
                     "Az ár fix, &euro;%d a teljes járműért, max. 4 utas, az indulás előtt megbeszélve, útdíj és csomag beleértve. "
                     "A fenti árajánlat erre az útvonalra van kitöltve, így a foglalás csak néhány kattintás." % (rel, p))
        else:
            intro = ("Taxit keres a %s útvonalon taxióra és bonyodalom nélkül? Ez egy privát transzfer fix áron, egyetlen helyi sofőrrel. "
                     "Felveszem Önt az ajtónál, és kényelmesen a célhoz viszem, csomaggal együtt, átalányáron &euro;%d járművenként max. 4 utasra. "
                     "Pároknak és családoknak gyakran olcsóbb, mint a külön busz- vagy vonatjegyek, és mindig gyorsabb és háztól házig szól. "
                     "A fenti árajánlat már be van állítva erre az útvonalra." % (rel, p))
        whys = [("Fix ár &euro;%d" % p, "Egy ár járművenként max. 4 utasra, előre megbeszélve. Útdíj, üzemanyag és csomag beleértve, taxióra nélkül."),
                ("Háztól házig", "Felveszem Önt a pontos címén, és a cél ajtajánál teszem le. Nincsenek állomások, nincs átszállás."),
                ("Egyetlen helyi sofőr", "Mindent közvetlenül velem intéz, a foglalástól az érkezésig, telefonon, WhatsApp-on vagy e-mailben. Nincs call center."),
                ("Megállók igény szerint", "Hosszabb útvonalakon szívesen megállok egy kávéra, fotóra vagy egy rövid látnivalóra útközben.")]
        faqs = [("Mennyibe kerül egy taxi a %s útvonalon?" % rel,
                 "Fix &euro;%d járművenként max. 4 utasra, egy irány, útdíjjal, üzemanyaggal és csomaggal. Az oda-vissza út &euro;%d." % (p, rp)),
                ("A transzfer privát vagy közös?",
                 "Minden transzfer privát és háztól házig szól, egy Škoda Superbben. Nincs jármű-megosztás és nincs extra megálló, hacsak nem kéri."),
                ("Megállhat útközben?",
                 "Igen. Hosszabb útvonalakon szívesen megállok egy kávéra, fotóra vagy egy rövid látnivalóra. Csak jelezze a foglaláskor."),
                ("Mennyivel korábban foglaljak?",
                 "Legalább 2 órával korábban, hogy megerősítsem a járművet és a felvétel idejét. Gyors útért hívjon vagy írjon WhatsApp-on.")]
    else:
        heading = "Privát taxi: %s" % rel
        tagline = "Privát taxi és transzfer fix áron, %s, háztól házig." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("A %s útvonalon utazik? Privát taxit és transzfert vezetek fix áron, felvétellel az ajtajánál és letétellel pontosan ott, ahol lennie kell. "
                     "Az ár átalány, &euro;%d a teljes járműért, max. 4 utas, taxióra és állomáson való várakozás nélkül. "
                     "Kényelmes Škoda Superb, hely a csomagnak és egyetlen helyi sofőr, akit közvetlenül foglal. "
                     "A fenti árajánlat erre az útvonalra van kitöltve." % (rel, p))
        else:
            intro = ("Taxira van szüksége a %s útvonalon? Privát, háztól házig szóló transzfert kínálok fix áron, &euro;%d a teljes járműért, max. 4 utas. "
                     "A megbeszélt időpontban érkezem a címére, így soha nem vár az út szélén, és kényelmesen a célhoz viszem. "
                     "Taxióra nélkül, meglepetések nélkül, csak egyetlen helyi sofőr a foglalástól az érkezésig. A fenti árajánlat már be van állítva erre az útvonalra." % (rel, p))
        whys = [("Fix ár &euro;%d" % p, "Egy ár járművenként max. 4 utasra, az utazás előtt megbeszélve. Taxióra nélkül, meglepetések nélkül."),
                ("Háztól házig", "Felvétel a címén és letétel a cél ajtajánál, csomaggal együtt."),
                ("Nincs szükség taxiállomásra", "Előre foglalva, így soha nem vár egy arra járó taxira. Én megyek Önhöz."),
                ("Egyetlen helyi sofőr", "Mindent közvetlenül velem intéz, a foglalástól az érkezésig, telefonon, WhatsApp-on vagy e-mailben.")]
        faqs = [("Mennyibe kerül egy taxi a %s útvonalon?" % rel,
                 "Fix &euro;%d járművenként max. 4 utasra, egy irány, csomag beleértve. Az oda-vissza út &euro;%d." % (p, rp)),
                ("Hol vesz fel engem?",
                 "A pontos címén, legyen az ház, hotel vagy apartman. Küldje el a címet a foglaláskor, és megerősítem a találkozási pontot."),
                ("Mennyivel korábban foglaljak?",
                 "Legalább 2 órával korábban, hogy megerősítsem a járművet és a felvétel idejét. Gyors útért hívjon vagy írjon WhatsApp-on.")]

    if dd:
        faqs = [("Milyen hosszú az útvonal és mennyi ideig tart az út?",
                 "A %s útvonalon az út körülbelül %d km, és normál forgalomban nagyjából %s alatt tart, a nyári csúcsidőben kicsit tovább. A felvételt úgy tervezem, hogy egy lassabb szakasz soha ne siettesse Önt." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Jó napot, Antonio! Szeretném lefoglalni a %s transzfert (€%d).\n"
        "Adataim:\n- Felvétel dátuma: \n- Felvétel időpontja: \n- Utasok: \n- Felvételi cím: \n- Nevem: " % (rel, p))
    trust_line = ("Azonnali visszaigazolás e-mailben &middot; Nincs rejtett költség &middot; Járatkövetés beleértve"
                  if typ in ("to_airport", "from_airport")
                  else "Azonnali visszaigazolás e-mailben &middot; Nincs rejtett költség &middot; Fix ár, taxióra nélkül")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: TAXI Antonio Škoda Superbje a dalmát tengerparton" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d járművenként &middot; max. 4 utas</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Foglalás</a>
          <a class="btn btn-secondary" href="%s">Foglalás WhatsApp-on</a>
        </div>
        <p class="hero-trust-line">%s</p>
      </div>
    </div>
  </section>

  <section class="route-facts-section">
    <div class="container">
      <div class="route-facts">
%s
      </div>
    </div>
  </section>

  <section class="hub-intro">
    <div class="container">
      <span class="eyebrow center">%s</span>
      <h2 class="section-title">%s</h2>
      <p class="section-subtitle">%s</p>
    </div>
  </section>

  <section class="why-book">
    <div class="container">
      <span class="eyebrow center">Miért foglalja ezt a transzfert</span>
      <h2 class="section-title">Miért foglaljon %s taxit Antoniónál?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">A %s ára</h2>
      <p class="section-subtitle">Fix ár járművenként, max. 4 utas, csomag beleértve. Ugyanez az ár érvényes az ellenkező irányban is.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Egy irány</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Oda-vissza</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Előleg a megerősítéshez</div></div>
        <div class="route-fact"><div class="rf-value">Készpénz vagy kártya</div><div class="rf-label">A többi a nap folyamán</div></div>
      </div>
      <p class="hub-note">A 20%%-os előleg (minimum &euro;20) megerősíti a foglalást, a fennmaradó összeget az utazás napján fizeti, készpénzzel vagy kártyával. Az ellenkező irányba utazik? Lásd %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Vélemények</span>
      <h2 class="section-title">Mit mondanak az utasok</h2>
      <p class="section-subtitle">Valódi vélemények valódi utasoktól.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">GYIK</span>
      <h2 class="section-title">Taxi %s: gyakori kérdések</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Foglalja le %s transzferét</h2>
      <p class="section-subtitle">Fix ár &euro;%d járművenként, max. 4 utas. Erősítse meg néhány kattintással.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Foglalás</a>
        <a href="%s" class="btn btn-secondary">Foglalás WhatsApp-on</a>
      </div>
    </div>
  </section>

{{RELATED_LINKS}}
''' % (rel,
       rel, tagline, p, book, wa, trust_line, facts_html,
       rel, heading, intro,
       rel, why_html,
       rel, p, rp, revlink,
       rel, faq_html(faqs),
       rel, p, book, wa)

    desc = ("Privát taxi és transzfer, %s. Fix ár &euro;%d járművenként, max. 4 utas, háztól házig. Foglaljon közvetlenül Antoniónál." % (rel, p))
    if len(desc) > 160:
        desc = "Privát taxi és transzfer, %s. Fix ár &euro;%d járművenként, max. 4. Foglaljon Antoniónál." % (rel, p)
    keywords = "taxi %s, transzfer %s, reptéri transzfer %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Privát taxitranszfer",
         "name": "Taxi %s" % rel,
         "description": "Privát taxi és transzfer fix áron, %s, %d euró járművenként max. 4 utasra, háztól házig." % (rel, p),
         "provider": PROVIDER, "areaServed": [hfr, hto],
         "url": "https://taxisibenik.hr/hu/%s/" % huslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Privát egyirányú út, %s, járművenként max. 4 utasra. Oda-vissza %d euró." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": huslug, "title": "Taxi %s | Fix ár €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "hu")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated hu:", sum(made.values()), made, "| skipped:", skipped)
