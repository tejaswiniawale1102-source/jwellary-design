# EMERGENCY PRESENTATION GUIDE

## THE PROBLEM:
SQL Developer keeps making data disappear because it holds database sessions open.

## THE SOLUTION:
Follow these steps EXACTLY:

---

## BEFORE PRESENTATION (5 minutes before):

### Step 1: Restore Data
```bash
python QUICK_RESTORE.py
```

### Step 2: Verify Data
```bash
python quick_check.py
```
Should show: 48 products, 18 bookings, 16 customers

### Step 3: Start Flask
```bash
python app.py
```
Go to: http://127.0.0.1:5000

---

## DURING PRESENTATION:

### Part 1: Show Website (5 min)
- Browse products
- Show booking system
- Show admin dashboard
- **DO NOT touch SQL Developer yet**

### Part 2: Show Database (5 min)

1. **Open SQL Developer**
2. **Open file:** SAFE_PRESENTATION_QUERIES.sql
3. **Run STEP 1 first** - Verify counts (48, 16, 18)
   - If you see (1, 1, 1) → STOP → Run QUICK_RESTORE.py
4. **Run STEP 2** - Show 1NF
5. **Run STEP 3** - Show 2NF  
6. **Run STEP 4** - Show 3NF
7. **IMMEDIATELY CLOSE SQL Developer**

### Part 3: Back to Website
- Show it still works
- Done!

---

## IF DATA DISAPPEARS:

**Don't panic!** Just run:
```bash
python QUICK_RESTORE.py
```
Takes 5 seconds to restore everything.

---

## KEY FILES:

1. **QUICK_RESTORE.py** - Instant restore (use this!)
2. **SAFE_PRESENTATION_QUERIES.sql** - Only these queries
3. **quick_check.py** - Verify data exists

---

## SIMPLE RULE:

**SQL Developer = Quick in, quick out**
- Open it
- Run the 4 queries
- Close it immediately
- Don't leave it open!

**That's it!** Your presentation will go smoothly. 🎉
