-- ============================================================================
-- 2NF (SECOND NORMAL FORM) DEMONSTRATION
-- ============================================================================
-- Requirement: No PARTIAL DEPENDENCIES
-- (All non-key attributes must depend on the ENTIRE primary key)
-- ============================================================================

-- Query 1: Show BOOKING_DETAILS table structure
-- This table has a COMPOSITE PRIMARY KEY: (booking_id, product_id)
SELECT bd.booking_id, bd.product_id, bd.quantity, bd.price
FROM booking_details bd
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ Primary Key = booking_id + product_id (BOTH together)
-- ✓ quantity depends on BOTH booking_id AND product_id
-- ✓ price depends on BOTH booking_id AND product_id
-- ✓ NO partial dependency (attributes don't depend on just one part of the key)


-- Query 2: Prove NO partial dependency - product details are NOT in BOOKING_DETAILS
-- If product_name was in BOOKING_DETAILS, it would depend only on product_id
-- (partial dependency - BAD!)
-- Instead, we use JOIN to get product details:
SELECT bd.booking_id, bd.product_id, p.name, p.category, bd.quantity
FROM booking_details bd
JOIN products p ON bd.product_id = p.product_id
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ Product name is in PRODUCTS table (depends on product_id alone)
-- ✓ NOT duplicated in BOOKING_DETAILS
-- ✓ This avoids partial dependency!


-- Query 3: Show tables with SINGLE primary keys (automatically in 2NF)
SELECT product_id, name, category, price
FROM products
WHERE ROWNUM <= 3;

-- EXPLANATION:
-- ✓ Primary Key = product_id (single column)
-- ✓ All attributes (name, category, price) depend on product_id
-- ✓ No partial dependencies possible with single-column primary key

-- ============================================================================
-- CONCLUSION: Database is in 2NF
-- No partial dependencies - all non-key attributes depend on entire primary key
-- ============================================================================
