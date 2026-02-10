from db import get_connection
from werkzeug.security import generate_password_hash

print("="*80)
print("COMPLETE DATABASE SETUP - INSERTING ALL DATA")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# Step 1: Insert Customers (16 customers)
print("\n1. Inserting customers...")
customers_data = [
    (1, "Rahul Sharma", "9876543210", "rahul@gmail.com", "Pune"),
    (2, "Priya Deshmukh", "9876543210", "priya.d@gmail.com", "Mumbai"),
    (3, "Arjun Patel", "9123456789", "arjun.p@gmail.com", "Ahmedabad"),
    (4, "Sneha Reddy", "9234567890", "sneha.r@gmail.com", "Hyderabad"),
    (5, "Vikram Singh", "9345678901", "vikram.s@gmail.com", "Jaipur"),
    (6, "Ananya Iyer", "9456789012", "ananya.i@gmail.com", "Chennai"),
    (7, "Rohan Mehta", "9567890123", "rohan.m@gmail.com", "Pune"),
    (8, "Kavya Nair", "9678901234", "kavya.n@gmail.com", "Kochi"),
    (9, "Aditya Gupta", "9789012345", "aditya.g@gmail.com", "Delhi"),
    (10, "Ishita Joshi", "9890123456", "ishita.j@gmail.com", "Bangalore"),
    (11, "Karan Kapoor", "9901234567", "karan.k@gmail.com", "Chandigarh"),
    (12, "Meera Kulkarni", "9012345678", "meera.k@gmail.com", "Nashik"),
    (13, "Siddharth Rao", "9123450987", "siddharth.r@gmail.com", "Mysore"),
    (14, "Tanvi Shah", "9234561098", "tanvi.s@gmail.com", "Surat"),
    (15, "Nikhil Verma", "9345672109", "nikhil.v@gmail.com", "Lucknow"),
    (16, "Riya Malhotra", "9456783210", "riya.m@gmail.com", "Kolkata"),
]

for cust_id, name, phone, email, address in customers_data:
    hashed_pw = generate_password_hash("password123")
    cur.execute("""
        INSERT INTO customers (customer_id, customername, phone, email, password, address)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, (cust_id, name, phone, email, hashed_pw, address))

conn.commit()
print(f"   Inserted {len(customers_data)} customers")

# Step 2: Insert Products (18 products for demo)
print("\n2. Inserting products...")
products_data = [
    (1, "Premium Blazer", "Mens", 3500, "/static/images/mens10.jpg", 7000),
    (101, "Sapphire Premium Set", "Jewelry", 4500, "/static/images/sapphire_premium.png", 9000),
    (108, "Emerald Solitaire Ring", "Jewelry", 8000, "/static/images/ring1.jpg", 16000),
    (104, "Antique Temple Set", "Jewelry", 5200, "/static/images/temple_set.jpg", 10400),
    (105, "Pearl Choker Necklace", "Jewelry", 1400, "/static/images/pearl_choker.jpg", 2800),
    (106, "Ruby Wedding Set", "Jewelry", 13000, "/static/images/ruby_set.jpg", 26000),
    (201, "Royal Maroon Lehenga", "Womens", 11000, "/static/images/womens1.jpg", 22000),
    (202, "Emerald Silk Gown", "Womens", 10500, "/static/images/womens2.jpg", 21000),
    (203, "Bridal Red Anarkali", "Womens", 12400, "/static/images/womens3.jpg", 24800),
    (204, "Designer Saree", "Womens", 6750, "/static/images/womens4.jpg", 13500),
    (2, "Royal Blue Sherwani", "Mens", 16250, "/static/images/mens1.jpg", 32500),
    (3, "Black Tuxedo", "Mens", 2600, "/static/images/mens2.jpg", 5200),
    (4, "Grey Office Suit", "Mens", 5850, "/static/images/mens3.jpg", 11700),
    (5, "Cream Wedding Kurta", "Mens", 7000, "/static/images/mens4.jpg", 14000),
    (6, "Navy Blazer", "Mens", 10500, "/static/images/mens5.jpg", 21000),
    (7, "Maroon Sherwani", "Mens", 14400, "/static/images/mens6.jpg", 28800),
    (8, "White Formal Shirt", "Mens", 750, "/static/images/mens7.jpg", 1500),
    (9, "Brown Leather Jacket", "Mens", 8250, "/static/images/mens8.jpg", 16500),
]

for prod_id, name, category, price, image, market_price in products_data:
    cur.execute("""
        INSERT INTO products (product_id, name, category, price, image_path, market_price)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, (prod_id, name, category, price, image, market_price))

conn.commit()
print(f"   Inserted {len(products_data)} products")

