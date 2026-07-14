-- Add a destination-details column to bookings (drop-off address or a flight number).
-- The existing `flight` column now holds pickup details (arriving flight or address).
-- Run once against the taxisibenik database:
--   mysql -u <user> -p <dbname> < bookings-add-dropoff-details.sql

ALTER TABLE bookings
  ADD COLUMN dropoff_details VARCHAR(120) NULL AFTER flight;
