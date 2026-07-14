# -*- coding: utf-8 -*-
"""Generate the CROATIAN variant of every route page.

Mirrors scripts/gen_routes.py but writes src/pages/<en-slug>/hr/{meta.json,
content.html} with Croatian copy and a Croatian slug. Place names are kept in
the nominative via "relacija <A> - <B>" phrasing so the copy stays correct
across all routes without a full declension table. Run after gen_routes.py and
before build.py.
"""
import os, re, json, hashlib
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "src", "pages")

# --- price matrix (source of truth) ---
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

# Croatian display names (only airports differ; other places are already Croatian).
CRO_NAME = {'Split Airport':'Zračna luka Split','Zadar Airport':'Zračna luka Zadar',
            'Zagreb Airport':'Zračna luka Zagreb','Dubrovnik Airport':'Zračna luka Dubrovnik'}
cro = lambda n: CRO_NAME.get(n, n)

AIRPORT_SLUG = {'split-airport':'zracna-luka-split','zadar-airport':'zracna-luka-zadar',
                'zagreb-airport':'zracna-luka-zagreb','dubrovnik-airport':'zracna-luka-dubrovnik'}
def cro_slug(en_slug):
    s = en_slug.replace('taxi-', 'taksi-', 1).replace('-to-', '-')
    for a, b in AIRPORT_SLUG.items():
        s = s.replace(a, b)
    return s

PROVIDER = {
    "@type": "LocalBusiness", "name": "Taxi Antonio",
    "telephone": "+385994471013", "email": "info@taxisibenik.hr",
    "address": {"@type": "PostalAddress", "addressLocality": "Šibenik", "addressCountry": "HR"},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "142"},
}

def vhash(slug, n):
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n

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
    return "/hr/rezervacija/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

def route_type(frm, to):
    if to in AIRPORT_CITY: return "to_airport"
    if frm in AIRPORT_CITY: return "from_airport"
    if frm in MARINAS or to in MARINAS: return "marina"
    if frm in BIG_CITIES or to in BIG_CITIES: return "city"
    return "local"

def faq_html(items):
    return "\n".join(
        '          <div class="faq-item">\n            <h4>%s</h4>\n            <p>%s</p>\n          </div>' % (q, a)
        for q, a in items)

