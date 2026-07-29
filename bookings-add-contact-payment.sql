-- Booking form v2: preferred contact method, payment choice, company-invoice flag.
-- Run ONCE against the shared TAXI Antonio database (phpMyAdmin or:
--   mysql < bookings-add-contact-payment.sql) BEFORE deploying the new
-- booking form / booking-submit.php. The DB is shared by taxisibenik.hr and
-- taxiskradin.hr, so this migration only needs to run a single time.

ALTER TABLE bookings
  ADD COLUMN contact_method   VARCHAR(10) NULL AFTER notes,
  ADD COLUMN payment_option   VARCHAR(10) NULL AFTER contact_method,
  ADD COLUMN invoice_required TINYINT(1) NOT NULL DEFAULT 0 AFTER payment_option;
