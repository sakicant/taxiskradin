# Booking + Admin System: Setup Guide

This is the PHP + MySQL booking system that stores every request from the
`/book/` page and lets you manage bookings from a private admin dashboard.

It runs on your mydataknox hosting (Apache + PHP + MySQL). It cannot run in the
local static preview (that server only serves static files, it does not execute
PHP), so all testing happens on the host. Do a first test in a subfolder if you
want to be cautious, then move it to the web root.

## Files involved

| File | What it does |
|------|--------------|
| `config.sample.php` | Template for credentials. Copy to `config.php` on the server. |
| `config.php` | Your real DB + admin credentials. **Not** in git. Server only. |
| `schema.sql` | Creates the `bookings` table. Import once. |
| `db.php` | Database connection helper. |
| `booking-submit.php` | Receives a booking from `/book/`, saves it, emails you + the customer. |
| `admin/` | Password-protected dashboard (login, list, status/payment, notes, delete). |
| `.htaccess` | Blocks direct access to config/schema and disables directory listing. |
| `robots.txt` | Tells search engines not to index `/admin/`. |

## Shared database with taxisibenik.hr

taxiskradin.hr and taxisibenik.hr **share one MySQL database** for both bookings
and offers. Bookings from either site land in the same `bookings` table, and
offers you manage in one admin appear on both sites. Both domains live on the
same cPanel account, so `localhost` reaches the shared database from either
site's document root.

That means the database and tables already exist (they were created for
taxisibenik.hr). You do **not** create a new database or re-import the schema
files for taxiskradin.hr. You only create `config.php` (step below) pointing at
the same database.

## One-time setup

### 1. Reuse the existing shared database
Use the **same** `db_name`, `db_user`, `db_pass` that taxisibenik.hr already
uses (copy them from its `config.php`). Skip creating a new database and skip
importing `schema.sql` / `offers-schema.sql`, the `bookings` and `offers` tables
are already there. (`schema.sql` and `offers-schema.sql` are kept in the repo
only as the reference definition of the shared tables.)

### 3. Create config.php
1. Copy `config.sample.php` to `config.php` on the server.
2. Fill in `db_host` (usually `localhost`), `db_name`, `db_user`, `db_pass`.
3. Set `admin_email` (where booking alerts go) and `mail_from` (an address on your domain).
4. Set `admin_user` to whatever username you want to log in with.
5. Generate your password hash. In cPanel to Terminal (or ask support), run:
   ```
   php -r "echo password_hash('choose-a-strong-password', PASSWORD_DEFAULT), PHP_EOL;"
   ```
   Copy the printed line (starts with `$2y$...`) into `admin_pass_hash`.

### 4. Upload the files
Upload to your web root (same place as `index.html`):
`booking-submit.php`, `db.php`, `config.php`, `.htaccess`, `robots.txt`, and the
whole `admin/` folder. (`config.sample.php` and `schema.sql` can stay too; the
`.htaccess` blocks them from being fetched.)

## Testing checklist
1. Open `/book/?from=Šibenik - center&to=Split Airport (SPU)&trip=oneway&pax=2&lug=1&price=95`, fill date/time/contact, submit.
2. You should see the success message, get an email, and the customer gets an acknowledgement.
3. In phpMyAdmin, the `bookings` table should have the new row.
4. Go to `/admin/`, log in, and confirm the booking appears.
5. Change its **Status** and **Payment**, add a private note, refresh, confirm it saved.

## Day-to-day use
- Every booking from the site lands in `/admin/` as **New**.
- Set **Status**: New to Confirmed to Completed (or Cancelled).
- Set **Payment** independently: Unpaid to Deposit paid to Paid in full (you handle the actual money by email/transfer as you do now).
- Add private notes only you can see. Search by name/email/route, or filter by status.

## Security notes
- `config.php` holds your credentials and is gitignored, keep it that way.
- The admin area requires login and is set to `noindex`; `robots.txt` also hides it.
- Always run the site over HTTPS so the admin password is never sent in the clear.
- To change your admin password later, regenerate the hash (step 3.5) and update `config.php`.
