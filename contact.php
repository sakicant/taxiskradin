<?php
require __DIR__ . '/db.php';
header('Content-Type: application/json');

$to = 'info@taxiskradin.hr';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Throttle abuse: at most 6 messages per IP per hour.
if (!tx_rate_limit('contact', 6, 3600)) {
    http_response_code(429);
    echo json_encode(['success' => false, 'error' => 'Too many messages. Please try again shortly, or call/WhatsApp me.']);
    exit;
}

// Honeypot: real users never fill this hidden field.
if (isset($_POST['company']) && trim((string) $_POST['company']) !== '') {
    echo json_encode(['success' => true]);
    exit;
}

// GDPR: the sender must tick the privacy-policy consent box.
if (empty($_POST['consent'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Please accept the privacy policy to send your message.']);
    exit;
}

function clean_line($value) {
    return trim(str_replace(["\r", "\n"], '', $value));
}

$name    = isset($_POST['name']) ? clean_line($_POST['name']) : '';
$email   = isset($_POST['email']) ? clean_line($_POST['email']) : '';
$phone   = isset($_POST['phone']) ? clean_line($_POST['phone']) : '';
$topic   = isset($_POST['topic']) ? clean_line($_POST['topic']) : '';
$message = isset($_POST['message']) ? trim($_POST['message']) : '';

if ($name === '' || $email === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Please fill in all required fields with a valid email.']);
    exit;
}

$allowed_topics = ['General inquiry', 'Booking', 'Quote request', 'Day trip', 'Complaint', 'Other'];
if (!in_array($topic, $allowed_topics, true)) {
    $topic = 'General inquiry';
}

$subject = $topic . ' from ' . $name . ' (taxiskradin.hr)';

$body  = "New contact form submission from taxiskradin.hr\n\n";
$body .= "Topic: $topic\n";
$body .= "Name: $name\n";
$body .= "Email: $email\n";
$body .= "Phone: " . ($phone !== '' ? $phone : 'Not provided') . "\n\n";
$body .= "Message:\n$message\n";

$headers   = [];
$headers[] = 'From: TAXI Antonio Website <noreply@taxiskradin.hr>';
$headers[] = 'Reply-To: ' . $email;
$headers[] = 'X-Mailer: PHP/' . phpversion();

$sent = mail($to, $subject, $body, implode("\r\n", $headers));

if ($sent) {
    echo json_encode(['success' => true]);
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Could not send message. Please call or WhatsApp me instead.']);
}
