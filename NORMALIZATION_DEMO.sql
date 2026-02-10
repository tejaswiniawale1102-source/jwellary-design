-- ============================================================================
-- DATABASE NORMALIZATION DEMONSTRATION (1NF, 2NF, 3NF)
-- RentEasyIndia - Rental Management System
-- ============================================================================

-- ============================================================================
-- FIRST NORMAL FORM (1NF) - Atomic Values, No Repeating Groups
-- ============================================================================

-- 1NF Example: PRODUCTS Table
-- Each column contains atomic (indivisible) values
-- No repeating groups or arrays
SELECT 
    product_id AS "Product ID",
    name AS "Product Name",
    category AS "Category",
    price AS "Rent Price",
    market_price AS "Market Price",
    image_path AS "Image Path"
FROM products
FETCH FIRST 10 ROWS ONLY;

-- ✅ 1NF Satisfied:
-- - Each column has atomic values (single value per cell)
-- - No repeating groups (no Product1, Product2, Product3 columns)
-- - Each row is unique (product_id is primary key)

-- ============================================================================

-- 1NF Example: CUSTOMERS Table
SELECT 
    customer_id AS "Customer ID",
    customername AS "Name",
    email AS "Email",
    phone AS "Phone",
    address AS "Address"
FROM customers
FETCH FIRST 10 ROWS ONLY;

-- ✅ 1NF Satisfied:
-- - All attributes are atomic
-- - No multi-valued attributes
-- - Primary key exists (customer_id)

-- ============================================================================
-- SECOND NORMAL FORM (2NF) - 1NF + No Partial Dependencies
-- ============================================================================

-- 2NF Example: BOOKING_DETAILS Table
-- Demonstrates proper decomposition to eliminate partial dependencies
SELECT 
    bd.booking_detail_id AS "Detail ID",
    bd.booking_id AS "Booking ID",
    bd.product_id AS "Product ID",
    bd.quantity AS "Quantity",
    bd.price AS "Price"
FROM booking_details bd
FETCH FIRST 10 ROWS ONLY;

-- ✅ 2NF Satisfied:
-- - Meets 1NF requirements
-- - No partial dependencies (all non-key attributes depend on entire primary key)
-- - booking_detail_id is the primary key
-- - All other columns depend on the complete primary key

-- ============================================================================

-- 2NF Demonstration: Separate Tables Instead of Redundancy
-- WRONG (Violates 2NF): Storing product details in every booking
-- RIGHT (Follows 2NF): Store product_id and JOIN to get product details

SELECT 
    b.booking_id AS "Booking ID",
    bd.product_id AS "Product ID (Reference)",
    p.name AS "Product Name (from JOIN)",
    p.category AS "Category (from JOIN)",
    bd.price AS "Booking Price"
FROM bookings b
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
FETCH FIRST 10 ROWS ONLY;

-- ✅ 2NF Benefit: Product details stored once in PRODUCTS table
-- No redundancy of product name, category, etc. in booking_details

-- ============================================================================
-- THIRD NORMAL FORM (3NF) - 2NF + No Transitive Dependencies
-- ============================================================================

-- 3NF Example: BOOKINGS and CUSTOMERS Tables
-- Demonstrates elimination of transitive dependencies

-- WRONG (Violates 3NF): Storing customer details in bookings table
-- booking_id -> customer_id -> customername, email, phone

-- RIGHT (Follows 3NF): Separate CUSTOMERS table
SELECT 
    b.booking_id AS "Booking ID",
    b.customer_id AS "Customer ID (FK)",
    c.customername AS "Customer Name (from JOIN)",
    c.email AS "Email (from JOIN)",
    c.phone AS "Phone (from JOIN)",
    b.total_price AS "Total Price",
    b.status AS "Status"
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
FETCH FIRST 10 ROWS ONLY;

-- ✅ 3NF Satisfied:
-- - Meets 2NF requirements
-- - No transitive dependencies
-- - Customer details depend on customer_id, not booking_id
-- - Separate CUSTOMERS table eliminates redundancy

-- ============================================================================

-- 3NF Complete Example: Full Booking Information with JOINs
-- This query demonstrates how 3NF design requires JOINs but eliminates redundancy

SELECT 
    b.booking_id AS "Booking ID",
    c.customername AS "Customer",
    c.email AS "Customer Email",
    p.name AS "Product",
    p.category AS "Category",
    bd.quantity AS "Qty",
    b.total_price AS "Total",
    TO_CHAR(b.rent_date, 'DD-MON-YY') AS "Rent Date",
    TO_CHAR(b.return_date, 'DD-MON-YY') AS "Return Date",
    b.status AS "Status"
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
ORDER BY b.booking_id;

-- ✅ 3NF Benefits Demonstrated:
-- 1. No data redundancy (customer details stored once)
-- 2. No update anomalies (change customer email in one place)
-- 3. No insertion anomalies (can add customer without booking)
-- 4. No deletion anomalies (delete booking keeps customer data)

-- ============================================================================
-- NORMALIZATION SUMMARY
-- ============================================================================

-- Show table structure to demonstrate normalization
SELECT 
    'PRODUCTS' AS "Table",
    'product_id (PK)' AS "Primary Key",
    'Atomic values, no repeating groups' AS "1NF",
    'No partial dependencies' AS "2NF",
    'No transitive dependencies' AS "3NF"
FROM DUAL
UNION ALL
SELECT 
    'CUSTOMERS',
    'customer_id (PK)',
    'Atomic values',
    'No partial dependencies',
    'No transitive dependencies'
FROM DUAL
UNION ALL
SELECT 
    'BOOKINGS',
    'booking_id (PK)',
    'Atomic values',
    'No partial dependencies',
    'customer_id (FK) - no customer details stored'
FROM DUAL
UNION ALL
SELECT 
    'BOOKING_DETAILS',
    'booking_detail_id (PK)',
    'Atomic values',
    'No partial dependencies',
    'product_id (FK) - no product details stored'
FROM DUAL;

-- ============================================================================
-- END OF NORMALIZATION DEMONSTRATION
-- ============================================================================
