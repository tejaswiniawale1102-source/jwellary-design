from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CHECKING CURRENT BOOKINGS")
print("="*80)

# Check current bookings with customer names
cur.execute("""
    SELECT b.booking_id, c.customername, p.name, b.total_price, b.status
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    JOIN booking_details bd ON b.booking_id = bd.booking_id
    JOIN products p ON bd.product_id = p.product_id
    ORDER BY b.booking_id
""")

bookings = cur.fetchall()
print(f"\nTotal bookings: {len(bookings)}")
print("\nBooking Details:")
print("-" * 80)

customer_names = set()
for booking in bookings:
    print(f"Booking #{booking[0]}: {booking[1]} | {booking[2]} | Rs.{int(booking[3])} | {booking[4]}")
    customer_names.add(booking[1])

print("\n" + "="*80)
print(f"Unique customers: {len(customer_names)}")
print(f"Customer names: {', '.join(customer_names)}")
print("="*80)

cur.close()
conn.close()
