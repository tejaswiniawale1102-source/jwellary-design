# HOW TO SAFELY SHOW DATABASE IN ORACLE SQL DEVELOPER

## ⚠️ CRITICAL STEPS - Follow Exactly!

### Step 1: Before Opening SQL Developer

Run this to ensure data is committed:
```bash
python PERMANENT_FIX.py
```

### Step 2: Open Oracle SQL Developer CORRECTLY

1. Open Oracle SQL Developer
2. Connect to your database:
   - **Username:** system
   - **Password:** system
   - **Hostname:** localhost
   - **Port:** 1521
   - **Service name:** XEPDB1

### Step 3: Run SAFE Queries Only

Open the file: **PRESENTATION_QUERIES.sql**

This file contains 7 safe queries that demonstrate:
- ✅ Product catalog by category
- ✅ Sample products
- ✅ All bookings with customer names
- ✅ Booking statistics
- ✅ Customer database
- ✅ Database normalization (3NF)
- ✅ Overall system summary

**Run these queries ONE AT A TIME** by:
1. Highlight the query you want
2. Press F9 or click the "Run Statement" button
3. Show the results to your trainer

### Step 4: What to DEMONSTRATE

#### 1. Product Catalog
```sql
SELECT category, COUNT(*) FROM products GROUP BY category;
```
**Shows:** 6 categories with 48 total products

#### 2. Bookings with Customers
```sql
SELECT b.booking_id, c.customername, p.name, b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN booking_details bd ON b.booking_id = bd.booking_id
JOIN products p ON bd.product_id = p.product_id;
```
**Shows:** 18 bookings with customer names (demonstrates JOINs and normalization)

#### 3. Database Summary
```sql
SELECT 
    (SELECT COUNT(*) FROM products) AS "Products",
    (SELECT COUNT(*) FROM customers) AS "Customers",
    (SELECT COUNT(*) FROM bookings) AS "Bookings"
FROM DUAL;
```
**Shows:** Complete system overview

### Step 5: After Demonstration

**IMMEDIATELY after showing SQL Developer:**

1. **DO NOT run any other queries**
2. **Close SQL Developer** (File → Exit)
3. **Run verification:**
   ```bash
   python quick_check.py
   ```
4. If data is missing, run:
   ```bash
   python PERMANENT_FIX.py
   ```

---

## 🚫 NEVER RUN THESE DURING PRESENTATION:

```sql
DELETE FROM products;      -- ❌ NEVER
TRUNCATE TABLE bookings;   -- ❌ NEVER
UPDATE products SET ...;   -- ❌ NEVER
DROP TABLE ...;            -- ❌ NEVER
```

---

## ✅ SAFE Presentation Flow:

1. Show Flask website first (http://127.0.0.1:5000)
2. Demonstrate booking, browsing, admin features
3. Then open SQL Developer
4. Run queries from PRESENTATION_QUERIES.sql
5. Show the data matches what's on website
6. Close SQL Developer
7. Continue with Flask website

---

## Emergency Recovery

If something goes wrong:
```bash
python PERMANENT_FIX.py
python quick_check.py
```

Your data will be restored in seconds!
