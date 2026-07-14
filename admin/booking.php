<?php
require __DIR__ . '/auth.php';
tx_require_login();
tx_auto_complete_bookings();

$id = (int) ($_GET['id'] ?? 0);
$stmt = tx_db()->prepare('SELECT * FROM bookings WHERE id = ?');
$stmt->execute([$id]);
$b = $stmt->fetch();

$STATUSES = ['new', 'confirmed', 'completed', 'cancelled'];
$STATUS_LABELS = ['new' => 'Booking (unpaid)', 'confirmed' => 'Upcoming (confirmed)', 'completed' => 'Completed', 'cancelled' => 'Cancelled'];
$PAYMENTS = ['unpaid' => 'Unpaid', 'deposit' => 'Deposit paid', 'paid' => 'Paid in full'];

$csrf = tx_csrf_token();
$returnUrl = 'booking.php?id=' . $id;
function fmt_dt($date, $time) { if (!$date) return '&mdash;'; return e($date) . ($time ? ' ' . e(substr($time, 0, 5)) : ''); }
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title><?= $b ? 'Booking #' . (int) $b['id'] : 'Booking not found' ?> | TAXI Antonio Admin</title>
<link rel="stylesheet" href="admin.css">
</head>
<body class="admin-page">
  <header class="admin-header">
    <strong>TAXI Antonio &mdash; Booking</strong>
    <nav class="admin-nav">
      <a href="index.php">Bookings</a>
      <a href="offers.php">Offers</a>
      <a class="admin-logout" href="logout.php">Log out</a>
    </nav>
  </header>

  <div class="admin-wrap">
    <p class="admin-back"><a href="index.php">&larr; Back to all bookings</a></p>

    <?php if (!$b): ?>
      <p class="admin-empty">Booking not found. It may have been deleted.</p>
    <?php else: ?>
      <article class="booking-card booking-detail status-<?= e($b['status']) ?>">
        <div class="booking-head">
          <div>
            <span class="booking-id">#<?= (int) $b['id'] ?></span>
            <span class="booking-route"><?= e($b['pickup']) ?> &rarr; <?= e($b['dropoff']) ?></span>
            <span class="booking-trip"><?= $b['trip_type'] === 'return' ? 'Return' : 'One way' ?></span>
          </div>
          <span class="booking-received">received <?= e(date('j M Y H:i', strtotime($b['created_at']))) ?></span>
        </div>

        <div class="booking-grid">
          <div><span>Pickup</span><strong><?= fmt_dt($b['pickup_date'], $b['pickup_time']) ?></strong></div>
          <?php if ($b['trip_type'] === 'return'): ?>
          <div><span>Return</span><strong><?= fmt_dt($b['return_date'], $b['return_time']) ?></strong></div>
          <?php endif; ?>
          <div><span>Passengers</span><strong><?= (int) $b['passengers'] ?></strong></div>
          <div><span>Luggage</span><strong><?= (int) $b['luggage'] ?></strong></div>
          <div><span>Quoted price</span><strong><?= $b['quoted_price'] ? e($b['quoted_price']) : 'custom' ?></strong></div>
          <div><span>Name</span><strong><?= e($b['customer_name']) ?></strong></div>
          <div><span>Email</span><strong><a href="mailto:<?= e($b['customer_email']) ?>"><?= e($b['customer_email']) ?></a></strong></div>
          <div><span>Phone</span><strong><?= $b['customer_phone'] ? e($b['customer_phone']) : '&mdash;' ?></strong></div>
          <?php if ($b['flight']): ?><div><span>Pickup details</span><strong><?= e($b['flight']) ?></strong></div><?php endif; ?>
          <?php if (!empty($b['dropoff_details'])): ?><div><span>Destination details</span><strong><?= e($b['dropoff_details']) ?></strong></div><?php endif; ?>
        </div>

        <?php if ($b['notes']): ?><p class="booking-notes"><span>Customer notes:</span> <?= e($b['notes']) ?></p><?php endif; ?>

        <form method="POST" action="update.php" class="booking-edit">
          <input type="hidden" name="csrf" value="<?= e($csrf) ?>">
          <input type="hidden" name="id" value="<?= (int) $b['id'] ?>">
          <input type="hidden" name="return" value="<?= e($returnUrl) ?>">
          <input type="hidden" name="action" value="save_all">
          <div class="booking-edit-row">
            <label>Status
              <select name="status">
                <?php foreach ($STATUSES as $s): ?>
                  <option value="<?= $s ?>" <?= $b['status'] === $s ? 'selected' : '' ?>><?= $STATUS_LABELS[$s] ?></option>
                <?php endforeach; ?>
              </select>
            </label>
            <label>Payment
              <select name="payment">
                <?php foreach ($PAYMENTS as $val => $lbl): ?>
                  <option value="<?= $val ?>" <?= $b['payment'] === $val ? 'selected' : '' ?>><?= $lbl ?></option>
                <?php endforeach; ?>
              </select>
            </label>
          </div>
          <label class="booking-edit-notes">Private notes (only you see these)
            <textarea name="admin_notes" rows="3" placeholder="Add a private note..."><?= e($b['admin_notes']) ?></textarea>
          </label>
          <p class="booking-edit-hint">Marking a deposit or full payment on a new booking moves it to Upcoming automatically.</p>
          <button type="submit" class="admin-btn">Save changes</button>
        </form>

        <form method="POST" action="update.php" class="booking-delete" onsubmit="return confirm('Delete booking #<?= (int) $b['id'] ?>? This cannot be undone.');">
          <input type="hidden" name="csrf" value="<?= e($csrf) ?>">
          <input type="hidden" name="id" value="<?= (int) $b['id'] ?>">
          <input type="hidden" name="action" value="delete">
          <button type="submit" class="admin-link-danger">Delete booking</button>
        </form>
      </article>
    <?php endif; ?>
  </div>
</body>
</html>
