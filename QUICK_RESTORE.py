from db import get_connection

print("="*80)
print("EMERGENCY RESTORE - DATA DISAPPEARED AGAIN")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# Check current state
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]

print(f"\nCurrent state:")
print(f"  Products: {products}")
print(f"  Bookings: {bookings}")
print(f"  Customers: {customers}")

if products < 48 or bookings < 18 or customers < 16:
    print("\n[RESTORING FROM BACKUP...]")
    
    # Clear and restore
    try:
        cur.execute("DELETE FROM booking_details")
        cur.execute("DELETE FROM bookings")
        cur.execute("DELETE FROM products")
        
        cur.execute("INSERT INTO products SELECT * FROM products_backup")
        cur.execute("INSERT INTO bookings SELECT * FROM bookings_backup")
        cur.execute("INSERT INTO booking_details SELECT * FROM booking_details_backup")
        
        conn.commit()
        print("[OK] Data restored from backup")
    except Exception as e:
        print(f"Error: {e}")
    
    # Re-add customers
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
            pass
    
    conn.commit()

# Final check
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]

print("\n" + "="*80)
print("FINAL STATUS:")
print("="*80)
print(f"Products: {products}/48")
print(f"Bookings: {bookings}/18")
print(f"Customers: {customers}/16")

if products == 48 and bookings >= 18 and customers >= 16:
    print("\n[SUCCESS] All data restored!")
else:
    print("\n[WARNING] Some data still missing")

print("="*80)

cur.close()
conn.close()
