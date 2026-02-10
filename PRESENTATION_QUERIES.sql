-- ============================================================================
-- SAFE QUERIES FOR PRESENTATION IN ORACLE SQL DEVELOPER
-- ============================================================================
-- IMPORTANT: These are READ-ONLY queries. Safe to run during presentation.
-- DO NOT run any DELETE, UPDATE, TRUNCATE, or DROP commands!
-- ============================================================================

-- Query 1: Show all products by category
-- This demonstrates your product catalog
SELECT 
    category AS "Category",
    COUNT(*) AS "Total Products",
    AVG(price) AS "Avg Price",
    MIN(price) AS "Min Price",
    MAX(price) AS "Max Price"
FROM products
GROUP BY category
ORDER BY category;

-- ============================================================================

-- Query 2: Show sample products from each category
-- This shows actual product details
SELECT 
    product_id AS "ID",
    name AS "Product Name",
    category AS "Category",
    price AS "Rent Price",
    market_price AS "Market Price",
    image_path AS "Image"
FROM products
ORDER BY category, product_id
FETCH FIRST 20 ROWS ONLY;

-- ============================================================================

-- Query 3: Show all bookings with customer details
-- This demonstrates the booking system
SELECT 
    b.booking_id AS "Booking ID",
    c.customername AS "Customer",
    p.name AS "Product",
    b.total_price AS "Amount",
    TO_CHAR(b.rent_date, 'DD-MON-YYYY') AS "Rent Date",
    TO_CHAR(b.return_date, 'DD-MON-YYYY') AS "Return Date",
    b.status AS "Status"
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
ORDER BY b.booking_id;

-- ============================================================================

-- Query 4: Show booking statistics by status
-- This shows business analytics
SELECT 
    status AS "Booking Status",
    COUNT(*) AS "Count",
    SUM(total_price) AS "Total Revenue"
FROM bookings
GROUP BY status
ORDER BY status;

-- ============================================================================

-- Query 5: Show all customers
-- This demonstrates customer database
SELECT 
    customer_id AS "ID",
    customername AS "Name",
    email AS "Email",
    phone AS "Phone",
    address AS "Address"
FROM customers
ORDER BY customer_id;

-- ============================================================================

-- Query 6: Show database normalization (3NF)
-- This demonstrates proper database design
SELECT 
    b.booking_id AS "Booking ID",
    bd.product_id AS "Product ID",
    p.name AS "Product Name (from JOIN)",
    bd.quantity AS "Quantity",
    bd.price AS "Price"
FROM bookings b
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
FETCH FIRST 10 ROWS ONLY;

-- ============================================================================

-- Query 7: Quick summary for presentation
-- This shows overall system status
SELECT 
    'Products' AS "Table",
    (SELECT COUNT(*) FROM products) AS "Count"
FROM DUAL
UNION ALL
SELECT 
    'Customers' AS "Table",
    (SELECT COUNT(*) FROM customers) AS "Count"
FROM DUAL
UNION ALL
SELECT 
    'Bookings' AS "Table",
    (SELECT COUNT(*) FROM bookings) AS "Count"
FROM DUAL
UNION ALL
SELECT 
    'Reviews' AS "Table",
    (SELECT COUNT(*) FROM reviews) AS "Count"
FROM DUAL;

-- ============================================================================
-- END OF SAFE QUERIES
-- ============================================================================
