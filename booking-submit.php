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

// Authoritative fare lookup. prices.json is generated from the PRICES matrix
// in script.js at build time, so the server never trusts the ?price= value
// that came in through the booking URL (which a visitor could edit).
function tx_price_oneway($from, $to)
{
    static $PRICES = null;
    if ($PRICES === null) {
        $p = @file_get_contents(__DIR__ . '/prices.json');
        $PRICES = $p ? (json_decode($p, true) ?: []) : [];
    }
    if (isset($PRICES[$from][$to])) return $PRICES[$from][$to];
    if (isset($PRICES[$to][$from])) return $PRICES[$to][$from];
    return null;
}

// Honeypot: real users never see this hidden field, but form-spam bots fill it
// with links. Only reject on link-like content, so a browser or password
// manager auto-filling the hidden "company" field can't silently drop a real
// booking (an autofilled company name has no URL and passes through).
if (preg_match('#https?://|www\.#i', field('company'))) {
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

// Preferred contact method + payment choice + company-invoice flag (new form).
$contactMethod = field('contact_method', 20);
$paymentOption = field('payment_option', 20);
$invoiceReq    = !empty($_POST['invoice_required']) ? 1 : 0;
if ($contactMethod !== 'whatsapp' && $contactMethod !== 'email') $contactMethod = '';
if ($paymentOption !== 'full' && $paymentOption !== 'deposit') $paymentOption = '';

$errors = [];
if ($pickup === '' || $dropoff === '') $errors[] = 'pickup and destination';
if ($name === '') $errors[] = 'your name';
// Contact requirement honours the chosen method. Whatsapp-only bookings do not
// need an email; if one is given it must still be valid. A form with no method
// chooser (legacy) keeps the original "email required" rule.
if ($contactMethod === 'whatsapp') {
    if ($phone === '') $errors[] = 'your WhatsApp number';
    if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'a valid email';
} else {
    if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'a valid email';
}
if ($pickupDate === '') $errors[] = 'pickup date';
if ($pickupTime === '') $errors[] = 'pickup time';

if ($errors) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Please provide ' . implode(', ', $errors) . '.']);
    exit;
}

// Recompute the fixed fare from the route itself, ignoring the submitted
// price, so editing ?price= in the booking link cannot change what is stored.
if ($passengers >= 5) {
    $price = 'custom';                       // van needed, quoted by hand
} elseif ($pickup === $dropoff) {
    $price = 'meter';                        // local ride, on the taxi meter
} else {
    $ow = tx_price_oneway($pickup, $dropoff);
    if ($ow === null) {
        $price = 'custom';                   // no fixed fare for this route
    } else {
        $price = (string) ($trip === 'return' ? $ow * 2 : $ow);
    }
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
          customer_name, customer_email, customer_phone, flight, dropoff_details, notes,
          contact_method, payment_option, invoice_required)
         VALUES
         (NOW(), :pickup, :dropoff, :trip, :pdate, :ptime,
          :rdate, :rtime, :pax, :lug, :price,
          :name, :email, :phone, :flight, :dropoff_details, :notes,
          :contact_method, :payment_option, :invoice_required)'
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
        ':contact_method' => $nn($contactMethod),
        ':payment_option' => $nn($paymentOption),
        ':invoice_required' => $invoiceReq,
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
$lines[] = 'Fixed price: ' . (is_numeric($price) ? 'EUR ' . $price : ($price !== '' ? $price : 'custom'));
$lines[] = "Name: {$name}";
$lines[] = 'Email: ' . ($email !== '' ? $email : 'not provided');
$lines[] = 'Phone: ' . ($phone !== '' ? $phone : 'not provided');
if ($contactMethod !== '') {
    $lines[] = 'Preferred contact: ' . ($contactMethod === 'whatsapp' ? 'WhatsApp' : 'Email');
}
if ($paymentOption !== '') {
    $lines[] = 'Payment choice: ' . ($paymentOption === 'full' ? 'Pay in full' : 'Deposit to confirm (20%, min EUR 20)');
}
if ($invoiceReq) $lines[] = 'Company invoice: requested';
if ($flight !== '') $lines[] = "Pickup details: {$flight}";
if ($dropoffDet !== '') $lines[] = "Destination details: {$dropoffDet}";
if ($notes !== '') $lines[] = "Notes: {$notes}";
$summary = implode("\n", $lines);

$c = tx_config();
$headers = 'From: TAXI Antonio <' . $c['mail_from'] . ">\r\n" .
           ($email !== '' ? 'Reply-To: ' . $email . "\r\n" : '') .
           "Content-Type: text/plain; charset=utf-8\r\n";

// Notify Antonio.
@mail(
    $c['admin_email'],
    'New booking #' . $id . ': ' . $pickup . ' to ' . $dropoff,
    "New booking request (#{$id}) from taxiskradin.hr:\n\n{$summary}\n\nManage it in the admin dashboard.",
    $headers
);

// Acknowledge the customer, only when they left an email (WhatsApp-only
// bookings are confirmed by Antonio over WhatsApp instead).
if ($email !== '') {
    $custHeaders = 'From: TAXI Antonio <' . $c['mail_from'] . ">\r\n" .
                   'Reply-To: ' . $c['admin_email'] . "\r\n" .
                   "Content-Type: text/plain; charset=utf-8\r\n";
    @mail(
        $email,
        'Your TAXI Antonio booking request (#' . $id . ')',
        "Hi {$name},\n\nThank you for your booking request. I have received it and will confirm shortly, usually within a few hours.\n\nYour request:\n\n{$summary}\n\nIf anything is wrong, just reply to this email or call +385 99 447 1013.\n\nAntonio\nTAXI Antonio, Skradin",
        $custHeaders
    );
}

echo json_encode(['success' => true, 'id' => $id]);
