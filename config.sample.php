<?php
/**
 * Copy this file to config.php on the server and fill in real values.
 * config.php is gitignored so your credentials never end up in the repo.
 */

return [
    // MySQL / MariaDB connection (create the DB + user in cPanel first).
    'db_host' => 'localhost',
    'db_name' => 'YOUR_DB_NAME',
    'db_user' => 'YOUR_DB_USER',
    'db_pass' => 'YOUR_DB_PASSWORD',

    // Where booking notification emails are sent (you).
    'admin_email' => 'info@taxisibenik.hr',

    // "From" address for outgoing mail. Use an address on your own domain so
    // it is not flagged as spoofed.
    'mail_from' => 'noreply@taxisibenik.hr',

    // Admin dashboard login.
    // Username you type at /admin/, and a password HASH (not the raw password).
    // Generate the hash once by running, on the server:
    //   php -r "echo password_hash('your-strong-password', PASSWORD_DEFAULT), PHP_EOL;"
    // then paste the printed string below.
    'admin_user' => 'antonio',
    'admin_pass_hash' => 'PASTE_PASSWORD_HASH_HERE',
];
