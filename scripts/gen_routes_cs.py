# -*- coding: utf-8 -*-
"""Generate the CZECH variant of every route page. Mirrors gen_routes.py.
Place names kept nominative via "trasa <A> - <B>". Run after gen_routes.py."""
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
CS_NAME = {'Split Airport':'Letiště Split','Zadar Airport':'Letiště Zadar',
           'Zagreb Airport':'Letiště Zagreb','Dubrovnik Airport':'Letiště Dubrovnik'}
cs = lambda n: CS_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'letiste-split','zadar-airport':'letiste-zadar',
                'zagreb-airport':'letiste-zagreb','dubrovnik-airport':'letiste-dubrovnik'}
def cs_slug(en_slug):
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
    return "/cs/rezervace/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    cfr, cto = cs(frm), cs(to)
    rel = "%s - %s" % (cfr, cto)
    csslug = cs_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/cs/%s/">%s - %s</a>' % (cs_slug(rev), cto, cfr)) if rev else ("%s - %s" % (cto, cfr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Pevná cena, jednosměrná</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Vzdálenost</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Doba jízdy</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Zpáteční</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Pevná cena, jednosměrná</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Zpáteční</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Až 4</div><div class="rf-label">Cestující</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Soukromě, ode dveří ke dveřím</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Vaše soukromé taxi a transfer, trasa %s" % rel
        tagline = "Taxi a soukromý transfer za pevnou cenu, trasa %s, přímo k odletům." % rel
        intro = ("Letíte z letiště %s? Na trase %s nabízím soukromé taxi a transfer za pevnou cenu. "
                 "Jsem Antonio, místní řidič ze Šibeniku: vyzvednu vás u dveří a odvezu přímo k odletovému terminálu pohodlnou Škodou Superb. "
                 "Cena je pevná, &euro;%d za celé vozidlo, až 4 cestující, dohodnutá předem, bez taxametru a bez překvapení. "
                 "Vyzvednutí plánuji podle času vašeho letu, abyste dorazili s rezervou na odbavení. "
                 "Formulář s cenovou nabídkou výše je pro tuto trasu již vyplněný, takže cenu uvidíte a rezervujete v pár kliknutích." % (city, rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za celé vozidlo, až 4 cestující, dohodnutá předem. Mýtné, palivo a zavazadla v ceně, bez taxametru."),
                ("Přizpůsobené vašemu letu", "Řekněte mi čas odletu a spočítám to zpětně, abyste na terminál dorazili s časem na odbavení."),
                ("Ode dveří k terminálu", "Vyzvednutí u vaší adresy a odvoz přímo ke vchodu do odletového terminálu."),
                ("V kteroukoli hodinu", "Brzké ranní i pozdní noční lety nejsou problém. Jezdím nonstop za cenu dohodnutou předem.")]
        faqs = [("Kolik stojí taxi na trase %s?" % rel,
                 "Pevně &euro;%d za vozidlo, jednosměrná, až 4 cestující. Cena je za vozidlo, ne za osobu, a zahrnuje mýtné, palivo a zavazadla. Zpáteční jízda je &euro;%d." % (p, rp)),
                ("Kdy mám vyrazit na let?",
                 "Zpravidla asi 3 hodiny před mezinárodním letem a 2 hodiny před vnitrostátním. Řekněte mi čas letu a potvrdím přesné vyzvednutí."),
                ("Odvezete mě až k odletovému terminálu?",
                 "Ano. Odvezu vás přímo k odletovému terminálu a pomůžu se zavazadly. Žádná chůze z parkoviště a žádný shuttle bus."),
                ("S jakým předstihem rezervovat?",
                 "Alespoň 2 hodiny předem, abych potvrdil vozidlo a vyzvednutí, a dříve u ranních letů a v sezoně. Pro rychlou jízdu zavolejte nebo napište na WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Vaše vyzvednutí z letiště a transfer, trasa %s" % rel
        tagline = "Soukromé vyzvednutí z letiště a transfer za pevnou cenu, trasa %s, se sledováním letu." % rel
        intro = ("Právě jste přistáli na letišti %s? Soukromý transfer na trase %s sejme stres z příjezdu. "
                 "Přivítám vás v příletové hale s cedulkou se jménem, pomůžu se zavazadly a odvezu vás přímo do cíle pohodlnou Škodou Superb, "
                 "za pevnou cenu &euro;%d za celé vozidlo, až 4 cestující. Váš let sleduji v reálném čase, takže jsem na místě, ať přistanete dříve nebo později. "
                 "Žádná fronta na taxi, žádný sdílený shuttle a žádné příplatky. Formulář výše je pro tuto trasu již vyplněný." % (city, rel, p))
        whys = [("Přivítání s cedulkou", "Čekám v příletové hale s cedulkou s vaším jménem a pomůžu s taškami, ať jdete rovnou k vozidlu."),
                ("Sledování letu", "Váš let sleduji v reálném čase a přizpůsobím se dřívějšímu přistání nebo zpoždění, s čekáním zdarma."),
                ("Pevná cena &euro;%d" % p, "Jedna cena za celé vozidlo, až 4 cestující, dohodnutá předem. Mýtné, palivo a zavazadla v ceně, bez taxametru."),
                ("Rovnou k vašim dveřím", "Žádná fronta a žádné přestupy. Odvezu vás přímo na vaši adresu.")]
        faqs = [("Kde mě přivítáte?",
                 "V příletové hale, hned za výdejem zavazadel, s cedulkou s vaším jménem. Pomůžu se zavazadly a doprovodím vás k vozidlu."),
                ("Co když má můj let zpoždění?",
                 "Žádný problém. Váš let sleduji v reálném čase a přizpůsobím vyzvednutí skutečnému přistání, bez příplatku za čekání."),
                ("Kolik stojí transfer na trase %s?" % rel,
                 "Pevně &euro;%d za vozidlo až pro 4 cestující, jednosměrná, mýtné a zavazadla v ceně. Zpáteční jízda je &euro;%d." % (p, rp)),
                ("S jakým předstihem rezervovat?",
                 "Alespoň 2 hodiny předem, abych naplánoval podle vašeho letu. Pro vyzvednutí týž den po náhlé změně zavolejte nebo napište na WhatsApp.")]
    elif typ == "marina":
        heading = "Soukromý transfer z přístavu, trasa %s" % rel
        tagline = "Taxi a soukromý transfer za pevnou cenu, trasa %s. &euro;%d za vozidlo, až 4 cestující, načasovaný podle vaší lodi." % (rel, p)
        intro = ("Cestujete na trase %s? Provozuji soukromé taxi a transfer za pevnou cenu pro hosty přístavů, načasovaný podle vaší lodi a vašich cestovních plánů. "
                 "Vyzvednu vás s dostatkem místa na zavazadla a pohodlně vás odvezu celou cestu pohodlnou Škodou Superb, za paušální &euro;%d za vozidlo, až 4 cestující, dohodnutou před odjezdem. "
                 "Ať už nastupujete na svou jachtu, nebo pokračujete dál poté, co jste z ní vystoupili, žádný taxametr a žádné čekání na stanovišti, jen jeden místní řidič, kterého rezervujete přímo. "
                 "Je to soukromý transfer na dlouhou vzdálenost, ne krátká místní jízda, a nabídka výše je pro tuto trasu již nastavená, takže rezervace zabere pár kliknutí." % (rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za vozidlo až pro 4 cestující, dohodnutá předem. Mýtné, palivo a zavazadla v ceně, bez taxametru."),
                ("Načasováno podle vaší lodi", "Řekněte mi čas charteru, check-inu nebo odjezdu a vyzvednutí naplánuji podle něj, aby vás pomalejší úsek nikdy netlačil."),
                ("Místo na zavazadla", "Kufry, zásoby i lodní tašky se pohodlně vejdou do Škody Superb, s pomocí při nakládání a vykládání."),
                ("Jeden místní řidič", "Vše řešíte přímo se mnou, od rezervace po vysazení, telefonicky, přes WhatsApp nebo e-mail. Žádné call centrum.")]
        faqs = [("Kolik stojí transfer na trase %s?" % rel,
                 "Pevně &euro;%d za vozidlo až pro 4 cestující, jednosměrná, s mýtným, palivem a zavazadly v ceně. Zpáteční jízda je &euro;%d." % (p, rp)),
                ("Můžete mě vyzvednout přímo v přístavu?",
                 "Ano. Počkám na vás u vjezdu do přístavu nebo na recepci a pomůžu se zavazadly, ať jdete rovnou z mola do vozidla."),
                ("Můžete přizpůsobit transfer mé lodi?",
                 "Ano. Při rezervaci mi pošlete čas charteru, check-inu nebo odjezdu a vyzvednutí naplánuji podle něj."),
                ("S jakým předstihem rezervovat?",
                 "Alespoň 2 hodiny předem, abych potvrdil vozidlo a čas vyzvednutí. Pro rychlejší jízdu zavolejte nebo napište na WhatsApp.")]
    elif typ == "city":
        heading = "Soukromý transfer, trasa %s" % rel
        tagline = "Taxi a soukromý transfer za pevnou cenu, trasa %s, ode dveří ke dveřím." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Potřebujete spolehlivý transfer na trase %s? Nabízím taxi a soukromý transfer za pevnou cenu, ode dveří ke dveřím, pohodlnou Škodou Superb. "
                     "Vyzvednu vás u vaší přesné adresy a odvezu přímo do cíle, bez nechtěných zastávek a bez spolucestujících. "
                     "Cena je pevná, &euro;%d za celé vozidlo, až 4 cestující, dohodnutá před odjezdem, mýtné a zavazadla v ceně. "
                     "Nabídka výše je pro tuto trasu vyplněná, takže rezervace zabere pár kliknutí." % (rel, p))
        else:
            intro = ("Hledáte taxi na trase %s bez taxametru a bez starostí? Je to soukromý transfer za pevnou cenu s jedním místním řidičem. "
                     "Vyzvednu vás u dveří a pohodlně odvezu do cíle, i se zavazadly, za paušální cenu &euro;%d za vozidlo až pro 4 cestující. "
                     "Pro páry a rodiny to často vyjde levněji než samostatné jízdenky na autobus či vlak, a vždy je to rychlejší a ode dveří ke dveřím. "
                     "Nabídka výše je pro tuto trasu už nastavená." % (rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za vozidlo až pro 4 cestující, dohodnutá předem. Mýtné, palivo a zavazadla v ceně, bez taxametru."),
                ("Ode dveří ke dveřím", "Vyzvednu vás u vaší přesné adresy a vysadím u dveří cíle. Žádná nádraží, žádné přestupy."),
                ("Jeden místní řidič", "Vše řešíte přímo se mnou, od rezervace po příjezd, telefonicky, přes WhatsApp nebo e-mail. Žádné call centrum."),
                ("Zastávky na přání", "Na delších trasách se rád zastavím na kávu, fotku nebo krátkou zajímavost po cestě.")]
        faqs = [("Kolik stojí taxi na trase %s?" % rel,
                 "Pevně &euro;%d za vozidlo až pro 4 cestující, jednosměrná, s mýtným, palivem a zavazadly. Zpáteční jízda je &euro;%d." % (p, rp)),
                ("Je transfer soukromý nebo sdílený?",
                 "Každý transfer je soukromý a ode dveří ke dveřím, ve Škodě Superb. Žádné sdílení vozidla a žádné zastávky navíc, pokud o ně nepožádáte."),
                ("Můžete zastavit po cestě?",
                 "Ano. Na delších trasách se rád zastavím na kávu, fotku nebo krátkou zajímavost. Stačí říct při rezervaci."),
                ("S jakým předstihem rezervovat?",
                 "Alespoň 2 hodiny předem, abych potvrdil vozidlo a čas vyzvednutí. Pro rychlou jízdu zavolejte nebo napište na WhatsApp.")]
    else:
        heading = "Soukromé taxi, trasa %s" % rel
        tagline = "Taxi a soukromý transfer za pevnou cenu, trasa %s, ode dveří ke dveřím." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Cestujete na trase %s? Provozuji taxi a soukromý transfer za pevnou cenu, s vyzvednutím u vašich dveří a odvozem přesně tam, kam potřebujete. "
                     "Cena je paušální, &euro;%d za celé vozidlo, až 4 cestující, bez taxametru a bez čekání na stanovišti. "
                     "Pohodlná Škoda Superb, místo na zavazadla a jeden místní řidič, kterého rezervujete přímo. "
                     "Nabídka výše je pro tuto trasu vyplněná." % (rel, p))
        else:
            intro = ("Potřebujete taxi na trase %s? Nabízím soukromý transfer ode dveří ke dveřím za pevnou cenu &euro;%d za celé vozidlo, až 4 cestující. "
                     "Přijedu na vaši adresu v dohodnutý čas, takže nikdy nečekáte u silnice, a pohodlně vás odvezu do cíle. "
                     "Bez taxametru, bez překvapení, jen jeden místní řidič od rezervace po příjezd. Nabídka výše je pro tuto trasu už nastavená." % (rel, p))
        whys = [("Pevná cena &euro;%d" % p, "Jedna cena za vozidlo až pro 4 cestující, dohodnutá před jízdou. Bez taxametru, bez překvapení."),
                ("Ode dveří ke dveřím", "Vyzvednutí u vaší adresy a odvoz ke dveřím cíle, i se zavazadly."),
                ("Bez stanoviště", "Rezervováno předem, takže nikdy nečekáte na projíždějící taxi. Přijedu za vámi."),
                ("Jeden místní řidič", "Vše řešíte přímo se mnou, od rezervace po příjezd, telefonicky, přes WhatsApp nebo e-mail.")]
        faqs = [("Kolik stojí taxi na trase %s?" % rel,
                 "Pevně &euro;%d za vozidlo až pro 4 cestující, jednosměrná, zavazadla v ceně. Zpáteční jízda je &euro;%d." % (p, rp)),
                ("Kde mě vyzvednete?",
                 "U vaší přesné adresy, ať jde o dům, hotel nebo apartmán. Pošlete adresu při rezervaci a potvrdím místo setkání."),
                ("S jakým předstihem rezervovat?",
                 "Alespoň 2 hodiny předem, abych potvrdil vozidlo a čas vyzvednutí. Pro rychlou jízdu zavolejte nebo napište na WhatsApp.")]

    if dd:
        faqs = [("Jak dlouhá je trasa a jak dlouho trvá jízda?",
                 "Jízda na trase %s je zhruba %d km a trvá přibližně %s při běžném provozu, o něco déle ve špičce letní sezony. Vyzvednutí plánuji tak, aby vás pomalejší úsek nikdy netlačil." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Dobrý den Antonio, rád bych si rezervoval transfer %s (€%d).\n"
        "Moje údaje:\n- Datum vyzvednutí: \n- Čas vyzvednutí: \n- Cestující: \n- Adresa vyzvednutí: \n- Moje jméno: " % (rel, p))
    trust_line = ("Okamžité potvrzení e-mailem &middot; Bez skrytých poplatků &middot; Sledování letu v ceně"
                  if typ in ("to_airport", "from_airport")
                  else "Okamžité potvrzení e-mailem &middot; Bez skrytých poplatků &middot; Pevná cena, bez taxametru")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: Škoda Superb TAXI Antonio na dalmatském pobřeží" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d za vozidlo &middot; až 4 cestující</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Rezervovat</a>
          <a class="btn btn-secondary" href="%s">Rezervovat přes WhatsApp</a>
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
      <span class="eyebrow center">Proč rezervovat tento transfer</span>
      <h2 class="section-title">Proč rezervovat taxi %s u Antonia?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Cena %s</h2>
      <p class="section-subtitle">Pevná cena za vozidlo, až 4 cestující, zavazadla v ceně. Stejná cena platí i v opačném směru.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Jednosměrná</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Zpáteční</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Záloha na potvrzení</div></div>
        <div class="route-fact"><div class="rf-value">Hotovost nebo karta</div><div class="rf-label">Doplatek v den jízdy</div></div>
      </div>
      <p class="hub-note">Záloha 20%% (minimálně &euro;20) potvrdí rezervaci, doplatek zaplatíte v den jízdy, hotově nebo kartou. Cestujete opačným směrem? Viz %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Recenze</span>
      <h2 class="section-title">Co říkají cestující</h2>
      <p class="section-subtitle">Skutečné recenze skutečných cestujících.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s: časté dotazy</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Rezervujte transfer %s</h2>
      <p class="section-subtitle">Pevná cena &euro;%d za vozidlo, až 4 cestující. Potvrďte v pár kliknutích.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Rezervovat</a>
        <a href="%s" class="btn btn-secondary">Rezervovat přes WhatsApp</a>
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

    desc = ("Taxi a soukromý transfer, trasa %s. Pevná cena &euro;%d za vozidlo, až 4 cestující, ode dveří ke dveřím. Rezervujte přímo u Antonia." % (rel, p))
    if len(desc) > 158:
        desc = "Taxi a soukromý transfer, trasa %s. Pevná cena &euro;%d za vozidlo, až 4. Rezervujte u Antonia." % (rel, p)
    keywords = "taxi %s, transfer %s, letištní transfer %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Soukromý taxi transfer",
         "name": "Taxi %s" % rel,
         "description": "Taxi a soukromý transfer za pevnou cenu, trasa %s, %d eur za vozidlo až pro 4 cestující, ode dveří ke dveřím." % (rel, p),
         "provider": PROVIDER, "areaServed": [cfr, cto],
         "url": "https://taxisibenik.hr/cs/%s/" % csslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Soukromá jednosměrná jízda, trasa %s, za vozidlo až pro 4 cestující. Zpáteční %d eur." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": csslug, "title": "Taxi %s | Pevná cena €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "cs")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated cs:", sum(made.values()), made, "| skipped:", skipped)
