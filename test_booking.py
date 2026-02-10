from db import get_connection
import datetime

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("TESTING BOOKING FUNCTIONALITY")
print("="*80)

# Simulate a booking insert (like rent_now does)
print("\n1. Testing booking insert with all required fields...")

try:
    # Get next booking ID
    cur.execute("SELECT NVL(MAX(booking_id), 0) + 1 FROM bookings")
    test_booking_id = cur.fetchone()[0]
    
    # Test data
    customer_id = 1
    product_id = 101
    total_price = 5000
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=3)
    today_str = today.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    phone = "9999999999"
    address = "Test Address, Mumbai"
    location = "Mumbai"
    
    # Insert booking (same query as rent_now route)
    cur.execute("""
        INSERT INTO bookings (booking_id, customer_id, total_price, booking_date, rent_date, return_date, status, phone, address, location)
        VALUES (:1, :2, :3, SYSDATE, TO_DATE(:4, 'YYYY-MM-DD'), TO_DATE(:5, 'YYYY-MM-DD'), 'Confirmed', :6, :7, :8)
    """, [test_booking_id, customer_id, total_price, today_str, end_date_str, phone, address, location])
    
    # Insert booking_details
    cur.execute("""
        INSERT INTO booking_details (booking_id, product_id, quantity, price)
        VALUES (:1, :2, 1, :3)
    """, (test_booking_id, product_id, total_price))
    
    conn.commit()
    
    print(f"   [OK] Test booking #{test_booking_id} created successfully!")
    
    # Verify the booking
    cur.execute("""
        SELECT b.booking_id, c.customername, p.name, b.total_price, b.phone, b.address, b.location
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN booking_details bd ON b.booking_id = bd.booking_id
        JOIN products p ON bd.product_id = p.product_id
        WHERE b.booking_id = :1
    """, (test_booking_id,))
    
    result = cur.fetchone()
    if result:
        print(f"\n2. Verification:")
        print(f"   Booking ID: {result[0]}")
        print(f"   Customer: {result[1]}")
        print(f"   Product: {result[2]}")
        print(f"   Amount: Rs.{result[3]}")
        print(f"   Phone: {result[4]}")
        print(f"   Address: {result[5]}")
        print(f"   Location: {result[6]}")
    
    # Clean up test booking
    print(f"\n3. Cleaning up test booking...")
    cur.execute("DELETE FROM booking_details WHERE booking_id = :1", (test_booking_id,))
    cur.execute("DELETE FROM bookings WHERE booking_id = :1", (test_booking_id,))
    conn.commit()
    print("   [OK] Test booking removed")
    
    print("\n" + "="*80)
    print("[SUCCESS] Booking functionality is working correctly!")
    print("="*80)
    
except Exception as e:
    print(f"\n[ERROR] Booking test failed: {e}")
    import traceback
    traceback.print_exc()

cur.close()
conn.close()
