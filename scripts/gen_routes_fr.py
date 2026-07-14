# -*- coding: utf-8 -*-
"""Generate the FRENCH variant of every route page. Mirrors gen_routes.py.
Place names kept nominative via "trajet <A> - <B>". Run after gen_routes.py."""
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
FR_NAME = {'Split Airport':'Aéroport de Split','Zadar Airport':'Aéroport de Zadar',
           'Zagreb Airport':'Aéroport de Zagreb','Dubrovnik Airport':'Aéroport de Dubrovnik'}
fr = lambda n: FR_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'aeroport-split','zadar-airport':'aeroport-zadar',
                'zagreb-airport':'aeroport-zagreb','dubrovnik-airport':'aeroport-dubrovnik'}
def fr_slug(en_slug):
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
    return "/fr/reservation/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    ffr, fto = fr(frm), fr(to)
    rel = "%s - %s" % (ffr, fto)
    frslug = fr_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/fr/%s/">%s - %s</a>' % (fr_slug(rev), fto, ffr)) if rev else ("%s - %s" % (fto, ffr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Prix fixe, aller simple</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Distance</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Durée</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Aller-retour</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Prix fixe, aller simple</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Aller-retour</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Jusqu\'à 4</div><div class="rf-label">Passagers</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Privé, porte à porte</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Votre taxi privé et transfert, trajet %s" % rel
        tagline = "Taxi et transfert privé à prix fixe, trajet %s, directement aux départs." % rel
        intro = ("Vous partez de l'aéroport de %s ? Pour le trajet %s, je propose un taxi et un transfert privé à prix fixe. "
                 "Je suis Antonio, chauffeur local de Šibenik : je vous prends à votre adresse et vous conduis directement au terminal des départs dans une Škoda Superb confortable. "
                 "Le prix est fixe, &euro;%d pour tout le véhicule, jusqu'à 4 passagers, convenu à l'avance, sans compteur et sans surprises. "
                 "Je planifie la prise en charge selon l'heure de votre vol, pour que vous arriviez avec le temps de vous enregistrer. "
                 "Le formulaire de devis ci-dessus est déjà rempli pour ce trajet, vous voyez donc le prix et réservez en quelques clics." % (city, rel, p))
        whys = [("Prix fixe &euro;%d" % p, "Un prix pour tout le véhicule, jusqu'à 4 passagers, convenu à l'avance. Péages, carburant et bagages inclus, sans compteur."),
                ("Adapté à votre vol", "Indiquez-moi l'heure de départ et je calcule à rebours, pour que vous soyez au terminal à temps pour l'enregistrement."),
                ("De la porte au terminal", "Prise en charge à votre adresse et dépose directement à l'entrée du terminal des départs."),
                ("À toute heure", "Les vols tôt le matin ou tard le soir ne posent aucun problème. Je roule 24h/24 à un prix convenu à l'avance.")]
        faqs = [("Combien coûte un taxi sur le trajet %s ?" % rel,
                 "&euro;%d fixe par véhicule, aller simple, jusqu'à 4 passagers. Le prix est par véhicule, pas par personne, et comprend péages, carburant et bagages. Un aller-retour coûte &euro;%d." % (p, rp)),
                ("À quelle heure partir pour mon vol ?",
                 "En règle générale, environ 3 heures avant un vol international et 2 heures avant un vol intérieur. Indiquez-moi l'heure du vol et je confirme la prise en charge exacte."),
                ("Me déposez-vous jusqu'au terminal des départs ?",
                 "Oui. Je vous conduis directement au terminal des départs et vous aide avec les bagages. Pas de marche depuis le parking, pas de navette."),
                ("Combien de temps à l'avance réserver ?",
                 "Au moins 2 heures avant, pour que je confirme le véhicule et la prise en charge, et plus tôt pour les vols matinaux et en haute saison. Pour un trajet de dernière minute, appelez-moi ou écrivez-moi sur WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Votre prise en charge à l'aéroport et transfert, trajet %s" % rel
        tagline = "Prise en charge privée à l'aéroport et transfert à prix fixe, trajet %s, avec suivi de vol." % rel
        intro = ("Vous venez d'atterrir à l'aéroport de %s ? Un transfert privé pour le trajet %s enlève le stress de l'arrivée. "
                 "Je vous accueille dans le hall des arrivées avec une pancarte à votre nom, vous aide avec les bagages et vous conduis directement à destination dans une Škoda Superb confortable, "
                 "au prix fixe de &euro;%d pour tout le véhicule, jusqu'à 4 passagers. Je suis votre vol en temps réel, je suis donc là que vous atterrissiez en avance ou en retard. "
                 "Pas de file d'attente pour les taxis, pas de navette partagée et pas de majoration. Le formulaire ci-dessus est déjà rempli pour ce trajet." % (city, rel, p))
        whys = [("Accueil avec pancarte", "Je vous attends dans le hall des arrivées avec une pancarte à votre nom et vous aide avec les sacs, pour aller directement au véhicule."),
                ("Suivi de vol", "Je suis votre vol en temps réel et m'adapte à un atterrissage anticipé ou un retard, avec temps d'attente gratuit."),
                ("Prix fixe &euro;%d" % p, "Un prix pour tout le véhicule, jusqu'à 4 passagers, convenu à l'avance. Péages, carburant et bagages inclus, sans compteur."),
                ("Directement à votre porte", "Pas de file d'attente et pas de correspondance. Je vous conduis directement à votre adresse.")]
        faqs = [("Où m'accueillez-vous ?",
                 "Dans le hall des arrivées, juste après le retrait des bagages, avec une pancarte à votre nom. Je vous aide avec les bagages et vous accompagne au véhicule."),
                ("Et si mon vol est retardé ?",
                 "Aucun problème. Je suis votre vol en temps réel et adapte la prise en charge à l'atterrissage réel, sans majoration pour l'attente."),
                ("Combien coûte le transfert sur le trajet %s ?" % rel,
                 "&euro;%d fixe par véhicule jusqu'à 4 passagers, aller simple, péages et bagages inclus. Un aller-retour coûte &euro;%d." % (p, rp)),
                ("Combien de temps à l'avance réserver ?",
                 "Au moins 2 heures avant, pour que je planifie selon votre vol. Pour une prise en charge le jour même après un changement soudain, appelez-moi ou écrivez-moi sur WhatsApp.")]
    elif typ == "marina":
        heading = "Transfert privé de marina, trajet %s" % rel
        tagline = "Taxi et transfert privé à prix fixe, trajet %s. &euro;%d par véhicule, jusqu'à 4 passagers, calé sur votre bateau." % (rel, p)
        intro = ("Vous vous déplacez entre %s et %s ? Je propose un taxi et un transfert privé à prix fixe pour les clients des marinas, calé sur votre bateau et vos plans de voyage. "
                 "Je vous prends en charge avec toute la place nécessaire pour vos bagages et vous conduis confortablement sur tout le trajet dans une Škoda Superb, "
                 "pour un forfait de &euro;%d pour le véhicule, jusqu'à 4 passagers, convenu avant le départ. "
                 "Que vous rejoigniez votre yacht ou que vous poursuiviez votre route après en être descendu, il n'y a pas de compteur ni d'attente à une station, seulement un chauffeur local que vous réservez directement. "
                 "C'est un transfert privé longue distance, pas un court trajet local, et le devis ci-dessus est déjà prêt pour ce trajet, la réservation ne prend donc que quelques clics." % (ffr, fto, p))
        whys = [("Prix fixe &euro;%d" % p, "Un prix par véhicule jusqu'à 4 passagers, convenu à l'avance. Péages, carburant et bagages inclus, sans compteur."),
                ("Calé sur votre bateau", "Indiquez-moi l'heure de votre charter, de votre enregistrement ou de votre départ et je planifie la prise en charge autour, pour qu'un imprévu ne vous mette jamais en retard."),
                ("De la place pour vos bagages", "Valises, provisions et sacs de bateau tiennent tous dans une Škoda Superb confortable, avec un coup de main pour charger et décharger."),
                ("Un chauffeur local", "Vous traitez directement avec moi, de la réservation à l'arrivée, par téléphone, WhatsApp ou e-mail. Pas de centre d'appels.")]
        faqs = [("Combien coûte un transfert sur le trajet %s ?" % rel,
                 "&euro;%d fixe par véhicule jusqu'à 4 passagers, aller simple, avec péages, carburant et bagages inclus. Un aller-retour coûte &euro;%d." % (p, rp)),
                ("Pouvez-vous me prendre en charge directement à la marina ?",
                 "Oui. Je vous retrouve à l'entrée de la marina ou à la réception et vous aide avec les bagages, pour aller directement du ponton au véhicule."),
                ("Pouvez-vous caler le transfert sur mon bateau ?",
                 "Oui. Envoyez-moi l'heure de votre charter, de votre enregistrement ou de votre départ à la réservation et je planifie la prise en charge autour."),
                ("Combien de temps à l'avance réserver ?",
                 "Au moins 2 heures avant, pour que je confirme le véhicule et votre heure de prise en charge. Pour un trajet plus rapproché, appelez-moi ou écrivez-moi sur WhatsApp.")]
    elif typ == "city":
        heading = "Transfert privé, trajet %s" % rel
        tagline = "Taxi et transfert privé à prix fixe, trajet %s, porte à porte." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Vous cherchez un transfert fiable sur le trajet %s ? Je propose un taxi et un transfert privé à prix fixe, porte à porte, dans une Škoda Superb confortable. "
                     "Je vous prends à votre adresse exacte et vous conduis directement à destination, sans arrêts non désirés et sans autres passagers. "
                     "Le prix est fixe, &euro;%d pour tout le véhicule, jusqu'à 4 passagers, convenu avant le départ, péages et bagages inclus. "
                     "Le devis ci-dessus est rempli pour ce trajet, la réservation ne prend donc que quelques clics." % (rel, p))
        else:
            intro = ("Vous cherchez un taxi sur le trajet %s sans compteur ni tracas ? C'est un transfert privé à prix fixe avec un chauffeur local. "
                     "Je vous prends à la porte et vous conduis confortablement à destination, bagages compris, au tarif forfaitaire de &euro;%d par véhicule jusqu'à 4 passagers. "
                     "Pour les couples et les familles, cela revient souvent moins cher que des billets de bus ou de train séparés, et c'est toujours plus rapide et porte à porte. "
                     "Le devis ci-dessus est déjà prêt pour ce trajet." % (rel, p))
        whys = [("Prix fixe &euro;%d" % p, "Un prix par véhicule jusqu'à 4 passagers, convenu à l'avance. Péages, carburant et bagages inclus, sans compteur."),
                ("Porte à porte", "Je vous prends à votre adresse exacte et vous dépose devant la porte de la destination. Pas de gares, pas de correspondances."),
                ("Un chauffeur local", "Vous traitez directement avec moi, de la réservation à l'arrivée, par téléphone, WhatsApp ou e-mail. Pas de centre d'appels."),
                ("Arrêts sur demande", "Sur les trajets plus longs, je m'arrête volontiers pour un café, une photo ou une brève visite en chemin.")]
        faqs = [("Combien coûte un taxi sur le trajet %s ?" % rel,
                 "&euro;%d fixe par véhicule jusqu'à 4 passagers, aller simple, avec péages, carburant et bagages. Un aller-retour coûte &euro;%d." % (p, rp)),
                ("Le transfert est-il privé ou partagé ?",
                 "Chaque transfert est privé et porte à porte, dans une Škoda Superb. Pas de partage du véhicule et pas d'arrêts supplémentaires, sauf si vous le demandez."),
                ("Pouvez-vous vous arrêter en chemin ?",
                 "Oui. Sur les trajets plus longs, je m'arrête volontiers pour un café, une photo ou une brève visite. Il suffit de le dire à la réservation."),
                ("Combien de temps à l'avance réserver ?",
                 "Au moins 2 heures avant, pour que je confirme le véhicule et l'heure de prise en charge. Pour un trajet de dernière minute, appelez-moi ou écrivez-moi sur WhatsApp.")]
    else:
        heading = "Taxi privé, trajet %s" % rel
        tagline = "Taxi et transfert privé à prix fixe, trajet %s, porte à porte." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Vous voyagez sur le trajet %s ? Je propose un taxi et un transfert privé à prix fixe, avec prise en charge à votre porte et dépose exactement là où vous en avez besoin. "
                     "Le prix est forfaitaire, &euro;%d pour tout le véhicule, jusqu'à 4 passagers, sans compteur et sans attente à une station. "
                     "Une Škoda Superb confortable, de la place pour les bagages et un chauffeur local que vous réservez directement. "
                     "Le devis ci-dessus est rempli pour ce trajet." % (rel, p))
        else:
            intro = ("Vous avez besoin d'un taxi sur le trajet %s ? Je propose un transfert privé porte à porte à prix fixe de &euro;%d pour tout le véhicule, jusqu'à 4 passagers. "
                     "J'arrive à votre adresse à l'heure convenue, vous n'attendez donc jamais au bord de la route, et je vous conduis confortablement à destination. "
                     "Sans compteur, sans surprises, juste un chauffeur local de la réservation à l'arrivée. Le devis ci-dessus est déjà prêt pour ce trajet." % (rel, p))
        whys = [("Prix fixe &euro;%d" % p, "Un prix par véhicule jusqu'à 4 passagers, convenu avant le trajet. Sans compteur, sans surprises."),
                ("Porte à porte", "Prise en charge à votre adresse et dépose devant la porte de la destination, bagages compris."),
                ("Sans station nécessaire", "Réservé à l'avance, vous n'attendez donc jamais un taxi de passage. Je viens à vous."),
                ("Un chauffeur local", "Vous traitez directement avec moi, de la réservation à l'arrivée, par téléphone, WhatsApp ou e-mail.")]
        faqs = [("Combien coûte un taxi sur le trajet %s ?" % rel,
                 "&euro;%d fixe par véhicule jusqu'à 4 passagers, aller simple, bagages inclus. Un aller-retour coûte &euro;%d." % (p, rp)),
                ("Où me prenez-vous en charge ?",
                 "À votre adresse exacte, que ce soit une maison, un hôtel ou un appartement. Envoyez l'adresse à la réservation et je confirme le point de rendez-vous."),
                ("Combien de temps à l'avance réserver ?",
                 "Au moins 2 heures avant, pour que je confirme le véhicule et l'heure de prise en charge. Pour un trajet de dernière minute, appelez-moi ou écrivez-moi sur WhatsApp.")]

    if dd:
        faqs = [("Quelle est la distance du trajet et combien de temps dure-t-il ?",
                 "Le trajet %s fait environ %d km et dure à peu près %s en trafic normal, un peu plus aux heures de pointe en été. Je planifie la prise en charge pour qu'un tronçon plus lent ne vous mette jamais en retard." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Bonjour Antonio, je souhaite réserver le transfert %s (€%d).\n"
        "Mes informations :\n- Date de prise en charge : \n- Heure de prise en charge : \n- Passagers : \n- Adresse de prise en charge : \n- Mon nom : " % (rel, p))
    trust_line = ("Confirmation immédiate par e-mail &middot; Sans frais cachés &middot; Suivi de vol inclus"
                  if typ in ("to_airport", "from_airport")
                  else "Confirmation immédiate par e-mail &middot; Sans frais cachés &middot; Prix fixe, sans compteur")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s : la Škoda Superb de TAXI Antonio sur la côte dalmate" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d par véhicule &middot; jusqu'à 4 passagers</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Réserver</a>
          <a class="btn btn-secondary" href="%s">Réserver via WhatsApp</a>
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
      <span class="eyebrow center">Pourquoi réserver ce transfert</span>
      <h2 class="section-title">Pourquoi réserver votre taxi %s avec Antonio ?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Prix %s</h2>
      <p class="section-subtitle">Prix fixe par véhicule, jusqu'à 4 passagers, bagages inclus. Le même prix s'applique dans le sens inverse.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Aller simple</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Aller-retour</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Acompte pour confirmer</div></div>
        <div class="route-fact"><div class="rf-value">Espèces ou carte</div><div class="rf-label">Solde le jour même</div></div>
      </div>
      <p class="hub-note">Un acompte de 20%% (minimum &euro;20) confirme votre réservation, le solde se paie le jour même, en espèces ou par carte. Vous voyagez dans l'autre sens ? Voir %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Avis</span>
      <h2 class="section-title">Ce que disent les passagers</h2>
      <p class="section-subtitle">De vrais avis de vrais passagers.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s : questions fréquentes</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Réservez votre transfert %s</h2>
      <p class="section-subtitle">Prix fixe &euro;%d par véhicule, jusqu'à 4 passagers. Confirmez en quelques clics.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Réserver</a>
        <a href="%s" class="btn btn-secondary">Réserver via WhatsApp</a>
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

    desc = ("Taxi et transfert privé, trajet %s. Prix fixe &euro;%d par véhicule, jusqu'à 4 passagers, porte à porte. Réservez directement avec Antonio." % (rel, p))
    if len(desc) > 160:
        desc = "Taxi et transfert privé, trajet %s. Prix fixe &euro;%d par véhicule, jusqu'à 4. Réservez avec Antonio." % (rel, p)
    keywords = "taxi %s, transfert %s, transfert aéroport %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Transfert taxi privé",
         "name": "Taxi %s" % rel,
         "description": "Taxi et transfert privé à prix fixe, trajet %s, %d euros par véhicule jusqu'à 4 passagers, porte à porte." % (rel, p),
         "provider": PROVIDER, "areaServed": [ffr, fto],
         "url": "https://taxisibenik.hr/fr/%s/" % frslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Trajet privé aller simple, trajet %s, par véhicule jusqu'à 4 passagers. Aller-retour %d euros." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": frslug, "title": "Taxi %s | Prix fixe €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "fr")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated fr:", sum(made.values()), made, "| skipped:", skipped)
