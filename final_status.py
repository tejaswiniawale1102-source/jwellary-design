from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("FINAL DATABASE STATUS")
print("="*80)

# Products
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]

# Customers
cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]

# Bookings
cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]

# Booking diversity
cur.execute("""
    SELECT COUNT(DISTINCT b.customer_id) as unique_customers,
           COUNT(DISTINCT bd.product_id) as unique_products
    FROM bookings b
    JOIN booking_details bd ON b.booking_id = bd.booking_id
""")
diversity = cur.fetchone()

print(f"\nProducts:  {products}/48")
print(f"Customers: {customers}")
print(f"Bookings:  {bookings}/18")
print(f"\nBooking Diversity:")
print(f"  - Unique customers: {diversity[0]}")
print(f"  - Unique products:  {diversity[1]}")

# Show sample bookings
print("\n" + "="*80)
print("SAMPLE BOOKINGS (First 10):")
print("="*80)
cur.execute("""
    SELECT b.booking_id, c.customername, p.name, p.category, b.status
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    JOIN booking_details bd ON b.booking_id = bd.booking_id
    JOIN products p ON bd.product_id = p.product_id
    WHERE ROWNUM <= 10
    ORDER BY b.booking_id
""")

for row in cur.fetchall():
    print(f"#{row[0]:3d}: {row[1]:20s} | {row[2]:30s} | {row[3]:12s} | {row[4]}")

print("\n" + "="*80)
print("ALL DATA SAVED PERMANENTLY!")
print("="*80)

cur.close()
conn.close()
