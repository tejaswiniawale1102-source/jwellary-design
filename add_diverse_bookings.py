from db import get_connection
from werkzeug.security import generate_password_hash
import random

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CREATING DIVERSE CUSTOMERS AND BOOKINGS")
print("="*80)

# Diverse customer data
customers_data = [
    ("Priya Deshmukh", "9876543210", "priya.d@gmail.com", "Mumbai"),
    ("Arjun Patel", "9123456789", "arjun.p@gmail.com", "Ahmedabad"),
    ("Sneha Reddy", "9234567890", "sneha.r@gmail.com", "Hyderabad"),
    ("Vikram Singh", "9345678901", "vikram.s@gmail.com", "Jaipur"),
    ("Ananya Iyer", "9456789012", "ananya.i@gmail.com", "Chennai"),
    ("Rohan Mehta", "9567890123", "rohan.m@gmail.com", "Pune"),
    ("Kavya Nair", "9678901234", "kavya.n@gmail.com", "Kochi"),
    ("Aditya Gupta", "9789012345", "aditya.g@gmail.com", "Delhi"),
    ("Ishita Joshi", "9890123456", "ishita.j@gmail.com", "Bangalore"),
    ("Karan Kapoor", "9901234567", "karan.k@gmail.com", "Chandigarh"),
    ("Meera Kulkarni", "9012345678", "meera.k@gmail.com", "Nashik"),
    ("Siddharth Rao", "9123450987", "siddharth.r@gmail.com", "Mysore"),
    ("Tanvi Shah", "9234561098", "tanvi.s@gmail.com", "Surat"),
    ("Nikhil Verma", "9345672109", "nikhil.v@gmail.com", "Lucknow"),
    ("Riya Malhotra", "9456783210", "riya.m@gmail.com", "Kolkata"),
]

# Get all products for diverse bookings
cur.execute("SELECT product_id, name, price, category FROM products ORDER BY product_id")
all_products = cur.fetchall()

print(f"\nFound {len(all_products)} products for bookings")

# Delete existing customers except the first one (keep Rahul Sharma)
print("\n1. Cleaning up old customer data...")
cur.execute("SELECT customer_id FROM customers WHERE customer_id != 1")
old_customers = cur.fetchall()

for old_cust in old_customers:
    cur.execute("DELETE FROM customers WHERE customer_id = :1", (old_cust[0],))

conn.commit()
print(f"   Cleaned up {len(old_customers)} old customers")

# Add new diverse customers
print("\n2. Adding diverse customers...")
customer_ids = [1]  # Keep existing customer_id 1

for idx, (name, phone, email, address) in enumerate(customers_data, start=2):
    hashed_pw = generate_password_hash("password123")
    
    try:
        cur.execute("""
            INSERT INTO customers (customer_id, customername, phone, email, password, address)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (idx, name, phone, email, hashed_pw, address))
        customer_ids.append(idx)
        print(f"   Added: {name}")
    except Exception as e:
        print(f"   Error adding {name}: {e}")

conn.commit()
print(f"\n   Total customers: {len(customer_ids)}")

# Update existing bookings with diverse customers and products
print("\n3. Updating bookings with diverse data...")
cur.execute("SELECT booking_id FROM bookings ORDER BY booking_id")
booking_ids = [row[0] for row in cur.fetchall()]

print(f"   Found {len(booking_ids)} bookings to update")

for idx, booking_id in enumerate(booking_ids):
    # Assign different customer
    customer_id = customer_ids[idx % len(customer_ids)]
    
    # Assign different product
    product = all_products[idx % len(all_products)]
    product_id = product[0]
    product_price = int(product[2])
    
    # Random days (1-5)
    days = random.randint(1, 5)
    total_price = product_price * days
    
    # Update booking
    cur.execute("""
        UPDATE bookings 
        SET customer_id = :1, total_price = :2
        WHERE booking_id = :3
    """, (customer_id, total_price, booking_id))
    
    # Update booking_details
    cur.execute("""
        UPDATE booking_details 
        SET product_id = :1, price = :2
        WHERE booking_id = :3
    """, (product_id, total_price, booking_id))
    
    print(f"   Booking #{booking_id}: Customer {customer_id} -> Product {product[1]}")

conn.commit()

print("\n" + "="*80)
print("VERIFICATION:")
print("="*80)

# Verify diversity
cur.execute("""
    SELECT COUNT(DISTINCT b.customer_id) as unique_customers,
           COUNT(DISTINCT bd.product_id) as unique_products,
           COUNT(*) as total_bookings
    FROM bookings b
    JOIN booking_details bd ON b.booking_id = bd.booking_id
""")
result = cur.fetchone()

print(f"\nUnique customers in bookings: {result[0]}")
print(f"Unique products in bookings: {result[1]}")
print(f"Total bookings: {result[2]}")

print("\n" + "="*80)
print("SUCCESS! Bookings now have diverse customers and products!")
print("="*80)

cur.close()
conn.close()
