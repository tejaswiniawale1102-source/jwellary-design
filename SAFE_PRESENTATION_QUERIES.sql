-- ============================================================================
-- CRITICAL: CLOSE SQL DEVELOPER BEFORE RUNNING THESE QUERIES
-- ============================================================================
-- The problem: SQL Developer keeps an open session that makes data disappear
-- Solution: Use these queries ONLY during presentation, then close immediately
-- ============================================================================

-- STEP 1: Run this FIRST to verify data exists
-- ============================================================================
SELECT 
    (SELECT COUNT(*) FROM products) AS "Products",
    (SELECT COUNT(*) FROM customers) AS "Customers",
    (SELECT COUNT(*) FROM bookings) AS "Bookings"
FROM DUAL;

-- Expected result: Products=48, Customers=16, Bookings=18
-- If you see 1, 1, 1 -> STOP and run QUICK_RESTORE.py first!

-- ============================================================================
-- STEP 2: Show 1NF (First Normal Form)
-- ============================================================================
SELECT 
    product_id,
    name,
    category,
    price,
    market_price
FROM products
FETCH FIRST 10 ROWS ONLY;

-- Explain to trainers: Atomic values, no repeating groups, has primary key

-- ============================================================================
-- STEP 3: Show 2NF (Second Normal Form)
-- ============================================================================
SELECT 
    bd.booking_detail_id,
    bd.booking_id,
    bd.product_id AS "Product ID (FK)",
    p.name AS "Product Name (from JOIN)",
    bd.quantity,
    bd.price
FROM booking_details bd
JOIN products p ON bd.product_id = p.product_id
FETCH FIRST 10 ROWS ONLY;

-- Explain: Product details NOT stored in booking_details (no redundancy)

-- ============================================================================
-- STEP 4: Show 3NF (Third Normal Form)
-- ============================================================================
SELECT 
    b.booking_id,
    b.customer_id AS "Customer ID (FK)",
    c.customername AS "Customer Name (from JOIN)",
    c.email AS "Email (from JOIN)",
    p.name AS "Product",
    b.total_price,
    b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
ORDER BY b.booking_id
FETCH FIRST 10 ROWS ONLY;

-- Explain: Customer details in separate table (no transitive dependency)

-- ============================================================================
-- STEP 5: IMMEDIATELY AFTER DEMO - CLOSE SQL DEVELOPER!
-- ============================================================================
-- Then run: python QUICK_RESTORE.py (just to be safe)
-- ============================================================================
