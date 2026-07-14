# -*- coding: utf-8 -*-
"""Generate the DUTCH variant of every route page. Mirrors gen_routes.py.
Place names kept nominative via "traject <A> - <B>". Run after gen_routes.py."""
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
NL_NAME = {'Split Airport':'Luchthaven Split','Zadar Airport':'Luchthaven Zadar',
           'Zagreb Airport':'Luchthaven Zagreb','Dubrovnik Airport':'Luchthaven Dubrovnik'}
nl = lambda n: NL_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'luchthaven-split','zadar-airport':'luchthaven-zadar',
                'zagreb-airport':'luchthaven-zagreb','dubrovnik-airport':'luchthaven-dubrovnik'}
def nl_slug(en_slug):
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
    return "/nl/boeken/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    nfr, nto = nl(frm), nl(to)
    rel = "%s - %s" % (nfr, nto)
    nlslug = nl_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/nl/%s/">%s - %s</a>' % (nl_slug(rev), nto, nfr)) if rev else ("%s - %s" % (nto, nfr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Vaste prijs, enkele reis</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Afstand</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Reistijd</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Retour</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Vaste prijs, enkele reis</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Retour</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Tot 4</div><div class="rf-label">Passagiers</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Privé, van deur tot deur</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Uw privétaxi en transfer, traject %s" % rel
        tagline = "Taxi en privétransfer tegen vaste prijs, traject %s, rechtstreeks naar de vertrekhal." % rel
        intro = ("Vertrekt u vanaf de luchthaven %s? Voor het traject %s bied ik een privétaxi en transfer tegen vaste prijs. "
                 "Ik ben Antonio, een lokale chauffeur uit Šibenik: ik haal u op aan uw adres en breng u rechtstreeks naar de vertrekhal in een comfortabele Škoda Superb. "
                 "De prijs is vast, &euro;%d voor het hele voertuig, tot 4 passagiers, vooraf afgesproken, zonder taximeter en zonder verrassingen. "
                 "Ik plan het ophalen op basis van uw vluchttijd, zodat u op tijd bent om in te checken. "
                 "Het offerteformulier hierboven is al ingevuld voor dit traject, dus u ziet de prijs en boekt in een paar klikken." % (city, rel, p))
        whys = [("Vaste prijs &euro;%d" % p, "Eén prijs voor het hele voertuig, tot 4 passagiers, vooraf afgesproken. Tol, brandstof en bagage inbegrepen, zonder taximeter."),
                ("Afgestemd op uw vlucht", "Geef me uw vertrektijd door en ik reken terug, zodat u op tijd bij de terminal bent om in te checken."),
                ("Van de deur tot de terminal", "Ophalen aan uw adres en afzetten recht voor de ingang van de vertrekhal."),
                ("Op elk uur", "Vroege ochtend- of late avondvluchten zijn geen probleem. Ik rijd dag en nacht tegen een vooraf afgesproken prijs.")]
        faqs = [("Hoeveel kost een taxi op het traject %s?" % rel,
                 "Vast &euro;%d per voertuig, enkele reis, tot 4 passagiers. De prijs is per voertuig, niet per persoon, en omvat tol, brandstof en bagage. Een retour kost &euro;%d." % (p, rp)),
                ("Hoe laat moet ik vertrekken voor mijn vlucht?",
                 "In de regel ongeveer 3 uur voor een internationale vlucht en 2 uur voor een binnenlandse. Geef me uw vluchttijd door en ik bevestig het exacte ophalen."),
                ("Zet u me af tot aan de vertrekhal?",
                 "Ja. Ik breng u rechtstreeks naar de vertrekhal en help met de bagage. Geen wandeling vanaf de parkeerplaats, geen shuttlebus."),
                ("Hoe ver van tevoren reserveren?",
                 "Minstens 2 uur van tevoren, zodat ik het voertuig en het ophalen kan bevestigen, en eerder voor ochtendvluchten en in het hoogseizoen. Voor een snelle rit belt u of schrijft u me op WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Uw ophaalservice op de luchthaven en transfer, traject %s" % rel
        tagline = "Privé ophaalservice op de luchthaven en transfer tegen vaste prijs, traject %s, met vluchtmonitoring." % rel
        intro = ("Net geland op de luchthaven %s? Een privétransfer voor het traject %s neemt de stress van de aankomst weg. "
                 "Ik ontvang u in de aankomsthal met een naambordje, help met de bagage en breng u rechtstreeks naar uw bestemming in een comfortabele Škoda Superb, "
                 "tegen een vaste prijs van &euro;%d voor het hele voertuig, tot 4 passagiers. Ik volg uw vlucht in real time, dus ik ben er of u nu vroeg of laat landt. "
                 "Geen wachtrij voor de taxi, geen gedeelde shuttle en geen toeslagen. Het formulier hierboven is al ingevuld voor dit traject." % (city, rel, p))
        whys = [("Ontvangst met naambordje", "Ik wacht in de aankomsthal met een naambordje en help met de tassen, zodat u meteen naar het voertuig gaat."),
                ("Vluchtmonitoring", "Ik volg uw vlucht in real time en pas me aan een vroege landing of vertraging aan, met gratis wachttijd."),
                ("Vaste prijs &euro;%d" % p, "Eén prijs voor het hele voertuig, tot 4 passagiers, vooraf afgesproken. Tol, brandstof en bagage inbegrepen, zonder taximeter."),
                ("Rechtstreeks tot uw deur", "Geen wachtrij en geen overstappen. Ik breng u rechtstreeks naar uw adres.")]
        faqs = [("Waar ontvangt u me?",
                 "In de aankomsthal, meteen na het ophalen van de bagage, met een naambordje met uw naam. Ik help met de bagage en begeleid u naar het voertuig."),
                ("Wat als mijn vlucht vertraging heeft?",
                 "Geen probleem. Ik volg uw vlucht in real time en pas het ophalen aan de werkelijke landing aan, zonder toeslag voor het wachten."),
                ("Hoeveel kost de transfer op het traject %s?" % rel,
                 "Vast &euro;%d per voertuig tot 4 passagiers, enkele reis, tol en bagage inbegrepen. Een retour kost &euro;%d." % (p, rp)),
                ("Hoe ver van tevoren reserveren?",
                 "Minstens 2 uur van tevoren, zodat ik rond uw vlucht kan plannen. Voor een ophaalservice dezelfde dag na een plotselinge wijziging belt u of schrijft u me op WhatsApp.")]
    elif typ == "marina":
        heading = "Privé marinatransfer van %s naar %s" % (nfr, nto)
        tagline = "Taxi en privétransfer tegen vaste prijs, van %s naar %s. &euro;%d per voertuig, tot 4 passagiers, afgestemd op uw boot." % (nfr, nto, p)
        intro = ("Reist u tussen %s en %s? Ik rijd een privétaxi en transfer tegen vaste prijs voor marinagasten, afgestemd op uw boot en uw reisplannen. "
                 "Ik haal u op met ruimte genoeg voor uw bagage en breng u comfortabel de hele weg in een Škoda Superb, voor een vast bedrag van &euro;%d voor het voertuig, tot 4 passagiers, vooraf afgesproken. "
                 "Of u nu aan boord van uw jacht gaat of verder reist nadat u van boord bent gestapt, er is geen taximeter en geen wachten op een standplaats, gewoon één lokale chauffeur die u rechtstreeks boekt. "
                 "Dit is een privétransfer over langere afstand, geen korte lokale rit, en de offerte hierboven is al klaargezet voor dit traject, dus reserveren kost maar een paar klikken." % (nfr, nto, p))
        whys = [("Vaste prijs &euro;%d" % p, "Eén prijs per voertuig, tot 4 passagiers, vooraf afgesproken. Tol, brandstof en bagage inbegrepen, zonder taximeter."),
                ("Afgestemd op uw boot", "Geef me uw charter-, check-in- of vertrektijd door en ik plan het ophalen daaromheen, zodat een trager stukje u nooit onder druk zet."),
                ("Ruimte voor uw bagage", "Koffers, proviand en boottassen passen allemaal in een comfortabele Škoda Superb, met een handje bij het in- en uitladen."),
                ("Eén lokale chauffeur", "U regelt alles rechtstreeks met mij, van reservering tot aankomst, telefonisch, via WhatsApp of e-mail. Geen callcenter.")]
        faqs = [("Hoeveel kost een transfer van %s naar %s?" % (nfr, nto),
                 "Vast &euro;%d per voertuig tot 4 passagiers, enkele reis, met tol, brandstof en bagage inbegrepen. Een retour kost &euro;%d." % (p, rp)),
                ("Kunt u me recht bij de marina ophalen?",
                 "Ja. Ik ontmoet u bij de ingang of receptie van de marina en help met uw bagage, zodat u recht van de steiger naar het voertuig gaat."),
                ("Kunt u de transfer op mijn boot afstemmen?",
                 "Ja. Stuur me uw charter-, check-in- of vertrektijd bij de reservering en ik plan het ophalen daaromheen."),
                ("Hoe ver van tevoren reserveren?",
                 "Minstens 2 uur van tevoren, zodat ik het voertuig en de ophaaltijd kan bevestigen. Voor een snellere rit belt u of schrijft u me rechtstreeks op WhatsApp.")]
    elif typ == "city":
        heading = "Privétransfer, traject %s" % rel
        tagline = "Taxi en privétransfer tegen vaste prijs, traject %s, van deur tot deur." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Zoekt u een betrouwbare transfer op het traject %s? Ik bied een privétaxi en transfer tegen vaste prijs, van deur tot deur, in een comfortabele Škoda Superb. "
                     "Ik haal u op aan uw exacte adres en breng u rechtstreeks naar uw bestemming, zonder ongewenste stops en zonder medepassagiers. "
                     "De prijs is vast, &euro;%d voor het hele voertuig, tot 4 passagiers, vooraf afgesproken, tol en bagage inbegrepen. "
                     "De offerte hierboven is ingevuld voor dit traject, dus reserveren kost maar een paar klikken." % (rel, p))
        else:
            intro = ("Zoekt u een taxi op het traject %s zonder taximeter of gedoe? Dit is een privétransfer tegen vaste prijs met één lokale chauffeur. "
                     "Ik haal u op aan de deur en breng u comfortabel naar uw bestemming, inclusief bagage, tegen een vast tarief van &euro;%d per voertuig tot 4 passagiers. "
                     "Voor stellen en gezinnen is het vaak goedkoper dan aparte bus- of treinkaartjes, en het is altijd sneller en van deur tot deur. "
                     "De offerte hierboven is al klaargezet voor dit traject." % (rel, p))
        whys = [("Vaste prijs &euro;%d" % p, "Eén prijs per voertuig tot 4 passagiers, vooraf afgesproken. Tol, brandstof en bagage inbegrepen, zonder taximeter."),
                ("Van deur tot deur", "Ik haal u op aan uw exacte adres en zet u af voor de deur van de bestemming. Geen stations, geen overstappen."),
                ("Eén lokale chauffeur", "U regelt alles rechtstreeks met mij, van reservering tot aankomst, telefonisch, via WhatsApp of e-mail. Geen callcenter."),
                ("Stops op verzoek", "Op langere trajecten stop ik graag voor een koffie, een foto of een korte bezienswaardigheid onderweg.")]
        faqs = [("Hoeveel kost een taxi op het traject %s?" % rel,
                 "Vast &euro;%d per voertuig tot 4 passagiers, enkele reis, met tol, brandstof en bagage. Een retour kost &euro;%d." % (p, rp)),
                ("Is de transfer privé of gedeeld?",
                 "Elke transfer is privé en van deur tot deur, in een Škoda Superb. Geen delen van het voertuig en geen extra stops, tenzij u erom vraagt."),
                ("Kunt u onderweg stoppen?",
                 "Ja. Op langere trajecten stop ik graag voor een koffie, een foto of een korte bezienswaardigheid. Geef het gewoon door bij de reservering."),
                ("Hoe ver van tevoren reserveren?",
                 "Minstens 2 uur van tevoren, zodat ik het voertuig en de ophaaltijd kan bevestigen. Voor een snelle rit belt u of schrijft u me op WhatsApp.")]
    else:
        heading = "Privétaxi, traject %s" % rel
        tagline = "Taxi en privétransfer tegen vaste prijs, traject %s, van deur tot deur." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Reist u op het traject %s? Ik rijd een privétaxi en transfer tegen vaste prijs, met ophalen aan uw deur en afzetten precies waar u moet zijn. "
                     "De prijs is een vast bedrag, &euro;%d voor het hele voertuig, tot 4 passagiers, zonder taximeter en zonder wachten op een standplaats. "
                     "Een comfortabele Škoda Superb, ruimte voor uw bagage en één lokale chauffeur die u rechtstreeks boekt. "
                     "De offerte hierboven is ingevuld voor dit traject." % (rel, p))
        else:
            intro = ("Heeft u een taxi nodig op het traject %s? Ik bied een privétransfer van deur tot deur tegen een vaste prijs van &euro;%d voor het hele voertuig, tot 4 passagiers. "
                     "Ik kom op het afgesproken tijdstip naar uw adres, dus u wacht nooit langs de weg, en ik breng u comfortabel naar uw bestemming. "
                     "Zonder taximeter, zonder verrassingen, gewoon één lokale chauffeur van reservering tot aankomst. De offerte hierboven is al klaargezet voor dit traject." % (rel, p))
        whys = [("Vaste prijs &euro;%d" % p, "Eén prijs per voertuig tot 4 passagiers, vooraf afgesproken. Zonder taximeter, zonder verrassingen."),
                ("Van deur tot deur", "Ophalen aan uw adres en afzetten voor de deur van de bestemming, inclusief bagage."),
                ("Geen standplaats nodig", "Vooraf geboekt, dus u wacht nooit op een passerende taxi. Ik kom naar u toe."),
                ("Eén lokale chauffeur", "U regelt alles rechtstreeks met mij, van reservering tot aankomst, telefonisch, via WhatsApp of e-mail.")]
        faqs = [("Hoeveel kost een taxi op het traject %s?" % rel,
                 "Vast &euro;%d per voertuig tot 4 passagiers, enkele reis, bagage inbegrepen. Een retour kost &euro;%d." % (p, rp)),
                ("Waar haalt u me op?",
                 "Aan uw exacte adres, of het nu een huis, hotel of appartement is. Stuur het adres bij de reservering en ik bevestig de ontmoetingsplek."),
                ("Hoe ver van tevoren reserveren?",
                 "Minstens 2 uur van tevoren, zodat ik het voertuig en de ophaaltijd kan bevestigen. Voor een snelle rit belt u of schrijft u me op WhatsApp.")]

    if dd:
        faqs = [("Hoe lang is het traject en hoe lang duurt de rit?",
                 "De rit op het traject %s is ongeveer %d km en duurt ongeveer %s bij normaal verkeer, iets langer tijdens de zomerdrukte. Ik plan het ophalen zo dat een trager stukje u nooit onder druk zet." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Hallo Antonio, ik wil graag de transfer %s (€%d) boeken.\n"
        "Mijn gegevens:\n- Ophaaldatum: \n- Ophaaltijd: \n- Passagiers: \n- Ophaaladres: \n- Mijn naam: " % (rel, p))
    trust_line = ("Directe bevestiging per e-mail &middot; Geen verborgen kosten &middot; Vluchtmonitoring inbegrepen"
                  if typ in ("to_airport", "from_airport")
                  else "Directe bevestiging per e-mail &middot; Geen verborgen kosten &middot; Vaste prijs, geen taximeter")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: de Škoda Superb van TAXI Antonio aan de Dalmatische kust" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d per voertuig &middot; tot 4 passagiers</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Reserveren</a>
          <a class="btn btn-secondary" href="%s">Reserveren via WhatsApp</a>
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
      <span class="eyebrow center">Waarom deze transfer boeken</span>
      <h2 class="section-title">Waarom uw taxi %s bij Antonio boeken?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Prijs %s</h2>
      <p class="section-subtitle">Vaste prijs per voertuig, tot 4 passagiers, bagage inbegrepen. Dezelfde prijs geldt in de omgekeerde richting.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Enkele reis</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Retour</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Aanbetaling ter bevestiging</div></div>
        <div class="route-fact"><div class="rf-value">Contant of kaart</div><div class="rf-label">Rest op de dag zelf</div></div>
      </div>
      <p class="hub-note">Een aanbetaling van 20%% (minimaal &euro;20) bevestigt uw reservering, de rest betaalt u op de dag zelf, contant of met kaart. Reist u de andere kant op? Zie %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Beoordelingen</span>
      <h2 class="section-title">Wat passagiers zeggen</h2>
      <p class="section-subtitle">Echte beoordelingen van echte passagiers.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s: veelgestelde vragen</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Reserveer uw transfer %s</h2>
      <p class="section-subtitle">Vaste prijs &euro;%d per voertuig, tot 4 passagiers. Bevestig in een paar klikken.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Reserveren</a>
        <a href="%s" class="btn btn-secondary">Reserveren via WhatsApp</a>
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

    desc = ("Taxi en privétransfer, traject %s. Vaste prijs &euro;%d per voertuig, tot 4 passagiers, van deur tot deur. Boek rechtstreeks bij Antonio." % (rel, p))
    if len(desc) > 160:
        desc = "Taxi en privétransfer, traject %s. Vaste prijs &euro;%d per voertuig, tot 4. Boek bij Antonio." % (rel, p)
    keywords = "taxi %s, transfer %s, luchthaventransfer %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Privé taxitransfer",
         "name": "Taxi %s" % rel,
         "description": "Taxi en privétransfer tegen vaste prijs, traject %s, %d euro per voertuig tot 4 passagiers, van deur tot deur." % (rel, p),
         "provider": PROVIDER, "areaServed": [nfr, nto],
         "url": "https://taxisibenik.hr/nl/%s/" % nlslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Privérit enkele reis, traject %s, per voertuig tot 4 passagiers. Retour %d euro." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": nlslug, "title": "Taxi %s | Vaste prijs €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "nl")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated nl:", sum(made.values()), made, "| skipped:", skipped)
