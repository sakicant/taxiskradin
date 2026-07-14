# -*- coding: utf-8 -*-
"""Generate the GERMAN variant of every route page.

Mirrors scripts/gen_routes.py but writes src/pages/<en-slug>/de/{meta.json,
content.html} with German copy and a German slug. Place names are kept in the
nominative via "Strecke <A> - <B>" phrasing so the copy stays correct across
all routes without a declension table. Run after gen_routes.py, before build.py.
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

GER_NAME = {'Split Airport':'Flughafen Split','Zadar Airport':'Flughafen Zadar',
            'Zagreb Airport':'Flughafen Zagreb','Dubrovnik Airport':'Flughafen Dubrovnik'}
ger = lambda n: GER_NAME.get(n, n)

AIRPORT_SLUG = {'split-airport':'flughafen-split','zadar-airport':'flughafen-zadar',
                'zagreb-airport':'flughafen-zagreb','dubrovnik-airport':'flughafen-dubrovnik'}
def de_slug(en_slug):
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
    return "/de/buchen/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    gf, gt = ger(frm), ger(to)
    rel = "%s - %s" % (gf, gt)
    deslug = de_slug(slug)

    rev = slug_of.get((to, frm))
    revlink = ('<a href="/de/%s/">%s - %s</a>' % (de_slug(rev), gt, gf)) if rev else ("%s - %s" % (gt, gf))
    book = book_link(frm, to, p)

    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Festpreis, einfach</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Entfernung</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Fahrzeit</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Hin &amp; zurück</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Festpreis, einfach</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Hin &amp; zurück</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Bis zu 4</div><div class="rf-label">Fahrgäste</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Privat, Tür zu Tür</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Ihr privates Taxi und Transfer, Strecke %s" % rel
        tagline = "Taxi und privater Transfer zum Festpreis, Strecke %s, direkt zum Abflug." % rel
        intro = ("Sie fliegen ab Flughafen %s? Für die Strecke %s biete ich ein privates Taxi und einen Transfer zum Festpreis. "
                 "Ich bin Antonio, ein lokaler Fahrer aus Šibenik: Ich hole Sie an Ihrer Adresse ab und fahre Sie in einer komfortablen Škoda Superb "
                 "direkt zum Abflugterminal. Der Preis ist fest, &euro;%d für das ganze Fahrzeug, bis zu 4 Fahrgäste, im Voraus vereinbart, ohne Taxameter "
                 "und ohne Überraschungen. Ich plane die Abholung nach Ihrer Flugzeit, damit Sie mit genug Zeit zum Einchecken ankommen. "
                 "Das Angebotsformular oben ist für diese Strecke bereits ausgefüllt, sodass Sie den Preis sehen und mit wenigen Klicks buchen können." % (city, rel, p))
        whys = [("Festpreis &euro;%d" % p, "Ein Preis für das ganze Fahrzeug, bis zu 4 Fahrgäste, im Voraus vereinbart. Maut, Kraftstoff und Gepäck inklusive, kein Taxameter."),
                ("Auf Ihren Flug abgestimmt", "Nennen Sie mir Ihre Abflugzeit und ich rechne zurück, damit Sie mit Zeit zum Einchecken am Terminal sind."),
                ("Von der Tür zum Terminal", "Abholung an Ihrer Adresse und Absetzen direkt am Eingang des Abflugterminals."),
                ("Zu jeder Zeit", "Frühe und späte Flüge sind kein Problem. Ich fahre rund um die Uhr zu einem im Voraus vereinbarten Preis.")]
        faqs = [("Wie viel kostet ein Taxi auf der Strecke %s?" % rel,
                 "Fest &euro;%d pro Fahrzeug, einfache Fahrt, für bis zu 4 Fahrgäste. Der Preis gilt pro Fahrzeug, nicht pro Person, und umfasst Maut, Kraftstoff und Gepäck. Eine Hin- und Rückfahrt kostet &euro;%d." % (p, rp)),
                ("Wann sollte ich zum Flughafen aufbrechen?",
                 "In der Regel etwa 3 Stunden vor einem internationalen und 2 Stunden vor einem inländischen Flug. Nennen Sie mir Ihre Flugzeit und ich bestätige die genaue Abholung."),
                ("Fahren Sie bis zum Abflugterminal?",
                 "Ja. Ich fahre Sie direkt zum Abflugterminal und helfe mit dem Gepäck. Kein Fußweg vom Parkplatz und kein Shuttle."),
                ("Wie weit im Voraus sollte ich buchen?",
                 "Mindestens 2 Stunden vorher, damit ich Fahrzeug und Abholung bestätigen kann, und früher für frühe Flüge und die Hauptsaison. Für eine kurzfristige Fahrt rufen Sie an oder schreiben mir auf WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Ihre Flughafenabholung und Transfer, Strecke %s" % rel
        tagline = "Private Flughafenabholung und Transfer zum Festpreis, Strecke %s, mit Flugüberwachung." % rel
        intro = ("Gerade am Flughafen %s gelandet? Ein privater Transfer für die Strecke %s nimmt den Stress aus der Ankunft. "
                 "Ich empfange Sie in der Ankunftshalle mit einem Namensschild, helfe mit dem Gepäck und fahre Sie in einer komfortablen Škoda Superb "
                 "direkt zum Ziel, zum Festpreis von &euro;%d für das ganze Fahrzeug, bis zu 4 Fahrgäste. Ich verfolge Ihren Flug in Echtzeit, sodass ich da bin, "
                 "ob Sie früher oder später landen. Keine Taxischlange, kein Sammeltransfer und keine Preisaufschläge. "
                 "Das Formular oben ist für diese Strecke bereits ausgefüllt." % (city, rel, p))
        whys = [("Empfang mit Schild", "Ich warte in der Ankunftshalle mit einem Namensschild und helfe mit den Taschen, sodass Sie direkt zum Fahrzeug gehen."),
                ("Flugüberwachung", "Ich verfolge Ihren Flug in Echtzeit und passe mich früher Landung oder Verspätung an, mit kostenloser Wartezeit."),
                ("Festpreis &euro;%d" % p, "Ein Preis für das ganze Fahrzeug, bis zu 4 Fahrgäste, im Voraus vereinbart. Maut, Kraftstoff und Gepäck inklusive, kein Taxameter."),
                ("Direkt vor Ihre Tür", "Keine Schlange und kein Umsteigen. Ich fahre Sie direkt zu Ihrer Adresse.")]
        faqs = [("Wo empfangen Sie mich?",
                 "In der Ankunftshalle, direkt nach der Gepäckausgabe, mit einem Schild mit Ihrem Namen. Ich helfe mit dem Gepäck und begleite Sie zum Fahrzeug."),
                ("Was, wenn mein Flug Verspätung hat?",
                 "Kein Problem. Ich verfolge Ihren Flug in Echtzeit und passe die Abholung an die tatsächliche Landung an, ohne Aufpreis für die Wartezeit."),
                ("Wie viel kostet der Transfer auf der Strecke %s?" % rel,
                 "Fest &euro;%d pro Fahrzeug für bis zu 4 Fahrgäste, einfache Fahrt, Maut und Gepäck inklusive. Eine Hin- und Rückfahrt kostet &euro;%d." % (p, rp)),
                ("Wie weit im Voraus sollte ich buchen?",
                 "Mindestens 2 Stunden vorher, damit ich um Ihren Flug herum planen kann. Für eine Abholung am selben Tag nach einer kurzfristigen Änderung rufen Sie an oder schreiben auf WhatsApp.")]
    elif typ == "marina":
        heading = "Privater Marina-Transfer, Strecke %s" % rel
        tagline = "Privates Taxi und Transfer zum Festpreis, Strecke %s. &euro;%d pro Fahrzeug, bis zu 4 Fahrgäste, abgestimmt auf Ihr Boot." % (rel, p)
        intro = ("Fahren Sie auf der Strecke %s? Ich fahre ein privates Taxi und einen Transfer zum Festpreis für Marina-Gäste, abgestimmt auf Ihr Boot und Ihre Reisepläne. "
                 "Ich hole Sie mit viel Platz für Ihr Gepäck ab und fahre Sie den ganzen Weg bequem in einer Škoda Superb, zum Pauschalpreis von &euro;%d für das Fahrzeug, bis zu 4 Fahrgäste, vor der Fahrt vereinbart. "
                 "Ob Sie zu Ihrer Yacht kommen oder nach dem Ausschiffen weiterreisen, es gibt kein Taxameter und kein Warten am Stand, nur einen lokalen Fahrer, den Sie direkt buchen. "
                 "Das ist ein privater Transfer über eine längere Strecke, keine kurze Fahrt im Ort, und das Angebot oben ist für diese Strecke bereits eingestellt, sodass die Buchung nur wenige Klicks dauert." % (rel, p))
        whys = [("Festpreis &euro;%d" % p, "Ein Preis pro Fahrzeug für bis zu 4 Fahrgäste, im Voraus vereinbart. Maut, Kraftstoff und Gepäck inklusive, kein laufendes Taxameter."),
                ("Auf Ihr Boot abgestimmt", "Nennen Sie mir Ihre Charter-, Check-in- oder Abfahrtszeit und ich plane die Abholung darum herum, sodass eine langsame Strecke Sie nie in Eile bringt."),
                ("Platz für Ihr Gepäck", "Koffer, Proviant und Bootstaschen passen alle in eine komfortable Škoda Superb, mit einer helfenden Hand beim Ein- und Ausladen."),
                ("Ein lokaler Fahrer", "Sie haben direkt mit mir zu tun, von der Buchung bis zur Ankunft, per Telefon, WhatsApp oder E-Mail. Kein Callcenter.")]
        faqs = [("Wie viel kostet ein Transfer auf der Strecke %s?" % rel,
                 "Fest &euro;%d pro Fahrzeug für bis zu 4 Fahrgäste, einfache Fahrt, mit Maut, Kraftstoff und Gepäck. Eine Hin- und Rückfahrt kostet &euro;%d." % (p, rp)),
                ("Können Sie direkt an der Marina abholen?",
                 "Ja. Ich treffe Sie am Eingang oder an der Rezeption der Marina und helfe mit dem Gepäck, sodass Sie direkt vom Steg zum Fahrzeug gehen."),
                ("Können Sie den Transfer auf mein Boot abstimmen?",
                 "Ja. Senden Sie mir bei der Buchung Ihre Charter-, Check-in- oder Abfahrtszeit und ich plane die Abholung darum herum."),
                ("Wie weit im Voraus sollte ich buchen?",
                 "Mindestens 2 Stunden vorher, damit ich Fahrzeug und Abholzeit bestätigen kann. Für eine kurzfristige Fahrt rufen Sie an oder schreiben mir direkt auf WhatsApp.")]
    elif typ == "city":
        heading = "Privater Transfer, Strecke %s" % rel
        tagline = "Privates Taxi und Transfer zum Festpreis, Strecke %s, Tür zu Tür." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Brauchen Sie einen zuverlässigen Transfer auf der Strecke %s? Ich biete ein privates Taxi und einen Transfer zum Festpreis, Tür zu Tür, in einer komfortablen Škoda Superb. "
                     "Ich hole Sie an Ihrer genauen Adresse ab und fahre Sie direkt zum Ziel, ohne ungewollte Zwischenstopps und ohne Mitfahrer. "
                     "Der Preis ist fest, &euro;%d für das ganze Fahrzeug, bis zu 4 Fahrgäste, vor der Abfahrt vereinbart, Maut und Gepäck inklusive. "
                     "Das Angebot oben ist für diese Strecke ausgefüllt, sodass die Buchung nur wenige Klicks dauert." % (rel, p))
        else:
            intro = ("Suchen Sie ein Taxi auf der Strecke %s ohne Taxameter und Aufwand? Das ist ein privater Transfer zum Festpreis mit einem lokalen Fahrer. "
                     "Ich hole Sie an der Tür ab und fahre Sie bequem zum Ziel, samt Gepäck, zum Pauschalpreis von &euro;%d pro Fahrzeug für bis zu 4 Fahrgäste. "
                     "Für Paare und Familien ist es oft günstiger als getrennte Bus- oder Zugtickets, und immer schneller und Tür zu Tür. "
                     "Das Angebot oben ist für diese Strecke bereits eingestellt." % (rel, p))
        whys = [("Festpreis &euro;%d" % p, "Ein Preis pro Fahrzeug für bis zu 4 Fahrgäste, im Voraus vereinbart. Maut, Kraftstoff und Gepäck inklusive, kein laufendes Taxameter."),
                ("Tür zu Tür", "Ich hole Sie an Ihrer genauen Adresse ab und setze Sie an der Tür des Ziels ab. Keine Bahnhöfe, kein Umsteigen."),
                ("Ein lokaler Fahrer", "Sie haben direkt mit mir zu tun, von der Buchung bis zur Ankunft, per Telefon, WhatsApp oder E-Mail. Kein Callcenter."),
                ("Stopps auf Wunsch", "Auf längeren Strecken halte ich gern für einen Kaffee, ein Foto oder eine kurze Sehenswürdigkeit unterwegs.")]
        faqs = [("Wie viel kostet ein Taxi auf der Strecke %s?" % rel,
                 "Fest &euro;%d pro Fahrzeug für bis zu 4 Fahrgäste, einfache Fahrt, mit Maut, Kraftstoff und Gepäck. Eine Hin- und Rückfahrt kostet &euro;%d." % (p, rp)),
                ("Ist der Transfer privat oder geteilt?",
                 "Jeder Transfer ist privat und Tür zu Tür, in einer Škoda Superb. Kein Teilen des Fahrzeugs und keine zusätzlichen Stopps, außer Sie wünschen es."),
                ("Können Sie unterwegs anhalten?",
                 "Ja. Auf längeren Strecken halte ich gern für einen Kaffee, ein Foto oder eine kurze Sehenswürdigkeit. Sagen Sie einfach bei der Buchung Bescheid."),
                ("Wie weit im Voraus sollte ich buchen?",
                 "Mindestens 2 Stunden vorher, damit ich Fahrzeug und Abholzeit bestätigen kann. Für eine kurzfristige Fahrt rufen Sie an oder schreiben auf WhatsApp.")]
    else:  # local
        heading = "Privates Taxi, Strecke %s" % rel
        tagline = "Privates Taxi und Transfer zum Festpreis, Strecke %s, Tür zu Tür." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Sie reisen auf der Strecke %s? Ich fahre ein privates Taxi und einen Transfer zum Festpreis, mit Abholung an Ihrer Tür und Absetzen genau dort, wo Sie hinmüssen. "
                     "Der Preis ist pauschal &euro;%d für das ganze Fahrzeug, bis zu 4 Fahrgäste, ohne Taxameter und ohne Warten am Stand. "
                     "Eine komfortable Škoda Superb, Platz für Ihr Gepäck und ein lokaler Fahrer, den Sie direkt buchen. "
                     "Das Angebot oben ist für diese Strecke ausgefüllt." % (rel, p))
        else:
            intro = ("Brauchen Sie ein Taxi auf der Strecke %s? Ich biete einen privaten Transfer von Tür zu Tür zum Festpreis von &euro;%d für das ganze Fahrzeug, bis zu 4 Fahrgäste. "
                     "Ich komme zur vereinbarten Zeit an Ihre Adresse, sodass Sie nie am Straßenrand warten, und fahre Sie bequem zum Ziel. "
                     "Kein Taxameter, keine Überraschungen, nur ein lokaler Fahrer von der Buchung bis zur Ankunft. Das Angebot oben ist für diese Strecke bereits eingestellt." % (rel, p))
        whys = [("Festpreis &euro;%d" % p, "Ein Preis pro Fahrzeug für bis zu 4 Fahrgäste, vor der Fahrt vereinbart. Kein Taxameter, keine Überraschungen."),
                ("Tür zu Tür", "Abholung an Ihrer Adresse und Absetzen an der Tür des Ziels, samt Gepäck."),
                ("Kein Taxistand nötig", "Im Voraus gebucht, sodass Sie nie auf ein vorbeifahrendes Taxi warten. Ich komme zu Ihnen."),
                ("Ein lokaler Fahrer", "Sie haben direkt mit mir zu tun, von der Buchung bis zur Ankunft, per Telefon, WhatsApp oder E-Mail.")]
        faqs = [("Wie viel kostet ein Taxi auf der Strecke %s?" % rel,
                 "Fest &euro;%d pro Fahrzeug für bis zu 4 Fahrgäste, einfache Fahrt, Gepäck inklusive. Eine Hin- und Rückfahrt kostet &euro;%d." % (p, rp)),
                ("Wo holen Sie mich ab?",
                 "An Ihrer genauen Adresse, ob Haus, Hotel oder Apartment. Senden Sie die Adresse bei der Buchung und ich bestätige den Treffpunkt."),
                ("Wie weit im Voraus sollte ich buchen?",
                 "Mindestens 2 Stunden vorher, damit ich Fahrzeug und Abholzeit bestätigen kann. Für eine kurzfristige Fahrt rufen Sie an oder schreiben auf WhatsApp.")]

    if dd:
        faqs = [("Wie weit ist die Strecke und wie lange dauert die Fahrt?",
                 "Die Fahrt auf der Strecke %s ist rund %d km lang und dauert etwa %s bei normalem Verkehr, in der Sommerhauptzeit etwas länger. Ich plane die Abholung so, dass eine langsame Strecke Sie nie in Eile bringt." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join(
        '        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t)
        for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Hallo Antonio, ich möchte den Transfer %s (€%d) buchen.\n"
        "Meine Angaben:\n- Abholdatum: \n- Abholzeit: \n- Fahrgäste: \n- Abholadresse: \n- Mein Name: " % (rel, p))
    trust_line = ("Sofortige Bestätigung per E-Mail &middot; Keine versteckten Kosten &middot; Flugüberwachung inklusive"
                  if typ in ("to_airport", "from_airport")
                  else "Sofortige Bestätigung per E-Mail &middot; Keine versteckten Kosten &middot; Festpreis, kein Taxameter")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: Škoda Superb von TAXI Antonio an der dalmatinischen Küste" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d pro Fahrzeug &middot; bis zu 4 Fahrgäste</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Jetzt buchen</a>
          <a class="btn btn-secondary" href="%s">Über WhatsApp buchen</a>
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
      <span class="eyebrow center">Warum diesen Transfer buchen</span>
      <h2 class="section-title">Warum Ihr Taxi %s bei Antonio buchen?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Preis %s</h2>
      <p class="section-subtitle">Festpreis pro Fahrzeug, bis zu 4 Fahrgäste, Gepäck inklusive. Der gleiche Preis gilt in der Gegenrichtung.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Einfach</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Hin &amp; zurück</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Anzahlung zur Bestätigung</div></div>
        <div class="route-fact"><div class="rf-value">Bar oder Karte</div><div class="rf-label">Rest am Tag</div></div>
      </div>
      <p class="hub-note">Eine Anzahlung von 20%% (mindestens &euro;20) bestätigt Ihre Buchung, den Rest zahlen Sie am Tag der Fahrt, bar oder mit Karte. Reisen Sie in die Gegenrichtung? Siehe %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Bewertungen</span>
      <h2 class="section-title">Was Fahrgäste sagen</h2>
      <p class="section-subtitle">Echte Bewertungen von echten Fahrgästen.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s: Häufige Fragen</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Reservieren Sie Ihren Transfer %s</h2>
      <p class="section-subtitle">Festpreis &euro;%d pro Fahrzeug, bis zu 4 Fahrgäste. Bestätigung mit wenigen Klicks.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Jetzt buchen</a>
        <a href="%s" class="btn btn-secondary">Über WhatsApp buchen</a>
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

    desc = ("Privates Taxi und Transfer, Strecke %s. Festpreis &euro;%d pro Fahrzeug, bis zu 4 Fahrgäste, Tür zu Tür. Direkt bei Antonio buchen." % (rel, p))
    if len(desc) > 155:
        desc = "Privates Taxi und Transfer, Strecke %s. Festpreis &euro;%d pro Fahrzeug, bis zu 4. Direkt bei Antonio buchen." % (rel, p)
    keywords = "taxi %s, transfer %s, flughafentransfer %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service",
         "serviceType": "Privater Taxitransfer",
         "name": "Taxi %s" % rel,
         "description": "Privates Taxi und Transfer zum Festpreis, Strecke %s, %d Euro pro Fahrzeug für bis zu 4 Fahrgäste, Tür zu Tür." % (rel, p),
         "provider": PROVIDER,
         "areaServed": [gf, gt],
         "url": "https://taxisibenik.hr/de/%s/" % deslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Einfache private Fahrt, Strecke %s, pro Fahrzeug für bis zu 4 Fahrgäste. Hin und zurück %d Euro." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": deslug, "title": "Taxi %s | Festpreis €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}

    outdir = os.path.join(PAGES, slug, "de")
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
print("generated de:", sum(made.values()), made)
print("skipped (no matrix price):", skipped_noprice)
