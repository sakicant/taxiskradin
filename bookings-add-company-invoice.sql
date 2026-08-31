-- Booking form v3: company invoice details.
-- Run ONCE against the shared TAXI Antonio database (phpMyAdmin or:
--   mysql < bookings-add-company-invoice.sql) BEFORE deploying the new
-- booking form / booking-submit.php. The DB is shared by taxisibenik.hr and
-- taxiskradin.hr, so this migration only needs to run a single time.

ALTER TABLE bookings
  ADD COLUMN company_name    VARCHAR(160) NULL AFTER invoice_required,
  ADD COLUMN company_vat     VARCHAR(40)  NULL AFTER company_name,
  ADD COLUMN company_address VARCHAR(160) NULL AFTER company_vat,
  ADD COLUMN company_zip     VARCHAR(20)  NULL AFTER company_address,
  ADD COLUMN company_city    VARCHAR(80)  NULL AFTER company_zip;
