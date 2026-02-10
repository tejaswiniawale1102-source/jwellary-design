-- ============================================================================
-- 1NF (FIRST NORMAL FORM) DEMONSTRATION
-- ============================================================================
-- Requirement: All columns must contain ATOMIC (single, indivisible) values
-- ============================================================================

-- Query 1: Show PRODUCTS table - all values are atomic
SELECT product_id, name, category, price
FROM products
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ Each cell contains ONE value only
-- ✓ name = "Sapphire Premium Set" (not "Sapphire, Premium, Set")
-- ✓ category = "Jewelry" (not "Jewelry, Decor")
-- ✓ price = 4500 (not "4500, 5000, 6000")


-- Query 2: Show CUSTOMERS table - all values are atomic
SELECT customer_id, customername, email, phone
FROM customers
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ customername = "Rahul Sharma" (single name, not multiple names)
-- ✓ email = "rahul@example.com" (single email)
-- ✓ phone = "9876543210" (single phone number)


-- Query 3: Show BOOKINGS table - all values are atomic
SELECT booking_id, customer_id, total_price, rent_date, return_date, status
FROM bookings
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ No repeating groups
-- ✓ Each column has a single value
-- ✓ status = "Confirmed" (not "Confirmed, Pending")

-- ============================================================================
-- CONCLUSION: Database is in 1NF
-- All tables have atomic values with no repeating groups
-- ============================================================================
