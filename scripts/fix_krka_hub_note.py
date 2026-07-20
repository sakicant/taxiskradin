# -*- coding: utf-8 -*-
"""Repair the Krka hub's price note after the entrance route pages were dropped.

The hub originally linked to per-entrance route pages. Those were removed (a
15 EUR five-minute ride does not warrant its own page), so the note is rewritten
in every language to the deposit terms plus a single link to the Roski Slap
route page, which does still exist.

The Roski Slap link is written with the English slug; scripts/fix_page_links.py
then repoints it to each language's real slug. Run with --write.
"""
import os, io, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "src", "pages", "krka-national-park-transfers")
WRITE = "--write" in sys.argv

# deposit terms + "heading to the upper falls instead?" + link text
NOTE = {
 "en": ("A 20% advance payment (minimum &euro;20) confirms your booking, and the balance is paid on the day, in cash or by card. Heading to the quieter upper falls instead? See", "Skradin to Roški Slap"),
 "hr": ("Predujam od 20% (najmanje &euro;20) potvrđuje rezervaciju, a ostatak plaćate na dan vožnje, gotovinom ili karticom. Idete radije na mirniji gornji dio parka? Pogledajte", "Skradin - Roški Slap"),
 "de": ("Eine Anzahlung von 20% (mindestens &euro;20) bestätigt Ihre Buchung, den Rest zahlen Sie am Tag der Fahrt, bar oder mit Karte. Möchten Sie lieber zu den ruhigeren oberen Wasserfällen? Siehe", "Skradin - Roški Slap"),
 "pl": ("Zaliczka 20% (minimum &euro;20) potwierdza rezerwację, resztę płacisz w dniu przejazdu, gotówką lub kartą. Wolisz spokojniejsze górne wodospady? Zobacz", "Skradin - Roški Slap"),
 "cs": ("Záloha 20% (minimálně &euro;20) potvrzuje rezervaci, zbytek platíte v den jízdy, hotově nebo kartou. Chcete raději na klidnější horní vodopády? Podívejte se na", "Skradin - Roški Slap"),
 "it": ("Un anticipo del 20% (minimo &euro;20) conferma la prenotazione, il saldo si paga il giorno stesso, in contanti o con carta. Preferisce le cascate superiori, più tranquille? Vedi", "Skradin - Roški Slap"),
 "fr": ("Un acompte de 20% (minimum &euro;20) confirme votre réservation, le solde se règle le jour même, en espèces ou par carte. Vous préférez les chutes supérieures, plus calmes ? Voir", "Skradin - Roški Slap"),
 "nl": ("Een aanbetaling van 20% (minimaal &euro;20) bevestigt uw boeking, het saldo betaalt u op de dag zelf, contant of met kaart. Liever naar de rustigere bovenste watervallen? Zie", "Skradin - Roški Slap"),
 "sl": ("Predujem 20% (najmanj &euro;20) potrdi rezervacijo, ostalo plačate na dan vožnje, z gotovino ali kartico. Bi raje šli na mirnejše zgornje slapove? Poglejte", "Skradin - Roški Slap"),
 "hu": ("A 20% előleg (legalább &euro;20) megerősíti a foglalást, a fennmaradó összeget az út napján fizeti, készpénzzel vagy kártyával. Inkább a csendesebb felső vízeséseket nézné meg? Lásd", "Skradin - Roški Slap"),
 "sk": ("Záloha 20% (minimálne &euro;20) potvrdzuje rezerváciu, zvyšok platíte v deň jazdy, v hotovosti alebo kartou. Chcete radšej na pokojnejšie horné vodopády? Pozrite", "Skradin - Roški Slap"),
 "es": ("Un anticipo del 20% (mínimo &euro;20) confirma su reserva, y el resto se paga el mismo día, en efectivo o con tarjeta. ¿Prefiere las cascadas superiores, más tranquilas? Vea", "Skradin - Roški Slap"),
 "sv": ("En handpenning på 20% (minst &euro;20) bekräftar bokningen, resten betalas samma dag, kontant eller med kort. Vill du hellre till de lugnare övre fallen? Se", "Skradin - Roški Slap"),
 "sr": ("Avans od 20% (najmanje &euro;20) potvrđuje rezervaciju, a ostatak plaćate na dan vožnje, gotovinom ili karticom. Radije idete na mirniji gornji deo parka? Pogledajte", "Skradin - Roški Slap"),
 "no": ("Et forskudd på 20% (minimum &euro;20) bekrefter bestillingen, resten betales samme dag, kontant eller med kort. Vil du heller til de roligere øvre fossene? Se", "Skradin - Roški Slap"),
 "zh": ("支付 20%（最低 &euro;20）的预付款即可确认预订，余款在当天以现金或刷卡支付。想去更安静的上游瀑布吗？请看", "Skradin - Roški Slap"),
 "ko": ("20%(최소 &euro;20)의 예약금으로 예약이 확정되며, 잔금은 당일 현금 또는 카드로 결제합니다. 더 조용한 상류 폭포로 가시겠습니까? 다음을 참조하세요", "Skradin - Roški Slap"),
 "fi": ("20 prosentin ennakkomaksu (vähintään &euro;20) vahvistaa varauksen, ja loput maksetaan matkapäivänä käteisellä tai kortilla. Haluatko mieluummin rauhallisemmille yläputouksille? Katso", "Skradin - Roški Slap"),
 "ja": ("20%（最低 &euro;20）の前払いでご予約が確定し、残額は当日に現金またはカードでお支払いいただきます。より静かな上流の滝へ向かわれますか？こちらをご覧ください", "Skradin - Roški Slap"),
}

NOTE_RE = re.compile(r'<p class="hub-note">.*?</p>', re.DOTALL)
fixed, skipped, nolang = 0, 0, []

for lang in sorted(os.listdir(PAGE)):
    cp = os.path.join(PAGE, lang, "content.html")
    if not os.path.isfile(cp):
        continue
    if lang not in NOTE:
        nolang.append(lang)
        continue
    html = io.open(cp, encoding="utf-8", errors="ignore").read()
    if "krka-skradin-entrance" not in html and "krka-lozovac-entrance" not in html:
        skipped += 1
        continue
    lead, link_text = NOTE[lang]
    prefix = "" if lang == "en" else "/" + lang
    new_note = ('<p class="hub-note">%s <a href="%s/taxi-skradin-to-roski-slap/">%s</a>.</p>'
                % (lead, prefix, link_text))
    new_html, n = NOTE_RE.subn(new_note, html, count=1)
    if n != 1:
        nolang.append(lang + " (no hub-note found)")
        continue
    if WRITE:
        io.open(cp, "w", encoding="utf-8").write(new_html)
    fixed += 1

print("hub notes rewritten:", fixed)
print("already clean:", skipped)
if nolang:
    print("needs attention:", nolang)
if not WRITE:
    print("\n(dry run - nothing written. re-run with --write)")
