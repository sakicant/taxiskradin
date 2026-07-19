<?php
/**
 * Public endpoint that receives a booking from the /book/ page,
 * stores it in the database, and emails Antonio + the customer.
 * Returns JSON so the existing front-end fetch() keeps working.
 */

require __DIR__ . '/db.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Throttle abuse: at most 10 booking requests per IP per hour.
if (!tx_rate_limit('booking', 10, 3600)) {
    http_response_code(429);
    echo json_encode(['success' => false, 'error' => 'Too many requests. Please try again shortly, or call/WhatsApp me.']);
    exit;
}

function field($key, $max = 255)
{
    $v = isset($_POST[$key]) ? trim((string) $_POST[$key]) : '';
    $v = str_replace(["\r", "\n", "\0"], ' ', $v);
    return mb_substr($v, 0, $max);
}

// Honeypot: real users never fill this hidden field.
if (field('company') !== '') {
    echo json_encode(['success' => true]);
    exit;
}

// GDPR: the customer must tick the privacy-policy consent box.
if (empty($_POST['consent'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Please accept the privacy policy to send your booking.']);
    exit;
}

$pickup      = field('pickup', 120);
$dropoff     = field('dropoff', 120);
$trip        = field('trip', 20) === 'return' ? 'return' : 'oneway';
$pickupDate  = field('pickup_date', 20);
$pickupTime  = field('pickup_time', 20);
$returnDate  = field('return_date', 20);
$returnTime  = field('return_time', 20);
$passengers  = (int) field('passengers', 3);
$luggage     = (int) field('luggage', 3);
$price       = field('price', 40);
$name        = field('name', 120);
$email       = field('email', 160);
$phone       = field('phone', 60);
$flight      = field('flight', 120);
$dropoffDet  = field('dropoff_details', 120);
$notes       = isset($_POST['notes']) ? mb_substr(trim((string) $_POST['notes']), 0, 2000) : '';

$errors = [];
if ($pickup === '' || $dropoff === '') $errors[] = 'pickup and destination';
if ($name === '') $errors[] = 'your name';
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'a valid email';
if ($pickupDate === '') $errors[] = 'pickup date';
if ($pickupTime === '') $errors[] = 'pickup time';

if ($errors) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Please provide ' . implode(', ', $errors) . '.']);
    exit;
}

$passengers = max(1, min(4, $passengers));
$luggage    = max(0, min(9, $luggage));

// Normalise date/time to NULL when empty so MySQL accepts them.
$nn = function ($v) { return $v === '' ? null : $v; };

try {
    $stmt = tx_db()->prepare(
        'INSERT INTO bookings
         (created_at, pickup, dropoff, trip_type, pickup_date, pickup_time,
          return_date, return_time, passengers, luggage, quoted_price,
          customer_name, customer_email, customer_phone, flight, dropoff_details, notes)
         VALUES
         (NOW(), :pickup, :dropoff, :trip, :pdate, :ptime,
          :rdate, :rtime, :pax, :lug, :price,
          :name, :email, :phone, :flight, :dropoff_details, :notes)'
    );
    $stmt->execute([
        ':pickup' => $pickup,
        ':dropoff' => $dropoff,
        ':trip' => $trip,
        ':pdate' => $nn($pickupDate),
        ':ptime' => $nn($pickupTime),
        ':rdate' => $nn($returnDate),
        ':rtime' => $nn($returnTime),
        ':pax' => $passengers,
        ':lug' => $luggage,
        ':price' => $nn($price),
        ':name' => $name,
        ':email' => $email,
        ':phone' => $nn($phone),
        ':flight' => $nn($flight),
        ':dropoff_details' => $nn($dropoffDet),
        ':notes' => $notes === '' ? null : $notes,
    ]);
    $id = tx_db()->lastInsertId();
} catch (PDOException $e) {
    http_response_code(500);
    error_log('Booking insert failed: ' . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Could not save your booking. Please call or WhatsApp me instead.']);
    exit;
}

// Build a readable summary for the emails.
$lines = [
    "Route: {$pickup} -> {$dropoff}",
    'Trip: ' . ($trip === 'return' ? 'Return' : 'One way'),
    "Pickup: {$pickupDate} {$pickupTime}",
];
if ($trip === 'return') {
    $lines[] = 'Return: ' . ($returnDate !== '' ? $returnDate : 'not set') . ' ' . $returnTime;
}
$lines[] = "Passengers: {$passengers}   Luggage: {$luggage}";
$lines[] = 'Quoted price: ' . ($price !== '' ? $price : 'custom');
$lines[] = "Name: {$name}";
$lines[] = "Email: {$email}";
$lines[] = 'Phone: ' . ($phone !== '' ? $phone : 'not provided');
if ($flight !== '') $lines[] = "Pickup details: {$flight}";
if ($dropoffDet !== '') $lines[] = "Destination details: {$dropoffDet}";
if ($notes !== '') $lines[] = "Notes: {$notes}";
$summary = implode("\n", $lines);

$c = tx_config();
$headers = 'From: TAXI Antonio <' . $c['mail_from'] . ">\r\n" .
           'Reply-To: ' . $email . "\r\n" .
           "Content-Type: text/plain; charset=utf-8\r\n";

// Notify Antonio.
@mail(
    $c['admin_email'],
    'New booking #' . $id . ': ' . $pickup . ' to ' . $dropoff,
    "New booking request (#{$id}) from taxiskradin.hr:\n\n{$summary}\n\nManage it in the admin dashboard.",
    $headers
);

// Acknowledge the customer.
$custHeaders = 'From: TAXI Antonio <' . $c['mail_from'] . ">\r\n" .
               'Reply-To: ' . $c['admin_email'] . "\r\n" .
               "Content-Type: text/plain; charset=utf-8\r\n";
@mail(
    $email,
    'Your TAXI Antonio booking request (#' . $id . ')',
    "Hi {$name},\n\nThank you for your booking request. I have received it and will confirm shortly, usually within a few hours.\n\nYour request:\n\n{$summary}\n\nIf anything is wrong, just reply to this email or call +385 99 447 1013.\n\nAntonio\nTAXI Antonio, Skradin",
    $custHeaders
);

echo json_encode(['success' => true, 'id' => $id]);
