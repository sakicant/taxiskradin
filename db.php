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

// File-based per-IP rate limiter (no DB needed). Returns true if the request is
// allowed, false if the caller has exceeded $max requests within $windowSeconds.
function tx_rate_limit($bucket, $max, $windowSeconds)
{
    $ip  = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    $dir = sys_get_temp_dir() . '/tx_ratelimit';
    if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
    $file = $dir . '/' . $bucket . '_' . hash('sha256', $ip);
    $fp = @fopen($file, 'c+');
    if (!$fp) { return true; }
    @flock($fp, LOCK_EX);
    $now   = time();
    $raw   = stream_get_contents($fp);
    $times = array_filter(
        array_map('intval', $raw === '' ? [] : explode(',', $raw)),
        function ($t) use ($now, $windowSeconds) { return $t > $now - $windowSeconds; }
    );
    $allowed = count($times) < $max;
    if ($allowed) { $times[] = $now; }
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, implode(',', $times));
    @flock($fp, LOCK_UN);
    fclose($fp);
    return $allowed;
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
