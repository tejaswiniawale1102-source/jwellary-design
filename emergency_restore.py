from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("EMERGENCY RESTORE FROM BACKUP")
print("="*80)

# Step 1: Clear current data
print("\n1. Clearing corrupted data...")
try:
    cur.execute("DELETE FROM booking_details")
    cur.execute("DELETE FROM bookings")
    cur.execute("DELETE FROM products")
    conn.commit()
    print("   [OK] Cleared old data")
except Exception as e:
    print(f"   Error clearing: {e}")

# Step 2: Restore products from backup
print("\n2. Restoring products from backup...")
try:
    cur.execute("INSERT INTO products SELECT * FROM products_backup")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]
    print(f"   [OK] Restored {count} products")
except Exception as e:
    print(f"   Error restoring products: {e}")

# Step 3: Restore bookings from backup
print("\n3. Restoring bookings from backup...")
try:
    cur.execute("INSERT INTO bookings SELECT * FROM bookings_backup")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM bookings")
    count = cur.fetchone()[0]
    print(f"   [OK] Restored {count} bookings")
except Exception as e:
    print(f"   Error restoring bookings: {e}")

# Step 4: Restore booking_details from backup
print("\n4. Restoring booking details from backup...")
try:
    cur.execute("INSERT INTO booking_details SELECT * FROM booking_details_backup")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM booking_details")
    count = cur.fetchone()[0]
    print(f"   [OK] Restored {count} booking details")
except Exception as e:
    print(f"   Error restoring booking details: {e}")

# Step 5: Re-add diverse customers
print("\n5. Re-adding diverse customers...")
from werkzeug.security import generate_password_hash

customers_data = [
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
    try:
        hashed_pw = generate_password_hash("password123")
        cur.execute("""
            INSERT INTO customers (customer_id, customername, phone, email, password, address)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (cust_id, name, phone, email, hashed_pw, address))
    except:
        pass  # Skip if already exists

conn.commit()
print("   [OK] Customers restored")

# Final verification
print("\n" + "="*80)
print("FINAL STATUS:")
print("="*80)

cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]
print(f"Products: {products}")

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]
print(f"Customers: {customers}")

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]
print(f"Bookings: {bookings}")

print("\n[SUCCESS] ALL DATA RESTORED!")
print("="*80)

cur.close()
conn.close()
