-- ============================================================================
-- 3NF (THIRD NORMAL FORM) DEMONSTRATION
-- ============================================================================
-- Requirement: No TRANSITIVE DEPENDENCIES
-- (Non-key attributes should NOT depend on other non-key attributes)
-- ============================================================================

-- Query 1: Show BOOKINGS table - customer_id is stored, NOT customer name
SELECT booking_id, customer_id, total_price, rent_date, status
FROM bookings
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ Only customer_id is stored (foreign key)
-- ✓ Customer name is NOT stored here
-- ✓ Why? Because customername depends on customer_id (transitive dependency)


-- Query 2: Prove NO transitive dependency - customer details via JOIN
-- To get customer name, we JOIN with CUSTOMERS table:
SELECT b.booking_id, b.customer_id, c.customername, b.total_price
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ customername is in CUSTOMERS table (where it belongs)
-- ✓ NOT duplicated in BOOKINGS table
-- ✓ Avoids transitive dependency: booking_id → customer_id → customername


-- Query 3: Show BOOKING_DETAILS - product_id is stored, NOT product details
SELECT bd.booking_id, bd.product_id, bd.quantity, bd.price
FROM booking_details bd
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ Only product_id is stored (foreign key)
-- ✓ Product name, category are NOT stored here
-- ✓ Why? Because they depend on product_id (transitive dependency)


-- Query 4: Prove NO transitive dependency - product details via JOIN
SELECT bd.booking_id, bd.product_id, p.name, p.category, bd.quantity
FROM booking_details bd
JOIN products p ON bd.product_id = p.product_id
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ Product details are in PRODUCTS table (where they belong)
-- ✓ NOT duplicated in BOOKING_DETAILS table
-- ✓ Avoids transitive dependency: booking_id → product_id → product_name


-- Query 5: Complete example - booking with customer and product details
SELECT 
    b.booking_id,
    c.customername,
    p.name AS product_name,
    p.category,
    b.total_price,
    b.rent_date
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
WHERE ROWNUM <= 5;

-- EXPLANATION:
-- ✓ All information retrieved via proper JOINs
-- ✓ No redundant data stored
-- ✓ Each table stores only what directly depends on its primary key

-- ============================================================================
-- CONCLUSION: Database is in 3NF
-- No transitive dependencies - customer and product details in separate tables
-- ============================================================================
