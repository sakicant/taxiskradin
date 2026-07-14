# taxisibenik.hr — Full SEO Structure Reference

For site rebuild (non-WordPress version). Provided by the site owner as the final, locked-in SEO plan for the full multi-page rebuild. Titles, meta descriptions, slugs, and schema values listed here are final and must be preserved exactly, not auto-generated.

## Business overview

- Business name: TAXI Antonio
- Owner: Antonio Šakić
- Base: Šibenik, Croatia (also serves Skradin, Vodice, and wider Dalmatia)
- Vehicle: Škoda Superb
- Phone: +385 99 447 1013
- Schema rating: 4.9 stars / 125 reviews
- Primary language: English (canonical, served at site root)
- Additional languages (2026-07-05, expanded from the original 3): Croatian (hr), German (de), Polish (pl), Czech (cs), Italian (it), French (fr), Dutch (nl). Every page is meant to rank in Google in every language it's translated into, not just funnel everyone to one canonical version, hreflang tells Google these are equivalent pages so it can serve the right language per searcher rather than picking a single winner.

## Multi-language technical implementation

Pages are built page by page, English first, translations added later per page (not all at once). The build system is already fully wired for all 8 languages regardless of how many translations exist yet:

- Folder structure: `src/pages/<page-id>/<lang>/meta.json` + `content.html`. A `<page-id>` (e.g. `about`) groups every translation of that one logical page. Adding a new language to an existing page is just adding a new `<lang>` subfolder alongside `en/`.
- URL scheme: English is canonical and lives at the site root (`taxisibenik.hr/about/`). Every other language gets a prefix (`taxisibenik.hr/hr/o-meni/`, `taxisibenik.hr/de/...`, etc.), matching the pattern in the "URL structure logic" section below.
- hreflang: `build.py` automatically generates a reciprocal set of `<link rel="alternate" hreflang="...">` tags across every language variant that exists for a given page-id, plus `hreflang="x-default"` pointing at the English version. This regenerates on every build, so a page with only `en/` gets one self-referencing tag, and each additional language folder added later automatically appears on every sibling variant's hreflang set, no manual bookkeeping needed.
- Header language switcher: also generated per page from the same variant data, so it links to the equivalent URL of the *current* page in each language (not just that language's homepage), and greys out languages not yet translated for that specific page.
- See [[project-build-workflow]] memory for the day to day build process.

## Core SEO rules (apply to every page)

- SEO title format: `[Route or Page Name] | [Key Info] | TAXI Antonio`
- Meta descriptions: under 160 characters, include price where relevant, end with booking CTA
- Slugs: English slugs are canonical. Each language gets its own translated slug (all finalized, listed per page below).
- Schema: LocalBusiness schema on homepage. Route pages use standard page structure.
- No trailing "we/our/us" language, all copy uses first person singular (I, me, my).
- No "Škoda Superb or similar", always just "Škoda Superb".
- No em dashes anywhere in any content.

## Site structure: 62 pages total

Four tiers: Homepage, Hubs, Route Pages, Utility Pages.

### Tier 1: Homepage

URL: `taxisibenik.hr/`

SEO titles:
- EN: `Taxi Šibenik | Local Rides, Transfers & Day Trips | TAXI Antonio`
- HR: `Taksi Šibenik | Lokalne vožnje, transferi i izleti | TAXI Antonio`
- DE: `Taxi Šibenik | Lokale Fahrten, Transfers & Tagesausflüge | TAXI Antonio`
- PL: `Taxi Šibenik | Lokalne przejazdy, transfery i wycieczki | TAXI Antonio`

Meta descriptions:
- EN: Local taxi Šibenik available on demand and 24/7 when booked in advance. Airport transfers, city connections and day trips. English-speaking driver. Book directly with TAXI Antonio.
- HR: Lokalni taksi Šibenik dostupan na zahtjev i 24/7 uz prethodnu rezervaciju. Aerodromski transferi, gradske veze i izleti. Rezervirajte direktno kod TAXI Antonio.
- DE: Lokales Taxi Šibenik auf Abruf und rund um die Uhr bei Vorausbuchung. Flughafentransfers, Stadtverbindungen und Tagesausflüge. Direkt bei TAXI Antonio buchen.
- PL: Lokalna taksówka Šibenik dostępna na żądanie i 24/7 przy wcześniejszej rezerwacji. Transfery lotniskowe, połączenia miejskie i wycieczki. Zarezerwuj bezpośrednio u TAXI Antonio.

Schema (LocalBusiness):
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Taxi Antonio",
  "telephone": "+385994471013",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Šibenik",
    "addressCountry": "HR"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "125"
  }
}
```

### Tier 2: Hub pages (6 hubs)

Category landing pages, link down to relevant route pages beneath them. No price in title since they cover multiple routes.

**Hub: Airport Transfers**
Slugs: `airport-transfers-from-sibenik` / `aerodromski-transferi-sibenik` / `flughafentransfers-sibenik` / `transfery-lotniskowe-sibenik`
- EN title: `Airport Transfers from Šibenik | Fixed Prices | TAXI Antonio`
- HR title: `Aerodromski transferi iz Šibenika | Fiksne cijene | TAXI Antonio`
- DE title: `Flughafentransfers ab Šibenik | Festpreise | TAXI Antonio`
- PL title: `Transfery lotniskowe z Šibenika | Stałe ceny | TAXI Antonio`
- EN meta: Private airport transfers from Šibenik to Split, Zadar, Zagreb and Dubrovnik. Fixed prices, flight monitoring included. Book directly with local driver TAXI Antonio.
- HR meta: Privatni aerodromski transferi iz Šibenika do Splita, Zadra, Zagreba i Dubrovnika. Fiksne cijene, praćenje leta uključeno. Rezervirajte direktno kod TAXI Antonio.
- DE meta: Private Flughafentransfers von Šibenik nach Split, Zadar, Zagreb und Dubrovnik. Festpreise, Flugverfolgung inklusive. Direkt bei lokalem Fahrer TAXI Antonio buchen.
- PL meta: Prywatne transfery lotniskowe z Šibenika do Splitu, Zadaru, Zagrzebia i Dubrownika. Stałe ceny, śledzenie lotu w cenie. Zarezerwuj bezpośrednio u TAXI Antonio.

**Hub: City-to-City Transfers**
Slugs: `city-to-city-transfers` / `medjugradski-transferi-sibenik` / `staedte-transfers-sibenik` / `transfery-miedzymiastowe-sibenik`
- EN title: `City-to-City Transfers from Šibenik | Fixed Prices | TAXI Antonio`
- HR title: `Međugradski transferi iz Šibenika | Fiksne cijene | TAXI Antonio`
- DE title: `Städtetransfers ab Šibenik | Festpreise | TAXI Antonio`
- PL title: `Transfery międzymiastowe z Šibenika | Stałe ceny | TAXI Antonio`
- EN meta: Private fixed-price city-to-city transfers from Šibenik to Split, Zadar, Zagreb, Dubrovnik and beyond. Door-to-door, 24/7 when booked in advance. Book with TAXI Antonio.
- HR meta: Privatni međugradski transferi iz Šibenika do Splita, Zadra, Zagreba, Dubrovnika i dalje. Od vrata do vrata, 24/7 uz prethodnu rezervaciju. Rezervirajte kod TAXI Antonio.
- DE meta: Private Festpreis-Städtetransfers von Šibenik nach Split, Zadar, Zagreb, Dubrovnik und darüber hinaus. Tür-zu-Tür, rund um die Uhr bei Vorausbuchung. Bei TAXI Antonio buchen.
- PL meta: Prywatne transfery międzymiastowe z Šibenika do Splitu, Zadaru, Zagrzebia, Dubrownika i dalej. Door-to-door, 24/7 przy wcześniejszej rezerwacji. Zarezerwuj u TAXI Antonio.

**Hub: Marina Transfers**
Slugs: `marina-transfers-sibenik` / `marina-transferi-sibenik` / `marina-transfers-sibenik` / `transfery-marinowe-sibenik`
- EN title: `Marina Transfers Šibenik | D-Marin Mandalina & Marina Zaton | TAXI Antonio`
- HR title: `Marina transferi Šibenik | D-Marin Mandalina i Marina Zaton | TAXI Antonio`
- DE title: `Marina Transfers Šibenik | D-Marin Mandalina & Marina Zaton | TAXI Antonio`
- PL title: `Transfery marinowe Šibenik | D-Marin Mandalina i Marina Zaton | TAXI Antonio`
- EN meta: Private marina transfers from Šibenik to Split Airport, Zadar Airport and across Dalmatia. Serving D-Marin Mandalina and Marina Zaton. Fixed price. Book with TAXI Antonio.
- HR meta: Privatni marina transferi iz Šibenika do Aerodroma Split, Aerodroma Zadar i diljem Dalmacije. Usluga za D-Marin Mandalinu i Marinu Zaton. Fiksna cijena. Rezervirajte kod TAXI Antonio.
- DE meta: Private Marina Transfers von Šibenik zum Flughafen Split, Flughafen Zadar und durch ganz Dalmatien. D-Marin Mandalina und Marina Zaton werden bedient. Festpreis. Bei TAXI Antonio buchen.
- PL meta: Prywatne transfery marinowe z Šibenika na lotnisko Split, lotnisko Zadar i przez całą Dalmację. Obsługa D-Marin Mandalina i Marina Zaton. Stała cena. Zarezerwuj u TAXI Antonio.

**Hub: Transfers Šibenik**
Slugs: `transfers-sibenik` / `transferi-sibenik` / `transfers-sibenik` / `transfery-sibenik`
- EN title: `Šibenik Transfers | Airport & City-to-City Transfers | TAXI Antonio`
- HR title: `Transferi Šibenik | Aerodromski i međugradski transferi | TAXI Antonio`
- DE title: `Transfers Šibenik | Flughafen & Städtetransfers | TAXI Antonio`
- PL title: `Transfery Šibenik | Lotniskowe i międzymiastowe | TAXI Antonio`
- EN meta: Private Šibenik transfers to all airports and cities in Croatia. Door-to-door, 24/7 when booked in advance. Book with local driver TAXI Antonio.
- HR meta: Privatni transferi Šibenik do svih aerodroma i gradova u Hrvatskoj. Od vrata do vrata, 24/7 uz prethodnu rezervaciju. Rezervirajte kod TAXI Antonio.
- DE meta: Private Transfers Šibenik zu allen Flughäfen und Städten in Kroatien. Tür-zu-Tür, rund um die Uhr bei Vorausbuchung. Bei lokalem Fahrer TAXI Antonio buchen.
- PL meta: Prywatne transfery Šibenik do wszystkich lotnisk i miast w Chorwacji. Door-to-door, 24/7 przy wcześniejszej rezerwacji. Zarezerwuj u lokalnego kierowcy TAXI Antonio.

**Hub: Vodice Transfers**
Slugs: `vodice-transfers` / `vodice-transferi` / `vodice-transfers` / `vodice-transfery`
- EN title: `Vodice Transfers | Fixed Price Taxi Service | TAXI Antonio`
- HR title: `Vodice transferi | Fiksna cijena taxi usluge | TAXI Antonio`
- DE title: `Vodice Transfers | Festpreis Taxiservice | TAXI Antonio`
- PL title: `Vodice Transfery | Taxi po stałej cenie | TAXI Antonio`
- EN meta: Fixed-price private Vodice transfers. Split Airport from €115, Zadar Airport from €100, Šibenik from €30. Book directly with your local driver TAXI Antonio.
- HR meta: Privatni Vodice transferi po fiksnoj cijeni. Aerodrom Split od 115 €, Aerodrom Zadar od 100 €, Šibenik od 30 €. Rezervirajte direktno kod TAXI Antonio.
- DE meta: Private Vodice Transfers zum Festpreis. Flughafen Split ab 115 €, Flughafen Zadar ab 100 €, Šibenik ab 30 €. Direkt beim lokalen Fahrer TAXI Antonio buchen.
- PL meta: Prywatne transfery Vodice po stałej cenie. Lotnisko Split od 115 €, lotnisko Zadar od 100 €, Šibenik od 30 €. Zarezerwuj bezpośrednio u TAXI Antonio.

**Hub: Day Trips**
Slugs: `daytrips` / `izleti` / `tagesausfluege` / `wycieczki`
- EN title: `Day Trips to Krka & Plitvice | from Šibenik, Split & Zadar | TAXI Antonio`
- HR title: `Izleti do Krke i Plitvica | iz Šibenika, Splita i Zadra | TAXI Antonio`
- DE title: `Tagesausflüge nach Krka & Plitvice | ab Šibenik, Split & Zadar | TAXI Antonio`
- PL title: `Wycieczki do Krki i Plitvic | z Šibenika, Splitu i Zadaru | TAXI Antonio`
- EN meta: Private Day Trips to Krka & Plitvice with local English-speaking driver & fixed prices. Book directly with TAXI Antonio.
- HR meta: Privatni izleti do Krke i Plitvičkih jezera s lokalnim engleski govornim vozačem i fiksnim cijenama. Rezervirajte direktno kod TAXI Antonio.
- DE meta: Private Tagesausflüge nach Krka & Plitvice mit lokalem englischsprachigem Fahrer und Festpreisen. Direkt bei TAXI Antonio buchen.
- PL meta: Prywatne wycieczki do Krki i Jezior Plitwickich z lokalnym kierowcą mówiącym po angielsku i stałymi cenami. Zarezerwuj bezpośrednio u TAXI Antonio.

### Tier 3: Route pages (46 pages)

Every route page has: fixed price displayed prominently, door-to-door service mentioned, English-speaking driver mentioned, 24/7 availability with advance booking mentioned where relevant, a booking CTA (CabGrid Pro in WordPress version, needs replacement), a price table (one way / round trip), FAQ section.

Slugs listed as: English / Croatian / German / Polish.

- **Amadria Park Šibenik Transfers**: `amadria-park-sibenik-transfers` / `amadria-park-sibenik-transferi` / `amadria-park-sibenik-transfers` / `transfery-amadria-park-sibenik`. EN title: `Amadria Park Šibenik Transfers | Fixed Price | TAXI Antonio`
- **Dubrovnik to Šibenik — €485**: `taxi-dubrovnik-sibenik` / `taxi-dubrovnik-do-sibenika` / `taxi-dubrovnik-nach-sibenik` / `taksowka-dubrownik-sibenik`. EN: `Taxi Dubrovnik to Šibenik | Private Transfer €485`. HR: `Taxi Dubrovnik do Šibenika | Privatni transfer 485 € | TAXI Antonio`. DE: `Taxi Dubrovnik nach Šibenik | Privater Transfer 485 € | TAXI Antonio`. PL: `Taksówka Dubrownik do Šibenika | Prywatny transfer 485 € | TAXI Antonio`. EN meta: Private taxi from Dubrovnik (or airport) to Šibenik. Fixed €485 per car, English-speaking driver, door-to-door. HR meta: Privatni taxi iz Dubrovnika (ili aerodroma) do Šibenika. Fiksna cijena 485 € po vozilu, engleski govorni vozač, od vrata do vrata. DE meta: Privates Taxi von Dubrovnik (oder Flughafen) nach Šibenik. Festpreis 485 € pro Auto, englischsprachiger Fahrer, Tür-zu-Tür. PL meta: Prywatna taksówka z Dubrownika (lub lotniska) do Šibenika. Stała cena 485 € za samochód, kierowca mówiący po angielsku, door-to-door.
- **Dubrovnik to Zadar — €550**: `taxi-dubrovnik-zadar` / `taxi-dubrovnik-do-zadra` / `taxi-dubrovnik-nach-zadar` / `taksowka-dubrownik-zadar`. EN: `Taxi Dubrovnik to Zadar | Private Transfer €550 | TAXI Antonio`. HR: `Taxi Dubrovnik do Zadra | Privatni transfer 550 € | TAXI Antonio`. DE: `Taxi Dubrovnik nach Zadar | Privater Transfer 550 € | TAXI Antonio`. PL: `Taksówka Dubrownik do Zadaru | Prywatny transfer 550 € | TAXI Antonio`. EN meta: Private taxi from Dubrovnik to Zadar city or Zadar Airport. Fixed price €550 for up to 4 passengers. Door-to-door. Book directly.
- **Dubrovnik to Zadar Airport — €550**: `taxi-dubrovnik-zadar-airport` / `taxi-dubrovnik-do-zracne-luke-zadar` / `taxi-dubrovnik-zum-flughafen-zadar` / `taksowka-dubrownik-lotnisko-zadar`. EN: `Taxi Dubrovnik to Zadar Airport | Fixed Price Transfer €550`. HR: `Taxi Dubrovnik do Aerodroma Zadar | Fiksna cijena 550 € | TAXI Antonio`. DE: `Taxi Dubrovnik zum Flughafen Zadar | Festpreis 550 € | TAXI Antonio`. PL: `Taksówka Dubrownik na Lotnisko Zadar | Stała cena 550 € | TAXI Antonio`.
- **Krka from Šibenik — €100**: `day-trip-krka-national-park-sibenik` / `izlet-krka-nacionalni-park-sibenik` / `tagesausflug-krka-nationalpark-sibenik` / `wycieczka-krka-park-narodowy-sibenik`. EN: `Day Trip from Šibenik to Krka National Park | Fixed Price 100 €`. HR: `Privatni izlet iz Šibenika u Nacionalni park Krka | Fiksna cijena 100 € | TAXI Antonio`. DE: `Privater Tagesausflug von Šibenik zum Nationalpark Krka | Festpreis 100 € | TAXI Antonio`. PL: `Prywatna wycieczka z Šibenika do Parku Narodowego Krka | Stała cena 100 € | TAXI Antonio`. EN meta: Book a day trip from Šibenik to Krka Waterfalls with flexible pick-up. Flexible free time inside the park and a comfortable return transfer.
- **Krka from Split — €290**: `day-trip-krka-national-park-split` / `izlet-krka-nacionalni-park-split` / `tagesausflug-krka-nationalpark-split` / `wycieczka-krka-park-narodowy-split`. EN: `Private Day Trip from Split to Krka National Park | Fixed Price 290 €`. HR: `Privatni izlet iz Splita u Nacionalni park Krka | Fiksna cijena 290 € | TAXI Antonio`. DE: `Privater Tagesausflug von Split zum Nationalpark Krka | Festpreis 290 € | TAXI Antonio`. PL: `Prywatna wycieczka ze Splitu do Parku Narodowego Krka | Stała cena 290 € | TAXI Antonio`. EN meta: Book a private day trip from Split to Krka National Park. Direct pick-ups from Split hotels or the cruise port. Fixed price €290.
- **Krka from Zadar**: `day-trip-krka-national-park-zadar` / `izlet-krka-nacionalni-park-zadar` / `tagesausflug-krka-nationalpark-zadar` / `wycieczka-krka-park-narodowy-zadar`. EN: `Private Day Trip from Zadar to Krka National Park`. HR: `Privatni izlet iz Zadra u Nacionalni park Krka | Fiksna cijena | TAXI Antonio`. DE: `Privater Tagesausflug von Zadar zum Nationalpark Krka | Festpreis | TAXI Antonio`. PL: `Prywatna wycieczka z Zadaru do Parku Narodowego Krka | Stała cena | TAXI Antonio`. EN meta: Book a private Day Trip from Zadar to Krka. Fixed price, comfortable vehicle, up to 4 hours of waiting time included.
- **Makarska to Šibenik — €210**: `taxi-makarska-to-sibenik` / `taxi-makarska-do-sibenika` / `taxi-makarska-nach-sibenik` / `taksowka-makarska-sibenik`. EN: `Taxi Makarska to Šibenik | Fixed Transfer Price €210`. HR: `Taxi Makarska do Šibenika | Fiksna cijena 210 € | TAXI Antonio`. DE: `Taxi Makarska nach Šibenik | Festpreis 210 € | TAXI Antonio`. PL: `Taksówka Makarska do Šibenika | Stała cena 210 € | TAXI Antonio`. EN meta: Private taxi Makarska to Šibenik. Fixed €210 per car, English-speaking driver, door-to-door.
- **Plitvice from Šibenik — €500**: `day-trip-plitvice-lakes-national-park-sibenik` / `izlet-plitvicka-jezera-sibenik` / `tagesausflug-plitvicer-seen-sibenik` / `wycieczka-jeziora-plitwickie-sibenik`. EN: `Private Day Trip from Šibenik to Plitvice Lakes | Fixed Price €500`. HR: `Privatni izlet iz Šibenika do Plitvičkih jezera | Fiksna cijena 500 € | TAXI Antonio`. DE: `Privater Tagesausflug von Šibenik zu den Plitvicer Seen | Festpreis 500 € | TAXI Antonio`. PL: `Prywatna wycieczka z Šibenika do Jezior Plitwickich | Stała cena 500 € | TAXI Antonio`. EN meta: Private day trip from Šibenik to Plitvice Lakes National Park by Antonio. Fixed price €500 for up to 4 passengers.
- **Plitvice from Split — €650**: `day-trip-plitvice-lakes-national-park-split` / `izlet-plitvicka-jezera-split` / `tagesausflug-plitvicer-seen-split` / `wycieczka-jeziora-plitwickie-split`. EN: `Private Day Trip from Split to Plitvice Lakes | Fixed Price €650`. HR: `Privatni izlet iz Splita do Plitvičkih jezera | Fiksna cijena 650 € | TAXI Antonio`. DE: `Privater Tagesausflug von Split zu den Plitvicer Seen | Festpreis 650 € | TAXI Antonio`. PL: `Prywatna wycieczka ze Splitu do Jezior Plitwickich | Stała cena 650 € | TAXI Antonio`.
- **Primošten to Šibenik — €50**: `taxi-primosten-sibenik` / `taxi-primosten-do-sibenika` / `taxi-primosten-nach-sibenik` / `taksowka-primosten-sibenik`. EN: `Taxi Primošten to Šibenik | Private Transfer €50 | TAXI Antonio`. HR: `Taxi Primošten do Šibenika | Fiksna cijena 50 € | TAXI Antonio`. DE: `Taxi Primošten nach Šibenik | Festpreis 50 € | TAXI Antonio`. PL: `Taksówka Primošten do Šibenika | Stała cena 50 € | TAXI Antonio`.
- **Primošten to Zadar Airport — €160**: `taxi-primosten-zadar-airport` / `taxi-primosten-do-zracne-luke-zadar` / `taxi-primosten-zum-flughafen-zadar` / `taksowka-primosten-lotnisko-zadar`. EN: `Taxi Primošten to Zadar Airport | Fixed Price €160 | TAXI Antonio`. HR: `Taxi Primošten do Aerodroma Zadar | Fiksna cijena 160 € | TAXI Antonio`. DE: `Taxi Primošten zum Flughafen Zadar | Festpreis 160 € | TAXI Antonio`. PL: `Taksówka Primošten na Lotnisko Zadar | Stała cena 160 € | TAXI Antonio`.
- **Šibenik from Split (day trip) — €290**: `day-trip-sibenik-from-split` / `izlet-sibenik-iz-splita` / `tagesausflug-sibenik-ab-split` / `wycieczka-sibenik-ze-splitu`. EN: `Private Day Trip from Split to Šibenik | Fixed Price €290`. HR: `Privatni izlet iz Splita u Šibenik | Fiksna cijena 290 € | TAXI Antonio`. DE: `Privater Tagesausflug von Split nach Šibenik | Festpreis 290 € | TAXI Antonio`. PL: `Prywatna wycieczka ze Splitu do Šibenika | Stała cena 290 € | TAXI Antonio`. EN meta: Private Day Trip from Split to Šibenik with a local driver. Fixed price €290, up to 5 hours in Šibenik. Ideal for cruise passengers and families.
- **Šibenik from Zadar (day trip) — €260**: `day-trip-sibenik-from-zadar` / `izlet-sibenik-iz-zadra` / `tagesausflug-sibenik-ab-zadar` / `wycieczka-sibenik-z-zadaru`. EN: `Private Day Trip from Zadar to Šibenik | Fixed Price €260`. HR: `Privatni izlet iz Zadra u Šibenik | Fiksna cijena 260 € | TAXI Antonio`. DE: `Privater Tagesausflug von Zadar nach Šibenik | Festpreis 260 € | TAXI Antonio`. PL: `Prywatna wycieczka z Zadaru do Šibenika | Stała cena 260 € | TAXI Antonio`.
- **Šibenik to Dubrovnik — €485**: `taxi-sibenik-dubrovnik` / `taxi-sibenik-do-dubrovnika` / `taxi-sibenik-nach-dubrovnik` / `taksowka-sibenik-dubrownik`. EN: `Taxi Šibenik to Dubrovnik | Private Transfer €485`. HR: `Taxi Šibenik do Dubrovnika | Privatni transfer 485 € | TAXI Antonio`. DE: `Taxi Šibenik nach Dubrovnik | Privater Transfer 485 € | TAXI Antonio`. PL: `Taksówka Šibenik do Dubrownika | Prywatny transfer 485 € | TAXI Antonio`.
- **Šibenik to Makarska — €210**: `taxi-sibenik-to-makarska` / `taxi-sibenik-do-makarske` / `taxi-sibenik-nach-makarska` / `taksowka-sibenik-makarska`. EN: `Taxi Šibenik to Makarska | Fixed Transfer Price 210 €`. HR: `Taxi Šibenik do Makarske | Fiksna cijena 210 € | TAXI Antonio`. DE: `Taxi Šibenik nach Makarska | Festpreis 210 € | TAXI Antonio`. PL: `Taksówka Šibenik do Makarskiej | Stała cena 210 € | TAXI Antonio`.
- **Šibenik to Primošten — €50**: `taxi-sibenik-primosten` / `taxi-sibenik-do-primostena` / `taxi-sibenik-nach-primosten` / `taksowka-sibenik-primosten`. EN: `Taxi Šibenik to Primošten | Private Transfer €50`. HR: `Taxi Šibenik do Primošten | Fiksna cijena 50 € | TAXI Antonio`. DE: `Taxi Šibenik nach Primošten | Festpreis 50 € | TAXI Antonio`. PL: `Taksówka Šibenik do Primošten | Stała cena 50 € | TAXI Antonio`.
- **Šibenik to Skradin — €50**: `taxi-sibenik-skradin` / `taxi-sibenik-do-skradina` / `taxi-sibenik-nach-skradin` / `taksowka-sibenik-skradin`. EN: `Taxi Šibenik to Skradin | Fixed Transfer Price 50 €`. HR: `Taxi Šibenik do Skradina | Fiksna cijena 50 € | TAXI Antonio`. DE: `Taxi Šibenik nach Skradin | Festpreis 50 € | TAXI Antonio`. PL: `Taksówka Šibenik do Skradina | Stała cena 50 € | TAXI Antonio`.
- **Šibenik to Split — €140**: `taxi-sibenik-split` / `taxi-sibenik-do-splita` / `taxi-sibenik-nach-split` / `taksowka-sibenik-split`. EN: `Taxi Šibenik to Split center | Fixed Transfer Price €140`. HR: `Taxi Šibenik do Splita | Fiksna cijena 140 € | TAXI Antonio`. DE: `Taxi Šibenik nach Split | Festpreis 140 € | TAXI Antonio`. PL: `Taksówka Šibenik do Splitu | Stała cena 140 € | TAXI Antonio`. EN meta: Private taxi Šibenik to Split center or ferry port, about 1 to 1.25 hours. Fixed €140 per car, English-speaking driver, door-to-door.
- **Šibenik to Split Airport — €95**: `taxi-sibenik-split-airport` / `taxi-sibenik-do-zracne-luke-split` / `taxi-sibenik-zum-flughafen-split` / `taksowka-sibenik-lotnisko-split`. EN: `Taxi Šibenik to Split Airport | Fixed Price Transfer €95`. HR: `Taxi Šibenik do Aerodroma Split | Fiksna cijena 95 € | TAXI Antonio`. DE: `Taxi Šibenik zum Flughafen Split | Festpreis 95 € | TAXI Antonio`. PL: `Taksówka Šibenik na Lotnisko Split | Stała cena 95 € | TAXI Antonio`. EN meta: Book a private taxi Šibenik to Split Airport (SPU). Reliable, punctual, English-speaking driver. No hidden fees. 24/7 service.
- **Šibenik to Trogir — €95**: `taxi-sibenik-to-trogir` / `taxi-sibenik-do-trogira` / `taxi-sibenik-nach-trogir` / `taksowka-sibenik-trogir`. EN: `Taxi Šibenik to Trogir | Fixed Transfer Price €95`. HR: `Taxi Šibenik do Trogira | Fiksna cijena 95 € | TAXI Antonio`. DE: `Taxi Šibenik nach Trogir | Festpreis 95 € | TAXI Antonio`. PL: `Taksówka Šibenik do Trogiru | Stała cena 95 € | TAXI Antonio`.
- **Šibenik to Vodice — €30**: `taxi-sibenik-vodice` / `taxi-sibenik-do-vodica` / `taxi-sibenik-nach-vodice` / `taksowka-sibenik-vodice`. EN: `Taxi Šibenik to Vodice | Fixed Transfer Price €30`. HR: `Taxi Šibenik do Vodica | Fiksna cijena 30 € | TAXI Antonio`. DE: `Taxi Šibenik nach Vodice | Festpreis 30 € | TAXI Antonio`. PL: `Taksówka Šibenik do Vodic | Stała cena 30 € | TAXI Antonio`.
- **Šibenik to Zadar Airport — €130**: `taxi-sibenik-zadar-airport` / `taxi-sibenik-do-zracne-luke-zadar` / `taxi-sibenik-zum-flughafen-zadar` / `taksowka-sibenik-lotnisko-zadar`. EN: `Taxi Šibenik to Zadar Airport | Fixed Transfer Price €130`. HR: `Taxi Šibenik do Aerodroma Zadar | Fiksna cijena 130 € | TAXI Antonio`. DE: `Taxi Šibenik zum Flughafen Zadar | Festpreis 130 € | TAXI Antonio`. PL: `Taksówka Šibenik na Lotnisko Zadar | Stała cena 130 € | TAXI Antonio`.
- **Šibenik to Zagreb — €485**: `taxi-sibenik-zagreb` / `taxi-sibenik-do-zagreba` / `taxi-sibenik-nach-zagreb` / `taksowka-sibenik-zagrzeb`. EN: `Taxi Šibenik to Zagreb | Fixed Transfer Price €485`. HR: `Taxi Šibenik do Zagreba | Fiksna cijena 485 € | TAXI Antonio`. DE: `Taxi Šibenik nach Zagreb | Festpreis 485 € | TAXI Antonio`. PL: `Taksówka Šibenik do Zagrzebia | Stała cena 485 € | TAXI Antonio`. EN meta: Private taxi Šibenik to Zagreb. Drop off in center or airport. Takes about 3.5 to 4 hours. Fixed €485 per car, English-speaking driver, door-to-door.
- **Split Airport to Novalja — €250**: `taxi-split-airport-novalja` / `taxi-zracna-luka-split-novalja` / `taxi-flughafen-split-novalja` / `taksowka-lotnisko-split-novalja`. EN: `Taxi Split Airport to Novalja | Fixed Transfer Price €250`. HR: `Taxi Aerodrom Split do Novalje | Fiksna cijena 250 € | TAXI Antonio`. DE: `Taxi Flughafen Split nach Novalja | Festpreis 250 € | TAXI Antonio`. PL: `Taksówka Lotnisko Split do Novalji | Stała cena 250 € | TAXI Antonio`. EN meta: Private taxi Split Airport to Novalja, Pag and Zrće beach. Fixed price €250 for up to 4 passengers. Flight monitoring included.
- **Split Airport to Šibenik — €95**: `taxi-split-airport-sibenik` / `taxi-zracna-luka-split-do-sibenika` / `taxi-flughafen-split-nach-sibenik` / `taksowka-lotnisko-split-sibenik`. EN: `Taxi Split Airport to Šibenik | Fixed Price Transfer 95€`. HR: `Taxi Aerodrom Split do Šibenika | Fiksna cijena 95 € | TAXI Antonio`. DE: `Taxi Flughafen Split nach Šibenik | Festpreis 95 € | TAXI Antonio`. PL: `Taksówka Lotnisko Split do Šibenika | Stała cena 95 € | TAXI Antonio`. EN meta: Private taxi Split Airport to Šibenik. Fixed price €95. Includes flight monitoring, meet & greet, and an English-speaking local driver.
- **Split Airport to Vodice — €115**: `taxi-split-airport-vodice` / `taxi-zracna-luka-split-do-vodica` / `taxi-flughafen-split-nach-vodice` / `taksowka-lotnisko-split-vodice`. EN: `Taxi Split Airport to Vodice | Fixed Price Transfer €115`. HR: `Taxi Aerodrom Split do Vodica | Fiksna cijena 115 € | TAXI Antonio`. DE: `Taxi Flughafen Split nach Vodice | Festpreis 115 € | TAXI Antonio`. PL: `Taksówka Lotnisko Split do Vodic | Stała cena 115 € | TAXI Antonio`.
- **Split Airport to Zadar — €210**: `taxi-split-airport-zadar` / `taxi-zracna-luka-split-do-zadra` / `taxi-flughafen-split-nach-zadar` / `taksowka-lotnisko-split-zadar`. EN: `Taxi Split Airport to Zadar | Fixed Transfer Price €210`. HR: `Taxi Aerodrom Split do Zadra | Fiksna cijena 210 € | TAXI Antonio`. DE: `Taxi Flughafen Split nach Zadar | Festpreis 210 € | TAXI Antonio`. PL: `Taksówka Lotnisko Split do Zadaru | Stała cena 210 € | TAXI Antonio`.
- **Split to Šibenik — €140**: `taxi-split-sibenik` / `taxi-split-do-sibenika` / `taxi-split-nach-sibenik` / `taksowka-split-sibenik`. EN: `Taxi Split to Šibenik | Fixed Transfer Price €140`. HR: `Taxi Split do Šibenika | Fiksna cijena 140 € | TAXI Antonio`. DE: `Taxi Split nach Šibenik | Festpreis 140 € | TAXI Antonio`. PL: `Taksówka Split do Šibenika | Stała cena 140 € | TAXI Antonio`.
- **Split to Vodice — €155**: `taxi-split-to-vodice` / `taxi-split-do-vodica` / `taxi-split-nach-vodice` / `taksowka-split-vodice`. EN: `Taxi Split to Vodice | Private Transfer €155 | TAXI Antonio`. HR: `Taxi Split do Vodica | Fiksna cijena 155 € | TAXI Antonio`. DE: `Taxi Split nach Vodice | Festpreis 155 € | TAXI Antonio`. PL: `Taksówka Split do Vodic | Stała cena 155 € | TAXI Antonio`.
- **Split to Zadar — €230**: `taxi-split-zadar` / `taxi-split-do-zadra` / `taxi-split-nach-zadar` / `taksowka-split-zadar`. EN: `Taxi Split to Zadar | Fixed Price €230 | TAXI Antonio`. HR: `Taxi Split do Zadra | Fiksna cijena 230 € | TAXI Antonio`. DE: `Taxi Split nach Zadar | Festpreis 230 € | TAXI Antonio`. PL: `Taksówka Split do Zadaru | Stała cena 230 € | TAXI Antonio`.
- **Split to Zadar Airport — €210**: `taxi-split-zadar-airport` / `taxi-split-do-zracne-luke-zadar` / `taxi-split-zum-flughafen-zadar` / `taksowka-split-lotnisko-zadar`. EN: `Taxi Split to Zadar Airport | Fixed Transfer Price €210`. HR: `Taxi Split do Aerodroma Zadar | Fiksna cijena 210 € | TAXI Antonio`. DE: `Taxi Split zum Flughafen Zadar | Festpreis 210 € | TAXI Antonio`. PL: `Taksówka Split na Lotnisko Zadar | Stała cena 210 € | TAXI Antonio`.
- **Taxi Skradin** (links to taxiskradin.hr): `taxi-skradin` / `taxi-skradin-hr` / `taxi-skradin-de` / `taxi-skradin-pl`. EN: `Taxi Skradin | Krka National Park, Marina & Airport Transfer`. HR: `Taxi Skradin | Nacionalni park Krka, Marina i Aerodromski transferi | TAXI Antonio`. DE: `Taxi Skradin | Nationalpark Krka, Marina & Flughafentransfers | TAXI Antonio`. PL: `Taxi Skradin | Park Narodowy Krka, Marina i Transfery lotniskowe | TAXI Antonio`.
- **Zadar Airport to Šibenik — €130**: `taxi-zadar-airport-sibenik` / `taxi-zracna-luka-zadar-do-sibenika` / `taxi-flughafen-zadar-nach-sibenik` / `taksowka-lotnisko-zadar-sibenik`. EN: `Taxi Zadar Airport to Šibenik | Fixed Transfer Price €130`. HR: `Taxi Aerodrom Zadar do Šibenika | Fiksna cijena 130 € | TAXI Antonio`. DE: `Taxi Flughafen Zadar nach Šibenik | Festpreis 130 € | TAXI Antonio`. PL: `Taksówka Lotnisko Zadar do Šibenika | Stała cena 130 € | TAXI Antonio`. EN meta: Taxi Zadar Airport to Šibenik. Fixed price €130 per car. Includes flight monitoring, meet-and-greet, and an English-speaking driver.
- **Tisno Transfers**: `tisno-transfers` / `tisno-transferi` / `tisno-transfers` / `tisno-transfery`. EN: `Tisno Transfers | Fixed Price Taxi Service | TAXI Antonio`. HR: `Tisno transferi | Fiksna cijena taxi usluge | TAXI Antonio`. DE: `Tisno Transfers | Festpreis Taxiservice | TAXI Antonio`. PL: `Tisno Transfery | Taxi po stałej cenie | TAXI Antonio`. EN meta: Fixed-price private transfers to and from Tisno. Split Airport from €130, Zadar Airport from €115, Šibenik from €50.
- **Trogir to Šibenik — €95**: `taxi-trogir-to-sibenik` / `taxi-trogir-do-sibenika` / `taxi-trogir-nach-sibenik` / `taksowka-trogir-sibenik`. EN: `Taxi Trogir to Šibenik | Fixed Transfer Price €95`. HR: `Taxi Trogir do Šibenika | Fiksna cijena 95 € | TAXI Antonio`. DE: `Taxi Trogir nach Šibenik | Festpreis 95 € | TAXI Antonio`. PL: `Taksówka Trogir do Šibenika | Stała cena 95 € | TAXI Antonio`.
- **Vodice to Šibenik — €30**: `taxi-vodice-sibenik` / `taxi-vodice-do-sibenika` / `taxi-vodice-nach-sibenik` / `taksowka-vodice-sibenik`. EN: `Taxi Vodice to Šibenik | Fixed Transfer Price €30`. HR: `Taxi Vodice do Šibenika | Fiksna cijena 30 € | TAXI Antonio`. DE: `Taxi Vodice nach Šibenik | Festpreis 30 € | TAXI Antonio`. PL: `Taksówka Vodice do Šibenika | Stała cena 30 € | TAXI Antonio`.
- **Vodice to Split Airport — €115**: `taxi-vodice-split-airport` / `taxi-vodice-do-zracne-luke-split` / `taxi-vodice-zum-flughafen-split` / `taksowka-vodice-lotnisko-split`. EN: `Taxi Vodice to Split Airport | Fixed Transfer Price €115`. HR: `Taxi Vodice do Aerodroma Split | Fiksna cijena 115 € | TAXI Antonio`. DE: `Taxi Vodice zum Flughafen Split | Festpreis 115 € | TAXI Antonio`. PL: `Taksówka Vodice na Lotnisko Split | Stała cena 115 € | TAXI Antonio`.
- **Vodice to Zadar Airport — €100**: `taxi-vodice-zadar-airport` / `taxi-vodice-do-zracne-luke-zadar` / `taxi-vodice-zum-flughafen-zadar` / `taksowka-vodice-lotnisko-zadar`. EN: `Taxi Vodice to Zadar Airport | Fixed Transfer Price €100`. HR: `Taxi Vodice do Aerodroma Zadar | Fiksna cijena 100 € | TAXI Antonio`. DE: `Taxi Vodice zum Flughafen Zadar | Festpreis 100 € | TAXI Antonio`. PL: `Taksówka Vodice na Lotnisko Zadar | Stała cena 100 € | TAXI Antonio`.
- **Zadar Airport to Dubrovnik — €550**: `taxi-zadar-airport-dubrovnik` / `taxi-zracna-luka-zadar-do-dubrovnika` / `taxi-flughafen-zadar-nach-dubrovnik` / `taksowka-lotnisko-zadar-dubrownik`. EN: `Taxi Zadar Airport to Dubrovnik | Fixed Price Transfer €550`. HR: `Taxi Aerodrom Zadar do Dubrovnika | Fiksna cijena 550 € | TAXI Antonio`. DE: `Taxi Flughafen Zadar nach Dubrovnik | Festpreis 550 € | TAXI Antonio`. PL: `Taksówka Lotnisko Zadar do Dubrownika | Stała cena 550 € | TAXI Antonio`.
- **Zadar Airport to Primošten — €160**: `taxi-zadar-airport-primosten` / `taxi-zracna-luka-zadar-do-primostena` / `taxi-flughafen-zadar-nach-primosten` / `taksowka-lotnisko-zadar-primosten`. EN: `Taxi Zadar Airport to Primošten | Fixed Transfer Price €160`. HR: `Taxi Aerodrom Zadar do Primošten | Fiksna cijena 160 € | TAXI Antonio`. DE: `Taxi Flughafen Zadar nach Primošten | Festpreis 160 € | TAXI Antonio`. PL: `Taksówka Lotnisko Zadar do Primošten | Stała cena 160 € | TAXI Antonio`.
- **Zadar Airport to Split — €210**: `taxi-zadar-airport-split` / `taxi-zracna-luka-zadar-do-splita` / `taxi-flughafen-zadar-nach-split` / `taksowka-lotnisko-zadar-split`. EN: `Taxi Zadar Airport to Split Center | Fixed Price €210 | TAXI Antonio`. HR: `Taxi Aerodrom Zadar do Splita | Fiksna cijena 210 € | TAXI Antonio`. DE: `Taxi Flughafen Zadar nach Split | Festpreis 210 € | TAXI Antonio`. PL: `Taksówka Lotnisko Zadar do Splitu | Stała cena 210 € | TAXI Antonio`.
- **Zadar Airport to Vodice — €100**: `taxi-zadar-airport-vodice` / `taxi-zracna-luka-zadar-do-vodica` / `taxi-flughafen-zadar-nach-vodice` / `taksowka-lotnisko-zadar-vodice`. EN: `Taxi Zadar Airport to Vodice | Fixed Price €100 | TAXI Antonio`. HR: `Taxi Aerodrom Zadar do Vodica | Fiksna cijena 100 € | TAXI Antonio`. DE: `Taxi Flughafen Zadar nach Vodice | Festpreis 100 € | TAXI Antonio`. PL: `Taksówka Lotnisko Zadar do Vodic | Stała cena 100 € | TAXI Antonio`.
- **Zadar to Dubrovnik — €550**: `taxi-zadar-dubrovnik` / `taxi-zadar-do-dubrovnika` / `taxi-zadar-nach-dubrovnik` / `taksowka-zadar-dubrownik`. EN: `Taxi Zadar to Dubrovnik | Private Transfer €550 | TAXI Antonio`. HR: `Taxi Zadar do Dubrovnika | Privatni transfer 550 € | TAXI Antonio`. DE: `Taxi Zadar nach Dubrovnik | Privater Transfer 550 € | TAXI Antonio`. PL: `Taksówka Zadar do Dubrownika | Prywatny transfer 550 € | TAXI Antonio`.
- **Zadar to Šibenik — €140**: `taxi-zadar-sibenik` / `taxi-zadar-do-sibenika` / `taxi-zadar-nach-sibenik` / `taksowka-zadar-sibenik`. EN: `Taxi Zadar to Šibenik | Fixed Transfer Price €140`. HR: `Taxi Zadar do Šibenika | Fiksna cijena 140 € | TAXI Antonio`. DE: `Taxi Zadar nach Šibenik | Festpreis 140 € | TAXI Antonio`. PL: `Taksówka Zadar do Šibenika | Stała cena 140 € | TAXI Antonio`.
- **Zadar to Split — €230**: `taxi-zadar-split` / `taxi-zadar-do-splita` / `taxi-zadar-nach-split` / `taksowka-zadar-split`. EN: `Taxi Zadar to Split | Fixed Transfer Price €230`. HR: `Taxi Zadar do Splita | Fiksna cijena 230 € | TAXI Antonio`. DE: `Taxi Zadar nach Split | Festpreis 230 € | TAXI Antonio`. PL: `Taksówka Zadar do Splitu | Stała cena 230 € | TAXI Antonio`.
- **Zadar to Split Airport — €210**: `taxi-zadar-split-airport` / `taxi-zadar-do-zracne-luke-split` / `taxi-zadar-zum-flughafen-split` / `taksowka-zadar-lotnisko-split`. EN: `Taxi Zadar to Split Airport | Fixed Transfer Price €210`. HR: `Taxi Zadar do Aerodroma Split | Fiksna cijena 210 € | TAXI Antonio`. DE: `Taxi Zadar zum Flughafen Split | Festpreis 210 € | TAXI Antonio`. PL: `Taksówka Zadar na Lotnisko Split | Stała cena 210 € | TAXI Antonio`.
- **Zagreb to Šibenik — €485**: `taxi-zagreb-sibenik` / `taxi-zagreb-do-sibenika` / `taxi-zagreb-nach-sibenik` / `taksowka-zagrzeb-sibenik`. EN: `Taxi Zagreb to Šibenik | Fixed Transfer Price €485`. HR: `Taxi Zagreb do Šibenika | Fiksna cijena 485 € | TAXI Antonio`. DE: `Taxi Zagreb nach Šibenik | Festpreis 485 € | TAXI Antonio`. PL: `Taksówka Zagrzeb do Šibenika | Stała cena 485 € | TAXI Antonio`.

### Tier 4: Utility pages (no slug translation needed)

**About Me**
Slug: `about` (all languages)
- EN title: `About Antonio Šakić | Local Taxi Driver in Šibenik & Skradin | TAXI Antonio`
- HR title: `O Antoniju Šakiću | Lokalni vozač u Šibeniku | TAXI Antonio`
- DE title: `Über Antonio Šakić | Lokaler Taxifahrer in Šibenik | TAXI Antonio`
- PL title: `O Antoniu Šakiciu | Lokalny kierowca w Šibeniku | TAXI Antonio`
- EN meta: Meet Antonio Šakić, your local driver in Šibenik and Skradin. Over a decade of professional driving experience, founded TAXI Antonio in 2022.

**Contact**
Slug: `contact` (all languages)
- EN title: `TAXI Antonio | Contact`
- HR title: `TAXI Antonio | Kontakt | Šibenik | TAXI Antonio`
- DE title: `TAXI Antonio | Kontakt | Šibenik | TAXI Antonio`
- PL title: `TAXI Antonio | Kontakt | Šibenik | TAXI Antonio`
- EN meta: Contact Antonio directly for taxi and transfer services in Šibenik. Simple and personal booking guaranteed.

**FAQ**
Slug: `frequently-asked-questions` (all languages)
- EN title: `Frequently Asked Questions | TAXI Antonio Šibenik`
- HR title: `Često postavljana pitanja | TAXI Antonio Šibenik`
- DE title: `Häufig gestellte Fragen | TAXI Antonio Šibenik`
- PL title: `Często zadawane pytania | TAXI Antonio Šibenik`

**Privacy Policy**
Slug: `privacy-policy` (all languages)

**Terms & Conditions**
Slug: `terms-and-conditions` (all languages)

## URL structure logic

Each language gets its own URL prefix:
- English (canonical): `taxisibenik.hr/[english-slug]/`
- Croatian: `taxisibenik.hr/hr/[croatian-slug]/`
- German: `taxisibenik.hr/de/[german-slug]/`
- Polish: `taxisibenik.hr/pl/[polish-slug]/`

Each translated page must include a `hreflang` tag pointing to all four language versions plus `x-default` pointing to the English version.

## Internal linking logic

Hub pages link down to their relevant route pages. Route pages link back up to their parent hub. Airport transfer route pages also cross-link to the reverse route (e.g. Šibenik to Split Airport links to Split Airport to Šibenik). City-to-city route pages also cross-link to their reverse.

## Sitemap

Total pages: 62 x 4 languages = 248 URLs in sitemap.
- Priority: Homepage = 1.0, Hubs = 0.8, Route pages = 0.7, Utility pages = 0.4.
- Change frequency: Homepage = weekly, all others = monthly.

## Important notes for rebuild

1. All SEO titles and meta descriptions listed here are final and must be preserved exactly. Do not auto-generate new ones.
2. All slugs listed here are final. Do not change them.
3. Schema markup on homepage must match the values listed (name, phone, rating, review count).
4. The booking widget (currently CabGrid Pro in WordPress) needs a replacement in the non-WordPress version. A contact form or WhatsApp link works as a fallback.
5. Trustindex Google reviews widget must appear on hub pages.
6. Page content is in English as primary. The other three languages are translations of that content.
7. No content was auto-generated for the new site yet. Content is being rewritten by the owner to add personal expertise and topical authority.
