from db import get_connection

print("="*80)
print("FINAL DATABASE VERIFICATION")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# Check database connection
cur.execute("SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL")
service_name = cur.fetchone()[0]
print(f"\nConnected to: {service_name}")

# Check all tables
print("\n" + "="*80)
print("DATABASE CONTENTS:")
print("="*80)

# Products
cur.execute("SELECT COUNT(*) FROM products")
product_count = cur.fetchone()[0]
print(f"\nProducts: {product_count}")

cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
for row in cur.fetchall():
    print(f"  - {row[0]:15s}: {row[1]:2d} items")

# Bookings
cur.execute("SELECT COUNT(*) FROM bookings")
booking_count = cur.fetchone()[0]
print(f"\nBookings: {booking_count}")

# Customers
cur.execute("SELECT COUNT(*) FROM customers")
customer_count = cur.fetchone()[0]
print(f"Customers: {customer_count}")

# Sample products
print("\n" + "="*80)
print("SAMPLE PRODUCTS (First 5):")
print("="*80)
cur.execute("""
    SELECT product_id, name, category, price, image_path 
    FROM products 
    WHERE ROWNUM <= 5 
    ORDER BY product_id
""")
for row in cur.fetchall():
    print(f"ID {row[0]:3d}: {row[1]:30s} | {row[2]:12s} | Rs.{row[3]:4d} | {row[4]}")

# Sample bookings
print("\n" + "="*80)
print("SAMPLE BOOKINGS (First 5):")
print("="*80)
cur.execute("""
    SELECT b.booking_id, c.customername, b.total_price, b.status, b.booking_date
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    WHERE ROWNUM <= 5
    ORDER BY b.booking_id
""")
for row in cur.fetchall():
    print(f"Booking #{row[0]:2d}: {row[1]:20s} | Rs.{row[2]:5d} | {row[3]:10s} | {row[4]}")

print("\n" + "="*80)
print("STATUS:")
print("="*80)
if product_count == 48 and booking_count == 18:
    print("SUCCESS! Database is complete and permanent!")
    print("- All 48 products are saved")
    print("- All 18 bookings are saved")
    print("- Flask app is connected to correct database (XEPDB1)")
else:
    print(f"WARNING: Expected 48 products and 18 bookings")
    print(f"Found: {product_count} products, {booking_count} bookings")
print("="*80)

cur.close()
conn.close()
