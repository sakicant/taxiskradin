<?php
/**
 * Session, login guard, and CSRF helpers for the admin dashboard.
 */

require __DIR__ . '/../db.php';

if (session_status() !== PHP_SESSION_ACTIVE) {
    session_set_cookie_params([
        'httponly' => true,
        'samesite' => 'Lax',
        'secure'   => (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off'),
    ]);
    session_start();
}

function tx_is_logged_in()
{
    return !empty($_SESSION['admin_ok']);
}

function tx_require_login()
{
    if (!tx_is_logged_in()) {
        header('Location: login.php');
        exit;
    }
}

function tx_csrf_token()
{
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function tx_check_csrf()
{
    $sent = $_POST['csrf'] ?? '';
    if (!is_string($sent) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $sent)) {
        http_response_code(400);
        exit('Invalid request token. Go back and try again.');
    }
}

function e($v)
{
    return htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');
}

// Auto-complete: a confirmed booking becomes "completed" about 6 hours after
// its ride time (the return leg for return trips, otherwise the pickup).
// Runs on admin page loads, so no cron is required.
function tx_auto_complete_bookings()
{
    try {
        tx_db()->exec(
            "UPDATE bookings SET status = 'completed'
             WHERE status = 'confirmed' AND (
               (trip_type = 'return' AND return_date IS NOT NULL AND return_time IS NOT NULL
                  AND TIMESTAMP(return_date, return_time) + INTERVAL 6 HOUR < NOW())
               OR ((trip_type <> 'return' OR return_date IS NULL OR return_time IS NULL)
                  AND pickup_date IS NOT NULL AND pickup_time IS NOT NULL
                  AND TIMESTAMP(pickup_date, pickup_time) + INTERVAL 6 HOUR < NOW())
             )"
        );
    } catch (Throwable $e) {
        error_log('auto-complete failed: ' . $e->getMessage());
    }
}
