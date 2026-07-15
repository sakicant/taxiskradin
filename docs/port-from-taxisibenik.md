# Port checklist: upgrades from taxisibenik-code

Audited 2026-07-15 against C:\Users\sakic\taxisibenik-code (source project).
Each item below is MISSING here unless marked otherwise. Port by copying and
adapting the referenced source files, then `python build.py` and verify.

## Security and infrastructure (do before going live)

1. **Root `.htaccess`** - completely missing here. Port from taxisibenik
   `.htaccess`: HTTPS redirect, security headers (CSP, X-Frame-Options,
   nosniff, HSTS, Referrer-Policy, Permissions-Policy), FilesMatch deny for
   config files, Options -Indexes. SKIP the taxisibenik redirect map; this
   domain needs its own (old taxisibenik.hr/taxi-skradin URLs already 301
   here from the taxisibenik side).
2. **Admin: SHARED, not ported (owner decision 2026-07-15).** Both domains
   will live on the SAME cPanel account and share ONE database and ONE
   admin panel (the one at taxisibenik.hr/manage-k29q7x/). Therefore:
   a) DELETE the `admin/` folder here entirely; this site gets no admin.
   b) `config.php` here points at the SAME DB as taxisibenik
      (db name `taxisibenik-code`, user `antonio-code`).
   c) Add a `site` column to the shared tables (run once, in phpMyAdmin):
      `ALTER TABLE bookings ADD COLUMN site VARCHAR(10) NOT NULL DEFAULT 'sibenik' AFTER id;`
      `ALTER TABLE offers ADD COLUMN site VARCHAR(10) NOT NULL DEFAULT 'sibenik' AFTER id;`
      (offers also accepts 'both'.)
   d) `booking-submit.php` HERE stamps site='skradin'; on taxisibenik it
      stamps site='sibenik'. `offers-api.php` on each site filters
      WHERE site IN (<own site>, 'both').
   e) The taxisibenik admin gets a site badge + filter on bookings and a
      "show on" (sibenik/skradin/both) field on offers. Those edits happen
      in C:\Users\sakic\taxisibenik-code, not here.
   f) Emails: mail_from here stays noreply@taxiskradin.hr so customers see
      the domain they booked on; notifications go to the same inbox.
3. **`schema.sql`** - add `dropoff_details VARCHAR(120) NULL AFTER flight`
   (booking-submit.php writes it; fresh installs fail without it). Then
   `bookings-add-dropoff-details.sql` becomes redundant.
4. **Form hardening** - port from taxisibenik:
   - `db.php`: `tx_rate_limit()` file-based limiter.
   - `booking-submit.php` / `contact.php`: rate limiting, honeypot field
     (`company`), GDPR consent check (400 without `consent`).
   - All contact forms (home + contact, 11 langs): consent checkbox
     (`form-consent` markup linking each language's privacy slug) and
     honeypot field. CSS: `.form-consent`, `.hp-field` in styles.css.

## Bug fixes

5. **Cookie banner** - port `.cookie-banner[hidden] { display: none; }` in
   styles.css (without it the banner cannot be dismissed) and the
   "Accept Only Necessary" decline-button label in all footers.
6. **FAQ header** - taxisibenik's FAQ intro uses the dark `.page-hero` so the
   logo is visible before scroll. If/when this site gets an FAQ page, use
   `page-hero`, not the white `hub-intro`, for the top section.

## Build system

7. **`build.py`** - port from taxisibenik: sitemap with `xhtml:link`
   hreflang alternates per URL, and automatic BreadcrumbList JSON-LD on
   non-home pages (`HOME_LABEL` dict). Diff the two build.py files; they
   were identical at scaffold time, so the diff IS the upgrade list.

## Content and features

8. **Working hours** - footers and home pages here still show the OLD hours
   (Mon-Fri 07:00-21:00, Sat-Sun 06:00-15:00). New hours everywhere,
   including LocalBusiness openingHoursSpecification (weekday split shift =
   two specs): Mon-Fri 07:00-14:00 and 16:00-21:00, Sat-Sun 06:00-16:00.
9. **Offers page redesign** - port the `.rlo` return-leg banner: script.js
   offers rendering (auto SAVE%, countdown that expires 1h before the
   pickup window, pickup filter, prefilled WhatsApp/email booking links)
   and the `.rlo` CSS block. Also the extra fonts in
   `src/partials/base.html` (Barlow, Barlow Condensed 600/700, wider
   Cormorant Garamond weights).
10. **Booking widget** - port the i18n layer (`const I18N` + `t()`), the
    GROUPS ordering convention, and the option icons (incl. the wine glass
    used for wineries on taxisibenik). Keep this site's own PRICES/GROUPS
    data; port only the mechanics.
11. **GA4** - the loader pattern exists here but check the ID: taxisibenik
    uses its own property (G-HBG0GSXSHZ). taxiskradin.hr needs its OWN GA4
    property ID; the loader auto-disables on the placeholder.
12. **Arrival notes** - taxisibenik's service-area pages carry an
    "Arriving by plane?" `.hub-note-arrival` callout linking reverse
    airport routes. Port the CSS and apply the pattern where relevant.
13. **Wineries (planned)** - Sladic and Bibich are a short hop from Skradin.
    When adding them here: transport-only framing (see the disclaimer
    wording on taxisibenik's winery pages), Skradin-origin route pages,
    "Visit Local Wineries" item in the Transfers menu, wineries group +
    wine icon in the widget. Cross-link with taxisibenik's winery pages
    (Sibenik-origin) instead of competing.
14. **Partners page (optional)** - taxisibenik has /partners/ in 11 langs
    (travel agents, apartment/villa owners, agencies; taxi-provider
    partnerships explicitly not sought). Reuse `scripts/gen_partners.py`
    with adapted copy if wanted here.
15. **llms.txt / robots.txt** - refresh llms.txt for this site's real page
    set (hours, offers, partner/winery sections when added). robots.txt:
    disallow the PHP endpoints, reference the sitemap, and never mention
    the secret admin path.

## Already present here (verified at audit)

- `.claude/rules/` (synced 2026-07-15, identical to taxisibenik).
- Same src/pages + partials structure, build.py base, PRICES-driven widget.
- GA loader scaffold (needs own ID), booking backend files, offers API.
