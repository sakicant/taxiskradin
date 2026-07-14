# -*- coding: utf-8 -*-
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

# Real road distance/time from OSRM (docs/route-distances.json), keyed "From|To".
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

PROVIDER = {
    "@type": "LocalBusiness", "name": "Taxi Antonio",
    "telephone": "+385994471013", "email": "info@taxisibenik.hr",
    "address": {"@type": "PostalAddress", "addressLocality": "Šibenik", "addressCountry": "HR"},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "142"},
}

def vhash(slug, n):
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n

# --- parse route list ---
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
    return "/book/?from=%s&to=%s&price=%s&trip=oneway&pax=1&lug=1" % (bkey(frm), bkey(to), price)

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
    rev = slug_of.get((to, frm))
    revlink = ('<a href="/%s/">%s to %s</a>' % (rev, to, frm)) if rev else ("%s to %s" % (to, frm))
    book = book_link(frm, to, p)

    dd = DIST.get("%s|%s" % (frm, to))
    dist_km = dd["km"] if dd else None
    dist_t = fmt_time(dd["sec"]) if dd else None
    if dd:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fixed, one way</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">Distance</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">Drive time</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Return</div></div>'
            % (p, dist_km, dist_t, rp))
    else:
        facts_html = (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Fixed, one way</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Return</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Up to 4</div><div class="rf-label">Passengers</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">Private, door to door</div></div>'
            % (p, rp))

    # ---- direction/type-specific copy ----
    if typ == "to_airport":
        city = AIRPORT_CITY[to]
        heading = "Your Private Taxi and Transfer to %s" % to
        tagline = "Fixed-price private taxi and transfer from %s to %s. &euro;%d per car, up to 4 passengers, straight to departures." % (frm, to, p)
        intro = ("Flying out of %s? A taxi or private transfer from %s to %s is the simple, stress-free way to make your flight. "
                 "I am Antonio, a local Šibenik driver, and I collect you at your door in %s and drive you straight to the departures terminal "
                 "in a comfortable Škoda Superb. The price is fixed at &euro;%d for the whole car, up to 4 passengers, agreed before you travel, "
                 "with no meter and no surprises. I plan the pickup around your flight time and get you there with time to check in. "
                 "The quote form above is already filled in for this route, so you can see the price and book in a couple of taps."
                 % (city, frm, to, frm, p))
        whys = [("Fixed &euro;%d Price" % p, "One price for the whole car, up to 4 passengers, agreed upfront. Tolls, fuel and luggage included, no meter."),
                ("Planned Around Your Flight", "Tell me your departure time and I work back from it, so you reach the terminal with room to check in."),
                ("Door to Departures", "Pickup at your %s address and drop-off right at the %s departures entrance." % (frm, to)),
                ("Any Hour", "Early-morning and late-night flights are no problem. I run around the clock for a price fixed in advance.")]
        faqs = [("How much is a taxi from %s to %s?" % (frm, to),
                 "A fixed &euro;%d per car, one way, for up to 4 passengers. The price is per vehicle, not per person, and includes tolls, fuel and luggage. A return trip is &euro;%d." % (p, rp)),
                ("What time should I leave %s for my flight?" % frm,
                 "As a rule, about 3 hours before an international flight and 2 hours before a domestic one. Tell me your flight time and I will confirm the exact pickup."),
                ("Do you drop us right at the departures terminal?",
                 "Yes. I take you straight to the departures drop-off at %s and help with your luggage. No parking walk, no shuttle." % to),
                ("How far in advance should I book?",
                 "At least 2 hours ahead so I can confirm the car and your pickup, and earlier for early-morning flights and high season. For a sooner ride, call or WhatsApp me directly.")]
    elif typ == "from_airport":
        city = AIRPORT_CITY[frm]
        heading = "Your Airport Pickup and Transfer to %s" % to
        tagline = "Private airport pickup and transfer from %s to %s. &euro;%d per car, up to 4, meet-and-greet with your flight tracked." % (frm, to, p)
        intro = ("Just landed at %s? A private transfer from %s to %s takes the stress out of arrival. I meet you in the arrivals hall with a name sign, "
                 "help with your luggage and drive you straight to %s in a comfortable Škoda Superb, at a fixed &euro;%d for the whole car, up to 4 passengers. "
                 "I track your flight in real time, so whether you land early or late I am there when you come out. No taxi queue, no shared shuttle, no surge pricing. "
                 "The quote form above is already filled in for this route, so you can see the price and book in a couple of taps."
                 % (city, frm, to, to, p))
        whys = [("Meet and Greet", "I wait in the arrivals hall with a name sign and help with your bags, so you walk straight to the car."),
                ("Flight Tracked", "I watch your flight in real time and adjust to early landings or delays, with free waiting time."),
                ("Fixed &euro;%d Price" % p, "One price for the whole car, up to 4 passengers, agreed upfront. Tolls, fuel and luggage included, no meter."),
                ("Straight to Your Door", "No queue and no changes. I drive you directly to your address in %s." % to)]
        faqs = [("Where do you meet me at %s?" % frm,
                 "In the arrivals hall, just after baggage reclaim, holding a sign with your name. I help with the luggage and walk you to the car."),
                ("What if my flight is delayed?",
                 "No problem. I track your flight in real time and adjust the pickup to the actual landing, with no extra charge for the wait."),
                ("How much is the transfer from %s to %s?" % (frm, to),
                 "A fixed &euro;%d per car for up to 4 passengers, one way, tolls and luggage included. A return trip is &euro;%d." % (p, rp)),
                ("How far in advance should I book?",
                 "At least 2 hours ahead so I can plan around your flight. For a same-day pickup after a sudden change, call or WhatsApp me and I will help if I can.")]
    elif typ == "marina":
        heading = "Private Marina Transfer from %s to %s" % (frm, to)
        tagline = "Fixed-price private taxi and transfer from %s to %s. &euro;%d per car, up to 4 passengers, timed around your boat." % (frm, to, p)
        intro = ("Transferring between %s and %s? I run a private, fixed-price taxi and transfer for marina guests, timed around your boat and your travel plans. "
                 "I collect you with plenty of room for your luggage and drive you comfortably the whole way in a Škoda Superb, for a flat &euro;%d for the car, up to 4 passengers, agreed before you travel. "
                 "Whether you are joining your yacht or heading onward after stepping off it, there is no meter and no waiting at a rank, just one local driver you book directly. "
                 "This is a long-distance private transfer, not a short local hop, and the quote above is already set for this route, so booking takes a couple of taps."
                 % (frm, to, p))
        whys = [("Fixed &euro;%d Price" % p, "One price per car for up to 4 passengers, agreed upfront. Tolls, fuel and luggage included, no meter running."),
                ("Timed Around Your Boat", "Tell me your charter, check-in or departure time and I plan the pickup around it, so a slow patch never leaves you rushed."),
                ("Room for Your Luggage", "Suitcases, provisions and boat bags all fit in a comfortable Škoda Superb, with a hand loading and unloading."),
                ("One Local Driver", "You deal with me directly from booking to drop-off, by phone, WhatsApp or email. No call centre.")]
        faqs = [("How much is a transfer from %s to %s?" % (frm, to),
                 "A fixed &euro;%d per car for up to 4 passengers, one way, with tolls, fuel and luggage included. A return trip is &euro;%d." % (p, rp)),
                ("Can you collect right at the marina?",
                 "Yes. I meet you at the marina entrance or reception and help with your luggage, so you go straight from the pontoon to the car."),
                ("Can you time the transfer around my boat?",
                 "Yes. Send me your charter, check-in or departure time when you book and I plan the pickup around it."),
                ("How far in advance should I book?",
                 "At least 2 hours ahead so I can confirm the car and your pickup time. For a sooner ride, call or WhatsApp me directly.")]
    elif typ == "city":
        heading = "Private Transfer from %s to %s" % (frm, to)
        tagline = "Fixed-price private taxi and transfer from %s to %s. &euro;%d per car, up to 4 passengers, door to door." % (frm, to, p)
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Need a reliable transfer from %s to %s? I offer a private, fixed-price taxi and transfer, door to door, in a comfortable Škoda Superb. "
                     "I pick you up at your exact address in %s and take you straight to %s, with no stops you did not ask for and no shared passengers. "
                     "The price is a fixed &euro;%d for the whole car, up to 4 passengers, agreed before you set off, tolls and luggage included. "
                     "The quote above is filled in for this route, so you can see the price and book in a couple of taps."
                     % (frm, to, frm, to, p))
        else:
            intro = ("Looking for a taxi from %s to %s without the meter or the hassle? This is a private, fixed-price transfer with one local driver. "
                     "I collect you at the door in %s and drive you comfortably to %s, luggage and all, for a flat &euro;%d per car for up to 4 passengers. "
                     "For couples and families it often works out cheaper than separate bus or train tickets, and it is always faster and door to door. "
                     "The quote above is already set for this route, so booking takes a couple of taps."
                     % (frm, to, frm, to, p))
        whys = [("Fixed &euro;%d Price" % p, "One price per car for up to 4 passengers, agreed upfront. Tolls, fuel and luggage included, no meter running."),
                ("Door to Door", "I pick you up at your exact address in %s and drop you at the door in %s. No stations, no changes." % (frm, to)),
                ("One Local Driver", "You deal with me directly from booking to drop-off, by phone, WhatsApp or email. No call centre."),
                ("Stops on Request", "On the longer routes I am happy to stop for a coffee, a photo or a quick sight along the way.")]
        faqs = [("How much is a taxi from %s to %s?" % (frm, to),
                 "A fixed &euro;%d per car for up to 4 passengers, one way, with tolls, fuel and luggage included. A return trip is &euro;%d." % (p, rp)),
                ("Is the transfer private or shared?",
                 "Every transfer is private and door to door, in a Škoda Superb. No vehicle sharing and no extra stops unless you ask for them."),
                ("Can you stop along the way?",
                 "Yes. On the longer routes I am happy to stop for a coffee, a photo or a quick sight. Just let me know when booking."),
                ("How far in advance should I book?",
                 "At least 2 hours ahead so I can confirm the car and your pickup time. For a sooner ride, call or WhatsApp me directly.")]
    else:  # local
        heading = "Private Taxi from %s to %s" % (frm, to)
        tagline = "Fixed-price private taxi and transfer from %s to %s. &euro;%d per car, up to 4 passengers, door to door." % (frm, to, p)
        v = vhash(slug, 2)
        if v == 0:
            intro = ("Getting from %s to %s? I run a private, fixed-price taxi and transfer between the two, picking you up at your door in %s and "
                     "dropping you right where you need to be in %s. The price is a flat &euro;%d for the whole car, up to 4 passengers, with no meter and "
                     "no waiting at a rank. A comfortable Škoda Superb, room for your luggage, and one local driver you book directly. "
                     "The quote above is filled in for this route, so booking takes a couple of taps."
                     % (frm, to, frm, to, p))
        else:
            intro = ("Need a taxi from %s to %s? I offer a private, door-to-door transfer at a fixed &euro;%d for the whole car, up to 4 passengers. "
                     "I come to your address in %s at the agreed time, so you never wait at the roadside, and drive you comfortably to %s. "
                     "No meter, no surprises, just one local driver from booking to drop-off. The quote above is already set for this route."
                     % (frm, to, p, frm, to))
        whys = [("Fixed &euro;%d Price" % p, "One price per car for up to 4 passengers, agreed before you travel. No meter, no surprises."),
                ("Door to Door", "Pickup at your address in %s and drop-off at the door in %s, luggage and all." % (frm, to)),
                ("No Rank Needed", "Booked in advance, so you are never left waiting for a passing taxi. I come to you."),
                ("One Local Driver", "You deal with me directly from booking to drop-off, by phone, WhatsApp or email.")]
        faqs = [("How much is a taxi from %s to %s?" % (frm, to),
                 "A fixed &euro;%d per car for up to 4 passengers, one way, luggage included. A return trip is &euro;%d." % (p, rp)),
                ("Where do you pick up?",
                 "At your exact address in %s, whether a home, hotel or apartment. Send the address when you book and I will confirm the meeting point." % frm),
                ("How far in advance should I book?",
                 "At least 2 hours ahead so I can confirm the car and your pickup time. For a sooner ride, call or WhatsApp me directly.")]

    if dd:
        faqs = [("How far is %s from %s, and how long is the drive?" % (to, frm),
                 "The drive from %s to %s is around %d km and takes roughly %s in normal traffic, a little longer at busy times in summer. I plan the pickup so a slow patch never leaves you rushed." % (frm, to, dist_km, dist_t))] + faqs

    why_html = "\n".join(
        '        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t)
        for h, t in whys)

    tagline = re.sub(r'\. &euro;\d+ per car, up to 4(?: passengers)?,', ',', tagline)
    wa = "https://wa.me/385994471013?text=" + quote(
        "Hi Antonio, I would like to book the %s to %s transfer (€%d).\n"
        "My details:\n- Pickup date: \n- Pickup time: \n- Passengers: \n- Pickup address: \n- My name: " % (frm, to, p))
    trust_line = ("Instant confirmation by email &middot; No hidden fees &middot; Flight monitoring included"
                  if typ in ("to_airport", "from_airport")
                  else "Instant confirmation by email &middot; No hidden fees &middot; Fixed price, no meter")

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      <img src="/assets/img/hero-transfers.webp" alt="Taxi %s to %s: TAXI Antonio's Škoda Superb on the Dalmatian coast" loading="eager">
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>Taxi %s to %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d per car &middot; up to 4 passengers</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?3d034c475d3887585236cfe8dbc'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">Book now</a>
          <a class="btn btn-secondary" href="%s">Book through WhatsApp</a>
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
      <span class="eyebrow center">%s to %s</span>
      <h2 class="section-title">%s</h2>
      <p class="section-subtitle">%s</p>
    </div>
  </section>

  <section class="why-book">
    <div class="container">
      <span class="eyebrow center">Why Book This Transfer</span>
      <h2 class="section-title">Why Book Your %s to %s Taxi with Antonio?</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">%s to %s Price</h2>
      <p class="section-subtitle">Fixed per car, up to 4 passengers, luggage included. The same price applies in the opposite direction.</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">One way</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">Return</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">Advance to confirm</div></div>
        <div class="route-fact"><div class="rf-value">Cash or card</div><div class="rf-label">Balance on the day</div></div>
      </div>
      <p class="hub-note">A 20%% advance payment (minimum &euro;20) confirms your booking, and the balance is paid on the day, in cash or by card. Travelling the other way? See %s.</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">Reviews</span>
      <h2 class="section-title">What Passengers Say</h2>
      <p class="section-subtitle">Real reviews from real passengers.</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?4aa50a27517a87560776ec90a85'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">FAQ</span>
      <h2 class="section-title">Taxi %s to %s: Frequently Asked Questions</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">Reserve Your %s to %s Transfer</h2>
      <p class="section-subtitle">Fixed &euro;%d per car, up to 4 passengers. Confirm in a couple of taps.</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">Book now</a>
        <a href="%s" class="btn btn-secondary">Book through WhatsApp</a>
      </div>
    </div>
  </section>

