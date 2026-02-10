from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("DATABASE CONNECTION CHECK")
print("="*80)

# Check which database we're connected to
cur.execute("SELECT SYS_CONTEXT('USERENV', 'DB_NAME') FROM DUAL")
db_name = cur.fetchone()[0]
print(f"\nConnected to database: {db_name}")

cur.execute("SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM DUAL")
service_name = cur.fetchone()[0]
print(f"Service name: {service_name}")

cur.execute("SELECT SYS_CONTEXT('USERENV', 'CURRENT_USER') FROM DUAL")
current_user = cur.fetchone()[0]
print(f"Current user: {current_user}")

# Check products table
print("\n" + "="*80)
print("CURRENT DATABASE CONTENTS:")
print("="*80)

cur.execute("SELECT COUNT(*) FROM products")
product_count = cur.fetchone()[0]
print(f"\nTotal products: {product_count}")

cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
print("\nProducts by category:")
for row in cur.fetchall():
    print(f"  - {row[0]:15s}: {row[1]:2d} products")

# Show sample products
print("\nSample products (first 5):")
cur.execute("""
    SELECT product_id, name, category, image_path 
    FROM products 
    WHERE ROWNUM <= 5 
    ORDER BY product_id
""")
for row in cur.fetchall():
    print(f"  ID {row[0]:3d}: {row[1]:30s} | {row[2]:15s} | {row[3]}")

# Check bookings
cur.execute("SELECT COUNT(*) FROM bookings")
booking_count = cur.fetchone()[0]
print(f"\nTotal bookings: {booking_count}")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
if product_count == 48 and booking_count == 18:
    print("✓ You are connected to the NEW database with all data!")
    print("✓ Your Flask app should be working correctly.")
else:
    print("✗ WARNING: This appears to be an OLD database!")
    print(f"  Expected: 48 products, 18 bookings")
    print(f"  Found: {product_count} products, {booking_count} bookings")
print("="*80)

cur.close()
conn.close()
