<?php
/**
 * Shared config loader + PDO connection.
 * Included by booking-submit.php and the admin pages.
 */

function tx_config()
{
    static $config = null;
    if ($config === null) {
        $path = __DIR__ . '/config.php';
        if (!is_file($path)) {
            http_response_code(500);
            exit('Configuration missing. Copy config.sample.php to config.php.');
        }
        $config = require $path;
    }
    return $config;
}

function tx_db()
{
    static $pdo = null;
    if ($pdo === null) {
        $c = tx_config();
        $dsn = "mysql:host={$c['db_host']};dbname={$c['db_name']};charset=utf8mb4";
        try {
            $pdo = new PDO($dsn, $c['db_user'], $c['db_pass'], [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
            ]);
        } catch (PDOException $e) {
            http_response_code(500);
            error_log('DB connection failed: ' . $e->getMessage());
            exit('Database connection failed.');
        }
    }
    return $pdo;
}