{{RELATED_LINKS}}
''' % (frm, to,
       frm, to, tagline, p, book, wa, trust_line, facts_html,
       frm, to, heading, intro,
       frm, to, why_html,
       frm, to, p, rp, revlink,
       frm, to, faq_html(faqs),
       frm, to, p, book, wa)

    # meta
    desc = ("Private taxi and transfer from %s to %s. Fixed &euro;%d per car, up to 4 passengers, door to door. Book direct with Antonio." % (frm, to, p))
    if len(desc) > 154:
        desc = "Private taxi and transfer from %s to %s. Fixed &euro;%d per car, up to 4. Book direct with Antonio." % (frm, to, p)
    keywords = "taxi %s to %s, transfer %s to %s, %s to %s taxi, %s to %s transfer" % (
        frm.lower(), to.lower(), frm.lower(), to.lower(), frm.lower(), to.lower(), frm.lower(), to.lower())
    schema = [
        {"@context": "https://schema.org", "@type": "Service",
         "serviceType": "Private taxi transfer",
         "name": "Taxi %s to %s" % (frm, to),
         "description": "Private, fixed-price taxi and transfer from %s to %s, %d euros per car for up to 4 passengers, door to door." % (frm, to, p),
         "provider": PROVIDER,
         "areaServed": [frm, to],
         "url": "https://taxisibenik.hr/%s/" % slug,
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": "One-way private transfer from %s to %s, per car for up to 4 passengers. Return %d euros." % (frm, to, rp)}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": re.sub('&euro;', '', a).replace('&amp;', '&')}} for q, a in faqs]},
    ]
    meta = {"slug": slug, "title": "Taxi %s to %s | Fixed €%d Transfer | TAXI Antonio" % (frm, to, p),
            "description": desc.replace('&euro;', '€'), "keywords": keywords,
            "og_image": "https://taxisibenik.hr/assets/img/hero-transfers.webp", "schema": schema}

    outdir = os.path.join(PAGES, slug, "en")
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "content.html"), "w", encoding="utf-8").write(content)
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return typ

made = {"to_airport":0,"from_airport":0,"city":0,"local":0,"marina":0}
skipped_exist = 0; skipped_noprice = 0
for frm, to, slug in rows:
    if price(key(frm), key(to)) is None:
        skipped_noprice += 1; continue
    if slug == "taxi-sibenik-to-split-airport":  # hand-built template, keep as-is
        skipped_exist += 1; continue
    t = build(frm, to, slug)
    made[t] += 1
print("generated:", sum(made.values()), made)
print("skipped (already exist):", skipped_exist, "| skipped (no matrix price):", skipped_noprice)
