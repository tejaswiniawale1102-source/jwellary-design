from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("ALL 18 BOOKINGS WITH CUSTOMER NAMES")
print("="*80)

# Query to show all bookings with customer names
cur.execute("""
    SELECT 
        b.booking_id,
        c.customername,
        p.name AS product_name,
        b.total_price,
        b.rent_date,
        b.return_date,
        b.status
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    JOIN booking_details bd ON b.booking_id = bd.booking_id
    JOIN products p ON bd.product_id = p.product_id
    ORDER BY b.booking_id
""")

bookings = cur.fetchall()

print(f"\nTotal Bookings: {len(bookings)}\n")
print(f"{'ID':<5} {'Customer':<20} {'Product':<30} {'Price':<10} {'Status':<10}")
print("-" * 85)

for booking in bookings:
    print(f"{booking[0]:<5} {booking[1]:<20} {booking[2]:<30} Rs.{int(booking[3]):<8} {booking[6]:<10}")

print("\n" + "="*80)
print("ALL CUSTOMERS")
print("="*80)

cur.execute("""
    SELECT customer_id, customername, phone, email
    FROM customers
    ORDER BY customer_id
""")

customers = cur.fetchall()
print(f"\nTotal Customers: {len(customers)}\n")
print(f"{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<30}")
print("-" * 70)

for customer in customers:
    print(f"{customer[0]:<5} {customer[1]:<20} {customer[2] or 'N/A':<15} {customer[3]:<30}")

print("\n" + "="*80)

cur.close()
conn.close()
