# COMPLETE DATABASE SETUP INSTRUCTIONS

## This will give you a FRESH, CLEAN database with:
- 16 customers with diverse names
- 18 products
- 18 bookings
- All properly normalized (1NF, 2NF, 3NF)

---

## Step-by-Step Instructions:

### Step 1: Run SQL Setup (in Oracle SQL Developer)

1. Open Oracle SQL Developer
2. Open the file: **COMPLETE_DATABASE_SETUP.sql**
3. Click "Run Script" (F5)
4. Wait for it to complete (creates all tables)
5. **Close SQL Developer**

### Step 2: Insert Data (in Terminal)

```bash
python COMPLETE_SETUP.py
```

This will insert:
- 16 customers
- 18 products
- 18 bookings
- 18 booking details

### Step 3: Verify

```bash
python quick_check.py
```

Should show:
- Products: 18/18 ✅
- Bookings: 18/18 ✅
- Customers: 16/16 ✅

---

## What You Get:

### Customers (16):
1. Rahul Sharma
2. Priya Deshmukh
3. Arjun Patel
4. Sneha Reddy
5. Vikram Singh
6. Ananya Iyer
7. Rohan Mehta
8. Kavya Nair
9. Aditya Gupta
10. Ishita Joshi
11. Karan Kapoor
12. Meera Kulkarni
13. Siddharth Rao
14. Tanvi Shah
15. Nikhil Verma
16. Riya Malhotra

### Products (18):
- Jewelry: 6 items
- Mens: 9 items
- Womens: 4 items

### Bookings (18):
- Confirmed: 10
- Pending: 5
- Returned: 3

---

## For Your Presentation:

After setup, use:
- **SAFE_PRESENTATION_QUERIES.sql** - Show database in SQL Developer
- **show_all_data.py** - Show data in terminal (safer!)

---

## If Something Goes Wrong:

Just run the setup again:
1. Run COMPLETE_DATABASE_SETUP.sql
2. Run python COMPLETE_SETUP.py

Takes 30 seconds total.

---

**This is a CLEAN START - no more data disappearing!**
