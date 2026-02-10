from db import get_connection
from datetime import datetime, timedelta
import random

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("RESTORING DUMMY BOOKINGS")
print("="*80)

# Get existing customers and products
cur.execute("SELECT customer_id FROM customers")
customer_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT product_id, price FROM products")
products = cur.fetchall()

print(f"\nFound {len(customer_ids)} customers and {len(products)} products")

# Create dummy bookings with correct schema
base_date = datetime.now()

bookings_to_create = [
    (902, 1, 5500, 'Confirmed'),
    (903, 1, 3500, 'Confirmed'),
    (904, 1, 6000, 'Pending'),
    (905, 1, 4200, 'Confirmed'),
    (906, 1, 7800, 'Returned'),
    (907, 1, 3900, 'Confirmed'),
    (908, 1, 5200, 'Pending'),
    (909, 1, 4800, 'Confirmed'),
    (910, 1, 6500, 'Returned'),
    (911, 1, 3200, 'Confirmed'),
    (912, 1, 5900, 'Pending'),
    (913, 1, 4100, 'Confirmed'),
    (914, 1, 7200, 'Returned'),
    (915, 1, 3800, 'Pending'),
    (916, 1, 5500, 'Confirmed'),
    (917, 1, 22000, 'Confirmed'),
    (918, 1, 18000, 'Pending'),
]

print(f"\nCreating {len(bookings_to_create)} bookings...")
created_count = 0

for booking_id, customer_id, total_price, status in bookings_to_create:
    # Random dates
    days_ago = random.randint(1, 30)
    rent_date = base_date - timedelta(days=days_ago)
    return_date = rent_date + timedelta(days=random.randint(3, 10))
    
    try:
        # Insert booking with ONLY the 7 columns that exist
        cur.execute("""
            INSERT INTO bookings (booking_id, customer_id, total_price, booking_date, rent_date, return_date, status)
            VALUES (:1, :2, :3, SYSDATE, :4, :5, :6)
        """, (booking_id, customer_id, total_price, rent_date, return_date, status))
        
        # Insert booking_detail with a random product
        product = random.choice(products)
        cur.execute("""
            INSERT INTO booking_details (booking_id, product_id, quantity, price)
            VALUES (:1, :2, 1, :3)
        """, (booking_id, product[0], product[1]))
        
        created_count += 1
        print(f"  Created booking {booking_id} ({status})")
    except Exception as e:
        if "ORA-00001" in str(e):
            print(f"  Booking {booking_id} already exists, skipping")
        else:
            print(f"  Error creating booking {booking_id}: {e}")

conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM bookings")
total = cur.fetchone()[0]
print(f"\nCreated {created_count} new bookings")
print(f"Total bookings now: {total}")

cur.close()
conn.close()

print("\n" + "="*80)
print("DUMMY BOOKINGS RESTORED!")
print("="*80)
