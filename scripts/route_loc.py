# -*- coding: utf-8 -*-
"""Shared localization engine for route pages, used by BOTH taxiskradin.hr and
taxisibenik.hr.

`TR[lang]` holds every translatable string for a route page. `build_page(lang,
ctx)` assembles the content.html + meta.json for one route in one language,
using route-phrasing "A - B" (ctx['rel']) so place names stay in the nominative
and no declension table is needed.

Site-specific bits (hero image, trustindex ids, book-link prefix, domain,
provider) are passed in via `ctx`, so the same strings serve both sites.

WhatsApp rule (owner): the prefilled wa.me message is ENGLISH for every language
EXCEPT hr and sr, which stay Croatian. The message always embeds the route and
price so it is a custom message per page.
"""
import os, json
from urllib.parse import quote

AIRPORTS = ["Split Airport", "Zadar Airport", "Zagreb Airport", "Dubrovnik Airport"]

_I18N_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n")

# Languages whose prefilled WhatsApp message stays Croatian.
WA_CROATIAN = ("hr", "sr")


def _wa(lang, frm, to, rel, p):
    if lang in WA_CROATIAN:
        txt = ("Pozdrav Antonio, želio bih rezervirati transfer %s (€%d).\n"
               "Moji podaci:\n- Datum polaska: \n- Vrijeme polaska: \n"
               "- Broj putnika: \n- Adresa preuzimanja: \n- Moje ime: " % (rel, p))
    else:
        txt = ("Hi Antonio, I would like to book the %s to %s transfer (€%d).\n"
               "My details:\n- Pickup date: \n- Pickup time: \n"
               "- Passengers: \n- Pickup address: \n- My name: " % (frm, to, p))
    return "https://wa.me/385994471013?text=" + quote(txt)


def slug_for(lang, en_slug):
    """Localized slug: drop '-to-' and map the airport slug fragments."""
    s = en_slug.replace("-to-", "-")
    for a, b in TR[lang]["airport_slug"].items():
        s = s.replace(a, b)
    return s


def name_for(lang, name):
    return TR[lang]["airport_name"].get(name, name)


def _facts_html(tr, ctx):
    p, rp = ctx["p"], ctx["rp"]
    if ctx["dd"]:
        return (
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">%s</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%d km</div><div class="rf-label">%s</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">~%s</div><div class="rf-label">%s</div></div>\n'
            '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">%s</div></div>'
            % (p, tr["rf_fixed_oneway_lbl"], ctx["km"], tr["rf_distance_lbl"],
               ctx["t"], tr["rf_drivetime_lbl"], rp, tr["rf_return_lbl"]))
    return (
        '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">%s</div></div>\n'
        '        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">%s</div></div>\n'
        '        <div class="route-fact"><div class="rf-value">%s</div><div class="rf-label">%s</div></div>\n'
        '        <div class="route-fact"><div class="rf-value">Škoda Superb</div><div class="rf-label">%s</div></div>'
        % (p, tr["rf_fixed_oneway_lbl"], rp, tr["rf_return_lbl"],
           tr["rf_upto4_val"], tr["rf_upto4_lbl"], tr["rf_skoda_lbl"]))


def _faq_html(items):
    return "\n".join(
        '          <div class="faq-item">\n            <h4>%s</h4>\n            <p>%s</p>\n          </div>' % (q, a)
        for q, a in items)


