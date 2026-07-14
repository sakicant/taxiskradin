# -*- coding: utf-8 -*-
"""Generate the POLISH variant of every route page. Mirrors gen_routes.py.
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
PL_NAME = {'Split Airport':'Lotnisko Split','Zadar Airport':'Lotnisko Zadar',
           'Zagreb Airport':'Lotnisko Zagreb','Dubrovnik Airport':'Lotnisko Dubrovnik'}
pl = lambda n: PL_NAME.get(n, n)
AIRPORT_SLUG = {'split-airport':'lotnisko-split','zadar-airport':'lotnisko-zadar',
                'zagreb-airport':'lotnisko-zagreb','dubrovnik-airport':'lotnisko-dubrovnik'}
def pl_slug(en_slug):
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
    return "/pl/rezerwacja/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    pfr, pto = pl(frm), pl(to)
    rel = "%s - %s" % (pfr, pto)
    plslug = pl_slug(slug)
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/pl/%s/">%s - %s</a>' % (pl_slug(rev), pto, pfr)) if rev else ("%s - %s" % (pto, pfr))
    book = book_link(frm, to, p)
    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Stała cena, w jedną stronę</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Odległość</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Czas jazdy</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">W obie strony</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Stała cena, w jedną stronę</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">W obie strony</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Do 4</div><div class="rf-label">Pasażerowie</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Prywatnie, od drzwi do drzwi</div></div>'
            % (p, rp))

    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Twoje prywatne taxi i transfer, trasa %s" % rel
        tagline = "Taxi i prywatny transfer w stałej cenie, trasa %s, prosto do odlotów." % rel
        intro = ("Wylatujesz z lotniska %s? Na trasie %s oferuję prywatne taxi i transfer w stałej cenie. "
                 "Jestem Antonio, lokalny kierowca z Šibenika: odbieram Cię spod drzwi i wiozę prosto do terminalu odlotów wygodną Škodą Superb. "
                 "Cena jest stała, &euro;%d za cały pojazd, do 4 pasażerów, ustalona przed podróżą, bez taksometru i bez niespodzianek. "
                 "Planuję odbiór według godziny Twojego lotu, żebyś dotarł z zapasem na odprawę. "
                 "Formularz wyceny powyżej jest już wypełniony dla tej trasy, więc zobaczysz cenę i zarezerwujesz w kilku kliknięciach." % (city, rel, p))
        whys = [("Stała cena &euro;%d" % p, "Jedna cena za cały pojazd, do 4 pasażerów, ustalona z góry. Opłaty drogowe, paliwo i bagaż w cenie, bez taksometru."),
                ("Dopasowane do Twojego lotu", "Podaj godzinę wylotu, a policzę wstecz, żebyś dotarł na terminal z czasem na odprawę."),
                ("Od drzwi do terminalu", "Odbiór spod Twojego adresu i podwiezienie prosto pod wejście do terminalu odlotów."),
                ("O każdej porze", "Wczesne i późne loty to żaden problem. Jeżdżę całą dobę w cenie ustalonej z góry.")]
        faqs = [("Ile kosztuje taxi na trasie %s?" % rel,
                 "Stałe &euro;%d za pojazd, w jedną stronę, do 4 pasażerów. Cena jest za pojazd, nie za osobę, i obejmuje opłaty drogowe, paliwo i bagaż. W obie strony &euro;%d." % (p, rp)),
                ("O której wyjechać na lot?",
                 "Zwykle około 3 godzin przed lotem międzynarodowym i 2 godzin przed krajowym. Podaj godzinę lotu, a potwierdzę dokładny odbiór."),
                ("Podwozisz pod sam terminal odlotów?",
                 "Tak. Wiozę Cię prosto pod terminal odlotów i pomagam z bagażem. Bez spaceru z parkingu i bez shuttle busa."),
                ("Z jakim wyprzedzeniem rezerwować?",
                 "Co najmniej 2 godziny wcześniej, żebym potwierdził pojazd i odbiór, a wcześniej dla porannych lotów i w sezonie. Na szybki kurs zadzwoń lub napisz na WhatsApp.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Twój odbiór z lotniska i transfer, trasa %s" % rel
        tagline = "Prywatny odbiór z lotniska i transfer w stałej cenie, trasa %s, z monitorowaniem lotu." % rel
        intro = ("Właśnie wylądowałeś na lotnisku %s? Prywatny transfer na trasie %s zdejmuje stres z przyjazdu. "
                 "Witam Cię w hali przylotów z tabliczką z imieniem, pomagam z bagażem i wiozę prosto do celu wygodną Škodą Superb, "
                 "w stałej cenie &euro;%d za cały pojazd, do 4 pasażerów. Monitoruję Twój lot na bieżąco, więc jestem na miejscu, czy wylądujesz wcześniej, czy później. "
                 "Bez kolejki po taxi, bez wspólnego busa i bez dopłat. Formularz powyżej jest już wypełniony dla tej trasy." % (city, rel, p))
        whys = [("Powitanie z tabliczką", "Czekam w hali przylotów z tabliczką z Twoim imieniem i pomagam z torbami, żebyś od razu poszedł do pojazdu."),
                ("Monitorowanie lotu", "Monitoruję Twój lot na bieżąco i dostosowuję się do wcześniejszego lądowania lub opóźnienia, z darmowym oczekiwaniem."),
                ("Stała cena &euro;%d" % p, "Jedna cena za cały pojazd, do 4 pasażerów, ustalona z góry. Opłaty drogowe, paliwo i bagaż w cenie, bez taksometru."),
                ("Prosto pod Twoje drzwi", "Bez kolejki i bez przesiadek. Wiozę Cię prosto pod Twój adres.")]
        faqs = [("Gdzie mnie witasz?",
                 "W hali przylotów, zaraz za odbiorem bagażu, z tabliczką z Twoim imieniem. Pomagam z bagażem i odprowadzam do pojazdu."),
                ("Co jeśli mój lot jest opóźniony?",
                 "Żaden problem. Monitoruję Twój lot na bieżąco i dostosowuję odbiór do faktycznego lądowania, bez dopłaty za oczekiwanie."),
                ("Ile kosztuje transfer na trasie %s?" % rel,
                 "Stałe &euro;%d za pojazd do 4 pasażerów, w jedną stronę, opłaty drogowe i bagaż w cenie. W obie strony &euro;%d." % (p, rp)),
                ("Z jakim wyprzedzeniem rezerwować?",
                 "Co najmniej 2 godziny wcześniej, żebym zaplanował pod Twój lot. Na odbiór tego samego dnia po nagłej zmianie zadzwoń lub napisz na WhatsApp.")]
    elif typ == "marina":
        heading = "Prywatny transfer z mariny, trasa %s" % rel
        tagline = "Taxi i prywatny transfer w stałej cenie, trasa %s. &euro;%d za pojazd, do 4 pasażerów, z dopasowaniem do godzin Pana/Pani rejsu." % (rel, p)
        intro = ("Potrzebuje Pan/Pani transferu na trasie %s? Prowadzę prywatne taxi i transfer w stałej cenie dla gości marin, dopasowany do godzin rejsu i planów podróży. "
                 "Odbieram Pana/Panią z dużą ilością miejsca na bagaż i wiozę wygodnie przez całą trasę wygodną Škodą Superb, w cenie ryczałtowej &euro;%d za pojazd, do 4 pasażerów, ustalonej przed wyjazdem. "
                 "Niezależnie od tego, czy wsiada Pan/Pani na swój jacht, czy rusza dalej po zejściu na ląd, nie ma taksometru ani czekania na postoju, tylko jeden lokalny kierowca, którego rezerwuje Pan/Pani bezpośrednio. "
                 "To prywatny transfer na dłuższą trasę, nie krótki lokalny kurs, a wycena powyżej jest już ustawiona dla tej trasy, więc rezerwacja to kilka kliknięć." % (rel, p))
        whys = [("Stała cena &euro;%d" % p, "Jedna cena za pojazd do 4 pasażerów, ustalona z góry. Opłaty drogowe, paliwo i bagaż w cenie, bez taksometru."),
                ("Dopasowane do Pana/Pani rejsu", "Proszę podać godzinę czarteru, zaokrętowania lub wypłynięcia, a zaplanuję odbiór pod nią, żeby wolniejszy odcinek nigdy Pana/Pani nie poganiał."),
                ("Miejsce na Pana/Pani bagaż", "Walizki, prowiant i torby żeglarskie zmieszczą się w wygodnej Škodzie Superb, a ja pomogę przy załadunku i rozładunku."),
                ("Jeden lokalny kierowca", "Załatwia Pan/Pani wszystko bezpośrednio ze mną, od rezerwacji do przyjazdu, telefonicznie, przez WhatsApp lub e-mail. Bez call center.")]
        faqs = [("Ile kosztuje transfer na trasie %s?" % rel,
                 "Stałe &euro;%d za pojazd do 4 pasażerów, w jedną stronę, z opłatami drogowymi, paliwem i bagażem w cenie. W obie strony &euro;%d." % (p, rp)),
                ("Czy odbiór jest możliwy prosto z mariny?",
                 "Tak. Spotykam Pana/Panią przy wejściu do mariny lub w recepcji i pomagam z bagażem, żeby przejść prosto z pomostu do pojazdu."),
                ("Czy można dopasować transfer do mojego rejsu?",
                 "Tak. Proszę przesłać godzinę czarteru, zaokrętowania lub wypłynięcia przy rezerwacji, a zaplanuję odbiór pod nią."),
                ("Z jakim wyprzedzeniem rezerwować?",
                 "Co najmniej 2 godziny wcześniej, żebym potwierdził pojazd i godzinę odbioru. Na szybszy kurs zadzwoń lub napisz na WhatsApp.")]
    elif typ == "city":
        heading = "Prywatny transfer, trasa %s" % rel
        tagline = "Taxi i prywatny transfer w stałej cenie, trasa %s, od drzwi do drzwi." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Potrzebujesz pewnego transferu na trasie %s? Oferuję taxi i prywatny transfer w stałej cenie, od drzwi do drzwi, wygodną Škodą Superb. "
                     "Odbieram Cię spod dokładnego adresu i wiozę prosto do celu, bez niechcianych postojów i bez współpasażerów. "
                     "Cena jest stała, &euro;%d za cały pojazd, do 4 pasażerów, ustalona przed wyjazdem, opłaty drogowe i bagaż w cenie. "
                     "Wycena powyżej jest wypełniona dla tej trasy, więc rezerwacja to kilka kliknięć." % (rel, p))
        else:
            intro = ("Szukasz taxi na trasie %s bez taksometru i bez zachodu? To prywatny transfer w stałej cenie z jednym lokalnym kierowcą. "
                     "Odbieram Cię spod drzwi i wiozę wygodnie do celu, z bagażem, w cenie ryczałtowej &euro;%d za pojazd do 4 pasażerów. "
                     "Dla par i rodzin często wychodzi taniej niż osobne bilety autobusowe czy kolejowe, a zawsze jest szybciej i od drzwi do drzwi. "
                     "Wycena powyżej jest już ustawiona dla tej trasy." % (rel, p))
        whys = [("Stała cena &euro;%d" % p, "Jedna cena za pojazd do 4 pasażerów, ustalona z góry. Opłaty drogowe, paliwo i bagaż w cenie, bez taksometru."),
                ("Od drzwi do drzwi", "Odbieram Cię spod dokładnego adresu i zostawiam pod drzwiami celu. Bez dworców, bez przesiadek."),
                ("Jeden lokalny kierowca", "Załatwiasz wszystko bezpośrednio ze mną, od rezerwacji do przyjazdu, telefonicznie, przez WhatsApp lub e-mail. Bez call center."),
                ("Postoje na życzenie", "Na dłuższych trasach chętnie zatrzymam się na kawę, zdjęcie albo krótką atrakcję po drodze.")]
        faqs = [("Ile kosztuje taxi na trasie %s?" % rel,
                 "Stałe &euro;%d za pojazd do 4 pasażerów, w jedną stronę, z opłatami drogowymi, paliwem i bagażem. W obie strony &euro;%d." % (p, rp)),
                ("Transfer jest prywatny czy współdzielony?",
                 "Każdy transfer jest prywatny i od drzwi do drzwi, Škodą Superb. Bez dzielenia pojazdu i bez dodatkowych postojów, chyba że o nie poprosisz."),
                ("Czy możesz zatrzymać się po drodze?",
                 "Tak. Na dłuższych trasach chętnie zatrzymam się na kawę, zdjęcie albo krótką atrakcję. Wystarczy powiedzieć przy rezerwacji."),
                ("Z jakim wyprzedzeniem rezerwować?",
                 "Co najmniej 2 godziny wcześniej, żebym potwierdził pojazd i godzinę odbioru. Na szybki kurs zadzwoń lub napisz na WhatsApp.")]
    else:
        heading = "Prywatne taxi, trasa %s" % rel
        tagline = "Taxi i prywatny transfer w stałej cenie, trasa %s, od drzwi do drzwi." % rel
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Podróżujesz na trasie %s? Prowadzę taxi i prywatny transfer w stałej cenie, z odbiorem spod Twoich drzwi i dowozem dokładnie tam, gdzie trzeba. "
                     "Cena jest ryczałtowa, &euro;%d za cały pojazd, do 4 pasażerów, bez taksometru i bez czekania na postoju. "
                     "Wygodna Škoda Superb, miejsce na bagaż i jeden lokalny kierowca, którego rezerwujesz bezpośrednio. "
                     "Wycena powyżej jest wypełniona dla tej trasy." % (rel, p))
        else:
            intro = ("Potrzebujesz taxi na trasie %s? Oferuję prywatny transfer od drzwi do drzwi w stałej cenie &euro;%d za cały pojazd, do 4 pasażerów. "
                     "Przyjeżdżam pod Twój adres o ustalonej godzinie, więc nigdy nie czekasz przy drodze, i wiozę Cię wygodnie do celu. "
                     "Bez taksometru, bez niespodzianek, tylko jeden lokalny kierowca od rezerwacji do przyjazdu. Wycena powyżej jest już ustawiona dla tej trasy." % (rel, p))
        whys = [("Stała cena &euro;%d" % p, "Jedna cena za pojazd do 4 pasażerów, ustalona przed podróżą. Bez taksometru, bez niespodzianek."),
                ("Od drzwi do drzwi", "Odbiór spod Twojego adresu i dowóz pod drzwi celu, razem z bagażem."),
                ("Bez postoju", "Rezerwacja z wyprzedzeniem, więc nigdy nie czekasz na przejeżdżające taxi. Przyjeżdżam do Ciebie."),
                ("Jeden lokalny kierowca", "Załatwiasz wszystko bezpośrednio ze mną, od rezerwacji do przyjazdu, telefonicznie, przez WhatsApp lub e-mail.")]
        faqs = [("Ile kosztuje taxi na trasie %s?" % rel,
                 "Stałe &euro;%d za pojazd do 4 pasażerów, w jedną stronę, bagaż w cenie. W obie strony &euro;%d." % (p, rp)),
                ("Skąd mnie odbierasz?",
                 "Spod Twojego dokładnego adresu, czy to dom, hotel czy apartament. Prześlij adres przy rezerwacji, a potwierdzę miejsce spotkania."),
                ("Z jakim wyprzedzeniem rezerwować?",
                 "Co najmniej 2 godziny wcześniej, żebym potwierdził pojazd i godzinę odbioru. Na szybki kurs zadzwoń lub napisz na WhatsApp.")]

    if dd:
        faqs = [("Jak długa jest trasa i ile trwa przejazd?",
                 "Przejazd na trasie %s to około %d km i trwa mniej więcej %s przy normalnym ruchu, nieco dłużej w szczycie sezonu latem. Planuję odbiór tak, żeby wolniejszy odcinek nigdy Cię nie poganiał." % (rel, dist_km, dist_t))] + faqs

    why_html = "\n".join('        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t) for h, t in whys)

    wa = "https://wa.me/385994471013?text=" + quote(
        "Cześć Antonio, chciałbym zarezerwować transfer %s (€%d).\n"
        "Moje dane:\n- Data odbioru: \n- Godzina odbioru: \n- Pasażerowie: \n- Adres odbioru: \n- Moje imię: " % (rel, p))
    trust_line = ("Natychmiastowe potwierdzenie e-mailem &middot; Bez ukrytych opłat &middot; Monitorowanie lotu w cenie"
                  if typ in ("to_airport", "from_airport")
                  else "Natychmiastowe potwierdzenie e-mailem &middot; Bez ukrytych opłat &middot; Stała cena, bez taksometru")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s: Škoda Superb TAXI Antonio na dalmatyńskim wybrzeżu" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d za pojazd &middot; do 4 pasażerów</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Zarezerwuj</a>
          <a class="btn btn-secondary" href="%s">Rezerwuj przez WhatsApp</a>
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
      <span class="eyebrow center">Dlaczego warto zarezerwować ten transfer</span>
      <h2 class="section-title">Dlaczego warto zarezerwować taxi %s u Antonio?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">Cena %s</h2>
      <p class="section-subtitle">Stała cena za pojazd, do 4 pasażerów, bagaż w cenie. Ta sama cena obowiązuje w drugą stronę.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">W jedną stronę</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">W obie strony</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Zaliczka na potwierdzenie</div></div>
        <div class="route-fact"><div class="rf-value">Gotówka lub karta</div><div class="rf-label">Reszta w dniu przejazdu</div></div>
      </div>
      <p class="hub-note">Zaliczka 20%% (minimum &euro;20) potwierdza rezerwację, resztę płacisz w dniu przejazdu, gotówką lub kartą. Podróżujesz w drugą stronę? Zobacz %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Opinie</span>
      <h2 class="section-title">Co mówią pasażerowie</h2>
      <p class="section-subtitle">Prawdziwe opinie prawdziwych pasażerów.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s: częste pytania</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Zarezerwuj transfer %s</h2>
      <p class="section-subtitle">Stała cena &euro;%d za pojazd, do 4 pasażerów. Potwierdź w kilku kliknięciach.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Zarezerwuj</a>
        <a href="%s" class="btn btn-secondary">Rezerwuj przez WhatsApp</a>
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

    desc = ("Taxi i prywatny transfer, trasa %s. Stała cena &euro;%d za pojazd, do 4 pasażerów, od drzwi do drzwi. Rezerwuj bezpośrednio u Antonio." % (rel, p))
    if len(desc) > 158:
        desc = "Taxi i prywatny transfer, trasa %s. Stała cena &euro;%d za pojazd, do 4. Rezerwuj u Antonio." % (rel, p)
    keywords = "taxi %s, transfer %s, transfer lotniskowy %s" % (rel.lower(), rel.lower(), rel.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "serviceType": "Prywatny transfer taxi",
         "name": "Taxi %s" % rel,
         "description": "Taxi i prywatny transfer w stałej cenie, trasa %s, %d euro za pojazd do 4 pasażerów, od drzwi do drzwi." % (rel, p),
         "provider": PROVIDER, "areaServed": [pfr, pto],
         "url": "https://taxisibenik.hr/pl/%s/" % plslug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "Prywatny przejazd w jedną stronę, trasa %s, za pojazd do 4 pasażerów. W obie strony %d euro." % (rel, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": plslug, "title": "Taxi %s | Stała cena €%d | TAXI Antonio" % (rel, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}
    outdir = os.path.join(PAGES, slug, "pl")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"marina":0,"city":0,"local":0}; skipped=0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None: skipped += 1; continue
    made[build(frm, to, slug)] += 1
print("generated pl:", sum(made.values()), made, "| skipped:", skipped)
