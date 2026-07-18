# Booking + Offers System: Setup Guide

This is the PHP + MySQL system behind the `/book/` page and the offers feed. It
stores every booking request in the shared database and emails you and the
customer. There is **no admin panel on taxiskradin.hr**: you manage bookings and
offers from the existing admin on taxisibenik.hr, because both sites share one
database (see below).

It runs on your mydataknox hosting (Apache + PHP + MySQL). It cannot run in the
local static preview (that server only serves static files, it does not execute
PHP), so all testing happens on the host.

## Files involved

| File | What it does |
|------|--------------|
| `config.sample.php` | Template for credentials. Copy to `config.php` on the server. |
| `config.php` | Your real DB credentials. **Not** in git. Server only. |
| `db.php` | Database connection helper. |
| `booking-submit.php` | Receives a booking from `/book/`, saves it to the shared DB, emails you + the customer. |
| `offers-api.php` | Public JSON feed the `/special-offers/` page reads. |
| `schema.sql` / `offers-schema.sql` | Reference definitions of the shared `bookings` and `offers` tables. Not re-imported (the tables already exist). |
| `.htaccess` | Blocks direct access to config/schema and disables directory listing. |
| `robots.txt` | Excludes the PHP endpoints from indexing. |

## Shared database and admin with taxisibenik.hr

taxiskradin.hr and taxisibenik.hr **share one MySQL database** for both bookings
and offers. Bookings from either site land in the same `bookings` table, and
offers you manage appear on both sites. Both domains live on the same cPanel
account, so `localhost` reaches the shared database from either site's document
root.

Because the data is shared, you also **share one admin**: the private dashboard
already on taxisibenik.hr manages everything. There is no separate login for
taxiskradin.hr, and no `admin/` folder is deployed to this domain.

The database and tables already exist (created for taxisibenik.hr), so you do
**not** create a new database or re-import the schema files. You only create
`config.php` pointing at the same database.

## One-time setup

### 1. Reuse the existing shared database
Use the **same** `db_name`, `db_user`, `db_pass` that taxisibenik.hr already
uses (copy them from its `config.php`). Do not create a new database and do not
import `schema.sql` / `offers-schema.sql`, the tables are already there.

### 2. Create config.php
1. Copy `config.sample.php` to `config.php` on the server.
2. Fill in `db_host` (usually `localhost`), `db_name`, `db_user`, `db_pass` with
   the shared-database values.
3. Set `admin_email` (where booking alerts go) and `mail_from` (an address on
   your domain).

### 3. Upload the files
Upload to your web root (same place as `index.html`): `booking-submit.php`,
`offers-api.php`, `db.php`, `config.php`, and `.htaccess`. (`config.sample.php`,
`schema.sql` and `offers-schema.sql` can stay too; the `.htaccess` blocks them
from being fetched.) Do **not** upload an `admin/` folder, there is none.

## Testing checklist
1. Open `/book/?from=Skradin - center&to=Split Airport (SPU)&trip=oneway&pax=2&lug=1&price=110`, fill date/time/contact, submit.
2. You should see the success message, get an email, and the customer gets an acknowledgement.
3. In phpMyAdmin, the shared `bookings` table should have the new row.
4. Open the admin on taxisibenik.hr, log in, and confirm the booking appears (its email notes it came from taxiskradin.hr).

## Day-to-day use
- Bookings from both sites land in the shared admin on taxisibenik.hr as **New**.
- Offers you add or edit in that admin appear on both sites' offers pages.
- The per-booking email tells you which site each request came from.

## Security notes
- `config.php` holds your credentials and is gitignored, keep it that way.
- Always run the site over HTTPS so nothing sensitive is sent in the clear.
- The admin login and its protection live on taxisibenik.hr; nothing to expose here.
