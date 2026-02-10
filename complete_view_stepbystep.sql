-- ============================================================================
-- COMPLETE DATABASE VIEW - Step by Step Query Building
-- Shows: All Products, All Bookings, All Customer Names
-- ============================================================================

-- ============================================================================
-- STEP 1: Start with BOOKINGS table (the main table)
-- ============================================================================
SELECT 
    booking_id,
    customer_id,
    total_price,
    rent_date,
    return_date,
    status
FROM bookings;

-- OUTPUT: Shows bookings but only customer_id (not customer name)
-- PROBLEM: We need customer NAME, not just ID


-- ============================================================================
-- STEP 2: Add CUSTOMERS table to get customer names
-- ============================================================================
SELECT 
    b.booking_id,
    b.customer_id,
    c.customername,           -- NOW we have customer name!
    b.total_price,
    b.rent_date,
    b.return_date,
    b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id;

-- OUTPUT: Shows bookings with customer names
-- PROBLEM: We still don't see PRODUCT details


-- ============================================================================
-- STEP 3: Add BOOKING_DETAILS to connect bookings with products
-- ============================================================================
SELECT 
    b.booking_id,
    c.customername,
    bd.product_id,            -- Product ID from booking_details
    bd.quantity,
    b.total_price,
    b.rent_date,
    b.return_date,
    b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id;

-- OUTPUT: Shows bookings with customer names and product_id
-- PROBLEM: We need product NAME and CATEGORY, not just ID


-- ============================================================================
-- STEP 4: FINAL QUERY - Add PRODUCTS table to get product details
-- ============================================================================
SELECT 
    b.booking_id AS "Booking ID",
    c.customername AS "Customer Name",
    p.name AS "Product Name",
    p.category AS "Category",
    p.price AS "Product Price",
    bd.quantity AS "Quantity",
    b.total_price AS "Total Paid",
    b.rent_date AS "Rent Date",
    b.return_date AS "Return Date",
    b.status AS "Status"
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
ORDER BY b.booking_id DESC;

-- ============================================================================
-- THIS IS YOUR FINAL QUERY!
-- Copy the query above (STEP 4) and run it in Oracle SQL Developer
-- ============================================================================

-- OUTPUT: Complete view showing:
-- ✓ All bookings
-- ✓ Customer names (from CUSTOMERS table)
-- ✓ Product names (from PRODUCTS table)
-- ✓ Product categories
-- ✓ All booking details

-- ============================================================================
-- NORMALIZATION PROOF:
-- ============================================================================
-- 1NF: All values are atomic (single values in each cell)
-- 2NF: No partial dependencies (product details in PRODUCTS, not BOOKING_DETAILS)
-- 3NF: No transitive dependencies (customer names in CUSTOMERS, not BOOKINGS)
--      All data retrieved via proper JOINs!
-- ============================================================================
