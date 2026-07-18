<?php
/**
 * Copy this file to config.php on the server and fill in real values.
 * config.php is gitignored so your credentials never end up in the repo.
 *
 * SHARED DATABASE (bookings + offers):
 * taxiskradin.hr and taxisibenik.hr share ONE MySQL database, so bookings from
 * both sites land in the same `bookings` table and offers managed in one admin
 * appear on both sites. To do this, set db_host/db_name/db_user/db_pass below to
 * the SAME values as taxisibenik.hr's config.php. Do NOT create a second
 * database and do NOT re-import schema.sql / offers-schema.sql (the tables
 * already exist in the shared database). Both domains are on the same cPanel
 * account, so 'localhost' reaches the shared database from either docroot.
 */

return [
    // MySQL / MariaDB connection. Use the SAME credentials as taxisibenik.hr
    // so the two sites share one bookings + offers database.
    'db_host' => 'localhost',
    'db_name' => 'YOUR_SHARED_DB_NAME',
    'db_user' => 'YOUR_SHARED_DB_USER',
    'db_pass' => 'YOUR_SHARED_DB_PASSWORD',

    // Where booking notification emails are sent (you). The booking email itself
    // states which site the request came from, so a shared inbox is fine.
    'admin_email' => 'info@taxiskradin.hr',

    // "From" address for outgoing mail. Use an address on your own domain so
    // it is not flagged as spoofed.
    'mail_from' => 'noreply@taxiskradin.hr',

    // Admin dashboard login.
    // Username you type at the admin URL, and a password HASH (not the raw
    // password). Generate the hash once by running, on the server:
    //   php -r "echo password_hash('your-strong-password', PASSWORD_DEFAULT), PHP_EOL;"
    // then paste the printed string below.
    'admin_user' => 'antonio',
    'admin_pass_hash' => 'PASTE_PASSWORD_HASH_HERE',
];