def build_page(lang, ctx):
    """Return (content_html, meta_dict) for one route in one language."""
    tr = TR[lang]
    rel = ctx["rel"]
    p, rp = ctx["p"], ctx["rp"]
    typ = ctx["typ"]
    fmt = dict(rel=rel, p=p, rp=rp, city=ctx.get("city", ""),
               km=ctx.get("km") or 0, t=ctx.get("t") or "", rell=rel.lower())

    def F(s):
        return s.format(**fmt)

    block = tr["types"][typ]
    heading = F(block["heading"])
    tagline = F(block["tagline"])
    if typ in ("city", "local"):
        intro = F(block["intro0"] if ctx["v"] == 0 else block["intro1"])
    else:
        intro = F(block["intro"])
    whys = [(F(h), F(x)) for h, x in block["whys"]]
    faqs = [(F(q), F(a)) for q, a in block["faqs"]]
    if ctx["dd"]:
        faqs = [(F(tr["dist_faq_q"]), F(tr["dist_faq_a"]))] + faqs

    why_html = "\n".join(
        '        <div class="why-book-item">\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (h, t)
        for h, t in whys)

    wa = _wa(lang, ctx["frm"], ctx["to"], rel, p)
    trust_line = tr["trust_air"] if typ in ("to_airport", "from_airport") else tr["trust_generic"]
    hub_note = tr["hub_note"].format(revlink=ctx["revlink_html"], **{k: v for k, v in fmt.items() if k != "rell"})

    content = '''  <section id="hero" class="hero daytrip-hero">
    <div class="hero-bg">
      %s
      <div class="hero-overlay"></div>
    </div>
    <div class="container" id="book">
      <div class="hero-content">
        <h1>%s %s</h1>
        <p class="hero-tagline">%s</p>
        <p class="daytrip-price">&euro;%d %s</p>
        <div class="hero-trust">
          <script defer async src='https://cdn.trustindex.io/loader.js?%s'></script>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="%s">%s</a>
          <a class="btn btn-secondary" href="%s">%s</a>
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
      <span class="eyebrow center">%s</span>
      <h2 class="section-title">%s</h2>
      <div class="why-book-grid">
%s
      </div>
    </div>
  </section>

  <section class="hub-routes hub-routes-alt">
    <div class="container">
      <h2 class="section-title">%s</h2>
      <p class="section-subtitle">%s</p>
      <div class="route-facts">
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">%s</div></div>
        <div class="route-fact"><div class="rf-value">&euro;%d</div><div class="rf-label">%s</div></div>
        <div class="route-fact"><div class="rf-value">20%%</div><div class="rf-label">%s</div></div>
        <div class="route-fact"><div class="rf-value">%s</div><div class="rf-label">%s</div></div>
      </div>
      <p class="hub-note">%s</p>
    </div>
  </section>

  <section id="reviews" class="reviews">
    <div class="container">
      <span class="eyebrow center">%s</span>
      <h2 class="section-title">%s</h2>
      <p class="section-subtitle">%s</p>
      <div class="reviews-widget">
        <script defer async src='https://cdn.trustindex.io/loader.js?%s'></script>
      </div>
    </div>
  </section>

  <section id="faq" class="faq">
    <div class="container">
      <span class="eyebrow center">%s</span>
      <h2 class="section-title">%s</h2>
      <div class="faq-grid">
        <div class="faq-group">
%s
        </div>
      </div>
    </div>
  </section>

  <section class="daytrip-cta">
    <div class="container">
      <h2 class="section-title">%s</h2>
      <p class="section-subtitle">%s</p>
      <div class="hero-actions">
        <a href="%s" class="btn btn-primary">%s</a>
        <a href="%s" class="btn btn-secondary">%s</a>
      </div>
    </div>
  </section>

{{RELATED_LINKS}}
''' % (ctx["hero_html"],
       tr["taxi_word"], rel, tagline, p, tr["per_car"], ctx["ti_hero"],
       ctx["book_link"], tr["book_now"], wa, tr["book_wa"], trust_line,
       _facts_html(tr, ctx),
       rel, heading, intro,
       tr["why_eyebrow"], F(tr["why_title"]), why_html,
       F(tr["price_title"]), tr["price_sub"],
       p, tr["price_oneway_lbl"], rp, tr["price_return_lbl"],
       tr["price_advance_lbl"], tr["price_balance_val"], tr["price_balance_lbl"],
       hub_note,
       tr["reviews_eyebrow"], tr["reviews_title"], tr["reviews_sub"], ctx["ti_reviews"],
       tr["faq_eyebrow"], F(tr["faq_title"]), _faq_html(faqs),
       F(tr["cta_title"]), F(tr["cta_sub"]),
       ctx["book_link"], tr["book_now"], wa, tr["book_wa"])

    desc = F(tr["meta_desc"])
    if len(desc) > 155:
        desc = F(tr["meta_desc_short"])
    keywords = F(tr["keywords"])
    faq_schema_text = lambda a: a.replace("&euro;", "").replace("&amp;", "&").replace("&middot;", "-")
    schema = [
        {"@context": "https://schema.org", "@type": "Service",
         "serviceType": tr["schema_servicetype"],
         "name": F(tr["schema_name"]),
         "description": F(tr["schema_desc"]),
         "provider": ctx["provider"],
         "areaServed": [ctx["rel_from"], ctx["rel_to"]],
         "url": ctx["page_url"],
         "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                    "description": F(tr["schema_offer_desc"])}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": faq_schema_text(a)}} for q, a in faqs]},
    ]
    meta = {"slug": ctx["slug"],
            "title": F(tr["meta_title"]),
            "description": desc.replace("&euro;", "€"),
            "keywords": keywords,
            "og_image": ctx["og_image"], "schema": schema}
    return content, meta



# Translation tables are loaded from scripts/i18n/<lang>.json (one file per
# language). Drop a new file in to add a language; no code change needed.
TR = {}
for _f in sorted(os.listdir(_I18N_DIR)):
    if _f.endswith(".json"):
        TR[_f[:-5]] = json.load(open(os.path.join(_I18N_DIR, _f), encoding="utf-8"))
