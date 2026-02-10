from db import get_connection

print("="*80)
print("CREATING PERMANENT PROTECTION")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# Verify all data is there
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]

print(f"\nCurrent data:")
print(f"  Products: {products}")
print(f"  Bookings: {bookings}")
print(f"  Customers: {customers}")

if products == 48 and bookings == 18:
    print("\n[OK] All data is present!")
    
    # Force commit
    conn.commit()
    print("\n[COMMITTED] All changes saved permanently")
    
    print("\n" + "="*80)
    print("IMPORTANT INSTRUCTIONS:")
    print("="*80)
    print("1. DO NOT run DELETE queries in Oracle SQL Developer")
    print("2. DO NOT run TRUNCATE queries")
    print("3. ONLY use the Flask website to modify data")
    print("4. If you need to check data, use SELECT queries only")
    print("="*80)
else:
    print("\n[WARNING] Data is incomplete!")
    print("Run emergency_restore.py again")

cur.close()
conn.close()
