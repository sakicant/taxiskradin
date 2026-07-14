<?php
require __DIR__ . '/auth.php';

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    tx_check_csrf();
    $c = tx_config();
    $user = trim($_POST['username'] ?? '');
    $pass = (string) ($_POST['password'] ?? '');

    // Small delay to slow brute-force attempts.
    usleep(300000);

    if (
        hash_equals($c['admin_user'], $user)
        && !empty($c['admin_pass_hash'])
        && password_verify($pass, $c['admin_pass_hash'])
    ) {
        session_regenerate_id(true);
        $_SESSION['admin_ok'] = true;
        header('Location: index.php');
        exit;
    }
    $error = 'Wrong username or password.';
}

if (tx_is_logged_in()) {
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Admin login | TAXI Antonio</title>
<link rel="stylesheet" href="admin.css">
</head>
<body class="admin-login-page">
  <form class="admin-card admin-login" method="POST" action="login.php">
    <h1>TAXI Antonio Admin</h1>
    <?php if ($error): ?><p class="admin-error"><?= e($error) ?></p><?php endif; ?>
    <input type="hidden" name="csrf" value="<?= e(tx_csrf_token()) ?>">
    <label for="username">Username</label>
    <input type="text" id="username" name="username" autocomplete="username" required>
    <label for="password">Password</label>
    <input type="password" id="password" name="password" autocomplete="current-password" required>
    <button type="submit" class="admin-btn admin-btn-primary">Log in</button>
  </form>
</body>
</html>
