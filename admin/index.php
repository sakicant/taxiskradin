<?php
require __DIR__ . '/auth.php';
tx_require_login();
tx_auto_complete_bookings();

$STATUSES = ['new', 'confirmed', 'completed', 'cancelled'];
// Owner-facing labels for the workflow states.
$STATUS_LABELS = [
    'new'       => 'Booking (unpaid)',
    'confirmed' => 'Upcoming (confirmed)',
    'completed' => 'Completed',
    'cancelled' => 'Cancelled',
];
$CHIP_LABELS = [
    'new' => 'Bookings', 'confirmed' => 'Upcoming', 'completed' => 'Completed', 'cancelled' => 'Cancelled',
];

$statusFilter = $_GET['status'] ?? '';
$q = trim($_GET['q'] ?? '');

$where = [];
$params = [];
if (in_array($statusFilter, $STATUSES, true)) {
    $where[] = 'status = ?';
    $params[] = $statusFilter;
}
if ($q !== '') {
    $where[] = '(customer_name LIKE ? OR customer_email LIKE ? OR pickup LIKE ? OR dropoff LIKE ?)';
    $like = '%' . $q . '%';
    array_push($params, $like, $like, $like, $like);
}
$sql = 'SELECT id, created_at, pickup, dropoff, pickup_date, pickup_time, customer_name, status, payment FROM bookings';
if ($where) $sql .= ' WHERE ' . implode(' AND ', $where);
$sql .= ' ORDER BY (pickup_date IS NULL), pickup_date ASC, pickup_time ASC LIMIT 500';
$stmt = tx_db()->prepare($sql);
$stmt->execute($params);
$bookings = $stmt->fetchAll();

$counts = ['all' => 0, 'new' => 0, 'confirmed' => 0, 'completed' => 0, 'cancelled' => 0];
foreach (tx_db()->query('SELECT status, COUNT(*) c FROM bookings GROUP BY status') as $r) {
    $counts[$r['status']] = (int) $r['c'];
    $counts['all'] += (int) $r['c'];
}

function chip_url($status)
{
    $params = $_GET;
    if ($status === '') unset($params['status']); else $params['status'] = $status;
    return 'index.php' . ($params ? '?' . http_build_query($params) : '');
}
function fmt_date($date) { return $date ? date('j M Y', strtotime($date)) : '&mdash;'; }
function fmt_time($time) { return $time ? substr($time, 0, 5) : '&mdash;'; }
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Bookings | TAXI Antonio Admin</title>
<link rel="stylesheet" href="admin.css">
</head>
<body class="admin-page">
  <header class="admin-header">
    <strong>TAXI Antonio &mdash; Bookings</strong>
    <nav class="admin-nav">
      <a href="index.php" class="active">Bookings</a>
      <a href="offers.php">Offers</a>
      <a class="admin-logout" href="logout.php">Log out</a>
    </nav>
  </header>

  <div class="admin-wrap">
    <form class="admin-search" method="GET" action="index.php">
      <?php if ($statusFilter): ?><input type="hidden" name="status" value="<?= e($statusFilter) ?>"><?php endif; ?>
      <input type="search" name="q" placeholder="Search name, email, route..." value="<?= e($q) ?>">
      <button type="submit" class="admin-btn">Search</button>
      <?php if ($q): ?><a class="admin-btn admin-btn-ghost" href="<?= e(chip_url($statusFilter)) ?>">Clear</a><?php endif; ?>
    </form>

    <nav class="admin-chips">
      <a class="admin-chip <?= $statusFilter === '' ? 'active' : '' ?>" href="<?= e(chip_url('')) ?>">All (<?= $counts['all'] ?>)</a>
      <?php foreach ($STATUSES as $s): ?>
        <a class="admin-chip status-<?= $s ?> <?= $statusFilter === $s ? 'active' : '' ?>" href="<?= e(chip_url($s)) ?>"><?= $CHIP_LABELS[$s] ?> (<?= $counts[$s] ?>)</a>
      <?php endforeach; ?>
    </nav>

    <?php if (!$bookings): ?>
      <p class="admin-empty">No bookings found.</p>
    <?php else: ?>
    <div class="admin-table-wrap">
      <table class="admin-table">
        <thead>
          <tr><th>Ref</th><th>Client</th><th>Route</th><th>Date</th><th>Time</th><th>Status</th></tr>
        </thead>
        <tbody>
          <?php foreach ($bookings as $b): $url = 'booking.php?id=' . (int) $b['id']; ?>
          <tr class="row-link status-<?= e($b['status']) ?>" onclick="if(!window.getSelection().toString())location.href='<?= $url ?>'">
            <td class="col-ref"><a href="<?= $url ?>">#<?= (int) $b['id'] ?></a></td>
            <td><?= e($b['customer_name']) ?></td>
            <td class="col-route"><?= e($b['pickup']) ?> <span>&rarr;</span> <?= e($b['dropoff']) ?></td>
            <td><?= fmt_date($b['pickup_date']) ?></td>
            <td><?= fmt_time($b['pickup_time']) ?></td>
            <td><span class="status-badge status-<?= e($b['status']) ?>"><?= $CHIP_LABELS[$b['status']] ?? ucfirst($b['status']) ?></span></td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <?php endif; ?>
  </div>
</body>
</html>
