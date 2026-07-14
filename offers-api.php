<?php
/**
 * Public read-only JSON feed of active special offers.
 * Consumed by /special-offers/ on the front end.
 */
require __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

try {
    $stmt = tx_db()->query(
        "SELECT id, route_from, route_to, offer_date, window_start, window_end,
                price, original_price, capacity, note
         FROM offers
         WHERE status = 'active' AND (offer_date IS NULL OR offer_date >= CURDATE())
         ORDER BY (offer_date IS NULL), offer_date ASC, window_start ASC
         LIMIT 100"
    );
    echo json_encode(['offers' => $stmt->fetchAll()], JSON_UNESCAPED_UNICODE);
} catch (Throwable $e) {
    http_response_code(500);
    error_log('offers-api failed: ' . $e->getMessage());
    echo json_encode(['offers' => [], 'error' => 'Could not load offers.']);
}
