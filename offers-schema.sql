-- Special / last-minute offers (empty-leg discounts).
-- Run once against the taxisibenik database:
--   mysql -u <user> -p <dbname> < offers-schema.sql

CREATE TABLE IF NOT EXISTS offers (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  route_from     VARCHAR(120) NOT NULL,
  route_to       VARCHAR(120) NOT NULL,
  offer_date     DATE NULL,
  window_start   TIME NULL,
  window_end     TIME NULL,
  price          DECIMAL(8,2) NOT NULL,
  original_price DECIMAL(8,2) NULL,
  capacity       TINYINT UNSIGNED NOT NULL DEFAULT 4,
  note           VARCHAR(255) NULL,
  status         ENUM('active','hidden') NOT NULL DEFAULT 'active',
  created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