def build(frm, to, slug):
    p = price(key(frm), key(to))
    rp = p * 2
    typ = route_type(frm, to)
    cf, ct = cro(frm), cro(to)
    rel = "%s - %s" % (cf, ct)
    hrslug = cro_slug(slug)

    rev = slug_of.get((to, frm))
    revlink = ('<a href="/hr/%s/">%s - %s</a>' % (cro_slug(rev), ct, cf)) if rev else ("%s - %s" % (ct, cf))
    book = book_link(frm, to, p)

    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fiksno, jedan smjer</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Udaljenost</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Trajanje vožnje</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Povratno</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fiksno, jedan smjer</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Povratno</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Do 4</div><div class="rf-label">Putnici</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Privatno, od vrata do vrata</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Vaš privatni taksi i transfer, relacija %s" % rel
        tagline = "Taksi i privatni transfer po fiksnoj cijeni, relacija %s, ravno do odlaska." % rel
        intro = ("Letite iz zračne luke %s? Za relaciju %s nudim privatni taksi transfer po fiksnoj cijeni. "
                 "Ja sam Antonio, lokalni vozač iz Šibenika: preuzimam vas na vašoj adresi i vozim izravno do odlaznog terminala "
                 "udobnom Škodom Superb. Cijena je fiksna, &euro;%d za cijelo vozilo, do 4 putnika, dogovorena unaprijed, bez taksimetra "
                 "i bez iznenađenja. Polazak usklađujem s vremenom leta kako biste stigli s dovoljno vremena za prijavu. "
                 "Obrazac za ponudu iznad već je ispunjen za ovu rutu, pa cijenu vidite i rezervirate u nekoliko dodira." % (city, rel, p))
        whys = [("Fiksna cijena &euro;%d" % p, "Jedna cijena za cijelo vozilo, do 4 putnika, dogovorena unaprijed. Cestarine, gorivo i prtljaga uključeni, bez taksimetra."),
                ("Usklađeno s vašim letom", "Recite mi vrijeme polaska i planiram unatrag, da stignete na terminal s vremenom za prijavu."),
                ("Od vrata do terminala", "Preuzimanje na vašoj adresi i dovoz do samog ulaza u odlazni terminal."),
                ("U svako doba", "Rani jutarnji i kasni noćni letovi nisu problem. Vozim 0-24 po cijeni dogovorenoj unaprijed.")]
        faqs = [("Koliko košta taksi na relaciji %s?" % rel,
                 "Fiksno &euro;%d po vozilu, jedan smjer, za do 4 putnika. Cijena je po vozilu, ne po osobi, i uključuje cestarine, gorivo i prtljagu. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Kada trebam krenuti na let?",
                 "U pravilu oko 3 sata prije međunarodnog leta i 2 sata prije domaćeg. Recite mi vrijeme leta i potvrdit ću točno vrijeme preuzimanja."),
                ("Vozite li do samog odlaznog terminala?",
                 "Da. Vozim vas izravno do odlaznog terminala i pomažem s prtljagom. Bez hoda od parkirališta i bez shuttle busa."),
                ("Koliko unaprijed trebam rezervirati?",
                 "Barem 2 sata unaprijed da potvrdim vozilo i preuzimanje, a ranije za rane jutarnje letove i sezonu. Za brži termin nazovite ili pišite na WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Vaše preuzimanje u zračnoj luci i transfer, relacija %s" % rel
        tagline = "Privatno preuzimanje i transfer po fiksnoj cijeni, relacija %s, uz praćenje leta." % rel
        intro = ("Upravo ste sletjeli u zračnu luku %s? Privatni transfer za relaciju %s skida stres s dolaska. "
                 "Dočekujem vas u dolaznoj zoni s natpisom s imenom, pomažem s prtljagom i vozim izravno na odredište udobnom Škodom Superb, "
                 "po fiksnoj cijeni od &euro;%d za cijelo vozilo, do 4 putnika. Let pratim u stvarnom vremenu, pa sam tu bez obzira slijećete li ranije ili kasnije. "
                 "Bez reda za taksi, bez dijeljenja i bez naglog poskupljenja. Obrazac iznad već je ispunjen za ovu rutu." % (city, rel, p))
        whys = [("Doček s natpisom", "Čekam u dolaznoj zoni s natpisom s vašim imenom i pomažem s torbama, da odmah krenete do vozila."),
                ("Praćenje leta", "Let pratim u stvarnom vremenu i prilagođavam se ranijem slijetanju ili kašnjenju, uz besplatno čekanje."),
                ("Fiksna cijena &euro;%d" % p, "Jedna cijena za cijelo vozilo, do 4 putnika, dogovorena unaprijed. Cestarine, gorivo i prtljaga uključeni, bez taksimetra."),
                ("Ravno do vrata", "Bez reda i bez presjedanja. Vozim vas izravno na vašu adresu.")]
        faqs = [("Gdje me dočekujete?",
                 "U dolaznoj zoni, odmah nakon preuzimanja prtljage, s natpisom s vašim imenom. Pomažem s prtljagom i vodim vas do vozila."),
                ("Što ako mi let kasni?",
                 "Nema problema. Let pratim u stvarnom vremenu i prilagođavam preuzimanje stvarnom slijetanju, bez dodatne naplate čekanja."),
                ("Koliko košta transfer na relaciji %s?" % rel,
                 "Fiksno &euro;%d po vozilu za do 4 putnika, jedan smjer, cestarine i prtljaga uključeni. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Koliko unaprijed trebam rezervirati?",
                 "Barem 2 sata unaprijed da planiram prema vašem letu. Za isti dan nakon nagle promjene nazovite ili pišite na WhatsApp.")]
    elif typ == "marina":
        heading = "Privatni transfer za goste marina, relacija %s" % rel
        tagline = "Privatni taksi i transfer po fiksnoj cijeni, relacija %s, usklađeno s vašim plovilom." % rel
        intro = ("Putujete na relaciji %s? Vozim privatni taksi i transfer po fiksnoj cijeni za goste marina, usklađen s vašim plovilom i planom putovanja. "
                 "Preuzimam vas uz obilje mjesta za prtljagu i udobno vas vozim cijelim putem u Škodi Superb, po ravnoj cijeni od &euro;%d za vozilo, do 4 putnika, dogovorenoj prije polaska. "
                 "Bilo da se ukrcavate na svoju jahtu ili nastavljate dalje nakon što ste s nje sišli, nema taksimetra i nema čekanja na stajalištu, samo jedan lokalni vozač kojeg rezervirate izravno. "
                 "Ovo je transfer na dužoj relaciji, a ne kratka lokalna vožnja, i ponuda iznad već je postavljena za ovu rutu, pa rezervacija traje nekoliko dodira." % (rel, p))
        whys = [("Fiksna cijena &euro;%d" % p, "Jedna cijena po vozilu za do 4 putnika, dogovorena unaprijed. Cestarine, gorivo i prtljaga uključeni, bez taksimetra."),
                ("Usklađeno s vašim plovilom", "Recite mi vrijeme najma, prijave ili polaska i planiram preuzimanje prema njemu, da vas usporeni dio nikad ne požuri."),
                ("Mjesta za prtljagu", "Kovčezi, namirnice i brodske torbe stanu u udobnu Škodu Superb, uz pomoć pri utovaru i istovaru."),
                ("Jedan lokalni vozač", "Dogovarate se izravno sa mnom od rezervacije do dolaska, telefonom, WhatsAppom ili e-poštom. Bez pozivnog centra.")]
        faqs = [("Koliko košta transfer na relaciji %s?" % rel,
                 "Fiksno &euro;%d po vozilu za do 4 putnika, jedan smjer, s cestarinama, gorivom i prtljagom. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Možete li me preuzeti u samoj marini?",
                 "Da. Dočekujem vas na ulazu u marinu ili na recepciji i pomažem s prtljagom, da s pontona odmah dođete do vozila."),
                ("Možete li uskladiti transfer s mojim plovilom?",
                 "Da. Pošaljite mi vrijeme najma, prijave ili polaska pri rezervaciji i planiram preuzimanje prema njemu."),
                ("Koliko unaprijed trebam rezervirati?",
                 "Barem 2 sata unaprijed da potvrdim vozilo i vrijeme preuzimanja. Za brži termin nazovite ili pišite izravno na WhatsApp.")]
    elif typ == "city":
        heading = "Privatni transfer, relacija %s" % rel
        tagline = "Privatni taksi i transfer po fiksnoj cijeni, relacija %s, od vrata do vrata." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Trebate pouzdan transfer na relaciji %s? Nudim privatni taksi i transfer po fiksnoj cijeni, od vrata do vrata, udobnom Škodom Superb. "
                     "Preuzimam vas na točnoj adresi i vozim izravno na odredište, bez usputnih zaustavljanja koja niste tražili i bez suputnika. "
                     "Cijena je fiksna, &euro;%d za cijelo vozilo, do 4 putnika, dogovorena prije polaska, cestarine i prtljaga uključeni. "
                     "Ponuda iznad ispunjena je za ovu rutu, pa rezervacija traje nekoliko dodira." % (rel, p))
        else:
            intro = ("Tražite taksi na relaciji %s bez taksimetra i gužve? Ovo je privatni transfer po fiksnoj cijeni s jednim lokalnim vozačem. "
                     "Preuzimam vas na vratima i udobno vozim na odredište, s prtljagom, po ravnoj cijeni od &euro;%d po vozilu za do 4 putnika. "
                     "Za parove i obitelji često je povoljnije od odvojenih autobusnih ili vlakskih karata, a uvijek je brže i od vrata do vrata. "
                     "Ponuda iznad već je postavljena za ovu rutu." % (rel, p))
        whys = [("Fiksna cijena &euro;%d" % p, "Jedna cijena po vozilu za do 4 putnika, dogovorena unaprijed. Cestarine, gorivo i prtljaga uključeni, bez taksimetra."),
                ("Od vrata do vrata", "Preuzimam vas na točnoj adresi i ostavljam pred vratima odredišta. Bez kolodvora i bez presjedanja."),
                ("Jedan lokalni vozač", "Dogovarate se izravno sa mnom od rezervacije do dolaska, telefonom, WhatsAppom ili e-poštom. Bez pozivnog centra."),
                ("Zaustavljanja na zahtjev", "Na duljim rutama rado stanem za kavu, fotografiju ili kratku znamenitost usput.")]
        faqs = [("Koliko košta taksi na relaciji %s?" % rel,
                 "Fiksno &euro;%d po vozilu za do 4 putnika, jedan smjer, s cestarinama, gorivom i prtljagom. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Je li transfer privatan ili dijeljen?",
                 "Svaki je transfer privatan i od vrata do vrata, u Škodi Superb. Bez dijeljenja vozila i bez dodatnih zaustavljanja osim ako ih zatražite."),
                ("Možete li stati usput?",
                 "Da. Na duljim rutama rado stanem za kavu, fotografiju ili kratku znamenitost. Samo javite pri rezervaciji."),
                ("Koliko unaprijed trebam rezervirati?",
                 "Barem 2 sata unaprijed da potvrdim vozilo i vrijeme preuzimanja. Za brži termin nazovite ili pišite na WhatsApp.")]
    else:  # local
        heading = "Privatni taksi, relacija %s" % rel
        tagline = "Privatni taksi i transfer po fiksnoj cijeni, relacija %s, od vrata do vrata." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Putujete na relaciji %s? Vozim privatni taksi i transfer po fiksnoj cijeni, s preuzimanjem na vašim vratima i dovozom točno tamo gdje trebate biti. "
                     "Cijena je ravnih &euro;%d za cijelo vozilo, do 4 putnika, bez taksimetra i bez čekanja na stajalištu. "
                     "Udobna Škoda Superb, mjesta za prtljagu i jedan lokalni vozač kojeg rezervirate izravno. "
                     "Ponuda iznad ispunjena je za ovu rutu." % (rel, p))
        else:
            intro = ("Trebate taksi na relaciji %s? Nudim privatni transfer od vrata do vrata po fiksnoj cijeni od &euro;%d za cijelo vozilo, do 4 putnika. "
                     "Dolazim na vašu adresu u dogovoreno vrijeme, pa nikad ne čekate uz cestu, i udobno vas vozim na odredište. "
                     "Bez taksimetra, bez iznenađenja, samo jedan lokalni vozač od rezervacije do dolaska. Ponuda iznad već je postavljena za ovu rutu." % (rel, p))
        whys = [("Fiksna cijena &euro;%d" % p, "Jedna cijena po vozilu za do 4 putnika, dogovorena prije putovanja. Bez taksimetra, bez iznenađenja."),
                ("Od vrata do vrata", "Preuzimanje na vašoj adresi i dovoz pred vrata odredišta, zajedno s prtljagom."),
                ("Bez stajališta", "Rezervirano unaprijed, pa nikad ne čekate slobodni taksi. Dolazim po vas."),
                ("Jedan lokalni vozač", "Dogovarate se izravno sa mnom od rezervacije do dolaska, telefonom, WhatsAppom ili e-poštom.")]
        faqs = [("Koliko košta taksi na relaciji %s?" % rel,
                 "Fiksno &euro;%d po vozilu za do 4 putnika, jedan smjer, prtljaga uključena. Povratna vožnja je &euro;%d." % (p, rp)),
                ("Gdje me preuzimate?",
                 "Na vašoj točnoj adresi, bila to kuća, hotel ili apartman. Pošaljite adresu pri rezervaciji i potvrdit ću mjesto sastanka."),
                ("Koliko unaprijed trebam rezervirati?",
                 "Barem 2 sata unaprijed da potvrdim vozilo i vrijeme preuzimanja. Za brži termin nazovite ili pišite na WhatsApp.")]

    if dd:
        faqs = [("Kolika je udaljenost i koliko traje vožnja?",
                 "Vožnja na relaciji %s duga je oko %d km i traje otprilike %s u uobičajenom prometu, nešto duže u ljetnim gužvama. Polazak planiram tako da vas usporeni dio nikad ne požuri." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join(
        '        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t)
        for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Pozdrav Antonio, želio bih rezervirati transfer %s (€%d).\n"
        "Moji podaci:\n- Datum polaska: \n- Vrijeme polaska: \n- Broj putnika: \n- Adresa preuzimanja: \n- Moje ime: " % (rel, p))
    trust_line = ("Trenutna potvrda e-poštom &middot; Bez skrivenih troškova &middot; Praćenje leta uključeno"
                  if typ in ("to_airport", "from_airport")
                  else "Trenutna potvrda e-poštom &middot; Bez skrivenih troškova &middot; Fiksna cijena, bez taksimetra")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taksi %s: Škoda Superb TAXI Antonio na dalmatinskoj obali" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taksi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d po vozilu &middot; do 4 putnika</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Rezerviraj</a>
          <a class="btn btn-secondary" href="%s">Rezerviraj putem WhatsAppa</a>
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
      <span class="eyebrow center">Zašto rezervirati ovaj transfer</span>
      <h2 class="section-title">Zašto rezervirati taksi %s kod Antonija?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Cijena %s</h2>
      <p class="section-subtitle">Fiksno po vozilu, do 4 putnika, prtljaga uključena. Ista cijena vrijedi u suprotnom smjeru.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Jedan smjer</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Povratno</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Predujam za potvrdu</div></div>
        <div class="route-fact"><div class="rf-value">Gotovina ili kartica</div><div class="rf-label">Ostatak na dan</div></div>
      </div>
      <p class="hub-note">Predujam od 20%% (najmanje &euro;20) potvrđuje rezervaciju, a ostatak plaćate na dan vožnje, gotovinom ili karticom. Putujete u suprotnom smjeru? Pogledajte %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Recenzije</span>
      <h2 class="section-title">Što kažu putnici</h2>
      <p class="section-subtitle">Prave recenzije pravih putnika.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">Česta pitanja</span>
      <h2 class="section-title">Taksi %s: često postavljana pitanja</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Rezervirajte transfer %s</h2>
      <p class="section-subtitle">Fiksno &euro;%d po vozilu, do 4 putnika. Potvrda u nekoliko dodira.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Rezerviraj</a>
        <a href="%s" class="btn btn-secondary">Rezerviraj putem WhatsAppa</a>
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

    desc = ("Privatni taksi i transfer, relacija %s. Fiksno &euro;%d po vozilu, do 4 putnika, od vrata do vrata. Rezervirajte izravno kod Antonija." % (rel, p))
    if len(desc) > 155:
        desc = "Privatni taksi i transfer, relacija %s. Fiksno &euro;%d po vozilu, do 4. Rezervirajte izravno kod Antonija." % (rel, p)
    keywords = "taksi %s, transfer %s, prijevoz %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service",
         "serviceType": "Privatni taksi transfer",
         "name": "Taksi %s" % rel,
         "description": "Privatni taksi i transfer po fiksnoj cijeni, relacija %s, %d eura po vozilu za do 4 putnika, od vrata do vrata." % (rel, p),
         "provider": PROVIDER,
         "areaServed": [cf, ct],
         "url": "https://taxisibenik.hr/hr/%s/" % hrslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Jednosmjerni privatni transfer, relacija %s, po vozilu za do 4 putnika. Povratno %d eura." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": hrslug, "title": "Taksi %s | Fiksna cijena €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}

    outdir = os.path.join(PAGES, slug, "hr")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}
skipped_noprice = 0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None:
        skipped_noprice += 1; continue
    t = build(frm, to, slug)
    made[t] += 1
print("generated hr:", sum(made.values()), made)
print("skipped (no matrix price):", skipped_noprice)
