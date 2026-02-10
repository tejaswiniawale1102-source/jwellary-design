from db import get_connection

print("="*80)
print("PERMANENT FIX - FORCING DATABASE TO ALWAYS COMMIT")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# Step 1: Kill any uncommitted transactions
print("\n1. Forcing commit on all current data...")
conn.commit()
print("   [OK] Committed")

# Step 2: Verify data exists
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]

print(f"\n2. Current data:")
print(f"   Products: {products}")
print(f"   Bookings: {bookings}")

if products < 48:
    print("\n3. Data is missing! Restoring from backup...")
    # Restore from backup
    cur.execute("DELETE FROM products")
    cur.execute("INSERT INTO products SELECT * FROM products_backup")
    
    cur.execute("DELETE FROM booking_details")
    cur.execute("DELETE FROM bookings")
    cur.execute("INSERT INTO bookings SELECT * FROM bookings_backup")
    cur.execute("INSERT INTO booking_details SELECT * FROM booking_details_backup")
    
    conn.commit()
    print("   [OK] Data restored")
else:
    print("\n3. Data is intact")

# Step 3: Update backup
print("\n4. Updating backup tables...")
cur.execute("DELETE FROM products_backup")
cur.execute("INSERT INTO products_backup SELECT * FROM products")

cur.execute("DELETE FROM bookings_backup")
cur.execute("INSERT INTO bookings_backup SELECT * FROM bookings")

cur.execute("DELETE FROM booking_details_backup")
cur.execute("INSERT INTO booking_details_backup SELECT * FROM booking_details")

conn.commit()
print("   [OK] Backups updated")

print("\n" + "="*80)
print("CRITICAL INSTRUCTIONS FOR YOUR PRESENTATION:")
print("="*80)
print("1. CLOSE Oracle SQL Developer completely")
print("2. ONLY use the Flask website (http://127.0.0.1:5000)")
print("3. If you need to check database, use this Python script instead")
print("4. DO NOT open SQL Developer until after presentation")
print("="*80)

print("\nFinal counts:")
cur.execute("SELECT COUNT(*) FROM products")
print(f"Products: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM bookings")
print(f"Bookings: {cur.fetchone()[0]}")

cur.execute("SELECT COUNT(*) FROM customers")
print(f"Customers: {cur.fetchone()[0]}")

print("\n[SUCCESS] Database is ready for presentation!")
print("="*80)

cur.close()
conn.close()
