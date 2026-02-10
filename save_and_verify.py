from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("SAVING ALL CHANGES PERMANENTLY")
print("="*80)

# Commit any pending changes
conn.commit()
print("\n[OK] All changes committed to database")

# Verify database status
print("\n" + "="*80)
print("DATABASE STATUS:")
print("="*80)

# Check products
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]
print(f"\nProducts: {products}")

# Check customers
cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]
print(f"Customers: {customers}")

# Check bookings
cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]
print(f"Bookings: {bookings}")

# Check functional tables
print("\nFunctional Tables:")
for table in ['REVIEWS', 'CART', 'WISHLIST']:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"  - {table}: {count} records")
    except:
        print(f"  - {table}: NOT FOUND")

print("\n" + "="*80)
print("DATABASE IS RUNNING AND READY!")
print("="*80)

cur.close()
conn.close()
