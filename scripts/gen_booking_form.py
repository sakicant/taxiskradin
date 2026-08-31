# -*- coding: utf-8 -*-
"""Regenerate the /book/ page for every language in the v3 layout.

Section order: 1 your trip, 2 your details, 3 payment, 4 transfer details,
then the terms checkbox. Reuses each language's EXISTING translated field
labels/placeholders (pulled by stable element id from the current
content.html) and injects the shared strings from scripts/booking_i18n.json.
Terms/Privacy link URLs and labels come from each page's meta.json.

    python scripts/gen_booking_form.py <site-root>

Fails loudly if an expected string cannot be extracted, so a structural change
never silently produces a broken page.
"""
import os, io, re, json, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
I18N = json.load(io.open(os.path.join(ROOT, 'scripts', 'booking_i18n.json'), encoding='utf-8'))
LANGS = list(I18N.keys())

PHONE = '+385994471013'


def rd(p):
    return io.open(p, encoding='utf-8').read()


def grab(pattern, text, label, flags=re.S):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit('  MISSING [%s]' % label)
    return m.group(1).strip()


def label_for(text, *fids):
    """Label text for the first id that is present (ids changed in v3)."""
    for fid in fids:
        m = re.search(r'<label for="%s">(.*?)</label>' % re.escape(fid), text, re.S)
        if m:
            return m.group(1).strip()
    raise SystemExit('  MISSING [label %s]' % ' / '.join(fids))


def placeholder_of(text, fid):
    return grab(r'id="%s"[^>]*?placeholder="([^"]*)"' % re.escape(fid), text, 'placeholder ' + fid)


def strip_flag(s):
    return re.sub(r'\s*<span class="field-flag".*?</span>\s*', '', s, flags=re.S).strip()


def page_url_label(lang, page_dir):
    meta = json.load(io.open(os.path.join(ROOT, 'src', 'pages', page_dir, lang, 'meta.json'), encoding='utf-8'))
    slug = meta['slug']
    title = (meta.get('title', '') or '').split('|')[0].strip()
    url = ('/%s/' % slug) if lang == 'en' else ('/%s/%s/' % (lang, slug))
    return url, title


TIME_SCRIPT = """  <script>
  (function(){
    var o='';
    for(var h=0;h<24;h++){for(var m=0;m<60;m+=5){var t=(h<10?'0':'')+h+':'+(m<10?'0':'')+m;o+='<option value="'+t+'">'+t+'</option>';}}
    ['book-time','book-return-time'].forEach(function(id){var s=document.getElementById(id);if(s)s.insertAdjacentHTML('beforeend',o);});
  })();
  </script>
"""


