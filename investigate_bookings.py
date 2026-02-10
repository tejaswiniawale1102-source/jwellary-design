from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("INVESTIGATING MISSING BOOKINGS")
print("="*80)

# Check total bookings
cur.execute("SELECT COUNT(*) FROM bookings")
total_bookings = cur.fetchone()[0]
print(f"\nTotal Bookings in Database: {total_bookings}")

# Check bookings by status
print("\nBookings by Status:")
cur.execute("SELECT status, COUNT(*) FROM bookings GROUP BY status")
for row in cur.fetchall():
    print(f"  {row[0]:15s}: {row[1]} bookings")

# Check if there are bookings without booking_details
print("\nBookings WITHOUT booking_details (orphaned):")
cur.execute("""
    SELECT b.booking_id, b.customer_id, b.total_price, b.status
    FROM bookings b
    WHERE NOT EXISTS (
        SELECT 1 FROM booking_details bd WHERE bd.booking_id = b.booking_id
    )
""")
orphaned = cur.fetchall()
if orphaned:
    print(f"  Found {len(orphaned)} orphaned bookings:")
    for row in orphaned:
        print(f"    Booking ID: {row[0]}, Customer: {row[1]}, Total: Rs.{row[2]}, Status: {row[3]}")
else:
    print("  None found - all bookings have booking_details")

# Check all bookings
print("\nAll Bookings:")
cur.execute("SELECT booking_id, customer_id, total_price, status FROM bookings ORDER BY booking_id DESC")
all_bookings = cur.fetchall()
for row in all_bookings[:10]:
    print(f"  ID: {row[0]}, Customer: {row[1]}, Total: Rs.{row[2]}, Status: {row[3]}")

if len(all_bookings) > 10:
    print(f"  ... and {len(all_bookings) - 10} more")

cur.close()
conn.close()
