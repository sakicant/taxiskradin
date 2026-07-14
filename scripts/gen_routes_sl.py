# -*- coding: utf-8 -*-
"""Generate the SLOVENIAN variant of every route page. Mirrors gen_routes.py.
Place names kept nominative via "relacija <A> - <B>". Run after gen_routes.py."""
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
SL_NAME = {'Split Airport':'Letališče Split','Zadar Airport':'Letališče Zadar',
           'Zagreb Airport':'Letališče Zagreb','Dubrovnik Airport':'Letališče Dubrovnik'}
sl = lambda n: SL_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'letalisce-split','zadar-airport':'letalisce-zadar',
                'zagreb-airport':'letalisce-zagreb','dubrovnik-airport':'letalisce-dubrovnik'}
def sl_slug(en_slug):
    s = en_slug.replace('taxi-', 'taksi-', 1).replace('-to-', '-')
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
    return "/sl/rezervacija/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    sfr, sto = sl(frm), sl(to)
    rel = "%s - %s" % (sfr, sto)
    slslug = sl_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/sl/%s/">%s - %s</a>' % (sl_slug(rev), sto, sfr)) if rev else ("%s - %s" % (sto, sfr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fiksno, enosmerno</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Razdalja</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Čas vožnje</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Povratno</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fiksno, enosmerno</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Povratno</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Do 4</div><div class="rf-label">Potniki</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Zasebno, od vrat do vrat</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Vaš zasebni taksi in prevoz, relacija %s" % rel
        tagline = "Taksi in zasebni prevoz po fiksni ceni, relacija %s, naravnost do odhodov." % rel
        intro = ("Odhajate z letališča %s? Za relacijo %s ponujam zasebni taksi in prevoz po fiksni ceni. "
                 "Sem Antonio, lokalni voznik iz Šibenika: poberem vas na vašem naslovu in vas odpeljem naravnost do odhodnega terminala v udobni Škodi Superb. "
                 "Cena je fiksna, &euro;%d za celotno vozilo, do 4 potnike, dogovorjena vnaprej, brez taksimetra in brez presenečenj. "
                 "Prevzem načrtujem glede na uro vašega leta, da prispete z dovolj časa za prijavo. "
                 "Obrazec za ponudbo zgoraj je za to relacijo že izpolnjen, tako da vidite ceno in rezervirate v nekaj klikih." % (city, rel, p))
        whys = [("Fiksna cena &euro;%d" % p, "Ena cena za celotno vozilo, do 4 potnike, dogovorjena vnaprej. Cestnine, gorivo in prtljaga vključeni, brez taksimetra."),
                ("Prilagojeno vašemu letu", "Povejte mi uro odhoda in izračunam nazaj, da ste na terminalu pravočasno za prijavo."),
                ("Od vrat do terminala", "Prevzem na vašem naslovu in dostava naravnost pred vhod v odhodni terminal."),
                ("Ob vsaki uri", "Zgodnji jutranji in pozni večerni leti niso težava. Vozim 24 ur na dan po vnaprej dogovorjeni ceni.")]
        faqs = [("Koliko stane taksi na relaciji %s?" % rel,
                 "Fiksno &euro;%d na vozilo, enosmerno, do 4 potnike. Cena je na vozilo, ne na osebo, in vključuje cestnine, gorivo in prtljago. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Kdaj naj se odpravim na let?",
                 "Praviloma približno 3 ure pred mednarodnim letom in 2 uri pred domačim. Povejte mi uro leta in potrdim natančen prevzem."),
                ("Me odpeljete do samega odhodnega terminala?",
                 "Da. Odpeljem vas naravnost do odhodnega terminala in pomagam s prtljago. Brez hoje s parkirišča in brez shuttle avtobusa."),
                ("Kako dolgo vnaprej rezervirati?",
                 "Vsaj 2 uri prej, da potrdim vozilo in prevzem, in prej za jutranje lete in v visoki sezoni. Za hitro vožnjo pokličite ali pišite na WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Vaš prevzem na letališču in prevoz, relacija %s" % rel
        tagline = "Zasebni prevzem na letališču in prevoz po fiksni ceni, relacija %s, s spremljanjem leta." % rel
        intro = ("Ste pravkar pristali na letališču %s? Zasebni prevoz za relacijo %s odvzame stres ob prihodu. "
                 "Pričakam vas v prihodni dvorani s tablico z imenom, pomagam s prtljago in vas odpeljem naravnost na cilj v udobni Škodi Superb, "
                 "po fiksni ceni &euro;%d za celotno vozilo, do 4 potnike. Vaš let spremljam v realnem času, zato sem tam, ne glede na to, ali pristanete prej ali pozneje. "
                 "Brez vrste za taksi, brez skupnega prevoza in brez pribitkov. Obrazec zgoraj je za to relacijo že izpolnjen." % (city, rel, p))
        whys = [("Sprejem s tablico", "Čakam v prihodni dvorani s tablico z vašim imenom in pomagam s torbami, da greste naravnost do vozila."),
                ("Spremljanje leta", "Vaš let spremljam v realnem času in se prilagodim zgodnjemu pristanku ali zamudi, z brezplačnim čakanjem."),
                ("Fiksna cena &euro;%d" % p, "Ena cena za celotno vozilo, do 4 potnike, dogovorjena vnaprej. Cestnine, gorivo in prtljaga vključeni, brez taksimetra."),
                ("Naravnost do vaših vrat", "Brez vrste in brez prestopanja. Odpeljem vas naravnost na vaš naslov.")]
        faqs = [("Kje me pričakate?",
                 "V prihodni dvorani, takoj za prevzemom prtljage, s tablico z vašim imenom. Pomagam s prtljago in vas pospremim do vozila."),
                ("Kaj če ima moj let zamudo?",
                 "Brez težav. Vaš let spremljam v realnem času in prevzem prilagodim dejanskemu pristanku, brez pribitka za čakanje."),
                ("Koliko stane prevoz na relaciji %s?" % rel,
                 "Fiksno &euro;%d na vozilo do 4 potnike, enosmerno, cestnine in prtljaga vključeni. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Kako dolgo vnaprej rezervirati?",
                 "Vsaj 2 uri prej, da načrtujem glede na vaš let. Za prevzem isti dan po nenadni spremembi pokličite ali pišite na WhatsApp.")]
    elif typ == "marina":
        heading = "Zasebni prevoz za marino, relacija %s" % rel
        tagline = "Taksi in zasebni prevoz po fiksni ceni, relacija %s. &euro;%d na vozilo, do 4 potnike, prilagojeno vaši plovbi." % (rel, p)
        intro = ("Se prevažate na relaciji %s? Vozim zasebni taksi in prevoz po fiksni ceni za goste marin, prilagojen vaši plovbi in vašim potovalnim načrtom. "
                 "Poberem vas z dovolj prostora za prtljago in vas udobno odpeljem vso pot v Škodi Superb, po pavšalni ceni &euro;%d za vozilo, do 4 potnike, dogovorjeni pred potjo. "
                 "Naj se vkrcavate na svojo jahto ali nadaljujete pot potem, ko z nje stopite, ni taksimetra in ni čakanja na postajališču, samo en lokalni voznik, ki ga rezervirate neposredno. "
                 "To je zasebni prevoz na daljše razdalje, ne kratek lokalni skok, in ponudba zgoraj je za to relacijo že nastavljena, tako da rezervacija traja le nekaj klikov." % (rel, p))
        whys = [("Fiksna cena &euro;%d" % p, "Ena cena za vozilo, do 4 potnike, dogovorjena vnaprej. Cestnine, gorivo in prtljaga vključeni, brez taksimetra."),
                ("Prilagojeno vaši plovbi", "Povejte mi uro najema, prijave ali odhoda in prevzem načrtujem glede na to, da vas počasnejši odsek nikoli ne priganja."),
                ("Prostor za vašo prtljago", "Kovčki, zaloge in ladijske torbe se udobno zložijo v Škodo Superb, s pomočjo pri natovarjanju in raztovarjanju."),
                ("En lokalni voznik", "Vse urejate neposredno z mano, od rezervacije do prihoda, po telefonu, WhatsAppu ali e-pošti. Brez klicnega centra.")]
        faqs = [("Koliko stane prevoz na relaciji %s?" % rel,
                 "Fiksno &euro;%d na vozilo, do 4 potnike, enosmerno, s cestninami, gorivom in prtljago. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Me lahko poberete kar v marini?",
                 "Da. Pričakam vas pri vhodu v marino ali na recepciji in pomagam s prtljago, tako da greste naravnost s pomola do vozila."),
                ("Lahko prevoz prilagodite moji plovbi?",
                 "Da. Ob rezervaciji mi pošljite uro najema, prijave ali odhoda in prevzem načrtujem glede na to."),
                ("Kako dolgo vnaprej rezervirati?",
                 "Vsaj 2 uri prej, da potrdim vozilo in uro prevzema. Za hitrejšo vožnjo me pokličite ali pišite na WhatsApp.")]
    elif typ == "city":
        heading = "Zasebni prevoz, relacija %s" % rel
        tagline = "Taksi in zasebni prevoz po fiksni ceni, relacija %s, od vrat do vrat." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Potrebujete zanesljiv prevoz na relaciji %s? Ponujam zasebni taksi in prevoz po fiksni ceni, od vrat do vrat, v udobni Škodi Superb. "
                     "Poberem vas na vašem točnem naslovu in vas odpeljem naravnost na cilj, brez nezaželenih postankov in brez sopotnikov. "
                     "Cena je fiksna, &euro;%d za celotno vozilo, do 4 potnike, dogovorjena pred odhodom, cestnine in prtljaga vključeni. "
                     "Ponudba zgoraj je za to relacijo izpolnjena, tako da rezervacija traja le nekaj klikov." % (rel, p))
        else:
            intro = ("Iščete taksi na relaciji %s brez taksimetra in zapletov? To je zasebni prevoz po fiksni ceni z enim lokalnim voznikom. "
                     "Poberem vas pred vrati in vas udobno odpeljem na cilj, skupaj s prtljago, po pavšalni ceni &euro;%d na vozilo do 4 potnike. "
                     "Za pare in družine je pogosto ceneje kot ločene avtobusne ali vlakovne vozovnice, in vedno je hitreje ter od vrat do vrat. "
                     "Ponudba zgoraj je za to relacijo že nastavljena." % (rel, p))
        whys = [("Fiksna cena &euro;%d" % p, "Ena cena na vozilo do 4 potnike, dogovorjena vnaprej. Cestnine, gorivo in prtljaga vključeni, brez taksimetra."),
                ("Od vrat do vrat", "Poberem vas na vašem točnem naslovu in vas odložim pred vrati cilja. Brez postaj, brez prestopanja."),
                ("En lokalni voznik", "Vse urejate neposredno z mano, od rezervacije do prihoda, po telefonu, WhatsAppu ali e-pošti. Brez klicnega centra."),
                ("Postanki na željo", "Na daljših relacijah se rad ustavim za kavo, fotografijo ali kratko znamenitost po poti.")]
        faqs = [("Koliko stane taksi na relaciji %s?" % rel,
                 "Fiksno &euro;%d na vozilo do 4 potnike, enosmerno, s cestninami, gorivom in prtljago. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Je prevoz zaseben ali deljen?",
                 "Vsak prevoz je zaseben in od vrat do vrat, v Škodi Superb. Brez deljenja vozila in brez dodatnih postankov, razen če jih zahtevate."),
                ("Se lahko ustavite po poti?",
                 "Da. Na daljših relacijah se rad ustavim za kavo, fotografijo ali kratko znamenitost. Samo povejte ob rezervaciji."),
                ("Kako dolgo vnaprej rezervirati?",
                 "Vsaj 2 uri prej, da potrdim vozilo in uro prevzema. Za hitro vožnjo pokličite ali pišite na WhatsApp.")]
    else:
        heading = "Zasebni taksi, relacija %s" % rel
        tagline = "Taksi in zasebni prevoz po fiksni ceni, relacija %s, od vrat do vrat." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Potujete na relaciji %s? Vozim zasebni taksi in prevoz po fiksni ceni, s prevzemom pred vašimi vrati in dostavo točno tja, kamor morate. "
                     "Cena je pavšalna, &euro;%d za celotno vozilo, do 4 potnike, brez taksimetra in brez čakanja na postajališču. "
                     "Udobna Škoda Superb, prostor za prtljago in en lokalni voznik, ki ga rezervirate neposredno. "
                     "Ponudba zgoraj je za to relacijo izpolnjena." % (rel, p))
        else:
            intro = ("Potrebujete taksi na relaciji %s? Ponujam zasebni prevoz od vrat do vrat po fiksni ceni &euro;%d za celotno vozilo, do 4 potnike. "
                     "Pridem na vaš naslov ob dogovorjenem času, tako da nikoli ne čakate ob cesti, in vas udobno odpeljem na cilj. "
                     "Brez taksimetra, brez presenečenj, samo en lokalni voznik od rezervacije do prihoda. Ponudba zgoraj je za to relacijo že nastavljena." % (rel, p))
        whys = [("Fiksna cena &euro;%d" % p, "Ena cena na vozilo do 4 potnike, dogovorjena pred vožnjo. Brez taksimetra, brez presenečenj."),
                ("Od vrat do vrat", "Prevzem na vašem naslovu in dostava pred vrata cilja, skupaj s prtljago."),
                ("Brez postajališča", "Rezervirano vnaprej, tako da nikoli ne čakate na mimoidoči taksi. Pridem k vam."),
                ("En lokalni voznik", "Vse urejate neposredno z mano, od rezervacije do prihoda, po telefonu, WhatsAppu ali e-pošti.")]
        faqs = [("Koliko stane taksi na relaciji %s?" % rel,
                 "Fiksno &euro;%d na vozilo do 4 potnike, enosmerno, prtljaga vključena. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Kje me poberete?",
                 "Na vašem točnem naslovu, naj bo to hiša, hotel ali apartma. Pošljite naslov ob rezervaciji in potrdim mesto srečanja."),
                ("Kako dolgo vnaprej rezervirati?",
                 "Vsaj 2 uri prej, da potrdim vozilo in uro prevzema. Za hitro vožnjo pokličite ali pišite na WhatsApp.")]

    if dd:
        faqs = [("Kako dolga je relacija in koliko traja vožnja?",
                 "Vožnja na relaciji %s je približno %d km in traja okoli %s pri običajnem prometu, nekoliko dlje v poletni konici. Prevzem načrtujem tako, da vas počasnejši odsek nikoli ne priganja." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Pozdravljeni Antonio, rad bi rezerviral prevoz %s (€%d).\n"
        "Moji podatki:\n- Datum prevzema: \n- Ura prevzema: \n- Potniki: \n- Naslov prevzema: \n- Moje ime: " % (rel, p))
    trust_line = ("Takojšnja potrditev po e-pošti &middot; Brez skritih stroškov &middot; Spremljanje leta vključeno"
                  if typ in ("to_airport", "from_airport")
                  else "Takojšnja potrditev po e-pošti &middot; Brez skritih stroškov &middot; Fiksna cena, brez taksimetra")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taksi %s: Škoda Superb TAXI Antonio na dalmatinski obali" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taksi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d na vozilo &middot; do 4 potnike</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Rezerviraj</a>
          <a class="btn btn-secondary" href="%s">Rezerviraj prek WhatsAppa</a>
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
      <span class="eyebrow center">Zakaj rezervirati ta prevoz</span>
      <h2 class="section-title">Zakaj rezervirati taksi %s pri Antoniu?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Cena %s</h2>
      <p class="section-subtitle">Fiksna cena na vozilo, do 4 potnike, prtljaga vključena. Enaka cena velja v nasprotni smeri.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Enosmerno</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Povratno</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Predujem za potrditev</div></div>
        <div class="route-fact"><div class="rf-value">Gotovina ali kartica</div><div class="rf-label">Ostanek na dan vožnje</div></div>
      </div>
      <p class="hub-note">Predujem 20%% (najmanj &euro;20) potrdi rezervacijo, ostanek plačate na dan vožnje, z gotovino ali kartico. Potujete v nasprotni smeri? Glejte %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Mnenja</span>
      <h2 class="section-title">Kaj pravijo potniki</h2>
      <p class="section-subtitle">Pristna mnenja pravih potnikov.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taksi %s: pogosta vprašanja</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Rezervirajte prevoz %s</h2>
      <p class="section-subtitle">Fiksna cena &euro;%d na vozilo, do 4 potnike. Potrdite v nekaj klikih.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Rezerviraj</a>
        <a href="%s" class="btn btn-secondary">Rezerviraj prek WhatsAppa</a>
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

    desc = ("Taksi in zasebni prevoz, relacija %s. Fiksna cena &euro;%d na vozilo, do 4 potnike, od vrat do vrat. Rezervirajte neposredno pri Antoniu." % (rel, p))
    if len(desc) > 160:
        desc = "Taksi in zasebni prevoz, relacija %s. Fiksna cena &euro;%d na vozilo, do 4. Rezervirajte pri Antoniu." % (rel, p)
    keywords = "taksi %s, prevoz %s, letališki prevoz %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Zasebni taksi prevoz",
         "name": "Taksi %s" % rel,
         "description": "Taksi in zasebni prevoz po fiksni ceni, relacija %s, %d evrov na vozilo do 4 potnike, od vrat do vrat." % (rel, p),
         "provider": PROVIDER, "areaServed": [sfr, sto],
         "url": "https://taxisibenik.hr/sl/%s/" % slslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Zasebna enosmerna vožnja, relacija %s, na vozilo do 4 potnike. Povratno %d evrov." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": slslug, "title": "Taksi %s | Fiksna cena €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "sl")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated sl:", sum(made.values()), made, "| skipped:", skipped)