def build(lang):
    src = os.path.join(ROOT, 'src', 'pages', 'book', lang, 'content.html')
    text = rd(src)
    t = I18N[lang]

    eyebrow = grab(r'<span class="eyebrow">(.*?)</span>', text, 'eyebrow')
    h1 = grab(r'<h1>(.*?)</h1>', text, 'h1')
    sub = grab(r'<p class="page-hero-sub">(.*?)</p>', text, 'hero sub')

    sec1 = re.sub(r'^\s*\d+\.\s*', '', grab(r'<h3>(.*?)</h3>', text, 'first h3'))
    from_l = label_for(text, 'book-from');   from_ph = placeholder_of(text, 'book-from')
    to_l = label_for(text, 'book-to');       to_ph = placeholder_of(text, 'book-to')
    trip_l = label_for(text, 'book-trip')
    oneway = grab(r'<option value="oneway">(.*?)</option>', text, 'oneway option')
    retopt = grab(r'<option value="return">(.*?)</option>', text, 'return option')
    pax_l = label_for(text, 'book-pax');     lug_l = label_for(text, 'book-lug')
    price_inner = grab(r'<p class="booking-price-line"[^>]*>(.*?)</p>', text, 'price line')
    date_l = label_for(text, 'book-date');   time_l = label_for(text, 'book-time')
    rdate_l = label_for(text, 'book-return-date'); rtime_l = label_for(text, 'book-return-time')
    flight_l = label_for(text, 'book-flight');     flight_ph = placeholder_of(text, 'book-flight')
    dropoff_l = label_for(text, 'book-dropoff-details'); dropoff_ph = placeholder_of(text, 'book-dropoff-details')
    notes_l = label_for(text, 'book-notes');       notes_ph = placeholder_of(text, 'book-notes')
    email_l = strip_flag(label_for(text, 'book-email'))
    phone_l = strip_flag(label_for(text, 'book-phone-cc', 'book-phone'))
    submit = grab(r'<button type="submit"[^>]*>(.*?)</button>', text, 'submit button')
    wa_href = grab(r'href="(https://wa\.me/[^"]*)"', text, 'whatsapp href')

    terms_url, terms_label = page_url_label(lang, 'terms-and-conditions')
    priv_url, priv_label = page_url_label(lang, 'privacy-policy')
    consent = (t['consent_text']
               .replace('{terms}', '<a href="%s">%s</a>' % (terms_url, terms_label))
               .replace('{privacy}', '<a href="%s">%s</a>' % (priv_url, priv_label)))
    call_link = '<a href="tel:%s">%s</a>' % (PHONE, t['call_label'])
    wa_link = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (wa_href, t['wa_label'])
    hint = (t['hint_text'].replace('{call}', call_link).replace('{wa}', wa_link))

    hero = (
        '  <section class="page-hero">\n'
        '    <div class="container">\n'
        '      <span class="eyebrow">%s</span>\n'
        '      <h1>%s</h1>\n'
        '      <p class="page-hero-sub">%s</p>\n'
        '    </div>\n'
        '  </section>\n\n'
    ) % (eyebrow, h1, sub)

    form = (
        '  <section class="page-content">\n'
        '    <div class="container booking-page">\n'
        '      <form class="booking-form" id="booking-page-form" action="/booking-submit.php" method="POST" data-req-label="%(req)s" data-opt-label="%(opt)s">\n\n'
        '        <h3>1. %(sec1)s</h3>\n'
        '        <p class="booking-section-hint">%(trip_hint)s</p>\n\n'
        '        <label for="book-from">%(from_l)s</label>\n'
        '        <input type="text" id="book-from" name="from" required placeholder="%(from_ph)s">\n\n'
        '        <label for="book-to">%(to_l)s</label>\n'
        '        <input type="text" id="book-to" name="to" required placeholder="%(to_ph)s">\n\n'
        '        <div class="quote-field">\n'
        '          <label for="book-trip">%(trip_l)s</label>\n'
        '          <select id="book-trip" name="trip">\n'
        '            <option value="oneway">%(oneway)s</option>\n'
        '            <option value="return">%(retopt)s</option>\n'
        '          </select>\n'
        '        </div>\n'
        '        <div class="quote-field-row">\n'
        '          <div class="quote-field">\n'
        '            <label for="book-pax">%(pax_l)s</label>\n'
        '            <input type="number" id="book-pax" name="passengers" min="1" max="12" value="1" required>\n'
        '          </div>\n'
        '          <div class="quote-field">\n'
        '            <label for="book-lug">%(lug_l)s</label>\n'
        '            <input type="number" id="book-lug" name="luggage" min="0" max="12" value="1" required>\n'
        '          </div>\n'
        '        </div>\n\n'
        '        <p class="booking-price-line" id="booking-price-line" hidden>%(price_inner)s</p>\n\n'
        '        <div class="quote-field-row">\n'
        '          <div class="quote-field">\n'
        '            <label for="book-date">%(date_l)s</label>\n'
        '            <input type="date" id="book-date" name="book-date" required>\n'
        '          </div>\n'
        '          <div class="quote-field">\n'
        '            <label for="book-time">%(time_l)s</label>\n'
        '            <select id="book-time" name="book-time" required><option value="">--:--</option></select>\n'
        '          </div>\n'
        '        </div>\n'
        '        <p class="form-hint form-hint-center">%(hint)s</p>\n\n'
        '        <div class="quote-field-row" id="book-return-fields" hidden>\n'
        '          <div class="quote-field">\n'
        '            <label for="book-return-date">%(rdate_l)s</label>\n'
        '            <input type="date" id="book-return-date" name="book-return-date">\n'
        '          </div>\n'
        '          <div class="quote-field">\n'
        '            <label for="book-return-time">%(rtime_l)s</label>\n'
        '            <select id="book-return-time" name="book-return-time"><option value="">--:--</option></select>\n'
        '          </div>\n'
        '        </div>\n\n'
        '        <h3>2. %(details_section)s</h3>\n\n'
        '        <label for="book-name">%(name_label)s</label>\n'
        '        <input type="text" id="book-name" name="name" required>\n\n'
        '        <div class="form-choice" role="group" aria-labelledby="contact-method-legend">\n'
        '          <span class="form-choice-legend" id="contact-method-legend">%(contact_legend)s</span>\n'
        '          <div class="form-choice-options">\n'
        '            <label class="form-choice-option">\n'
        '              <input type="radio" name="contact_method" value="email" required>\n'
        '              <span>%(email_l)s</span>\n'
        '            </label>\n'
        '            <label class="form-choice-option">\n'
        '              <input type="radio" name="contact_method" value="whatsapp" required>\n'
        '              <span>WhatsApp</span>\n'
        '            </label>\n'
        '          </div>\n'
        '        </div>\n\n'
        '        <label for="book-email">%(email_l)s <span class="field-flag" id="email-flag"></span></label>\n'
        '        <input type="email" id="book-email" name="email">\n\n'
        '        <label for="book-phone-cc">%(phone_l)s <span class="field-flag" id="phone-flag"></span></label>\n'
        '        <div class="phone-row">\n'
        '          <select id="book-phone-cc" name="phone_cc"><option value="">%(country_label)s</option></select>\n'
        '          <input type="tel" id="book-phone" name="phone" placeholder="%(phone_ph)s" inputmode="tel">\n'
        '        </div>\n'
        '        <p class="form-subhint">%(phone_subhint)s</p>\n\n'
        '        <h3>3. %(payment_section)s</h3>\n\n'
        '        <div class="form-choice" role="group" aria-labelledby="payment-legend">\n'
        '          <span class="form-choice-legend" id="payment-legend">%(pay_legend)s</span>\n'
        '          <div class="form-choice-options">\n'
        '            <label class="form-choice-option">\n'
        '              <input type="radio" name="payment_option" value="deposit" required>\n'
        '              <span>%(deposit_label)s<span class="opt-sub">%(deposit_sub)s</span></span>\n'
        '            </label>\n'
        '          </div>\n'
        '        </div>\n\n'
        '        <label class="form-consent">\n'
        '          <input type="checkbox" id="book-invoice" name="invoice_required" value="1">\n'
        '          <span>%(invoice_label)s</span>\n'
        '        </label>\n\n'
        '        <div id="book-invoice-fields" class="invoice-fields" hidden>\n'
        '          <label for="book-co-name">%(co_name)s</label>\n'
        '          <input type="text" id="book-co-name" name="company_name" autocomplete="organization">\n\n'
        '          <label for="book-co-vat">%(co_vat)s</label>\n'
        '          <input type="text" id="book-co-vat" name="company_vat">\n\n'
        '          <label for="book-co-address">%(co_address)s</label>\n'
        '          <input type="text" id="book-co-address" name="company_address" autocomplete="street-address">\n\n'
        '          <div class="quote-field-row">\n'
        '            <div class="quote-field">\n'
        '              <label for="book-co-zip">%(co_zip)s</label>\n'
        '              <input type="text" id="book-co-zip" name="company_zip" autocomplete="postal-code">\n'
        '            </div>\n'
        '            <div class="quote-field">\n'
        '              <label for="book-co-city">%(co_city)s</label>\n'
        '              <input type="text" id="book-co-city" name="company_city" autocomplete="address-level2">\n'
        '            </div>\n'
        '          </div>\n'
        '        </div>\n\n'
        '        <h3>4. %(transfer_section)s</h3>\n\n'
        '        <label for="book-flight">%(flight_l)s</label>\n'
        '        <input type="text" id="book-flight" name="book-flight" placeholder="%(flight_ph)s">\n\n'
        '        <label for="book-dropoff-details">%(dropoff_l)s</label>\n'
        '        <input type="text" id="book-dropoff-details" name="book-dropoff-details" placeholder="%(dropoff_ph)s">\n\n'
        '        <label for="book-notes">%(notes_l)s</label>\n'
        '        <textarea id="book-notes" name="book-notes" rows="4" placeholder="%(notes_ph)s"></textarea>\n\n'
        '        <input type="text" id="book-company" name="company" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">\n\n'
        '        <label class="form-consent">\n'
        '          <input type="checkbox" id="book-consent" name="consent" value="1" required>\n'
        '          <span>%(consent)s</span>\n'
        '        </label>\n'
        '        <button type="submit" class="btn btn-primary">%(submit)s</button>\n'
        '        <p class="form-note" id="booking-page-note"></p>\n'
        '      </form>\n'
        '    </div>\n'
        '  </section>\n'
    ) % {
        'req': t['req_word'], 'opt': t['opt_word'],
        'sec1': sec1, 'trip_hint': t['trip_hint'],
        'from_l': from_l, 'from_ph': from_ph, 'to_l': to_l, 'to_ph': to_ph,
        'trip_l': trip_l, 'oneway': oneway, 'retopt': retopt,
        'pax_l': pax_l, 'lug_l': lug_l, 'price_inner': price_inner,
        'date_l': date_l, 'time_l': time_l, 'hint': hint,
        'rdate_l': rdate_l, 'rtime_l': rtime_l,
        'details_section': t['details_section'], 'name_label': t['name_label'],
        'contact_legend': t['contact_legend'], 'email_l': email_l,
        'phone_l': phone_l, 'country_label': t['country_label'],
        'phone_ph': t['phone_ph'], 'phone_subhint': t['phone_subhint'],
        'payment_section': t['payment_section'], 'pay_legend': t['pay_legend'],
        'deposit_label': t['deposit_label'], 'deposit_sub': t['deposit_sub'],
        'invoice_label': t['invoice_label'],
        'co_name': t['co_name'], 'co_vat': t['co_vat'], 'co_address': t['co_address'],
        'co_zip': t['co_zip'], 'co_city': t['co_city'],
        'transfer_section': t['transfer_section'],
        'flight_l': flight_l, 'flight_ph': flight_ph,
        'dropoff_l': dropoff_l, 'dropoff_ph': dropoff_ph,
        'notes_l': notes_l, 'notes_ph': notes_ph,
        'consent': consent, 'submit': submit,
    }

    return hero + form + TIME_SCRIPT


def main():
    for lang in LANGS:
        out = build(lang)
        dest = os.path.join(ROOT, 'src', 'pages', 'book', lang, 'content.html')
        tmp = dest + '.tmp'
        io.open(tmp, 'w', encoding='utf-8', newline='').write(out)
        os.replace(tmp, dest)
        print('  wrote', lang)
    print('done:', len(LANGS), 'booking pages')


if __name__ == '__main__':
    main()
