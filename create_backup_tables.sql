-- ============================================================================
-- PERMANENT DATABASE BACKUP - RentEasyIndia
-- Run this ONCE to create backup tables that preserve your data
-- ============================================================================

-- Create backup table for products (if not exists)
CREATE TABLE products_backup AS SELECT * FROM products;

-- Create backup table for bookings (if not exists)
CREATE TABLE bookings_backup AS SELECT * FROM bookings;

-- Create backup table for booking_details (if not exists)
CREATE TABLE booking_details_backup AS SELECT * FROM booking_details;

-- Create backup table for customers (if not exists)
CREATE TABLE customers_backup AS SELECT * FROM customers;

-- Verify backups
SELECT 'PRODUCTS_BACKUP' as table_name, COUNT(*) as record_count FROM products_backup
UNION ALL
SELECT 'BOOKINGS_BACKUP', COUNT(*) FROM bookings_backup
UNION ALL
SELECT 'BOOKING_DETAILS_BACKUP', COUNT(*) FROM booking_details_backup
UNION ALL
SELECT 'CUSTOMERS_BACKUP', COUNT(*) FROM customers_backup;

-- ============================================================================
-- BACKUP COMPLETE!
-- ============================================================================
