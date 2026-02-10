-- ============================================================================
-- SQL QUERIES TO VIEW ALL BOOKINGS AND CUSTOMERS
-- ============================================================================

-- Query 1: View all 18 bookings with customer names
-- Copy and run this in Oracle SQL Developer
SELECT 
    b.booking_id AS "Booking ID",
    c.customername AS "Customer Name",
    p.name AS "Product Name",
    b.total_price AS "Total Price",
    b.rent_date AS "Rent Date",
    b.return_date AS "Return Date",
    b.status AS "Status",
    b.phone AS "Phone",
    b.location AS "Location"
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
ORDER BY b.booking_id;

-- ============================================================================

-- Query 2: View all customers
SELECT 
    customer_id AS "Customer ID",
    customername AS "Customer Name",
    phone AS "Phone",
    email AS "Email",
    address AS "Address"
FROM customers
ORDER BY customer_id;

-- ============================================================================

-- Query 3: Booking summary by customer
SELECT 
    c.customername AS "Customer Name",
    COUNT(b.booking_id) AS "Total Bookings",
    SUM(b.total_price) AS "Total Spent"
FROM customers c
LEFT JOIN bookings b ON c.customer_id = b.customer_id
GROUP BY c.customername
ORDER BY COUNT(b.booking_id) DESC;

-- ============================================================================

-- Query 4: Quick count verification
SELECT 
    (SELECT COUNT(*) FROM products) AS "Total Products",
    (SELECT COUNT(*) FROM customers) AS "Total Customers",
    (SELECT COUNT(*) FROM bookings) AS "Total Bookings"
FROM DUAL;
