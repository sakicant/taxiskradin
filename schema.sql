-- TAXI Antonio booking table.
-- Import once in phpMyAdmin (or `mysql < schema.sql`) after creating the database.

CREATE TABLE IF NOT EXISTS bookings (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    created_at     DATETIME NOT NULL,
    pickup         VARCHAR(120) NOT NULL,
    dropoff        VARCHAR(120) NOT NULL,
    trip_type      VARCHAR(20)  NOT NULL DEFAULT 'oneway',
    pickup_date    DATE NULL,
    pickup_time    TIME NULL,
    return_date    DATE NULL,
    return_time    TIME NULL,
    passengers     INT NOT NULL DEFAULT 1,
    luggage        INT NOT NULL DEFAULT 0,
    quoted_price   VARCHAR(40) NULL,
    customer_name  VARCHAR(120) NOT NULL,
    customer_email VARCHAR(160) NOT NULL,
    customer_phone VARCHAR(60) NULL,
    flight         VARCHAR(80) NULL,
    notes          TEXT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'new',
    payment        VARCHAR(20) NOT NULL DEFAULT 'unpaid',
    admin_notes    TEXT NULL,
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