# Step 3: Insert Bookings (18 bookings)
print("\n3. Inserting bookings...")
bookings_data = [
    (1, 1, 10500, '10-FEB-26', '12-FEB-26', 'Confirmed', '9876543210', 'Pune', 'Pune'),
    (902, 2, 13500, '11-FEB-26', '14-FEB-26', 'Confirmed', '9876543210', 'Mumbai', 'Mumbai'),
    (903, 3, 16000, '12-FEB-26', '15-FEB-26', 'Confirmed', '9123456789', 'Ahmedabad', 'Ahmedabad'),
    (904, 4, 10400, '13-FEB-26', '16-FEB-26', 'Pending', '9234567890', 'Hyderabad', 'Hyderabad'),
    (905, 5, 2800, '14-FEB-26', '17-FEB-26', 'Confirmed', '9345678901', 'Jaipur', 'Jaipur'),
    (906, 6, 26000, '15-FEB-26', '18-FEB-26', 'Returned', '9456789012', 'Chennai', 'Chennai'),
    (907, 7, 22000, '16-FEB-26', '19-FEB-26', 'Confirmed', '9567890123', 'Pune', 'Pune'),
    (908, 8, 21000, '17-FEB-26', '20-FEB-26', 'Pending', '9678901234', 'Kochi', 'Kochi'),
    (909, 9, 24800, '18-FEB-26', '21-FEB-26', 'Confirmed', '9789012345', 'Delhi', 'Delhi'),
    (910, 10, 13500, '19-FEB-26', '22-FEB-26', 'Returned', '9890123456', 'Bangalore', 'Bangalore'),
    (911, 11, 32500, '20-FEB-26', '23-FEB-26', 'Confirmed', '9901234567', 'Chandigarh', 'Chandigarh'),
    (912, 12, 5200, '21-FEB-26', '24-FEB-26', 'Pending', '9012345678', 'Nashik', 'Nashik'),
    (913, 13, 11700, '22-FEB-26', '25-FEB-26', 'Confirmed', '9123450987', 'Mysore', 'Mysore'),
    (914, 14, 14000, '23-FEB-26', '26-FEB-26', 'Returned', '9234561098', 'Surat', 'Surat'),
    (915, 15, 21000, '24-FEB-26', '27-FEB-26', 'Pending', '9345672109', 'Lucknow', 'Lucknow'),
    (916, 16, 28800, '25-FEB-26', '28-FEB-26', 'Confirmed', '9456783210', 'Kolkata', 'Kolkata'),
    (917, 1, 1500, '26-FEB-26', '01-MAR-26', 'Confirmed', '9876543210', 'Pune', 'Pune'),
    (918, 2, 16500, '27-FEB-26', '02-MAR-26', 'Pending', '9876543210', 'Mumbai', 'Mumbai'),
]

for booking_id, cust_id, total, rent_date, return_date, status, phone, address, location in bookings_data:
    cur.execute("""
        INSERT INTO bookings (booking_id, customer_id, total_price, rent_date, return_date, status, phone, address, location)
        VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MON-YY'), TO_DATE(:5, 'DD-MON-YY'), :6, :7, :8, :9)
    """, (booking_id, cust_id, total, rent_date, return_date, status, phone, address, location))

conn.commit()
print(f"   Inserted {len(bookings_data)} bookings")

# Step 4: Insert Booking Details (18 booking details)
print("\n4. Inserting booking details...")
booking_details_data = [
    (1, 1, 1, 10500),
    (902, 2, 101, 13500),
    (903, 3, 108, 16000),
    (904, 4, 104, 10400),
    (905, 5, 105, 2800),
    (906, 6, 106, 26000),
    (907, 7, 201, 22000),
    (908, 8, 202, 21000),
    (909, 9, 203, 24800),
    (910, 10, 204, 13500),
    (911, 11, 2, 32500),
    (912, 12, 3, 5200),
    (913, 13, 4, 11700),
    (914, 14, 5, 14000),
    (915, 15, 6, 21000),
    (916, 16, 7, 28800),
    (917, 1, 8, 1500),
    (918, 2, 9, 16500),
]

for booking_id, product_id, quantity, price in booking_details_data:
    cur.execute("""
        INSERT INTO booking_details (booking_id, product_id, quantity, price)
        VALUES (:1, :2, :3, :4)
    """, (booking_id, product_id, quantity, price))

conn.commit()
print(f"   Inserted {len(booking_details_data)} booking details")

# Final verification
print("\n" + "="*80)
print("FINAL VERIFICATION:")
print("="*80)

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]
print(f"Customers: {customers}")

cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]
print(f"Products: {products}")

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]
print(f"Bookings: {bookings}")

cur.execute("SELECT COUNT(*) FROM booking_details")
booking_details = cur.fetchone()[0]
print(f"Booking Details: {booking_details}")

print("\n" + "="*80)
print("[SUCCESS] Database setup complete!")
print("="*80)
print("\nYou can now:")
print("1. Run your Flask app: python app.py")
print("2. View data in SQL Developer using SAFE_PRESENTATION_QUERIES.sql")
print("="*80)

cur.close()
conn.close()
