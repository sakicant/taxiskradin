# -*- coding: utf-8 -*-
"""Generate the SLOVAK variant of every route page. Mirrors gen_routes.py.
Place names kept nominative via "na trase <A> - <B>". Run after gen_routes.py."""
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
SK_NAME = {'Split Airport':'Letisko Split','Zadar Airport':'Letisko Zadar',
           'Zagreb Airport':'Letisko Zagreb','Dubrovnik Airport':'Letisko Dubrovnik'}
sk = lambda n: SK_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'letisko-split','zadar-airport':'letisko-zadar',
                'zagreb-airport':'letisko-zagreb','dubrovnik-airport':'letisko-dubrovnik'}
def sk_slug(en_slug):
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
    return "/sk/rezervacia/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    sfr, sto = sk(frm), sk(to)
    rel = "%s - %s" % (sfr, sto)
    skslug = sk_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/sk/%s/">%s - %s</a>' % (sk_slug(rev), sto, sfr)) if rev else ("%s - %s" % (sto, sfr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Pevná cena, jednosmerne</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Vzdialenosť</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Čas jazdy</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Spiatočne</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Pevná cena, jednosmerne</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Spiatočne</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Max. 4</div><div class="rf-label">Cestujúci</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Súkromne, od dverí k dverám</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Vaše súkromné taxi a transfer: %s" % rel
        tagline = "Súkromné taxi a transfer za pevnú cenu, %s, priamo k odletom." % rel
        intro = ("Odlietate z letiska %s? Na trase %s ponúkam súkromné taxi a transfer za pevnú cenu. "
                 "Som Antonio, miestny vodič zo Šibeniku: vyzdvihnem Vás na Vašej adrese a odveziem Vás priamo k odletovému terminálu pohodlnou Škodou Superb. "
                 "Cena je pevná, &euro;%d za celé vozidlo, max. 4 cestujúci, dohodnutá vopred, bez taxametra a bez prekvapení. "
                 "Čas vyzdvihnutia prispôsobím času Vášho letu, aby ste dorazili s dostatočnou rezervou na odbavenie. "
                 "Cenový formulár vyššie je už vyplnený pre túto trasu, takže vidíte cenu a rezervujete na pár kliknutí." % (city, rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za celé vozidlo, max. 4 cestujúci, dohodnutá vopred. Mýto, palivo a batožina v cene, bez taxametra."),
                ("Prispôsobené Vášmu letu", "Zadajte čas odletu a ja spätne vypočítam vyzdvihnutie, aby ste boli na termináli včas na odbavenie."),
                ("Od dverí k terminálu", "Vyzdvihnutie na Vašej adrese a vysadenie priamo pri vchode do odletového terminálu."),
                ("Kedykoľvek", "Skoré ranné ani neskoré večerné lety nie sú problém. Jazdím nonstop za vopred dohodnutú cenu.")]
        faqs = [("Koľko stojí taxi na trase %s?" % rel,
                 "Pevných &euro;%d za vozidlo, jednosmerne, max. 4 cestujúci. Cena je za vozidlo, nie za osobu, a zahŕňa mýto, palivo a batožinu. Spiatočná cesta stojí &euro;%d." % (p, rp)),
                ("Kedy mám vyraziť na svoj let?",
                 "Zvyčajne približne 3 hodiny pred medzinárodným a 2 hodiny pred vnútroštátnym letom. Zadajte čas letu a potvrdím presné vyzdvihnutie."),
                ("Odveziete ma až k odletovému terminálu?",
                 "Áno. Odveziem Vás priamo k odletovému terminálu a pomôžem s batožinou. Žiadna chôdza z parkoviska, žiadny shuttle bus."),
                ("S akým predstihom mám rezervovať?",
                 "Aspoň 2 hodiny vopred, aby som potvrdil vozidlo a vyzdvihnutie, pri skorších letoch a v hlavnej sezóne skôr. Pre rýchlu jazdu zavolajte alebo napíšte na WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Vaše vyzdvihnutie z letiska a transfer: %s" % rel
        tagline = "Súkromné vyzdvihnutie z letiska a transfer za pevnú cenu, %s, so sledovaním letu." % rel
        intro = ("Práve ste pristáli na letisku %s? Súkromný transfer na trase %s Vám zoberie stres z príletu. "
                 "V príletovej hale Vás čakám s tabuľkou s menom, pomôžem s batožinou a odveziem Vás priamo do cieľa pohodlnou Škodou Superb, "
                 "za pevnú cenu &euro;%d za celé vozidlo, max. 4 cestujúci. Váš let sledujem v reálnom čase, takže som tam, či pristanete skôr alebo neskôr. "
                 "Žiadny rad na taxi, žiadny zdieľaný transfer a žiadne príplatky. Formulár vyššie je už vyplnený pre túto trasu." % (city, rel, p))
        whys = [("Privítanie s tabuľkou s menom", "V príletovej hale Vás čakám s tabuľkou s menom a pomôžem s batožinou, aby ste išli priamo k vozidlu."),
                ("Sledovanie letu", "Váš let sledujem v reálnom čase a prispôsobím sa skoršiemu pristátiu alebo meškaniu, s čakaním zdarma."),
                ("Pevná cena &euro;%d" % p, "Jedna cena za celé vozidlo, max. 4 cestujúci, dohodnutá vopred. Mýto, palivo a batožina v cene, bez taxametra."),
                ("Priamo k Vašim dverám", "Žiadny rad a žiadne prestupovanie. Odveziem Vás priamo na Vašu adresu.")]
        faqs = [("Kde ma privítate?",
                 "V príletovej hale, hneď po výdaji batožiny, s tabuľkou s menom. Pomôžem s batožinou a odprevadím Vás k vozidlu."),
                ("Čo ak môj let mešká?",
                 "Žiadny problém. Váš let sledujem v reálnom čase a vyzdvihnutie prispôsobím skutočnému pristátiu, bez príplatku za čakanie."),
                ("Koľko stojí transfer na trase %s?" % rel,
                 "Pevných &euro;%d za vozidlo pre max. 4 cestujúcich, jednosmerne, mýto a batožina v cene. Spiatočná cesta stojí &euro;%d." % (p, rp)),
                ("S akým predstihom mám rezervovať?",
                 "Aspoň 2 hodiny vopred, aby som ho prispôsobil Vášmu letu. Pre vyzdvihnutie v ten istý deň po náhlej zmene zavolajte alebo napíšte na WhatsApp.")]
    elif typ == "marina":
        heading = "Súkromný marina transfer: %s" % rel
        tagline = "Súkromné taxi a transfer za pevnú cenu, %s, načasované podľa vašej lode." % rel
        intro = ("Cestujete na trase %s? Ponúkam súkromné taxi a transfer za pevnú cenu pre hostí marín, načasované podľa vašej lode a vašich cestovných plánov. "
                 "Vyzdvihnem vás s dostatkom miesta na batožinu a pohodlne vás odveziem celú cestu v Škode Superb, za paušálnu cenu &euro;%d za vozidlo, max. 4 cestujúci, dohodnutú vopred. "
                 "Či už prichádzate k svojej jachte alebo z nej pokračujete ďalej, bez taxametra a bez čakania na stanovišti, len jeden miestny vodič, ktorého rezervujete priamo. "
                 "Toto je diaľkový súkromný transfer, nie krátky miestny presun, a cenová ponuka vyššie je už nastavená pre túto trasu." % (rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za vozidlo pre max. 4 cestujúcich, dohodnutá vopred. Mýto, palivo a batožina v cene, bez taxametra."),
                ("Načasované podľa vašej lode", "Povedzte mi čas charteru, check-inu alebo odchodu a podľa toho naplánujem vyzdvihnutie, aby vás pomalší úsek nikdy netlačil do času."),
                ("Priestor na batožinu", "Kufre, zásoby aj lodné tašky sa zmestia do pohodlnej Škody Superb, s pomocou pri nakladaní a vykladaní."),
                ("Jeden miestny vodič", "Všetko vybavíte priamo so mnou, od rezervácie po príchod, telefonicky, cez WhatsApp alebo e-mailom. Žiadne call centrum.")]
        faqs = [("Koľko stojí transfer na trase %s?" % rel,
                 "Pevných &euro;%d za vozidlo pre max. 4 cestujúcich, jednosmerne, s mýtom, palivom a batožinou. Spiatočná cesta stojí &euro;%d." % (p, rp)),
                ("Môžete ma vyzdvihnúť priamo pri maríne?",
                 "Áno. Čakám vás pri vstupe do maríny alebo na recepcii a pomôžem s batožinou, aby ste sa z pontónu dostali rovno do vozidla."),
                ("Viete transfer načasovať podľa mojej lode?",
                 "Áno. Pošlite mi čas charteru, check-inu alebo odchodu pri rezervácii a podľa toho naplánujem vyzdvihnutie."),
                ("S akým predstihom mám rezervovať?",
                 "Aspoň 2 hodiny vopred, aby som potvrdil vozidlo a čas vyzdvihnutia. Pre rýchlu jazdu zavolajte alebo napíšte na WhatsApp.")]
    elif typ == "city":
        heading = "Súkromný transfer: %s" % rel
        tagline = "Súkromné taxi a transfer za pevnú cenu, %s, od dverí k dverám." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Potrebujete spoľahlivý transfer na trase %s? Ponúkam súkromné taxi a transfer za pevnú cenu, od dverí k dverám, pohodlnou Škodou Superb. "
                     "Vyzdvihnem Vás na Vašej presnej adrese a odveziem Vás priamo do cieľa, bez nechcených zastávok a spolucestujúcich. "
                     "Cena je pevná, &euro;%d za celé vozidlo, max. 4 cestujúci, dohodnutá pred odchodom, mýto a batožina v cene. "
                     "Cenová ponuka vyššie je vyplnená pre túto trasu, takže rezervácia je len pár kliknutí." % (rel, p))
        else:
            intro = ("Hľadáte taxi na trase %s bez taxametra a komplikácií? Toto je súkromný transfer za pevnú cenu s jedným miestnym vodičom. "
                     "Vyzdvihnem Vás pri dverách a pohodlne Vás odveziem do cieľa, aj s batožinou, za paušálnu cenu &euro;%d za vozidlo pre max. 4 cestujúcich. "
                     "Pre páry a rodiny to často vyjde lacnejšie než samostatné lístky na autobus či vlak, a vždy je to rýchlejšie a od dverí k dverám. "
                     "Cenová ponuka vyššie je už nastavená pre túto trasu." % (rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za vozidlo pre max. 4 cestujúcich, dohodnutá vopred. Mýto, palivo a batožina v cene, bez taxametra."),
                ("Od dverí k dverám", "Vyzdvihnem Vás na Vašej presnej adrese a vysadím pri dverách cieľa. Žiadne stanice, žiadne prestupy."),
                ("Jeden miestny vodič", "Všetko vybavíte priamo so mnou, od rezervácie po príchod, telefonicky, cez WhatsApp alebo e-mailom. Žiadne call centrum."),
                ("Zastávky na požiadanie", "Na dlhších trasách sa rád zastavím na kávu, fotku alebo krátku zaujímavosť cestou.")]
        faqs = [("Koľko stojí taxi na trase %s?" % rel,
                 "Pevných &euro;%d za vozidlo pre max. 4 cestujúcich, jednosmerne, s mýtom, palivom a batožinou. Spiatočná cesta stojí &euro;%d." % (p, rp)),
                ("Je transfer súkromný alebo zdieľaný?",
                 "Každý transfer je súkromný a od dverí k dverám, v Škode Superb. Žiadne zdieľanie vozidla a žiadne zastávky navyše, pokiaľ o ne nepožiadate."),
                ("Môžete zastaviť cestou?",
                 "Áno. Na dlhších trasách sa rád zastavím na kávu, fotku alebo krátku zaujímavosť. Stačí to spomenúť pri rezervácii."),
                ("S akým predstihom mám rezervovať?",
                 "Aspoň 2 hodiny vopred, aby som potvrdil vozidlo a čas vyzdvihnutia. Pre rýchlu jazdu zavolajte alebo napíšte na WhatsApp.")]
    else:
        heading = "Súkromné taxi: %s" % rel
        tagline = "Súkromné taxi a transfer za pevnú cenu, %s, od dverí k dverám." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Cestujete na trase %s? Jazdím súkromné taxi a transfer za pevnú cenu, s vyzdvihnutím pri Vašich dverách a vysadením presne tam, kde potrebujete byť. "
                     "Cena je paušálna, &euro;%d za celé vozidlo, max. 4 cestujúci, bez taxametra a bez čakania na stanovišti. "
                     "Pohodlná Škoda Superb, priestor na batožinu a jeden miestny vodič, ktorého rezervujete priamo. "
                     "Cenová ponuka vyššie je vyplnená pre túto trasu." % (rel, p))
        else:
            intro = ("Potrebujete taxi na trase %s? Ponúkam súkromný transfer od dverí k dverám za pevnú cenu, &euro;%d za celé vozidlo, max. 4 cestujúci. "
                     "Prídem na Vašu adresu v dohodnutom čase, takže nikdy nečakáte pri ceste, a pohodlne Vás odveziem do cieľa. "
                     "Bez taxametra, bez prekvapení, len jeden miestny vodič od rezervácie po príchod. Cenová ponuka vyššie je už nastavená pre túto trasu." % (rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za vozidlo pre max. 4 cestujúcich, dohodnutá pred jazdou. Bez taxametra, bez prekvapení."),
                ("Od dverí k dverám", "Vyzdvihnutie na Vašej adrese a vysadenie pri dverách cieľa, aj s batožinou."),
                ("Nie je potrebné stanovište", "Rezervované vopred, takže nikdy nečakáte na okoloidúce taxi. Prídem za Vami."),
                ("Jeden miestny vodič", "Všetko vybavíte priamo so mnou, od rezervácie po príchod, telefonicky, cez WhatsApp alebo e-mailom.")]
        faqs = [("Koľko stojí taxi na trase %s?" % rel,
                 "Pevných &euro;%d za vozidlo pre max. 4 cestujúcich, jednosmerne, batožina v cene. Spiatočná cesta stojí &euro;%d." % (p, rp)),
                ("Kde ma vyzdvihnete?",
                 "Na Vašej presnej adrese, či je to dom, hotel alebo apartmán. Pošlite adresu pri rezervácii a potvrdím miesto stretnutia."),
                ("S akým predstihom mám rezervovať?",
                 "Aspoň 2 hodiny vopred, aby som potvrdil vozidlo a čas vyzdvihnutia. Pre rýchlu jazdu zavolajte alebo napíšte na WhatsApp.")]

    if dd:
        faqs = [("Aká dlhá je trasa a ako dlho trvá cesta?",
                 "Na trase %s je cesta približne %d km a za bežnej premávky trvá zhruba %s, v letnej špičke o niečo dlhšie. Vyzdvihnutie plánujem tak, aby Vás pomalší úsek nikdy netlačil do času." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Dobrý deň, Antonio! Rád by som si rezervoval transfer %s (€%d).\n"
        "Moje údaje:\n- Dátum vyzdvihnutia: \n- Čas vyzdvihnutia: \n- Cestujúci: \n- Adresa vyzdvihnutia: \n- Moje meno: " % (rel, p))
    trust_line = ("Okamžité potvrdenie e-mailom &middot; Žiadne skryté poplatky &middot; Sledovanie letu v cene"
                  if typ in ("to_airport", "from_airport")
                  else "Okamžité potvrdenie e-mailom &middot; Žiadne skryté poplatky &middot; Pevná cena, bez taxametra")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: Škoda Superb od TAXI Antonio na dalmátskom pobreží" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d za vozidlo &middot; max. 4 cestujúci</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Rezervovať</a>
          <a class="btn btn-secondary" href="%s">Rezervovať cez WhatsApp</a>
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
      <span class="eyebrow center">Prečo rezervovať tento transfer</span>
      <h2 class="section-title">Prečo rezervovať taxi %s u Antonia?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Cena za trasu %s</h2>
      <p class="section-subtitle">Pevná cena za vozidlo, max. 4 cestujúci, batožina v cene. Rovnaká cena platí aj v opačnom smere.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Jednosmerne</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Spiatočne</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Záloha na potvrdenie</div></div>
        <div class="route-fact"><div class="rf-value">Hotovosť alebo karta</div><div class="rf-label">Zvyšok počas dňa</div></div>
      </div>
      <p class="hub-note">Záloha 20%% (minimum &euro;20) potvrdí rezerváciu, zvyšok zaplatíte v deň cesty, hotovosťou alebo kartou. Cestujete opačným smerom? Pozrite %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Recenzie</span>
      <h2 class="section-title">Čo hovoria cestujúci</h2>
      <p class="section-subtitle">Skutočné recenzie od skutočných cestujúcich.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">Časté otázky</span>
      <h2 class="section-title">Taxi %s: časté otázky</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Rezervujte si transfer %s</h2>
      <p class="section-subtitle">Pevná cena &euro;%d za vozidlo, max. 4 cestujúci. Potvrďte na pár kliknutí.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Rezervovať</a>
        <a href="%s" class="btn btn-secondary">Rezervovať cez WhatsApp</a>
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

    desc = ("Súkromné taxi a transfer, %s. Pevná cena &euro;%d za vozidlo, max. 4 cestujúci, od dverí k dverám. Rezervujte priamo u Antonia." % (rel, p))
    if len(desc) > 160:
        desc = "Súkromné taxi a transfer, %s. Pevná cena &euro;%d za vozidlo, max. 4. Rezervujte u Antonia." % (rel, p)
    keywords = "taxi %s, transfer %s, letiskový transfer %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Súkromný taxi transfer",
         "name": "Taxi %s" % rel,
         "description": "Súkromné taxi a transfer za pevnú cenu, %s, %d eur za vozidlo pre max. 4 cestujúcich, od dverí k dverám." % (rel, p),
         "provider": PROVIDER, "areaServed": [sfr, sto],
         "url": "https://taxisibenik.hr/sk/%s/" % skslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Súkromná jednosmerná jazda, %s, za vozidlo pre max. 4 cestujúcich. Spiatočne %d eur." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": skslug, "title": "Taxi %s | Pevná cena €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "sk")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated sk:", sum(made.values()), made, "| skipped:", skipped)
