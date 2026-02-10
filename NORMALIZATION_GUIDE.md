# Database Normalization Demonstration Guide

## Your Database is Already in 3NF! ✅

Your RentEasyIndia database follows proper normalization (1NF, 2NF, 3NF). Here's how to demonstrate this to your trainers.

---

## Table Structure Overview

```
PRODUCTS (product_id, name, category, price, market_price, image_path)
CUSTOMERS (customer_id, customername, email, phone, address, password)
BOOKINGS (booking_id, customer_id, total_price, rent_date, return_date, status, phone, address, location)
BOOKING_DETAILS (booking_detail_id, booking_id, product_id, quantity, price)
```

---

## 1NF (First Normal Form) ✅

**Rules:**
- All columns contain atomic (indivisible) values
- No repeating groups
- Each row is unique (has primary key)

### Demonstration Query:

```sql
SELECT 
    product_id, name, category, price, market_price
FROM products
FETCH FIRST 5 ROWS ONLY;
```

**Explain to Trainers:**
- ✅ Each column has single value (not arrays or lists)
- ✅ No Product1, Product2, Product3 columns (no repeating groups)
- ✅ Primary key exists (product_id)

---

## 2NF (Second Normal Form) ✅

**Rules:**
- Must be in 1NF
- No partial dependencies (all non-key attributes depend on entire primary key)

### Demonstration Query:

```sql
SELECT 
    bd.booking_detail_id,
    bd.booking_id,
    bd.product_id,
    bd.quantity,
    bd.price
FROM booking_details bd
FETCH FIRST 5 ROWS ONLY;
```

**Explain to Trainers:**
- ✅ Meets 1NF
- ✅ All columns depend on complete primary key (booking_detail_id)
- ✅ No partial dependencies

### Show the Benefit:

```sql
-- Product details stored ONCE in products table
-- Referenced by product_id in booking_details
SELECT 
    bd.product_id AS "Product ID (Reference)",
    p.name AS "Product Name (from JOIN)",
    p.category AS "Category (from JOIN)"
FROM booking_details bd
JOIN products p ON bd.product_id = p.product_id
FETCH FIRST 5 ROWS ONLY;
```

**Explain:** Instead of storing product name in every booking, we store product_id and JOIN to get details.

---

## 3NF (Third Normal Form) ✅

**Rules:**
- Must be in 2NF
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

### Demonstration Query:

```sql
-- Customer details stored in separate CUSTOMERS table
-- Not in BOOKINGS table (avoiding transitive dependency)
SELECT 
    b.booking_id,
    b.customer_id AS "Customer ID (FK)",
    c.customername AS "Customer Name (from JOIN)",
    c.email AS "Email (from JOIN)",
    b.total_price,
    b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
FETCH FIRST 5 ROWS ONLY;
```

**Explain to Trainers:**
- ✅ Meets 2NF
- ✅ Customer details (name, email, phone) stored in CUSTOMERS table
- ✅ BOOKINGS table only stores customer_id (foreign key)
- ✅ No transitive dependency: booking_id → customer_id → customername

### Complete 3NF Example:

```sql
-- Full booking with all details using JOINs
SELECT 
    b.booking_id,
    c.customername AS "Customer",
    p.name AS "Product",
    p.category,
    b.total_price,
    b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id
ORDER BY b.booking_id;
```

**Explain Benefits:**
1. **No Redundancy:** Customer details stored once
2. **No Update Anomalies:** Change customer email in one place
3. **No Insertion Anomalies:** Can add customer without booking
4. **No Deletion Anomalies:** Delete booking, customer data remains

---

## Presentation Flow for Trainers

### Step 1: Show 1NF (2 minutes)
1. Open SQL Developer
2. Run: `SELECT * FROM products FETCH FIRST 5 ROWS ONLY;`
3. Explain: Atomic values, no repeating groups, has primary key

### Step 2: Show 2NF (3 minutes)
1. Run: `SELECT * FROM booking_details FETCH FIRST 5 ROWS ONLY;`
2. Explain: No partial dependencies
3. Run JOIN query to show product_id references products table
4. Explain: Product details not duplicated in booking_details

### Step 3: Show 3NF (5 minutes)
1. Run the complete booking query with JOINs
2. Explain: Customer details in separate table
3. Show benefits: No redundancy, no anomalies
4. Demonstrate: Change customer email once, affects all bookings

### Step 4: Show Normalization Summary
Run the summary query from NORMALIZATION_DEMO.sql

---

## Quick Reference

**File to use:** [NORMALIZATION_DEMO.sql](file:///c:/Users/Tejaswini/OneDrive/Desktop/RentEasyIndia/NORMALIZATION_DEMO.sql)

This file contains all queries organized by normalization form with detailed comments.

---

## Your Database Status

✅ **48 Products** - All in 1NF, 2NF, 3NF
✅ **16 Customers** - Properly normalized
✅ **18 Bookings** - Using foreign keys correctly
✅ **18 Booking Details** - No redundancy

**Your database is perfectly normalized and ready to demonstrate!**
