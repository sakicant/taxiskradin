# Skradin Route Pages Master List (English)

The 21 route pages that exist on the live taxiskradin.hr, all Skradin-origin or
Skradin-destination. Slug pattern `taxi-<from>-to-<to>` matches the live URLs so
rankings and redirects carry over. Prices come from the PRICES matrix in
script.js (the "Skradin - center" node); this file only defines From/To/slug.

Names in From/To must match the DIST keys in docs/route-distances.json and the
MAPK mapping in the generator (Skradin, Zadar Airport, Split Airport, Šibenik,
Primošten, etc.).

Cross-linking rule: Šibenik-origin trips live on taxisibenik.hr, so
`taxi-skradin-to-sibenik` links its reverse leg to the sibenik domain instead of
hosting `taxi-sibenik-to-skradin` here.

Makarska (both directions) uses the EUR 210 fare added to the PRICES matrix on 2026-07-18.

| From | To | EN slug | One-way EUR |
|---|---|---|---|
| Skradin | Zadar Airport | `taxi-skradin-to-zadar-airport` | 105 |
| Zadar Airport | Skradin | `taxi-zadar-airport-to-skradin` | 105 |
| Skradin | Split Airport | `taxi-skradin-to-split-airport` | 110 |
| Split Airport | Skradin | `taxi-split-airport-to-skradin` | 110 |
| Skradin | Zagreb | `taxi-skradin-to-zagreb` | 485 |
| Zagreb | Skradin | `taxi-zagreb-to-skradin` | 485 |
| Skradin | Zadar | `taxi-skradin-to-zadar` | 130 |
| Zadar | Skradin | `taxi-zadar-to-skradin` | 130 |
| Skradin | Vodice | `taxi-skradin-to-vodice` | 60 |
| Vodice | Skradin | `taxi-vodice-to-skradin` | 60 |
| Skradin | Trogir | `taxi-skradin-to-trogir` | 100 |
| Trogir | Skradin | `taxi-trogir-to-skradin` | 100 |
| Skradin | Split | `taxi-skradin-to-split` | 140 |
| Split | Skradin | `taxi-split-to-skradin` | 140 |
| Skradin | Šibenik | `taxi-skradin-to-sibenik` | 50 |
| Skradin | Primošten | `taxi-skradin-to-primosten` | 80 |
| Primošten | Skradin | `taxi-primosten-to-skradin` | 80 |
| Skradin | Dubrovnik | `taxi-skradin-to-dubrovnik` | 485 |
| Dubrovnik | Skradin | `taxi-dubrovnik-to-skradin` | 485 |
| Skradin | Makarska | `taxi-skradin-to-makarska` | 210 |
| Makarska | Skradin | `taxi-makarska-to-skradin` | 210 |
| Skradin | Roški Slap | `taxi-skradin-to-roski-slap` | 50 |
| Roški Slap | Skradin | `taxi-roski-slap-to-skradin` | 50 |
| Roški Slap | Šibenik | `taxi-roski-slap-to-sibenik` | 90 |
| Roški Slap | Vodice | `taxi-roski-slap-to-vodice` | 90 |
| Roški Slap | Primošten | `taxi-roski-slap-to-primosten` | 110 |
| Roški Slap | Trogir | `taxi-roski-slap-to-trogir` | 110 |
| Roški Slap | Split | `taxi-roski-slap-to-split` | 150 |
| Roški Slap | Split Airport | `taxi-roski-slap-to-split-airport` | 100 |
| Roški Slap | Zadar | `taxi-roski-slap-to-zadar` | 135 |
| Roški Slap | Zadar Airport | `taxi-roski-slap-to-zadar-airport` | 110 |
| Vodice | Roški Slap | `taxi-vodice-to-roski-slap` | 90 |
| Primošten | Roški Slap | `taxi-primosten-to-roski-slap` | 110 |
| Trogir | Roški Slap | `taxi-trogir-to-roski-slap` | 110 |
| Split | Roški Slap | `taxi-split-to-roski-slap` | 150 |
| Split Airport | Roški Slap | `taxi-split-airport-to-roski-slap` | 100 |
| Zadar | Roški Slap | `taxi-zadar-to-roski-slap` | 135 |
| Zadar Airport | Roški Slap | `taxi-zadar-airport-to-roski-slap` | 110 |
