# -*- coding: utf-8 -*-
"""Generate the ITALIAN variant of every route page.

Mirrors scripts/gen_routes.py but writes src/pages/<en-slug>/it/{meta.json,
content.html} with Italian copy (informal "tu") and an Italian slug. Place names
are kept in the nominative via "tratta <A> - <B>" phrasing. Run after
gen_routes.py, before build.py.
"""
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

IT_NAME = {'Split Airport':'Aeroporto di Split','Zadar Airport':'Aeroporto di Zadar',
           'Zagreb Airport':'Aeroporto di Zagreb','Dubrovnik Airport':'Aeroporto di Dubrovnik'}
ita = lambda n: IT_NAME.get(n, n)

AIRPORT_SLUG = {'split-airport':'aeroporto-split','zadar-airport':'aeroporto-zadar',
                'zagreb-airport':'aeroporto-zagreb','dubrovnik-airport':'aeroporto-dubrovnik'}
def it_slug(en_slug):
    s = en_slug.replace('-to-', '-')
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
    return "/it/prenota/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    ifr, ito = ita(frm), ita(to)
    rel = "%s - %s" % (ifr, ito)
    itslug = it_slug(slug)

    rev = slug_of.get((to, frm))
    revlink = ('<a href="/it/%s/">%s - %s</a>' % (it_slug(rev), ito, ifr)) if rev else ("%s - %s" % (ito, ifr))
    book = book_link(frm, to, p)

    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fisso, solo andata</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Distanza</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Durata</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Andata e ritorno</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fisso, solo andata</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Andata e ritorno</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Fino a 4</div><div class="rf-label">Passeggeri</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Privato, porta a porta</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Il tuo taxi privato e transfer, tratta %s" % rel
        tagline = "Taxi e transfer privato a prezzo fisso, tratta %s, direttamente alle partenze." % rel
        intro = ("Voli dall'aeroporto di %s? Per la tratta %s offro un taxi privato e un transfer a prezzo fisso. "
                 "Sono Antonio, un autista locale di Šibenik: ti prendo al tuo indirizzo e ti porto direttamente al terminal partenze "
                 "in una comoda Škoda Superb. Il prezzo è fisso, &euro;%d per l'intero veicolo, fino a 4 passeggeri, concordato prima del viaggio, "
                 "senza tassametro e senza sorprese. Pianifico il ritiro in base all'orario del tuo volo, così arrivi con tempo per il check-in. "
                 "Il modulo del preventivo qui sopra è già compilato per questa tratta, così vedi il prezzo e prenoti in pochi tap." % (city, rel, p))
        whys = [("Prezzo fisso &euro;%d" % p, "Un prezzo per l'intero veicolo, fino a 4 passeggeri, concordato in anticipo. Pedaggi, carburante e bagagli inclusi, senza tassametro."),
                ("Su misura per il tuo volo", "Dimmi l'orario di partenza e calcolo a ritroso, così arrivi al terminal con il tempo per il check-in."),
                ("Dalla porta al terminal", "Ritiro al tuo indirizzo e arrivo direttamente all'ingresso del terminal partenze."),
                ("A qualsiasi ora", "Voli all'alba o a tarda notte non sono un problema. Guido 24 ore su 24 a un prezzo concordato in anticipo.")]
        faqs = [("Quanto costa un taxi sulla tratta %s?" % rel,
                 "Fisso &euro;%d per veicolo, solo andata, fino a 4 passeggeri. Il prezzo è per veicolo, non per persona, e include pedaggi, carburante e bagagli. Andata e ritorno &euro;%d." % (p, rp)),
                ("A che ora devo partire per il volo?",
                 "Di norma circa 3 ore prima di un volo internazionale e 2 ore prima di uno nazionale. Dimmi l'orario del volo e confermo il ritiro esatto."),
                ("Mi porti fino al terminal partenze?",
                 "Sì. Ti porto direttamente al terminal partenze e ti aiuto con i bagagli. Nessuna camminata dal parcheggio e nessuna navetta."),
                ("Con quanto anticipo devo prenotare?",
                 "Almeno 2 ore prima, così confermo veicolo e ritiro, e prima per i voli mattutini e in alta stagione. Per una corsa last minute chiamami o scrivimi su WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Il tuo ritiro in aeroporto e transfer, tratta %s" % rel
        tagline = "Ritiro privato in aeroporto e transfer a prezzo fisso, tratta %s, con monitoraggio del volo." % rel
        intro = ("Appena atterrato all'aeroporto di %s? Un transfer privato per la tratta %s toglie lo stress dall'arrivo. "
                 "Ti accolgo nell'area arrivi con un cartello con il tuo nome, ti aiuto con i bagagli e ti porto direttamente a destinazione in una comoda Škoda Superb, "
                 "al prezzo fisso di &euro;%d per l'intero veicolo, fino a 4 passeggeri. Monitoro il tuo volo in tempo reale, così sono lì che tu atterri in anticipo o in ritardo. "
                 "Nessuna fila per il taxi, nessuna navetta condivisa e nessun sovrapprezzo. Il modulo qui sopra è già compilato per questa tratta." % (city, rel, p))
        whys = [("Accoglienza con cartello", "Ti aspetto nell'area arrivi con un cartello con il tuo nome e ti aiuto con le valigie, così vai dritto al veicolo."),
                ("Monitoraggio del volo", "Monitoro il tuo volo in tempo reale e mi adatto ad atterraggi anticipati o ritardi, con attesa gratuita."),
                ("Prezzo fisso &euro;%d" % p, "Un prezzo per l'intero veicolo, fino a 4 passeggeri, concordato in anticipo. Pedaggi, carburante e bagagli inclusi, senza tassametro."),
                ("Dritto a casa tua", "Nessuna fila e nessun cambio. Ti porto direttamente al tuo indirizzo.")]
        faqs = [("Dove mi accogli?",
                 "Nell'area arrivi, subito dopo il ritiro bagagli, con un cartello con il tuo nome. Ti aiuto con i bagagli e ti accompagno al veicolo."),
                ("E se il mio volo è in ritardo?",
                 "Nessun problema. Monitoro il tuo volo in tempo reale e adatto il ritiro all'atterraggio effettivo, senza sovrapprezzo per l'attesa."),
                ("Quanto costa il transfer sulla tratta %s?" % rel,
                 "Fisso &euro;%d per veicolo fino a 4 passeggeri, solo andata, pedaggi e bagagli inclusi. Andata e ritorno &euro;%d." % (p, rp)),
                ("Con quanto anticipo devo prenotare?",
                 "Almeno 2 ore prima, così pianifico in base al tuo volo. Per un ritiro in giornata dopo un cambio improvviso, chiamami o scrivimi su WhatsApp.")]
    elif typ == "marina":
        heading = "Transfer privato da marina, da %s a %s" % (ifr, ito)
        tagline = "Taxi e transfer privato a prezzo fisso, da %s a %s. &euro;%d per veicolo, fino a 4 passeggeri, con orari studiati sulla Sua barca." % (ifr, ito, p)
        intro = ("Deve spostarsi tra %s e %s? Offro un taxi e transfer privato a prezzo fisso per gli ospiti delle marine, con orari studiati sulla Sua barca e sui Suoi programmi di viaggio. "
                 "La prendo con ampio spazio per i bagagli e La accompagno comodamente per tutto il tragitto in una Škoda Superb, alla tariffa fissa di &euro;%d per l'intero veicolo, fino a 4 passeggeri, concordata prima del viaggio. "
                 "Che stia raggiungendo il Suo yacht o proseguendo dopo essere sceso a terra, non c'è tassametro e nessuna attesa al posteggio, solo un autista locale che prenota direttamente. "
                 "È un transfer privato a lunga distanza, non una breve corsa locale, e il preventivo qui sopra è già impostato per questa tratta, così la prenotazione richiede pochi tap." % (ifr, ito, p))
        whys = [("Prezzo fisso &euro;%d" % p, "Un prezzo per l'intero veicolo, fino a 4 passeggeri, concordato in anticipo. Pedaggi, carburante e bagagli inclusi, senza tassametro."),
                ("Su misura per la Sua barca", "Mi comunichi l'orario del charter, del check-in o della partenza e pianifico il ritiro di conseguenza, così un tratto lento non Le mette mai fretta."),
                ("Spazio per i Suoi bagagli", "Valigie, provviste e borse da barca entrano tutte in una comoda Škoda Superb, con una mano nel carico e scarico."),
                ("Un autista locale", "Tratta direttamente con me, dalla prenotazione all'arrivo, per telefono, WhatsApp o email. Nessun call center.")]
        faqs = [("Quanto costa un transfer da %s a %s?" % (ifr, ito),
                 "Fisso &euro;%d per veicolo, fino a 4 passeggeri, solo andata, con pedaggi, carburante e bagagli inclusi. Andata e ritorno &euro;%d." % (p, rp)),
                ("Può venirmi a prendere direttamente alla marina?",
                 "Sì. La incontro all'ingresso della marina o alla reception e L'aiuto con i bagagli, così passa direttamente dal pontile al veicolo."),
                ("Può adattare il transfer agli orari della mia barca?",
                 "Sì. Mi invii l'orario del charter, del check-in o della partenza al momento della prenotazione e pianifico il ritiro di conseguenza."),
                ("Con quanto anticipo devo prenotare?",
                 "Almeno 2 ore prima, così confermo il veicolo e l'orario di ritiro. Per una corsa prima, mi chiami o mi scriva su WhatsApp.")]
    elif typ == "city":
        heading = "Transfer privato, tratta %s" % rel
        tagline = "Taxi e transfer privato a prezzo fisso, tratta %s, porta a porta." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Ti serve un transfer affidabile sulla tratta %s? Offro un taxi e un transfer privato a prezzo fisso, porta a porta, in una comoda Škoda Superb. "
                     "Ti prendo al tuo indirizzo esatto e ti porto direttamente a destinazione, senza soste indesiderate e senza altri passeggeri. "
                     "Il prezzo è fisso, &euro;%d per l'intero veicolo, fino a 4 passeggeri, concordato prima di partire, pedaggi e bagagli inclusi. "
                     "Il preventivo qui sopra è compilato per questa tratta, così prenotare richiede pochi tap." % (rel, p))
        else:
            intro = ("Cerchi un taxi sulla tratta %s senza tassametro e senza pensieri? È un transfer privato a prezzo fisso con un autista locale. "
                     "Ti prendo alla porta e ti porto comodamente a destinazione, bagagli inclusi, alla tariffa fissa di &euro;%d per veicolo fino a 4 passeggeri. "
                     "Per coppie e famiglie spesso conviene più dei biglietti separati di bus o treno, ed è sempre più veloce e porta a porta. "
                     "Il preventivo qui sopra è già impostato per questa tratta." % (rel, p))
        whys = [("Prezzo fisso &euro;%d" % p, "Un prezzo per veicolo fino a 4 passeggeri, concordato in anticipo. Pedaggi, carburante e bagagli inclusi, senza tassametro."),
                ("Porta a porta", "Ti prendo al tuo indirizzo esatto e ti lascio davanti alla porta di destinazione. Nessuna stazione, nessun cambio."),
                ("Un autista locale", "Tratti direttamente con me, dalla prenotazione all'arrivo, per telefono, WhatsApp o email. Nessun call center."),
                ("Soste su richiesta", "Sulle tratte più lunghe mi fermo volentieri per un caffè, una foto o una breve visita lungo il percorso.")]
        faqs = [("Quanto costa un taxi sulla tratta %s?" % rel,
                 "Fisso &euro;%d per veicolo fino a 4 passeggeri, solo andata, con pedaggi, carburante e bagagli. Andata e ritorno &euro;%d." % (p, rp)),
                ("Il transfer è privato o condiviso?",
                 "Ogni transfer è privato e porta a porta, in una Škoda Superb. Nessun veicolo condiviso e nessuna sosta extra, a meno che tu non la chieda."),
                ("Puoi fermarti lungo il percorso?",
                 "Sì. Sulle tratte più lunghe mi fermo volentieri per un caffè, una foto o una breve visita. Basta dirlo alla prenotazione."),
                ("Con quanto anticipo devo prenotare?",
                 "Almeno 2 ore prima, così confermo veicolo e orario di ritiro. Per una corsa last minute chiamami o scrivimi su WhatsApp.")]
    else:  # local
        heading = "Taxi privato, tratta %s" % rel
        tagline = "Taxi e transfer privato a prezzo fisso, tratta %s, porta a porta." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Viaggi sulla tratta %s? Offro un taxi e un transfer privato a prezzo fisso, con ritiro alla tua porta e arrivo esattamente dove ti serve. "
                     "Il prezzo è forfettario, &euro;%d per l'intero veicolo, fino a 4 passeggeri, senza tassametro e senza attese al posteggio. "
                     "Una comoda Škoda Superb, spazio per i bagagli e un autista locale che prenoti direttamente. "
                     "Il preventivo qui sopra è compilato per questa tratta." % (rel, p))
        else:
            intro = ("Ti serve un taxi sulla tratta %s? Offro un transfer privato porta a porta a prezzo fisso di &euro;%d per l'intero veicolo, fino a 4 passeggeri. "
                     "Arrivo al tuo indirizzo all'ora concordata, così non aspetti mai sul ciglio della strada, e ti porto comodamente a destinazione. "
                     "Senza tassametro, senza sorprese, solo un autista locale dalla prenotazione all'arrivo. Il preventivo qui sopra è già impostato per questa tratta." % (rel, p))
        whys = [("Prezzo fisso &euro;%d" % p, "Un prezzo per veicolo fino a 4 passeggeri, concordato prima del viaggio. Senza tassametro, senza sorprese."),
                ("Porta a porta", "Ritiro al tuo indirizzo e arrivo davanti alla porta di destinazione, bagagli inclusi."),
                ("Nessun posteggio necessario", "Prenotato in anticipo, così non aspetti mai un taxi di passaggio. Vengo io da te."),
                ("Un autista locale", "Tratti direttamente con me, dalla prenotazione all'arrivo, per telefono, WhatsApp o email.")]
        faqs = [("Quanto costa un taxi sulla tratta %s?" % rel,
                 "Fisso &euro;%d per veicolo fino a 4 passeggeri, solo andata, bagagli inclusi. Andata e ritorno &euro;%d." % (p, rp)),
                ("Dove effettui il ritiro?",
                 "Al tuo indirizzo esatto, che sia casa, hotel o appartamento. Invia l'indirizzo alla prenotazione e confermo il punto d'incontro."),
                ("Con quanto anticipo devo prenotare?",
                 "Almeno 2 ore prima, così confermo veicolo e orario di ritiro. Per una corsa last minute chiamami o scrivimi su WhatsApp.")]

    if dd:
        faqs = [("Quanto è lunga la tratta e quanto dura il viaggio?",
                 "Il viaggio sulla tratta %s è di circa %d km e dura all'incirca %s con traffico normale, un po' di più nei periodi di punta estivi. Pianifico il ritiro in modo che un tratto lento non ti metta mai fretta." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join(
        '        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t)
        for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Ciao Antonio, vorrei prenotare il transfer %s (€%d).\n"
        "I miei dati:\n- Data di ritiro: \n- Ora di ritiro: \n- Passeggeri: \n- Indirizzo di ritiro: \n- Il mio nome: " % (rel, p))
    trust_line = ("Conferma immediata via email &middot; Nessun costo nascosto &middot; Monitoraggio del volo incluso"
                  if typ in ("to_airport", "from_airport")
                  else "Conferma immediata via email &middot; Nessun costo nascosto &middot; Prezzo fisso, senza tassametro")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: la Škoda Superb di TAXI Antonio sulla costa dalmata" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d per veicolo &middot; fino a 4 passeggeri</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Prenota ora</a>
          <a class="btn btn-secondary" href="%s">Prenota su WhatsApp</a>
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
      <span class="eyebrow center">Perché prenotare questo transfer</span>
      <h2 class="section-title">Perché prenotare il tuo taxi %s con Antonio?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Prezzo %s</h2>
      <p class="section-subtitle">Prezzo fisso per veicolo, fino a 4 passeggeri, bagagli inclusi. Lo stesso prezzo vale nella direzione opposta.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Solo andata</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Andata e ritorno</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Acconto per confermare</div></div>
        <div class="route-fact"><div class="rf-value">Contanti o carta</div><div class="rf-label">Saldo il giorno stesso</div></div>
      </div>
      <p class="hub-note">Un acconto del 20%% (minimo &euro;20) conferma la prenotazione, il saldo si paga il giorno stesso, in contanti o con carta. Viaggi nella direzione opposta? Vedi %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Recensioni</span>
      <h2 class="section-title">Cosa dicono i passeggeri</h2>
      <p class="section-subtitle">Recensioni vere di passeggeri veri.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s: domande frequenti</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Prenota il tuo transfer %s</h2>
      <p class="section-subtitle">Prezzo fisso &euro;%d per veicolo, fino a 4 passeggeri. Conferma in pochi tap.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Prenota ora</a>
        <a href="%s" class="btn btn-secondary">Prenota su WhatsApp</a>
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

    desc = ("Taxi e transfer privato, tratta %s. Prezzo fisso &euro;%d per veicolo, fino a 4 passeggeri, porta a porta. Prenota direttamente con Antonio." % (rel, p))
    if len(desc) > 155:
        desc = "Taxi e transfer privato, tratta %s. Prezzo fisso &euro;%d per veicolo, fino a 4. Prenota con Antonio." % (rel, p)
    keywords = "taxi %s, transfer %s, transfer aeroporto %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service",
         "serviceType": "Transfer taxi privato",
         "name": "Taxi %s" % rel,
         "description": "Taxi e transfer privato a prezzo fisso, tratta %s, %d euro per veicolo fino a 4 passeggeri, porta a porta." % (rel, p),
         "provider": PROVIDER,
         "areaServed": [ifr, ito],
         "url": "https://taxisibenik.hr/it/%s/" % itslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Corsa privata di sola andata, tratta %s, per veicolo fino a 4 passeggeri. Andata e ritorno %d euro." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": itslug, "title": "Taxi %s | Prezzo fisso €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}

    outdir = os.path.join(PAGES, slug, "it")
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
print("generated it:", sum(made.values()), made)
print("skipped (no matrix price):", skipped_noprice)
