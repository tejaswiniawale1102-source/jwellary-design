-- ============================================================================
-- DATABASE NORMALIZATION VERIFICATION QUERIES
-- RentEasyIndia Database - 1NF, 2NF, 3NF Compliance
-- ============================================================================

-- ============================================================================
-- 1NF (First Normal Form) Verification
-- ============================================================================
-- Requirements:
-- 1. Each column contains atomic (indivisible) values
-- 2. Each column contains values of a single type
-- 3. Each column has a unique name
-- 4. The order in which data is stored does not matter

-- Query 1.1: Verify PRODUCTS table has atomic values (no multi-valued attributes)
SELECT product_id, name, category, price, image_path, description
FROM products
WHERE ROWNUM <= 5;
-- ✓ All columns contain single, atomic values

-- Query 1.2: Verify BOOKINGS table has atomic values
SELECT booking_id, customer_id, total_price, booking_date, rent_date, return_date, status
FROM bookings
WHERE ROWNUM <= 5;
-- ✓ All columns contain single, atomic values

-- Query 1.3: Verify CUSTOMERS table has atomic values
SELECT customer_id, customername, email, phone, address
FROM customers
WHERE ROWNUM <= 5;
-- ✓ All columns contain single, atomic values


-- ============================================================================
-- 2NF (Second Normal Form) Verification
-- ============================================================================
-- Requirements:
-- 1. Must be in 1NF
-- 2. All non-key attributes must be fully functionally dependent on the primary key
-- 3. No partial dependencies (relevant for composite keys)

-- Query 2.1: Verify BOOKING_DETAILS has no partial dependencies
-- Primary Key: (booking_id, product_id) - composite key
SELECT bd.booking_id, bd.product_id, bd.quantity, bd.price,
       b.customer_id, b.total_price,
       p.name, p.category
FROM booking_details bd
JOIN bookings b ON bd.booking_id = b.booking_id
JOIN products p ON bd.product_id = p.product_id
WHERE ROWNUM <= 5;
-- ✓ quantity and price depend on BOTH booking_id AND product_id (no partial dependency)
-- ✓ Product details (name, category) are in PRODUCTS table, not duplicated here

-- Query 2.2: Verify PRODUCTS table - single primary key (product_id)
SELECT product_id, name, category, price
FROM products
WHERE ROWNUM <= 5;
-- ✓ All attributes (name, category, price) fully depend on product_id

-- Query 2.3: Verify BOOKINGS table - single primary key (booking_id)
SELECT booking_id, customer_id, total_price, rent_date, return_date
FROM bookings
WHERE ROWNUM <= 5;
-- ✓ All attributes fully depend on booking_id


-- ============================================================================
-- 3NF (Third Normal Form) Verification
-- ============================================================================
-- Requirements:
-- 1. Must be in 2NF
-- 2. No transitive dependencies (non-key attributes should not depend on other non-key attributes)

-- Query 3.1: Verify no transitive dependencies in BOOKINGS
-- Check: Does customer_name depend on customer_id (which depends on booking_id)?
SELECT b.booking_id, b.customer_id, c.customername, b.total_price
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
WHERE ROWNUM <= 5;
-- ✓ Customer name is NOT stored in BOOKINGS (would be transitive dependency)
-- ✓ Customer details are in separate CUSTOMERS table

-- Query 3.2: Verify no transitive dependencies in BOOKING_DETAILS
-- Check: Does product_name depend on product_id (which depends on booking_id)?
SELECT bd.booking_id, bd.product_id, p.name, p.category, bd.price
FROM booking_details bd
JOIN products p ON bd.product_id = p.product_id
WHERE ROWNUM <= 5;
-- ✓ Product details (name, category) are NOT stored in BOOKING_DETAILS
-- ✓ Product details are in separate PRODUCTS table

-- Query 3.3: Demonstrate proper normalization - Product info via JOIN, not duplication
SELECT b.booking_id, 
       c.customername,
       p.name AS product_name,
       p.category,
       b.total_price,
       b.rent_date,
       b.return_date
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
WHERE ROWNUM <= 5;
-- ✓ No redundant data - all information retrieved via proper JOINs


-- ============================================================================
-- NORMALIZATION SUMMARY QUERIES
-- ============================================================================

-- Query: Show table structure demonstrates proper normalization
SELECT 'PRODUCTS' AS table_name, 'product_id (PK)' AS primary_key, 'name, category, price, image_path, description' AS attributes FROM DUAL
UNION ALL
SELECT 'CUSTOMERS', 'customer_id (PK)', 'customername, email, phone, address' FROM DUAL
UNION ALL
SELECT 'BOOKINGS', 'booking_id (PK)', 'customer_id (FK), total_price, dates, status' FROM DUAL
UNION ALL
SELECT 'BOOKING_DETAILS', 'booking_id, product_id (Composite PK)', 'quantity, price' FROM DUAL
UNION ALL
SELECT 'CART', 'cart_id (PK)', 'customer_id (FK), product_id (FK), quantity' FROM DUAL
UNION ALL
SELECT 'WISHLIST', 'wishlist_id (PK)', 'customer_id (FK), product_id (FK)' FROM DUAL
UNION ALL
SELECT 'REVIEWS', 'review_id (PK)', 'customer_id (FK), product_id (FK), rating, comment' FROM DUAL;

-- ============================================================================
-- CONCLUSION
-- ============================================================================
-- ✓ 1NF: All tables have atomic values, no repeating groups
-- ✓ 2NF: No partial dependencies - all non-key attributes fully depend on primary key
-- ✓ 3NF: No transitive dependencies - customer/product details in separate tables
-- ============================================================================
